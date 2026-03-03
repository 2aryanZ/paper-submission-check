---
name: paper-figure-styling
description: Comprehensive figure styling, color scheme, typography, legend design, layout, and cross-reference guide for academic papers in LaTeX. Covers colorblind-safe palettes, triple visual encoding (color+line+marker), all figure types (line, bar, heatmap, confusion matrix, ROC/PR, box/violin, radar, scatter, architecture, network graph, Sankey, timeline, waterfall, area), table visual design, caption formatting, cross-reference audit, hyperlink color policy, and cross-publisher adaptation (Elsevier, IEEE, Springer, ACM, USENIX). Use when creating figures, styling plots, choosing colors, designing legends, formatting tables, checking figure/table references, or preparing visual elements for journal or conference submission, 配色, 排版, 图表, 图例, 字体, 颜色.
---

# Paper Figure Styling & Visual Design

Systematic quality guide for all visual elements in academic papers. Applies to cybersecurity venues (S&P, CCS, USENIX Security, NDSS, TDSC, TIFS, Computers & Security) and general CS journals.

## Execution Safety [CRITICAL]

Before applying style changes:

- Do not change reported values, statistical results, labels, or ranking order.
- Do not alter figure semantics to "look better" (for example, axis range tricks that hide variance).
- Keep figure/table numbering and cross-references stable unless user explicitly requests renumbering.
- Preserve reproducibility: any style adjustment should be scriptable (LaTeX/pgfplots/matplotlib config), not manual one-off edits.

## Workflow

```
Figure Styling Progress:
- [ ] Phase 1: Color System Setup (palette + semantic mapping)
- [ ] Phase 2: Typography Audit (figure fonts, table fonts, sizes)
- [ ] Phase 3: Visual Encoding System (color + line style + marker)
- [ ] Phase 4: Per-Figure-Type Review
- [ ] Phase 5: Legend & Annotation Consistency
- [ ] Phase 6: Layout, Float Placement & Page Density
- [ ] Phase 7: Table Visual Design
- [ ] Phase 8: Caption & Label Formatting
- [ ] Phase 9: Cross-Reference & Hyperlink Audit
- [ ] Phase 10: Grayscale & Accessibility Test
- [ ] Phase 11: Publisher Compliance Final Check
```

---

## Phase 1: Color System

### Default Palette: Okabe-Ito (Wong)

```latex
\definecolor{acBlue}{HTML}{0072B2}       % proposed method / primary
\definecolor{acOrange}{HTML}{E69F00}      % baseline 3
\definecolor{acGreen}{HTML}{009E73}       % baseline 2 / benign class
\definecolor{acVermillion}{HTML}{D55E00}  % strongest baseline / attack class
\definecolor{acPurple}{HTML}{CC79A7}      % baseline 4
\definecolor{acSky}{HTML}{56B4E9}         % baseline 5 / auxiliary
\definecolor{acYellow}{HTML}{F0E442}      % caution: low contrast on white
\definecolor{acBlack}{HTML}{000000}       % reference / oracle / axis
```

### Rules

1. **Semantic lock**: Same entity = same color in ALL figures (e.g., F1 is always acBlue)
2. **Max 7 colors** per figure; split into subfigures if more needed
3. **Security domain**: vermillion/red → malicious/attack; blue/green → benign/normal
4. **Sequential data** (heatmaps): viridis, cividis, or inferno — NEVER jet/rainbow
5. **Diverging data**: RdBu or PiYG (centered at 0)
6. **Your method** always gets the most prominent color (acBlue) + solid line

### Hyperlink & Cross-Reference Colors

```latex
\usepackage[colorlinks=true,
  linkcolor=acBlue!80!black,   % internal refs (Fig., Table, Eq.)
  citecolor=acGreen!70!black,  % citation numbers/author-year
  urlcolor=acPurple!80!black,  % URLs
]{hyperref}
```

**Rule**: Colored links are often useful in review drafts. For camera-ready, follow venue policy exactly; some pipelines (for example IEEE PDF eXpress) require no active links/bookmarks. See [publisher-specs.md](publisher-specs.md) for per-publisher policy.

