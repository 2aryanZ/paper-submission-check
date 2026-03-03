# Color Palette Reference

Detailed color specifications for academic paper figures. Referenced by [SKILL.md](SKILL.md).

## Contents

- [1. Okabe-Ito Palette](#1-okabe-ito-palette-primary-recommendation)
- [2. Paul Tol Qualitative Palette](#2-paul-tol-qualitative-palette-alternative)
- [3. Sequential Colormaps](#3-sequential-colormaps-for-heatmaps--continuous-data)
- [4. Diverging Colormaps](#4-diverging-colormaps-for-data-centered-at-zero)
- [5. Cybersecurity Domain Color Conventions](#5-cybersecurity-domain-color-conventions)
- [6. Color Assignment Strategy](#6-color-assignment-strategy)
- [7. Supplementary Colors for Figures](#7-supplementary-colors-for-figures)
- [8. CMYK Conversion Notes](#8-cmyk-conversion-notes)
- [9. Color in Tables](#9-color-in-tables)

---

## 1. Okabe-Ito Palette (Primary Recommendation)

A widely used colorblind-safe palette for scientific figures, especially for categorical comparisons.

### Full Specification

| Name | HEX | RGB | Approximate CMYK | LaTeX Name | Visual Role |
|------|-----|-----|-------------------|------------|-------------|
| Blue | #0072B2 | (0, 114, 178) | (100, 36, 0, 30) | `acBlue` | Proposed method / Primary |
| Orange | #E69F00 | (230, 159, 0) | (0, 31, 100, 10) | `acOrange` | Baseline / Warning |
| Bluish Green | #009E73 | (0, 158, 115) | (100, 0, 27, 38) | `acGreen` | Benign / Success |
| Vermillion | #D55E00 | (213, 94, 0) | (0, 56, 100, 16) | `acVermillion` | Attack / Malicious / Alert |
| Reddish Purple | #CC79A7 | (204, 121, 167) | (0, 41, 18, 20) | `acPurple` | Auxiliary |
| Sky Blue | #56B4E9 | (86, 180, 233) | (63, 23, 0, 9) | `acSky` | Secondary / Background |
| Yellow | #F0E442 | (240, 228, 66) | (0, 5, 73, 6) | `acYellow` | Caution: low contrast on white |
| Black | #000000 | (0, 0, 0) | (0, 0, 0, 100) | `acBlack` | Reference / Axis / Text |

### LaTeX Definition Block

```latex
% Okabe-Ito colorblind-safe palette
\definecolor{acBlue}{HTML}{0072B2}
\definecolor{acOrange}{HTML}{E69F00}
\definecolor{acGreen}{HTML}{009E73}
\definecolor{acVermillion}{HTML}{D55E00}
\definecolor{acPurple}{HTML}{CC79A7}
\definecolor{acSky}{HTML}{56B4E9}
\definecolor{acYellow}{HTML}{F0E442}
\definecolor{acBlack}{HTML}{000000}
```

### Python (matplotlib) Definition

```python
OKABE_ITO = {
    'blue':       '#0072B2',
    'orange':     '#E69F00',
    'green':      '#009E73',
    'vermillion': '#D55E00',
    'purple':     '#CC79A7',
    'sky':        '#56B4E9',
    'yellow':     '#F0E442',
    'black':      '#000000',
}
OKABE_ITO_CYCLE = list(OKABE_ITO.values())

import matplotlib as mpl
mpl.rcParams['axes.prop_cycle'] = mpl.cycler(color=OKABE_ITO_CYCLE)
```

### pgfplots Cycle List

```latex
\pgfplotscreateplotcyclelist{okabe-ito}{
  {acBlue, mark=*},
  {acVermillion, mark=square*},
  {acGreen, mark=triangle*},
  {acOrange, mark=diamond*, dashed},
  {acPurple, mark=otimes*, dashed},
  {acSky, mark=star, dotted},
  {acBlack, mark=+, dashdotted},
}
\pgfplotsset{cycle list name=okabe-ito}
```

---

## 2. Paul Tol Qualitative Palette (Alternative)

For papers needing more than 7 colors or a different aesthetic. Verified colorblind-safe.

### Bright Variant (up to 7)

| Color | HEX | LaTeX |
|-------|-----|-------|
| Blue | #4477AA | `\definecolor{tolBlue}{HTML}{4477AA}` |
| Cyan | #66CCEE | `\definecolor{tolCyan}{HTML}{66CCEE}` |
| Green | #228833 | `\definecolor{tolGreen}{HTML}{228833}` |
| Yellow | #CCBB44 | `\definecolor{tolYellow}{HTML}{CCBB44}` |
| Red | #EE6677 | `\definecolor{tolRed}{HTML}{EE6677}` |
| Purple | #AA3377 | `\definecolor{tolPurple}{HTML}{AA3377}` |
| Grey | #BBBBBB | `\definecolor{tolGrey}{HTML}{BBBBBB}` |

### Muted Variant (up to 10)

| Color | HEX |
|-------|-----|
| Indigo | #332288 |
| Cyan | #88CCEE |
| Teal | #44AA99 |
| Green | #117733 |
| Olive | #999933 |
| Sand | #DDCC77 |
| Rose | #CC6677 |
| Wine | #882255 |
| Purple | #AA4499 |
| Pale Grey | #DDDDDD |

---

## 3. Sequential Colormaps (for Heatmaps & Continuous Data)

### Recommended (in order of preference)

| Colormap | When to Use | Colorblind Safe | LaTeX/pgfplots |
|----------|-------------|-----------------|----------------|
| **viridis** | Default for all sequential data | Yes | `colormap/viridis` |
| **cividis** | Strongest colorblind safety | Yes (designed for CVD) | `colormap/cividis` |
| **inferno** | High contrast; dark background emphasis | Yes | `colormap/hot2` (approx) |
| **plasma** | Alternative to viridis | Yes | `colormap/plasma` (custom) |

### Avoid for Quantitative Data

| Colormap | Problem |
|----------|---------|
| jet / rainbow | Non-uniform luminance; can create false visual boundaries |
| hot | Often poor perceptual uniformity for fine-grained comparisons |
| autumn / spring | Low distinction; not perceptually uniform |
| Red-green only encodings | Often inaccessible for readers with red-green CVD |

### pgfplots Custom Viridis Definition

```latex
\pgfplotsset{
  colormap={viridis}{
    rgb255(0cm)=(68,1,84)
    rgb255(1cm)=(72,36,117)
    rgb255(2cm)=(65,68,135)
    rgb255(3cm)=(53,95,141)
    rgb255(4cm)=(42,120,142)
    rgb255(5cm)=(33,145,140)
    rgb255(6cm)=(34,168,132)
    rgb255(7cm)=(68,191,112)
    rgb255(8cm)=(122,209,81)
    rgb255(9cm)=(189,223,38)
    rgb255(10cm)=(253,231,37)
  },
}
```

---

## 4. Diverging Colormaps (for Data Centered at Zero)

| Colormap | When to Use | Center Color |
|----------|-------------|-------------|
| **RdBu** (Red-Blue) | Correlation matrices, positive/negative change | White |
| **PiYG** (Pink-Yellow-Green) | Alternative diverging | White |
| **PRGn** (Purple-Green) | Colorblind-safe diverging | White |

**Rule**: Always set the center point at 0 (or the neutral value). Asymmetric ranges must still be visually centered.

---

## 5. Cybersecurity Domain Color Conventions

Standard semantic color assignments for security papers:

| Concept | Color | HEX | Rationale |
|---------|-------|-----|-----------|
| **Malicious / Attack** | Vermillion or Red | #D55E00 | Universal danger signal |
| **Benign / Normal** | Blue or Green | #0072B2 / #009E73 | Safety/trust association |
| **Suspicious / Anomalous** | Orange | #E69F00 | Warning level |
| **Unknown / Unlabeled** | Grey | #999999 | Neutral / no information |
| **Highlighted / Proposed** | Blue | #0072B2 | Primary emphasis |
| **C2 Communication** | Purple | #CC79A7 | Convention in kill-chain diagrams |
| **Lateral Movement** | Orange | #E69F00 | Internal propagation |
| **Data Exfiltration** | Vermillion | #D55E00 | High severity |
| **Reconnaissance** | Sky Blue | #56B4E9 | Early-stage, lower severity |

### Attack Kill Chain Color Progression

```
Recon (#56B4E9) → Weaponize (#E69F00) → Deliver (#CC79A7) → 
Exploit (#D55E00) → Install (#AA3377) → C2 (#882255) → Exfil (#000000)
```

Use gradient intensity: lighter shades for early stages, darker for later stages.

---

## 6. Color Assignment Strategy

### For Method Comparison Papers

1. **Your method**: Always Slot 1 (Blue, solid, circle) — most visually prominent
2. **Strongest competitor**: Slot 2 (Vermillion) — contrasts with Blue
3. **Other baselines**: Slots 3–6 in order of relevance
4. **Random/oracle reference**: Slot 7 (Black, dash-dot)

### For Ablation Studies

| Variant | Color Strategy |
|---------|---------------|
| Full model | Blue (same as method comparison) |
| w/o Component A | Vermillion (biggest drop highlighted) |
| w/o Component B | Orange |
| w/o Component C | Green |
| Other variants | Remaining palette colors |

### For Multi-Dataset Comparison

Option A: Same method = same color across datasets (preferred)
Option B: Same dataset = same color, different line style per method

**Rule**: Be consistent. Document your mapping and apply it to ALL figures.

---

## 7. Supplementary Colors for Figures

### Bar Chart Fill Colors

For bar charts where you need fill + border:

```latex
\definecolor{acBarFill}{HTML}{4E79A7}   % steel blue, good for bars
\definecolor{acParamLine}{HTML}{E15759} % red accent for overlay lines
```

### Shaded Region Colors

For confidence intervals or error bands:

```latex
% Use palette color with low opacity
fill=acBlue, fill opacity=0.15
fill=acVermillion, fill opacity=0.15
```

### Background / Grid Colors

```latex
\definecolor{acGridGray}{HTML}{D0D0D0}  % major grid
\definecolor{acBgGray}{HTML}{F8F8F8}    % plot background (optional)
```

---

## 8. CMYK Conversion Notes

Some publishers (especially for print journals) require CMYK color space.

**Key issues when converting RGB → CMYK**:
- Bright blues become duller
- Vivid greens shift toward teal
- Screen-bright colors will appear muted in print

**Mitigation**:
1. Test with `\usepackage[cmyk]{xcolor}` (converts all colors)
2. Verify in printed proof, not just screen
3. Okabe-Ito palette was designed with print in mind; conversion is acceptable
4. If using Elsevier / IEEE online-only journal → RGB is fine

---

## 9. Color in Tables

Tables should generally NOT use heavy coloring. Acceptable uses:

| Use Case | Implementation | Caution |
|----------|---------------|---------|
| Row striping (alternating) | `\rowcolors{2}{gray!5}{white}` | Very light; disable for print |
| Header row background | `\cellcolor{gray!15}` | Light gray only |
| Heatmap-style cells | Gradient fill based on value | Must include numeric values too |
| Highlight rows | `\rowcolor{acSky!15}` | Use sparingly for 1–2 key rows |

**Rule**: If the paper will be printed, avoid colored table backgrounds entirely. Numbers + bold/underline are sufficient.
