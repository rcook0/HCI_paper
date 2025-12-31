#!/usr/bin/env python3
"""
contrast_cli.py
Compute WCAG contrast ratios for foreground/background color pairs from a token JSON.
Usage:
  python contrast_cli.py tokens.json output.csv
Tokens JSON schema:
{
  "pairs": [
    {"component": "Primary Button", "state": "default", "theme": "Light",
     "fg": "#FFFFFF", "bg": "#0B5FFF", "notes": ""},
    ...
  ]
}
"""

import sys, json, csv, re

HEX_RE = re.compile(r'^#([0-9A-Fa-f]{6})$')

def srgb_to_linear(c):
    c = c / 255.0
    return c/12.92 if c <= 0.03928*255 else ((c+0.055)/1.055)**2.4

def parse_hex(h):
    m = HEX_RE.match(h)
    if not m:
        raise ValueError(f"Invalid hex color: {h}")
    v = int(m.group(1), 16)
    r = (v >> 16) & 0xFF
    g = (v >> 8) & 0xFF
    b = v & 0xFF
    return r, g, b

def rel_luminance(hex_color):
    r, g, b = parse_hex(hex_color)
    R = srgb_to_linear(r)
    G = srgb_to_linear(g)
    B = srgb_to_linear(b)
    # Rec. 709 coefficients per WCAG
    return 0.2126*R + 0.7152*G + 0.0722*B

def contrast_ratio(fg, bg):
    L1 = rel_luminance(fg)
    L2 = rel_luminance(bg)
    Llight = max(L1, L2)
    Ldark  = min(L1, L2)
    return (Llight + 0.05) / (Ldark + 0.05)

def pass_fail(ratio, large=False, level="AA"):
    if level == "AA":
        return ratio >= (3.0 if large else 4.5)
    if level == "AAA":
        return ratio >= (4.5 if large else 7.0)
    return False

def main():
    if len(sys.argv) != 3:
        print("Usage: python contrast_cli.py tokens.json output.csv")
        sys.exit(2)
    tokens_path, out_csv = sys.argv[1], sys.argv[2]
    with open(tokens_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    rows = []
    for p in data.get("pairs", []):
        fg = p["fg"]; bg = p["bg"]
        ratio = contrast_ratio(fg, bg)
        out = {
            "Component": p.get("component",""),
            "State": p.get("state",""),
            "Theme": p.get("theme",""),
            "Foreground": fg,
            "Background": bg,
            "ContrastRatio": f"{ratio:.2f}",
            "AA_Normal": "PASS" if pass_fail(ratio, large=False, level="AA") else "FAIL",
            "AA_Large": "PASS" if pass_fail(ratio, large=True, level="AA") else "FAIL",
            "AAA_Normal": "PASS" if pass_fail(ratio, large=False, level="AAA") else "FAIL",
            "AAA_Large": "PASS" if pass_fail(ratio, large=True, level="AAA") else "FAIL",
            "Notes": p.get("notes","")
        }
        rows.append(out)
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else [
            "Component","State","Theme","Foreground","Background","ContrastRatio",
            "AA_Normal","AA_Large","AAA_Normal","AAA_Large","Notes"
        ])
        writer.writeheader()
        for r in rows:
            writer.writerow(r)

if __name__ == "__main__":
    main()