For detailed palettes (Paul Tol, sequential, diverging, CMYK), see [color-reference.md](color-reference.md).

---

## Phase 2: Typography

### Figure Text — Font Family

Prefer clean, highly legible figure fonts (often sans-serif). If the venue template or style guide requires matching the document font, follow the venue rule.

```latex
\pgfplotsset{
  every axis/.append style={
    font=\sffamily\small,
    label style={font=\sffamily\small},
    tick label style={font=\sffamily\footnotesize},
    legend style={font=\sffamily\scriptsize},
    title style={font=\sffamily\small\bfseries},
  },
}
```

For TikZ architecture diagrams:
```latex
\begin{tikzpicture}[font=\sffamily\footnotesize, ...]
```

### Font Size Constraints

| Element | Minimum | Recommended | Context |
|---------|---------|-------------|---------|
| Axis labels | 7 pt | 8–9 pt | `\small` or `\footnotesize` |
| Tick labels | 6 pt | 7–8 pt | `\footnotesize` or `\scriptsize` |
| Legend text | 6 pt | 7–8 pt | `\scriptsize` |
| Panel labels (a)(b) | 8 pt bold | 8–10 pt bold | `\small\bfseries` |
| Annotations in figure | 6 pt | 7 pt | `\scriptsize` |
| Data value labels | 6 pt | 6–7 pt | `\scriptsize` or `\tiny` (edge case) |

**CRITICAL**: Avoid `\tiny` unless the venue explicitly permits very small labels. A practical target is >= 7pt at final print size.

### Table Text — Font Requirements

| Element | Font | Size | Style |
|---------|------|------|-------|
| Column headers | Same as body or sans-serif | `\small` | `\textbf{}` (bold) |
| Body text | Document main font | `\small` or `\footnotesize` | regular |
| Table notes | Document main font | `\footnotesize` or `\scriptsize` | regular |
| Best result | Document main font | same as body | `\textbf{}` |
| Second-best | Document main font | same as body | `\underline{}` (optional) |

**Rule**: Tables use the document's main font (serif for most templates). Figures use sans-serif. This is the standard convention.

### Font Embedding

XeLaTeX/LuaLaTeX: fonts auto-embedded. pdfLaTeX: add to preamble:
```latex
\usepackage[T1]{fontenc}  % ensures font embedding
```
For matplotlib exports: `plt.rcParams['pdf.fonttype'] = 42`

---

## Phase 3: Triple Encoding — Color + Line Style + Marker

**Rule**: Use at least two independent channels (for example color + marker, or color + line style). For high-stakes comparison plots, use triple encoding (color + line style + marker).

### Method Comparison Encoding Table

| Slot | Role | Color | Line | Marker | pgfplots |
|------|------|-------|------|--------|----------|
| 1 | **Your method** | acBlue | solid | ● `*` | `mark=*, acBlue, line width=1.2pt` |
| 2 | Baseline A | acVermillion | solid | ■ `square*` | `mark=square*, acVermillion` |
| 3 | Baseline B | acGreen | solid | ▲ `triangle*` | `mark=triangle*, acGreen` |
| 4 | Baseline C | acOrange | dashed | ◆ `diamond*` | `mark=diamond*, acOrange, dashed` |
| 5 | Baseline D | acPurple | dashed | ⊗ `otimes*` | `mark=otimes*, acPurple, dashed` |
| 6 | Baseline E | acSky | dotted | ★ `star` | `mark=star, acSky, dotted` |
| 7 | Reference | acBlack | dash-dot | + `+` | `mark=+, acBlack, dashdotted` |

### Metric Comparison Encoding Table (Same-Method, Multiple Metrics)

| Metric Type | Line | Marker | Semantic |
|-------------|------|--------|----------|
| Classification (F1, Prec, Recall, Acc) | solid | filled shapes | Direct decision metrics |
| Ranking (AUROC, AUPRC) | dashed | hollow or special shapes | Threshold-independent |
| Correlation (MCC, Kappa) | densely dashed | cross marks | Agreement metrics |

### Dimensions

