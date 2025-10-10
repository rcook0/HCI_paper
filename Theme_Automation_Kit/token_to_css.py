#!/usr/bin/env python3
# token_to_css.py
import sys, json, re
from pathlib import Path

def slug(key):
    return key.replace('.', '-').replace('_', '-')

def resolve_refs(mapping):
    pat = re.compile(r'\{([a-zA-Z0-9._-]+)\}')
    def subst(val):
        def repl(m):
            path = m.group(1)
            return mapping.get(path, m.group(0))
        return pat.sub(repl, val)
    out = {}
    for k,v in mapping.items():
        out[k] = subst(v) if isinstance(v, str) else v
    return out

def flatten(theme_dict, aliases):
    flat = {}
    def walk(prefix, obj):
        if isinstance(obj, dict):
            for k,v in obj.items():
                walk(f"{prefix}.{k}" if prefix else k, v)
        else:
            flat[prefix] = obj
    walk("", theme_dict)
    for ak,av in aliases.items():
        flat[ak] = av
    return resolve_refs(flat)

def css_block(selector, flat):
    lines = [f"{selector} {{"]
    for k in sorted(flat.keys()):
        v = flat[k]
        if isinstance(v, (int,float)): v = str(v)
        lines.append(f"  --{slug(k)}: {v};")
    lines.append("}")
    return "\n".join(lines)

def main():
    if len(sys.argv) != 3:
        print("Usage: python token_to_css.py tokens.themes.json out_dir/"); sys.exit(2)
    inp = Path(sys.argv[1]); outd = Path(sys.argv[2]); outd.mkdir(parents=True, exist_ok=True)
    data = json.loads(inp.read_text(encoding='utf-8'))
    themes = data.get("themes", {}); aliases = data.get("aliases", {})
    blocks = []
    for name, theme in themes.items():
        flat = flatten(theme, aliases)
        scoped = css_block(f':root[data-theme="{name}"]', flat)
        blocks.append(scoped)
        (outd / f"{name}.css").write_text(scoped + "\n", encoding="utf-8")
    if "light" in themes: blocks.append(":root { color-scheme: light dark; }\n@media (prefers-color-scheme: light) {\n  :root:not([data-theme]) { color-scheme: light; }\n}")
    if "dark" in themes:  blocks.append("@media (prefers-color-scheme: dark) {\n  :root:not([data-theme]) { color-scheme: dark; }\n}")
    (outd / "themes.css").write_text("\n\n".join(blocks) + "\n", encoding="utf-8")

if __name__ == "__main__":
    main()
