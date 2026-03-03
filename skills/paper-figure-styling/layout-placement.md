# Layout, Float Placement & Page Density

Comprehensive guide to LaTeX float mechanics, multi-figure/table arrangement, page density optimization, and troubleshooting. Referenced by [SKILL.md](SKILL.md).

## Contents

- [1. How LaTeX Floats Actually Work](#1-how-latex-floats-actually-work)
- [2. Double-Column Float Behavior](#2-double-column-float-behavior)
- [3. Page Density Parameters](#3-page-density-parameters--full-reference)
- [4. Single Figure/Table Templates](#4-single-figuretable-templates)
- [5. Multi-Figure Layout Templates](#5-multi-figure-layout-templates)
- [6. Figure + Table on Same Page](#6-figure--table-on-same-page)
- [7. Troubleshooting Guide](#7-troubleshooting-guide)
- [8. Compactness Techniques](#8-compactness-techniques)
- [9. Float Placement Decision Flowchart](#9-float-placement-decision-flowchart)
- [10. Packages Reference](#10-packages-reference)
- [11. Pre-Layout Audit Checklist](#11-pre-layout-audit-checklist)

---

## 1. How LaTeX Floats Actually Work

Understanding the float algorithm prevents 90% of layout disasters.

### The Float Queue

LaTeX maintains **two independent queues**: one for `figure`/`figure*` and one for `table`/`table*`. When a float cannot be placed immediately, it enters the queue. **All subsequent floats of the same type are blocked** until the queue clears.

```
Source order:  Fig 1 → Fig 2 → Fig 3 → Table 1 → Fig 4
If Fig 1 gets stuck: Fig 2, 3, 4 are ALL deferred
Table 1 is unaffected (different queue)
```

### Placement Specifier Behavior

| Specifier | Tries | Notes |
|-----------|-------|-------|
| `[t]` | Top of current/next page | Subject to `\topfraction` limit |
| `[b]` | Bottom of current/next page | Subject to `\bottomfraction` limit |
| `[h]` | Here (where declared) | Subject to `\textfraction`; fails silently if not enough room |
| `[p]` | Float-only page | Subject to `\floatpagefraction` |
| `[!]` | Override fraction limits | Use when floats drift too far from reference text |
| `[H]` | Force here (float pkg) | Removes float from queue entirely; can cause ordering issues |

**Evaluation order**: LaTeX tries specifiers left-to-right. `[!tb]` tries top first, then bottom. If all fail, float enters the deferred queue.

### Why Bare `[h]` Almost Always Fails

`[h]` means "place here if there's enough room **AND** the remaining text on this page satisfies `\textfraction`". With default `\textfraction=0.2`, if less than 20% of the page would be text after the float, LaTeX rejects `[h]` and silently converts it to `[t]`. Since most figures occupy >80% of a column, `[h]` rarely succeeds.

**Fix**: Prefer `[!ht]` (try here then top) or `[!htbp]` for maximum flexibility.

---

## 2. Double-Column Float Behavior

In double-column documents (`twocolumn`, `cas-dc`, `IEEEtran`), `figure*` and `table*` span both columns. Their placement rules differ significantly from single-column floats.

### Key Differences

| Feature | `figure` (single-col) | `figure*` (double-col) |
|---------|----------------------|----------------------|
| Width | `\columnwidth` (~90mm) | `\textwidth` (~190mm) |
| Allowed positions | `[!htbp]` | `[!tp]` only in standard LaTeX |
| Bottom placement | Works with `[b]` | **Silently ignored** without `dblfloatfix` |
| Earliest appearance | Same page or next | **Always next page** if mid-page |
| Queue | figure queue | Separate double-column figure queue |

### Enabling Bottom Placement for `figure*`

```latex
\usepackage{stfloats}  % or \usepackage{dblfloatfix}
% Now figure*[!b] works in double-column documents
```

### Ordering Issues

`figure` (single-col) and `figure*` (double-col) are in **different queues**. This means:
- `figure*` Fig.1 followed by `figure` Fig.2 → Fig.2 may appear BEFORE Fig.1
- Solution: Place all figures of the same numbering sequence in a consistent float type, or use `\FloatBarrier` between them

---

## 3. Page Density Parameters — Full Reference

### Float Fraction Parameters

| Parameter | Default | Recommended | Effect |
|-----------|---------|-------------|--------|
| `\topfraction` | 0.7 | **0.9** | Max fraction of page top occupied by floats |
| `\bottomfraction` | 0.3 | **0.8** | Max fraction of page bottom for floats |
| `\textfraction` | 0.2 | **0.1** | Min fraction of page that must be text |
| `\floatpagefraction` | 0.5 | **0.8** | Min fraction of float-only page that must be floats |
| `\dbltopfraction` | 0.7 | **0.9** | Same as topfraction for double-column floats |
| `\dblfloatpagefraction` | 0.5 | **0.8** | Same as floatpagefraction for double-col |

### Float Count Parameters

| Parameter | Default | Recommended | Effect |
|-----------|---------|-------------|--------|
| `topnumber` | 2 | **3** | Max floats at top of page |
| `bottomnumber` | 1 | **2** | Max floats at bottom of page |
| `totalnumber` | 3 | **5** | Max floats per page |
| `dbltopnumber` | 1 | **2** | Max double-col floats at top |

### Vertical Spacing Parameters

| Parameter | Default | Tight | Effect |
|-----------|---------|-------|--------|
| `\textfloatsep` | 20pt±2pt | **10pt±2pt−4pt** | Between float at top/bottom and text |
| `\floatsep` | 12pt±2pt | **8pt±2pt−2pt** | Between consecutive floats |
| `\intextsep` | 12pt±2pt | **8pt±2pt−2pt** | Around `[h]` floats embedded in text |
| `\dbltextfloatsep` | 20pt±2pt | **10pt±2pt−4pt** | Double-col float to text |
| `\dblfloatsep` | 12pt±2pt | **8pt±2pt−2pt** | Between double-col floats |

### Complete Preamble Block

```latex
% === Page density optimization ===
\renewcommand{\topfraction}{0.9}
\renewcommand{\bottomfraction}{0.8}
\renewcommand{\textfraction}{0.1}
\renewcommand{\floatpagefraction}{0.8}
\renewcommand{\dbltopfraction}{0.9}
\renewcommand{\dblfloatpagefraction}{0.8}
\setcounter{topnumber}{3}
\setcounter{bottomnumber}{2}
\setcounter{totalnumber}{5}
\setcounter{dbltopnumber}{2}

% === Tighter float spacing ===
\setlength{\textfloatsep}{10pt plus 2pt minus 4pt}
\setlength{\floatsep}{8pt plus 2pt minus 2pt}
\setlength{\intextsep}{8pt plus 2pt minus 2pt}
\setlength{\dbltextfloatsep}{10pt plus 2pt minus 4pt}
\setlength{\dblfloatsep}{8pt plus 2pt minus 2pt}

% === Allow bottom placement for figure* in double-col ===
\usepackage{stfloats}
```

---

## 4. Single Figure/Table Templates

### 4a. Single-Column Figure (in double-column paper)

```latex
\begin{figure}[!t]
\centering
\begin{tikzpicture}
\begin{axis}[
    width=\columnwidth,
    height=0.65\columnwidth,
    % ... axis options ...
]
% ... plots ...
\end{axis}
\end{tikzpicture}
\caption{Description of the figure.}
\label{fig:single_col}
\end{figure}
```

### 4b. Full-Width Figure (spanning both columns)

```latex
\begin{figure*}[!t]
\centering
% content spanning full width
\caption{Description.}
\label{fig:full_width}
\end{figure*}
```

### 4c. Single-Column Table

```latex
\begin{table}[!t]
\centering
\caption{Table Title}
\label{tab:single}
\small
\begin{tabular}{lcccc}
\toprule
\textbf{Method} & \textbf{F1↑} & \textbf{Prec↑} & \textbf{Recall↑} & \textbf{AUC↑} \\
\midrule
Method A & 95.3\% & 94.1\% & 96.5\% & 98.7\% \\
Method B & \textbf{99.1\%} & \textbf{98.2\%} & \textbf{100.0\%} & \textbf{99.9\%} \\
\bottomrule
\end{tabular}
\end{table}
```

### 4d. Wide Table Fitting Single Column

When a table is slightly wider than column width:

**Strategy 1: Reduce font + padding (preferred — preserves readability)**
```latex
\begin{table}[!t]
\centering\caption{...}\label{...}
\footnotesize
\setlength{\tabcolsep}{3pt}
\begin{tabular}{lccccccc}
...
\end{tabular}
\end{table}
```

**Strategy 2: Rescale (use sparingly — may shrink text below 6pt)**
```latex
\resizebox{\columnwidth}{!}{\begin{tabular}{...}...\end{tabular}}
```

**Strategy 3: Promote to full-width**
```latex
\begin{table*}[!t]  % spans both columns
...
\end{table*}
```

### Decision Guide: When to Use `table*` vs `table`

| Columns in table | Recommendation |
|-----------------|----------------|
| ≤ 5 | `table` (single column) |
| 6–7 | `table` with `\footnotesize` + reduced `\tabcolsep` |
| 8+ | `table*` (full width) |
| Complex multi-row with notes | `table*` for readability |

---

## 5. Multi-Figure Layout Templates

### 5a. Two Panels Side-by-Side (1×2) — The Most Common

```latex
\begin{figure*}[!t]
\centering
\begin{minipage}[b]{0.48\textwidth}
\centering
  % === Panel (a) content here ===
  \par\smallskip
  {\small\bfseries (a)} {\small Learning rate sensitivity}
\end{minipage}%          ← THIS % IS CRITICAL — prevents inter-panel space
\hfill
\begin{minipage}[b]{0.48\textwidth}
\centering
  % === Panel (b) content here ===
  \par\smallskip
  {\small\bfseries (b)} {\small Dropout rate sensitivity}
\end{minipage}
\caption{Hyperparameter sensitivity analysis on CICAPT-IIoT.}
\label{fig:hp_sensitivity}
\end{figure*}
```

**Why `%` after `\end{minipage}`**: LaTeX treats the line break as a space character. In a horizontal layout, this extra space pushes the second minipage to the next line. The `%` comment character eats the line break.

### 5b. 2×2 Grid

```latex
\begin{figure*}[!t]
\centering
%--- Row 1 ---
\begin{minipage}[b]{0.48\textwidth}\centering
  % Panel (a)
  \par\smallskip{\small\bfseries (a)} {\small Caption A}
\end{minipage}%
\hfill
\begin{minipage}[b]{0.48\textwidth}\centering
  % Panel (b)
  \par\smallskip{\small\bfseries (b)} {\small Caption B}
\end{minipage}

\vspace{6pt}  % vertical gap between rows

%--- Row 2 ---
\begin{minipage}[b]{0.48\textwidth}\centering
  % Panel (c)
  \par\smallskip{\small\bfseries (c)} {\small Caption C}
\end{minipage}%
\hfill
\begin{minipage}[b]{0.48\textwidth}\centering
  % Panel (d)
  \par\smallskip{\small\bfseries (d)} {\small Caption D}
\end{minipage}
\caption{Four-panel comparison.}
\label{fig:grid2x2}
\end{figure*}
```

### 5c. Three in a Row (1×3)

```latex
\begin{figure*}[!t]
\centering
\begin{minipage}[b]{0.32\textwidth}\centering
  % Panel (a)
  \par\smallskip{\small\bfseries (a)} {\small Dataset 1}
\end{minipage}%
\hfill
\begin{minipage}[b]{0.32\textwidth}\centering
  % Panel (b)
  \par\smallskip{\small\bfseries (b)} {\small Dataset 2}
\end{minipage}%
\hfill
\begin{minipage}[b]{0.32\textwidth}\centering
  % Panel (c)
  \par\smallskip{\small\bfseries (c)} {\small Dataset 3}
\end{minipage}
\caption{Comparison across three datasets.}
\label{fig:three_datasets}
\end{figure*}
```

### 5d. 2×3 Grid (6 panels — maximum recommended)

```latex
\begin{figure*}[!t]\centering
% Row 1
\begin{minipage}[b]{0.32\textwidth}\centering...(a)...\end{minipage}%
\hfill
\begin{minipage}[b]{0.32\textwidth}\centering...(b)...\end{minipage}%
\hfill
\begin{minipage}[b]{0.32\textwidth}\centering...(c)...\end{minipage}
\vspace{6pt}
% Row 2
\begin{minipage}[b]{0.32\textwidth}\centering...(d)...\end{minipage}%
\hfill
\begin{minipage}[b]{0.32\textwidth}\centering...(e)...\end{minipage}%
\hfill
\begin{minipage}[b]{0.32\textwidth}\centering...(f)...\end{minipage}
\caption{...}\label{fig:grid2x3}
\end{figure*}
```

### 5e. Mixed: One Large + Two Small

```latex
\begin{figure*}[!t]\centering
\begin{minipage}[b]{0.52\textwidth}\centering
  % Large panel (a) — architecture or main result
  \par\smallskip{\small\bfseries (a)} {\small Overall architecture}
\end{minipage}%
\hfill
\begin{minipage}[b]{0.46\textwidth}\centering
  \begin{minipage}[b]{\textwidth}\centering
    % Small panel (b) — top right
    \par\smallskip{\small\bfseries (b)} {\small Detail view}
  \end{minipage}\\[4pt]
  \begin{minipage}[b]{\textwidth}\centering
    % Small panel (c) — bottom right
    \par\smallskip{\small\bfseries (c)} {\small Statistics}
  \end{minipage}
\end{minipage}
\caption{...}\label{fig:mixed}
\end{figure*}
```

### Panel Width Quick Reference

| Panels per row | Width each | Separator |
|---------------|-----------|-----------|
| 2 | `0.48\textwidth` | `\hfill` |
| 3 | `0.32\textwidth` | `\hfill` |
| 4 | `0.24\textwidth` | `\hfill` |
| 1 large + 1 small | `0.55\textwidth` + `0.43\textwidth` | `\hfill` |

---

## 6. Figure + Table on Same Page

To maximize page density, you can place a figure and table on the same page:

### Same Column (Stacked)

```latex
% Both [!t] — LaTeX stacks them at top of same column
\begin{figure}[!t]
\centering
% ... figure content ...
\caption{Figure caption.}\label{fig:x}
\end{figure}

\begin{table}[!t]
\centering
\caption{Table caption.}\label{tab:x}
% ... table content ...
\end{table}
```

With `topnumber=3` and tight `\floatsep`, both fit on one column.

### Adjacent Columns (figure left, table right)

Not directly controllable in LaTeX's float algorithm. If needed, use a single `figure*` environment containing both:

```latex
\begin{figure*}[!t]
\centering
\begin{minipage}[b]{0.48\textwidth}\centering
  % Figure content
  \par\smallskip{\small (a) Visualization}
\end{minipage}%
\hfill
\begin{minipage}[b]{0.48\textwidth}\centering
  \captionof{table}{Table inside figure environment}
  \label{tab:inside_fig}
  \small
  \begin{tabular}{lcc}
  \toprule
  ... \\
  \bottomrule
  \end{tabular}
\end{minipage}
\caption{Combined figure and table.}
\label{fig:combined_with_table}
\end{figure*}
```

Requires `\usepackage{caption}` for `\captionof`.

---

## 7. Troubleshooting Guide

### Problem: Float Appears Many Pages After Reference

**Diagnosis**: The float queue is jammed — an earlier float couldn't be placed, blocking all later floats.

**Fixes** (in order of preference):
1. Add `!` to all float specifiers: `[!t]` not `[t]`
2. Tune page density parameters (Section 3)
3. Add `\FloatBarrier` (from `placeins` package) before the problematic float
4. Use `\clearpage` at section boundaries (forces all pending floats)
5. Reduce figure height so it fits on the current page

### Problem: Page with One Small Float and Huge Whitespace

**Cause**: `\floatpagefraction` default (0.5) creates a float-only page even if the float is small.

**Fix**: Set `\renewcommand{\floatpagefraction}{0.8}` — float-only pages require ≥80% coverage.

### Problem: "Too Many Unprocessed Floats" Error

**Cause**: LaTeX can buffer at most 18 floats. Dense sections with many figures overwhelm this.

**Fixes**:
1. Add `\clearpage` or `\FloatBarrier` periodically (every 3–4 figures)
2. Use `\usepackage{morefloats}` to increase the buffer (up to 36)
3. Combine small related figures into multi-panel figures

### Problem: `figure*` Appears Before Single-Column `figure`

**Cause**: `figure` and `figure*` are in different queues; they can overtake each other.

**Fixes**:
1. Place `\FloatBarrier` between different float types
2. Reorder in source so `figure*` comes first
3. If using `placeins` with `[section]` option, floats are constrained per section

### Problem: Table Overflows Column / Margin

**Diagnosis**: Table content wider than `\columnwidth`.

**Fixes** (in order of preference):
1. Reduce `\tabcolsep`: `\setlength{\tabcolsep}{3pt}`
2. Use `\footnotesize` or `\scriptsize` for the table
3. Abbreviate column headers (e.g., "Prec." instead of "Precision")
4. `\resizebox{\columnwidth}{!}{...}` (last resort — check font remains ≥ 6pt)
5. Promote to `table*` (full width)

### Problem: Subfigures Misaligned Vertically

**Cause**: Panels have different heights; `minipage` default aligns at center.

**Fix**: Use `\begin{minipage}[b]{...}` — aligns at bottom (baseline). Or `[t]` for top alignment.

### Problem: Unwanted Horizontal Gap Between Side-by-Side Panels

**Cause**: Missing `%` after `\end{minipage}`.

**Fix**: Always append `%` immediately:
```latex
\end{minipage}%     ← this % is mandatory
\hfill
\begin{minipage}...
```

### Problem: Caption Orphaned on Next Page

**Cause**: Figure + caption together exceed remaining page space. LaTeX defers the entire float.

**Fixes**:
1. Shorten caption (move details to text)
2. Reduce figure height by 5–10%
3. Use `\vspace{-2pt}` between figure content and `\caption`
4. Split into subfigures in a shorter arrangement

### Problem: Large Whitespace Above/Below Floats

**Cause**: Default `\textfloatsep` and `\floatsep` are generous (20pt, 12pt).

**Fix**: Apply tight spacing (Section 3). Be conservative — too tight looks cramped.

### Problem: Figures Cluster at End of Paper

**Cause**: Float queue backed up throughout the paper; all floats flush at `\end{document}`.

**Fixes**:
1. Add `\clearpage` at major section boundaries (before Related Work, before Experiments, etc.)
2. Use `\usepackage[section]{placeins}` for automatic per-section float barriers
3. Tune page density parameters

---

## 8. Compactness Techniques

When approaching page limits:

### Reduce Float Vertical Spacing

```latex
\setlength{\abovecaptionskip}{4pt}   % space above caption (default 10pt)
\setlength{\belowcaptionskip}{2pt}   % space below caption (default 0pt)
\setlength{\textfloatsep}{8pt plus 2pt minus 4pt}
\setlength{\floatsep}{6pt plus 2pt minus 2pt}
```

### Reduce Table Row Height

```latex
\renewcommand{\arraystretch}{1.0}  % default is 1.0; reduce to 0.95 if desperate
\setlength{\tabcolsep}{3pt}        % default 6pt
```

### Compact Captions

```latex
\usepackage[font=small, labelfont=bf, skip=4pt]{caption}
% skip=4pt: gap between figure and caption (default 10pt)
```

### Combine Related Small Figures

Instead of:
```
Figure 3: Learning rate sensitivity
Figure 4: Dropout sensitivity
```

Combine into:
```
Figure 3: (a) Learning rate sensitivity; (b) Dropout sensitivity
```

This saves caption overhead and float spacing (~1cm per combined figure).

### Merge Related Tables

Instead of separate Table 4 (hidden dim) and Table 5 (GNN depth), combine into:
```
Table 4: Model Capacity Analysis
  (upper section: hidden dim; lower section: GNN depth)
```

---

## 9. Float Placement Decision Flowchart

```
Is the float related to nearby text?
├── YES → Use [!ht] (try here first, then top)
│         Does it fit in the current column?
│         ├── YES → It will appear here or top of current/next page
│         └── NO → Does it need full width?
│                   ├── YES → Use figure*[!t] (double-column)
│                   └── NO → Reduce size or split
└── NO (standalone results) → Use [!t] (top of page is fine)
                               Multiple similar floats together?
                               ├── YES → Combine into multi-panel figure
                               └── NO → Keep separate with [!t]
```

---

## 10. Packages Reference

| Package | Purpose | Command |
|---------|---------|---------|
| `placeins` | Float barriers at section boundaries | `\usepackage[section]{placeins}` or manual `\FloatBarrier` |
| `stfloats` / `dblfloatfix` | Allow `figure*[b]` in double-column | `\usepackage{stfloats}` |
| `float` | Provides `[H]` (force here) | `\usepackage{float}` — use sparingly |
| `morefloats` | Increase float buffer beyond 18 | `\usepackage{morefloats}` |
| `caption` | Customize caption font/spacing | `\usepackage[font=small,skip=4pt]{caption}` |
| `subcaption` | Formal subfigure numbering (a), (b) | `\usepackage{subcaption}` — alternative to minipage approach |
| `afterpage` | Defer command to next page boundary | `\afterpage{\clearpage}` |
| `wrapfig` | Text-wrapped figures | Avoid in double-column academic papers |

---

## 11. Pre-Layout Audit Checklist

```
Layout Quality Audit:
- [ ] All floats have [!t] or [!ht] (no bare [h] or [t])
- [ ] Page density params in preamble (Section 3 block)
- [ ] stfloats/dblfloatfix loaded for double-column papers
- [ ] No page with > 40% whitespace (excluding final page)
- [ ] No float > 1 page from its first \ref in text
- [ ] All figure*/table* use [!t] not [!b]
- [ ] % after every \end{minipage} in side-by-side layouts
- [ ] minipage uses [b] alignment for consistent baselines
- [ ] \hfill between panels (not manual \hspace)
- [ ] Panel widths sum to < 1.0\textwidth (leave room for \hfill)
- [ ] \FloatBarrier or \clearpage at major section boundaries if needed
- [ ] No "Too many unprocessed floats" error
- [ ] Tables: \resizebox only if text stays ≥ 6pt
- [ ] Combined related figures/tables where possible (saves ~1cm each)
- [ ] Captions concise (long captions push floats to next page)
- [ ] Compiled PDF reviewed page-by-page for visual spacing
```