| Element | Value | Range |
|---------|-------|-------|
| Data line width | 1.0–1.2 pt | 0.8–1.5 pt |
| Marker size | 2.0–2.5 pt | 1.5–3.0 pt |
| Reference line | 0.4 pt | 0.3–0.5 pt |
| Axis line | 0.5 pt | 0.4–0.6 pt |
| Grid line | 0.3 pt | 0.2–0.4 pt |

---

## Phase 4: Per-Figure-Type Quick Checklist

### Line Charts (Sensitivity / Convergence / ROC / PR)
- [ ] Triple encoding applied
- [ ] Y-axis starts from a meaningful value (not always 0 — truncate if data is 85–100%)
- [ ] Grid: major only, `dashed, gray!30`
- [ ] X-axis log scale if values span orders of magnitude
- [ ] Zoomed inset if curves cluster in a small region

### Bar Charts (Comparison / Ablation / Grouped / Stacked)
- [ ] Your method highlighted (most prominent color or outlined)
- [ ] Value labels present if ≤ 8 bars; omit if cluttered
- [ ] Error bars (std or SEM) if reporting averaged results
- [ ] Hatching patterns for grayscale fallback in grouped bars
- [ ] Consistent bar width across all bar-chart figures
- [ ] Horizontal bars if category labels are long

### Heatmaps & Confusion Matrices
- [ ] Colormap: viridis (default) / cividis (strongest colorblind safety)
- [ ] Cell annotations: white text on dark, black on light (auto-threshold)
- [ ] Color bar present with label
- [ ] Axis labels = class names, not indices
- [ ] Normalized confusion matrix (row-normalized or total-normalized)

### ROC Curves
- [ ] Diagonal reference line (dashed gray, label: "Random")
- [ ] AUC value in legend: `APT-Fusion (AUC = 0.9912)`
- [ ] Both axes [0, 1]
- [ ] Zoomed inset near (0, 1) corner if curves overlap

### Precision-Recall Curves
- [ ] Baseline: horizontal line at class prevalence
- [ ] AUPRC value in legend
- [ ] Optional: iso-F1 contour lines

### Box Plots & Violin Plots
- [ ] Median line clearly visible (thick or colored)
- [ ] Individual points overlaid (jittered) if n ≤ 30
- [ ] Color by method (consistent with color system)
- [ ] Whiskers: 1.5×IQR standard

### Scatter Plots (t-SNE / UMAP / Feature Space)
- [ ] Different marker shapes per class (not just color)
- [ ] Alpha transparency 0.4–0.7 for overlap
- [ ] No axis ticks/labels for t-SNE/UMAP (dimensionless)
- [ ] Legend: class name + count

### Radar / Spider Charts
- [ ] 5–8 axes maximum
- [ ] All axes same scale [0, 100] or [0, 1]
- [ ] Fill alpha = 0.15–0.25; outline solid for proposed, dashed for baselines
- [ ] Axis labels outside the polygon

### Architecture / Pipeline Diagrams (TikZ)
- [ ] Max 2–3 accent colors + neutral (gray/black)
- [ ] Consistent box style: same `rounded corners`, same `line width`
- [ ] Arrow direction = data flow (left→right or top→bottom)
- [ ] All text in English (NO hard-coded Chinese in submission)
- [ ] Font: sans-serif, minimum 7pt
- [ ] Width fits column constraint

### Network / Graph Visualizations
- [ ] Node color by type (legend required)
- [ ] Node size by degree or importance
- [ ] Edge thickness by weight or confidence
- [ ] Force-directed or hierarchical layout (not random)

### Timeline / Attack Chain Diagrams
- [ ] Time axis clearly labeled with units
- [ ] Attack phases color-coded (recon→exploit→C2→exfil)
- [ ] Arrows show causal relationships
- [ ] Duration represented by segment length (proportional)

### Waterfall / Incremental Contribution Charts
- [ ] Positive increments one color; negative decrements another
- [ ] Connecting lines between bars
- [ ] Total bar visually distinct (darker or outlined)
- [ ] Labels on each segment showing delta value

### Stacked Area Charts
- [ ] Layer order: largest at bottom
- [ ] Semi-transparent fills (alpha 0.6–0.8)
- [ ] Legend order matches visual stacking order

