# Contrast CLI (WCAG AA/AAA)
**Purpose:** batch-compute contrast ratios for foreground/background pairs and flag WCAG conformance.

## Usage
```bash
python contrast_cli.py tokens.json contrast_results.csv
```

## Tokens JSON schema
```json
{
  "pairs": [
    {"component": "Primary Button", "state": "default", "theme": "Dark", "fg": "#FFFFFF", "bg": "#1F4ED8", "notes": ""}
  ]
}
```

## Output CSV columns
Component, State, Theme, Foreground, Background, ContrastRatio, AA_Normal, AA_Large, AAA_Normal, AAA_Large, Notes

## Targets
- AA Normal: ≥ 4.5:1
- AA Large: ≥ 3.0:1
- AAA Normal: ≥ 7.0:1
- AAA Large: ≥ 4.5:1