For per-type pgfplots/matplotlib templates, see [figure-types.md](figure-types.md).

---

## Phase 5: Legend & Annotation Design

### Legend Placement

| Scenario | Position | Code |
|----------|----------|------|
| ≤ 3 items, space inside | Top-right or bottom-right inside | `at={(0.97,0.03)}, anchor=south east` |
| 4–5 items | Below plot, one row | `at={(0.5,-0.22)}, anchor=north, columns=N` |
| 6–8 items | Below plot, multi-row | `at={(0.5,-0.28)}, columns=3 or 4` |
| Shared for subfigures | Centered below entire figure | Manual `\tikz` legend strip |

### Legend Rules

1. **No border** — `draw=none` (modern convention)
2. **Column sep** ≥ 4pt to avoid cramping
3. **Order matches** visual order in the plot
4. **Font** same as or one step smaller than axis labels
5. **Never** overlap data points with legend box
6. **Enough items**: if a legend has only 1 item, annotate directly on the figure instead

### In-Figure Annotations

| Type | When | Style |
|------|------|-------|
| Direct labels | ≤ 3 series | Text next to line/bar (no legend needed) |
| Callout arrows | Highlight specific points | Thin arrow + text box |
| Shaded regions | Confidence intervals | Fill alpha = 0.15–0.25 |
| Reference lines | Thresholds, baselines | Dashed thin line + label |
| Inset/zoom | Crowded region | Bordered small axis inside main axis |

---

## Phase 6: Layout, Float Placement & Page Density

### 6a. Float Placement — The #1 Source of Layout Disasters

**Placement specifier rules** (the `[!t]` in `\begin{figure}[!t]`):

| Specifier | Meaning | When to Use |
|-----------|---------|-------------|
| `[!t]` | Top of page, override restrictions | **Default for most figures/tables** |
| `[!b]` | Bottom of page | Secondary; use for less important floats |
| `[!ht]` | Here first, then top | When figure must stay near reference text |
| `[!htbp]` | Try all positions | Last resort; gives LaTeX maximum freedom |
| `[H]` | Force HERE (requires `float` pkg) | **Avoid** — breaks float queue; use only for debugging |

**CRITICAL rules**:
1. Prefer `!` when floats drift too far from references; do not add it blindly to every float.
2. Avoid bare `[h]`; prefer `[!ht]` or `[!htbp]`.
3. For `figure*` / `table*`, default to `[!t]`/`[!p]`; `[b]` needs `stfloats`/`dblfloatfix` and class compatibility.
4. Order preservation: LaTeX processes floats in order per type — a stuck `figure` blocks subsequent figures.

### 6b. Page Density Tuning — Eliminating Wasted Space

LaTeX defaults are **extremely conservative**. Add this block to preamble (see [layout-placement.md](layout-placement.md) §3 for full parameter reference):

```latex
\renewcommand{\topfraction}{0.9}    \renewcommand{\bottomfraction}{0.8}
\renewcommand{\textfraction}{0.1}   \renewcommand{\floatpagefraction}{0.8}
\renewcommand{\dbltopfraction}{0.9} \renewcommand{\dblfloatpagefraction}{0.8}
\setcounter{topnumber}{3}  \setcounter{bottomnumber}{2}
\setcounter{totalnumber}{5}\setcounter{dbltopnumber}{2}
\setlength{\textfloatsep}{10pt plus 2pt minus 4pt}
\setlength{\floatsep}{8pt plus 2pt minus 2pt}
\setlength{\intextsep}{8pt plus 2pt minus 2pt}
\setlength{\dbltextfloatsep}{10pt plus 2pt minus 4pt}
```

### 6c. Single Figure/Table Placement

| Scenario | Best Practice |
|----------|--------------|
| Single-column figure | `\begin{figure}[!t]` + `width=\columnwidth` |
| Full-width figure (double-col paper) | `\begin{figure*}[!t]` + `width=\textwidth` |
| Single-column table | `\begin{table}[!t]` + `\resizebox{\columnwidth}{!}{...}` if wide |
| Full-width table | `\begin{table*}[!t]` |
| Figure near its first reference | `\begin{figure}[!ht]` — "here" first, then top |
| Keep float in its section | Add `\usepackage[section]{placeins}` → auto `\FloatBarrier` at sections |

### 6d. Multi-Figure Arrangements

| Layout | Panel Width | Template |
|--------|-----------|----------|
| 1×2 (most common) | `0.48\textwidth` | `minipage[b]` + `\hfill` |
| 1×3 | `0.32\textwidth` | `minipage[b]` + `\hfill` |
| 2×2 grid | `0.48\textwidth`, `\\[6pt]` between rows | Two rows of 1×2 |
| 2×3 grid (max) | `0.32\textwidth` | Two rows of 1×3 |
| 1 large + 2 small | `0.55` + `0.43\textwidth` (nested) | Asymmetric layout |

**KEY**: Always add `%` after `\end{minipage}` to prevent unwanted space between panels.

For complete code templates of all layouts, see [layout-placement.md](layout-placement.md) §5.

### 6e. Common Layout Failures (Top 5)

| Symptom | Fix |
|---------|-----|
| Float appears pages after reference | Add `!` to specifier; tune density params |
| Whole page whitespace + one float | `\floatpagefraction` → 0.8 |
| Table overflows column | `\resizebox{\columnwidth}{!}{...}` or `\footnotesize` + `\tabcolsep=3pt` |
| Gap between side-by-side panels | Add `%` after `\end{minipage}` |
| `figure*` ignores `[b]` | Use `[!t]` or load `stfloats` / `dblfloatfix` |

For the complete 10-item failure table and troubleshooting flowchart, see [layout-placement.md](layout-placement.md) §7.

### 6f. Sizing & Subfigure Rules

- Use **relative** sizing: `width=\columnwidth` / `0.48\textwidth` — never hardcode cm/mm
- Labels **(a)**, **(b)**, **(c)**: bold, 8–10pt, centered below
- Max **6 subfigures** per figure; all comparison panels share **same Y-axis range**

For publisher-specific dimensions, see [publisher-specs.md](publisher-specs.md).

---

## Phase 7: Table Visual Design

### Mandatory Style Rules

1. **booktabs** package: `\toprule`, `\midrule`, `\bottomrule` only
2. **NO vertical lines** — never use `|` in column spec
3. **NO `\hline`** — use `\cmidrule(lr){a-b}` for partial separators
4. **Best result** per column: `\textbf{99.08\%}`
5. **Second best** (optional): `\underline{98.54\%}`
6. **Direction indicators** in header: Acc↑, FPR↓, Latency↓
7. Row grouping via `\cmidrule(lr)` + indentation or `\multirow`
8. Table notes via `threeparttable` + `tablenotes`

### Table Font & Spacing

| Element | Rule |
|---------|------|
| Whole table | `\small` or `\footnotesize` for dense tables |
| Column header | `\textbf{}`, same font as body |
| Line spacing | `\renewcommand{\arraystretch}{1.15}` for breathing room |
| Column padding | `\setlength{\tabcolsep}{4pt}` to prevent overflow |

### Table Width & Decimal Alignment

- Overflow fix: `\resizebox{\columnwidth}{!}{...}` or `tabularx`
- **Decimal consistency**: same column = same decimal places (99.10%, 98.54%, 97.32%)

---

## Phase 8: Caption & Label Formatting

### Caption Rules

1. **Self-contained**: readable without main text; include what, how, key takeaway
2. **End with period**; figure caption below, table caption above
3. **`\label` immediately after `\caption`** on consecutive lines
4. **Panel references in caption**: `(a) CICAPT-IIoT; (b) LANL` — in text: `Fig.~\ref{fig:x}(a)`
5. Caption format auto-handled by document class (Fig./TABLE/Figure:) — do NOT manually format; see [publisher-specs.md](publisher-specs.md) for per-publisher styles

---

## Phase 9: Cross-Reference & Hyperlink Audit

### Cross-Reference Checks

1. Every `\label{fig:*}` / `\label{tab:*}` must have a matching `\ref{}` in text
2. Every `\ref{}` must have a matching `\label{}`; check for "[?]" in compiled PDF
3. **Always** use `~` (non-breaking space): `Fig.~\ref{}`, `Table~\ref{}`, `Eq.~\eqref{}`
4. In-text: `Fig.~\ref{fig:x}` / `Table~\ref{tab:x}` / `Eq.~\eqref{eq:x}`
5. At sentence start: spell out fully — `Figure~\ref{}`, `Table~\ref{}`, `Equation~\eqref{}`

### Hyperlink Color Audit

1. Internal links (Fig/Table/Eq): subdued color, NOT bright red/neon blue
2. Citations: different hue from internal links
3. Camera-ready: follow venue rules (some require hidden links; IEEE PDF eXpress requires no active links/bookmarks)
4. All links of same type = same color throughout

```latex
% Review draft: subtle colored links
\hypersetup{
  colorlinks=true,
  linkcolor=black!70!blue,
  citecolor=black!60!green,
  urlcolor=black!60!purple
}
```

```latex
% Camera-ready when venue requires no active link styling
\hypersetup{hidelinks}
```

---

## Phase 10: Accessibility Testing

1. **Grayscale**: Convert PDF to grayscale; every series must be distinguishable by line style + marker alone
2. **Colorblind**: Test with Color Oracle or Coblis (Protanopia + Deuteranopia + Tritanopia)
3. **Contrast**: follow WCAG targets as baseline: normal text >= 4.5:1, graphical objects >= 3:1.

---

## Phase 11: Pre-Submission Figure Checklist

```
Complete Figure/Table Quality Checklist:

Color & Encoding:
- [ ] All figures use the SAME Okabe-Ito (or chosen) palette
- [ ] Same entity = same color/marker in every figure
- [ ] Triple encoding (color + line + marker) on all multi-series plots
- [ ] Grayscale test passed; colorblind simulation passed

Typography:
- [ ] Figure/text fonts follow venue template; labels remain legible (recommended >= 7pt)
- [ ] Any text below 6pt is explicitly allowed by the target venue
- [ ] All fonts embedded in PDF

Float Placement & Page Density:
- [ ] Float specifiers are intentional (avoid bare [h]; use `!` when drift occurs)
- [ ] Page density params tuned (topfraction=0.9, textfraction=0.1, etc.)
- [ ] No page with only one small float + large whitespace
- [ ] No float appears more than 1 page away from its first \ref
- [ ] figure* / table* placement matches class behavior (`[!t]` default; `[b]` only with verified support)
- [ ] No "Too many unprocessed floats" errors
- [ ] % after every \end{minipage} in side-by-side layouts

Content Quality:
- [ ] Plots are vector (pgfplots/tikz/PDF); raster images ≥ 300 DPI
- [ ] Every figure/table has \label and is \ref'd in text
- [ ] All \ref use ~ non-breaking space: Fig.~\ref, Table~\ref
- [ ] Captions are self-contained sentences ending with period
- [ ] ACM submissions: each figure has a meaningful `\Description{...}` accessibility text
- [ ] No Chinese/non-English text in any figure (submission version)
- [ ] Panel labels (a)(b)(c) present, bold, consistent style
- [ ] Legend does not overlap data; no border; correct order
- [ ] Axis labels include units in parentheses
- [ ] Figure width uses relative sizing (\columnwidth / \textwidth)

Tables:
- [ ] booktabs only, no vertical lines, no \hline
- [ ] Best result bolded per column; decimal places consistent
- [ ] Direction indicators (↑/↓) in headers
- [ ] No table overflows column width

Cross-References & Links:
- [ ] Hyperlinks follow venue policy (review vs camera-ready, PDF eXpress constraints if applicable)
- [ ] Internal ref color ≠ citation color ≠ URL color
- [ ] No overfull hbox warnings from figures/tables
```

---

## Additional Resources

- [color-reference.md](color-reference.md) — Full palette specs, LaTeX/Python definitions, CMYK notes, domain conventions
- [figure-types.md](figure-types.md) — Per-type pgfplots/TikZ/matplotlib templates with code
- [publisher-specs.md](publisher-specs.md) — Detailed per-publisher specs, caption styles, file format requirements
- [layout-placement.md](layout-placement.md) — Float mechanics deep dive, multi-figure templates, page density tuning, troubleshooting guide
