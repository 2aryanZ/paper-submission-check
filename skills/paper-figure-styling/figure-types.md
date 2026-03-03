# Figure Type Templates & Guidelines

Per-type code templates and design rules for academic papers. Referenced by [SKILL.md](SKILL.md).

All templates assume the Okabe-Ito palette is defined (see [color-reference.md](color-reference.md)).

## Contents

- [1. Line Chart](#1-line-chart--method-comparison--sensitivity-analysis)
- [2. Bar Chart](#2-bar-chart--performance-comparison--ablation)
- [3. Dual-Axis Chart](#3-dual-axis-chart--performance-vs-cost-tradeoff)
- [4. ROC Curve](#4-roc-curve)
- [5. Precision-Recall Curve](#5-precision-recall-curve)
- [6. Heatmap / Confusion Matrix](#6-heatmap--confusion-matrix)
- [7. Box Plot / Violin Plot](#7-box-plot--violin-plot)
- [8. Scatter Plot](#8-scatter-plot--t-sne--umap--feature-visualization)
- [9. Radar / Spider Chart](#9-radar--spider-chart)
- [10. Architecture / Pipeline Diagram](#10-architecture--pipeline-diagram-tikz)
- [11. Network / Graph Visualization](#11-network--graph-visualization)
- [12. Timeline / Attack Progression Diagram](#12-timeline--attack-progression-diagram)
- [13. Waterfall / Incremental Contribution Chart](#13-waterfall--incremental-contribution-chart)

---

## 1. Line Chart — Method Comparison / Sensitivity Analysis

### When to Use
- Hyperparameter sensitivity (x = param value, y = metric)
- Convergence curves (x = epoch, y = loss/metric)
- Threshold sweeps (x = threshold, y = metric)

### pgfplots Template

```latex
\begin{tikzpicture}
\begin{axis}[
    width=\columnwidth,
    height=0.65\columnwidth,
    xlabel={Hyperparameter $\lambda$},
    ylabel={F1 Score (\%)},
    xmin=0, xmax=1,
    ymin=85, ymax=100,
    grid=major,
    grid style={dashed, gray!30},
    legend style={at={(0.5,-0.25)}, anchor=north, legend columns=3,
                  font=\sffamily\scriptsize, draw=none, column sep=4pt},
    every axis plot/.append style={line width=1.0pt, mark size=2.0pt},
    font=\sffamily\small,
    label style={font=\sffamily\small},
    tick label style={font=\sffamily\footnotesize},
]
\addplot[mark=*, acBlue] coordinates {(0.1,88) (0.3,93) (0.5,97) (0.7,95) (0.9,91)};
\addplot[mark=square*, acVermillion] coordinates {(0.1,85) (0.3,89) (0.5,92) (0.7,90) (0.9,87)};
\addplot[mark=triangle*, acGreen] coordinates {(0.1,82) (0.3,86) (0.5,90) (0.7,88) (0.9,84)};
\legend{APT-Fusion, Baseline A, Baseline B}
\end{axis}
\end{tikzpicture}
```

### Design Rules
- Y-axis range: truncate to data range (e.g., 85–100 not 0–100) for visibility
- X-axis: use log scale (`xmode=log`) if values span orders of magnitude
- At most 7 lines per plot; split into subfigures if more
- Solid lines for proposed + primary baselines; dashed for secondary
- Error band: `\addplot[fill=acBlue, fill opacity=0.15, draw=none] ... \closedcycle;`

### With Error Bands (Confidence Interval)

```latex
\addplot[name path=upper, draw=none] coordinates {(0.1,90) (0.5,99) (0.9,93)};
\addplot[name path=lower, draw=none] coordinates {(0.1,86) (0.5,95) (0.9,89)};
\addplot[fill=acBlue, fill opacity=0.15] fill between[of=upper and lower];
\addplot[mark=*, acBlue, line width=1.0pt] coordinates {(0.1,88) (0.5,97) (0.9,91)};
```

---

## 2. Bar Chart — Performance Comparison / Ablation

### When to Use
- Comparing methods on a single metric across datasets
- Ablation study (full model vs. variants)
- Category-level performance breakdown

### Grouped Bar Template

```latex
\begin{tikzpicture}
\begin{axis}[
    width=\columnwidth,
    height=0.6\columnwidth,
    ybar=2pt,
    bar width=8pt,
    ylabel={F1 Score (\%)},
    ymin=70, ymax=100,
    symbolic x coords={CICAPT-IIoT, LANL, DARPA},
    xtick=data,
    x tick label style={font=\sffamily\footnotesize},
    legend style={at={(0.5,-0.22)}, anchor=north, legend columns=3,
                  font=\sffamily\scriptsize, draw=none, column sep=4pt},
    nodes near coords,
    nodes near coords style={font=\sffamily\scriptsize, color=black},
    every node near coord/.append style={yshift=2pt},
    font=\sffamily\small,
    grid=major,
    grid style={dashed, gray!15},
    ymajorgrids=true,
    xmajorgrids=false,
]
\addplot[fill=acBlue, draw=acBlue!80!black] coordinates
    {(CICAPT-IIoT, 99.08) (LANL, 98.89) (DARPA, 97.5)};
\addplot[fill=acVermillion!75, draw=acVermillion!80!black] coordinates
    {(CICAPT-IIoT, 92.3) (LANL, 93.7) (DARPA, 89.2)};
\addplot[fill=acGreen!75, draw=acGreen!80!black] coordinates
    {(CICAPT-IIoT, 88.1) (LANL, 87.4) (DARPA, 85.9)};
\legend{APT-Fusion, Baseline A, Baseline B}
\end{axis}
\end{tikzpicture}
```

### With Hatching (Grayscale Fallback)

```latex
\pgfplotsset{
    /pgfplots/bar cycle list/.style={/pgfplots/cycle list={
        {fill=acBlue, draw=acBlue!80!black},
        {fill=acVermillion!75, draw=acVermillion!80!black,
         postaction={pattern=north east lines, pattern color=white}},
        {fill=acGreen!75, draw=acGreen!80!black,
         postaction={pattern=dots, pattern color=white}},
    }},
}
```

### Stacked Bar Template

```latex
\begin{axis}[
    ybar stacked,
    bar width=12pt,
    symbolic x coords={Method A, Method B, Method C},
    xtick=data,
    legend style={at={(0.5,-0.22)}, anchor=north, legend columns=3,
                  font=\sffamily\scriptsize, draw=none},
    ylabel={Execution Time (s)},
]
\addplot[fill=acBlue!70] coordinates {(Method A,12) (Method B,15) (Method C,20)};
\addplot[fill=acOrange!70] coordinates {(Method A,8) (Method B,5) (Method C,3)};
\addplot[fill=acGreen!70] coordinates {(Method A,3) (Method B,4) (Method C,2)};
\legend{Preprocessing, Training, Inference}
\end{axis}
```

### Design Rules
- Bar width: 8–14pt depending on number of groups
- Gap between groups ≥ bar width
- Value labels: omit if bars are crowded or if exact values are in a table
- Sort bars by value (descending) unless categorical order is meaningful
- Your method: always leftmost or otherwise first in the group

---

## 3. Dual-Axis Chart — Performance vs. Cost Tradeoff

### When to Use
- F1 vs. Parameters (model complexity analysis)
- Accuracy vs. Inference time
- Any two metrics with different scales

### Template

```latex
\begin{tikzpicture}
\begin{axis}[
    width=\columnwidth,
    height=0.6\columnwidth,
    xlabel={Hidden Dimension $d$},
    ylabel={F1 Score (\%)},
    ymin=80, ymax=100,
    xtick={64, 128, 256, 512},
    axis y line*=left,
    ylabel style={color=acBlue!80!black},
    ybar, bar width=14pt,
    font=\sffamily\small,
    nodes near coords,
    nodes near coords style={font=\sffamily\scriptsize},
    legend style={at={(0.5,-0.25)}, anchor=north, legend columns=2,
                  font=\sffamily\scriptsize, draw=none, column sep=6pt},
]
\addplot[fill=acBlue!75, draw=acBlue!80!black]
    coordinates {(64, 93.09) (128, 83.77) (256, 94.39) (512, 95.69)};
\addlegendentry{F1}
\addlegendimage{mark=diamond*, acVermillion, line width=1.2pt, dashed}
\addlegendentry{Params (M)}
\end{axis}

\begin{axis}[
    width=\columnwidth,
    height=0.6\columnwidth,
    ylabel={Parameters (M)},
    ymin=0, ymax=50,
    xtick={64, 128, 256, 512},
    axis y line*=right,
    axis x line=none,
    ylabel style={color=acVermillion!80!black},
]
\addplot[mark=diamond*, acVermillion, line width=1.2pt, dashed, mark size=2.5pt]
    coordinates {(64, 0.70) (128, 2.74) (256, 10.87) (512, 43.31)};
\end{axis}
\end{tikzpicture}
```

### Design Rules
- Left Y-axis color matches bars; right Y-axis color matches line
- Always include both Y-axis labels with units
- Legend must explain both scales

---

## 4. ROC Curve

### When to Use
- Binary classification performance at various thresholds
- Comparing multiple detectors

### Template

```latex
\begin{axis}[
    width=\columnwidth,
    height=\columnwidth,  % square for ROC
    xlabel={False Positive Rate},
    ylabel={True Positive Rate},
    xmin=0, xmax=1, ymin=0, ymax=1,
    grid=major, grid style={dashed, gray!20},
    legend style={at={(0.98,0.02)}, anchor=south east,
                  font=\sffamily\scriptsize, draw=none},
    font=\sffamily\small,
]
% Random classifier baseline
\addplot[acBlack!40, dashed, thin] coordinates {(0,0) (1,1)};
\addlegendentry{Random}

% Methods
\addplot[acBlue, mark=none, line width=1.2pt]
    coordinates {(0,0) (0.001,0.85) (0.01,0.95) (0.05,0.98) (0.1,0.99) (1,1)};
\addlegendentry{APT-Fusion (AUC=0.9912)}

\addplot[acVermillion, mark=none, line width=1.0pt, dashed]
    coordinates {(0,0) (0.005,0.70) (0.02,0.88) (0.1,0.95) (0.3,0.98) (1,1)};
\addlegendentry{Baseline A (AUC=0.9534)}
\end{axis}
```

### Design Rules
- **Square** aspect ratio (width = height)
- Include diagonal baseline (dashed gray)
- AUC value in legend: `Method (AUC = X.XXXX)`
- No markers on smooth curves (too many points)
- If all curves cluster near (0,1), add a **zoomed inset**

### Zoomed Inset

```latex
\begin{axis}[
    % ... main ROC axis ...
]
% Main curves here
\end{axis}

% Inset
\begin{axis}[
    at={(0.35\columnwidth, 0.08\columnwidth)},
    width=0.45\columnwidth, height=0.45\columnwidth,
    xmin=0, xmax=0.05, ymin=0.9, ymax=1,
    xlabel={}, ylabel={},
    font=\sffamily\tiny,
    axis background/.style={fill=white},
    axis line style={thin},
]
% Same curves, zoomed range
\end{axis}
```

---

## 5. Precision-Recall Curve

### When to Use
- Imbalanced datasets (cybersecurity: attack ≪ normal)
- More informative than ROC when positive class is rare

### Template

```latex
\begin{axis}[
    width=\columnwidth,
    height=\columnwidth,
    xlabel={Recall},
    ylabel={Precision},
    xmin=0, xmax=1, ymin=0, ymax=1,
    grid=major, grid style={dashed, gray!20},
    legend style={at={(0.02,0.02)}, anchor=south west,
                  font=\sffamily\scriptsize, draw=none},
    font=\sffamily\small,
]
% Prevalence baseline (e.g., 1% positive rate)
\addplot[acBlack!30, dashed, thin] coordinates {(0,0.01) (1,0.01)};
\addlegendentry{Prevalence}

\addplot[acBlue, mark=none, line width=1.2pt]
    coordinates {(0.5,1.0) (0.8,0.98) (0.95,0.95) (0.99,0.90) (1.0,0.85)};
\addlegendentry{APT-Fusion (AUPRC=0.9896)}
\end{axis}
```

### Design Rules
- Legend at **bottom-left** (opposite to ROC)
- Include prevalence baseline
- AUPRC value in legend
- Iso-F1 contour lines optional (shows F1-score levels)

---

## 6. Heatmap / Confusion Matrix

### When to Use
- Confusion matrix (predicted vs. actual classes)
- Correlation matrix (feature correlations)
- Attention weight visualization
- Hyperparameter grid search results

### pgfplots Confusion Matrix Template

```latex
\begin{axis}[
    width=0.8\columnwidth,
    height=0.8\columnwidth,
    xlabel={Predicted Label},
    ylabel={True Label},
    xticklabels={Normal, Attack},
    yticklabels={Attack, Normal},
    xtick={0, 1},
    ytick={0, 1},
    colormap/viridis,
    colorbar,
    colorbar style={ylabel={Count}},
    point meta min=0,
    point meta max=5000,
    font=\sffamily\small,
    tick label style={font=\sffamily\footnotesize},
]
\addplot[matrix plot, mesh/cols=2, mesh/rows=2,
         point meta=explicit] coordinates {
    (0,0) [4850]  (1,0) [12]
    (0,1) [3]     (1,1) [135]
};

% Cell annotations (white on dark, black on light)
\node[font=\sffamily\small, white] at (axis cs:0,0) {4850};
\node[font=\sffamily\small, white] at (axis cs:1,1) {135};
\node[font=\sffamily\small] at (axis cs:1,0) {12};
\node[font=\sffamily\small] at (axis cs:0,1) {3};
\end{axis}
```

### Design Rules
- Colormap: viridis (default) or cividis (strongest CVD safety)
- Cell annotations: **white text** on dark cells, **black text** on light cells
- Auto-threshold: annotation color flips at ~50% of max value
- Colorbar always present with label
- Axis labels: class names (not 0/1 indices)
- For normalized confusion matrix: show percentages with 1 decimal

---

## 7. Box Plot / Violin Plot

### When to Use
- Distribution of results across multiple runs
- Comparing variance across methods
- Showing robustness (low variance = robust)

### pgfplots Box Plot Template

```latex
\begin{axis}[
    width=\columnwidth,
    height=0.55\columnwidth,
    ylabel={F1 Score (\%)},
    boxplot/draw direction=y,
    xtick={1, 2, 3},
    xticklabels={APT-Fusion, Baseline A, Baseline B},
    x tick label style={font=\sffamily\footnotesize},
    font=\sffamily\small,
]
\addplot+[boxplot, fill=acBlue!30, draw=acBlue,
          boxplot prepared={
    median=98.9, upper quartile=99.2, lower quartile=98.5,
    upper whisker=99.5, lower whisker=97.8}]
    coordinates {};

\addplot+[boxplot, fill=acVermillion!30, draw=acVermillion,
          boxplot prepared={
    median=92.3, upper quartile=93.1, lower quartile=91.0,
    upper whisker=94.2, lower whisker=89.5}]
    coordinates {};
\end{axis}
```

### Design Rules
- Fill color: light (30% opacity) version of the method color
- Border color: full-strength method color
- Median line: thick, full color
- Individual data points overlaid if n ≤ 30 (jitter horizontally)
- Violin plot preferred when showing distribution shape matters

---

## 8. Scatter Plot — t-SNE / UMAP / Feature Visualization

### When to Use
- Embedding visualization (t-SNE, UMAP)
- Feature space separation quality
- Showing cluster structure

### pgfplots Template

```latex
\begin{axis}[
    width=\columnwidth,
    height=\columnwidth,
    xlabel={}, ylabel={},  % no labels for t-SNE/UMAP
    xtick=\empty, ytick=\empty,  % no ticks
    legend style={at={(0.02,0.98)}, anchor=north west,
                  font=\sffamily\scriptsize, draw=none},
    font=\sffamily\small,
    clip=false,
]
\addplot[only marks, mark=*, mark size=1pt, acBlue, opacity=0.5]
    coordinates {(1,2) (1.5,2.3) ...};
\addlegendentry{Normal (n=9500)}

\addplot[only marks, mark=triangle*, mark size=1.5pt, acVermillion, opacity=0.7]
    coordinates {(5,6) (5.2,5.8) ...};
\addlegendentry{Attack (n=500)}
\end{axis}
```

### Design Rules
- **No axis ticks or labels** for t-SNE/UMAP (dimensions are meaningless)
- Different **marker shapes** per class (not just color)
- Transparency: alpha=0.4–0.7 for overlapping points
- Attack class: larger markers (1.5×) and higher opacity for visibility
- Legend: class name + sample count
- Mark size: 0.8–1.5pt for large n (>1000); 2–3pt for small n (<200)

---

## 9. Radar / Spider Chart

### When to Use
- Multi-metric comparison across methods (5–8 metrics)
- Showing method strengths/weaknesses at a glance

### pgfplots Template (requires `pgfplots-radar` or manual polar)

```latex
% Manual approach using polar coordinates
\begin{polaraxis}[
    width=0.8\columnwidth,
    xtick={0, 60, 120, 180, 240, 300},
    xticklabels={F1, Precision, Recall, AUROC, AUPRC, MCC},
    x tick label style={font=\sffamily\footnotesize, anchor=south},
    ymin=80, ymax=100,
    ytick={80, 85, 90, 95, 100},
    y tick label style={font=\sffamily\tiny},
    legend style={at={(1.15,0.5)}, font=\sffamily\scriptsize, draw=none},
]
\addplot[acBlue, fill=acBlue, fill opacity=0.15, line width=1.0pt]
    coordinates {(0,99.1) (60,98.2) (120,100) (180,99.1) (240,100) (300,99.1) (360,99.1)};
\addlegendentry{APT-Fusion}

\addplot[acVermillion, fill=acVermillion, fill opacity=0.1, line width=0.8pt, dashed]
    coordinates {(0,92.3) (60,90.5) (120,94.1) (180,95.2) (240,93.8) (300,92.0) (360,92.3)};
\addlegendentry{Baseline}
\end{polaraxis}
```

### Design Rules
- **5–8 axes** maximum (more becomes unreadable)
- All axes same scale: [0,100] or normalize to [0,1]
- Your method: solid fill, higher opacity (0.15); baselines: lower (0.10), dashed
- Axis labels outside the polygon
- Grid rings: 3–5 concentric levels

---

## 10. Architecture / Pipeline Diagram (TikZ)

### When to Use
- System/model overview (Fig. 1 of most papers)
- Data processing pipeline
- Module interaction diagram

### Style Template

```latex
\begin{tikzpicture}[
    font=\sffamily\footnotesize,
    >=Latex,
    box/.style={draw=black!70, rounded corners=2pt, line width=0.6pt,
                fill=black!3, minimum height=10mm, minimum width=22mm,
                inner sep=3pt},
    accent/.style={box, fill=acBlue!8, draw=acBlue!60},
    arrow/.style={-Latex, line width=0.6pt, draw=black!60},
    label/.style={font=\sffamily\scriptsize, text=black!70},
    node distance=8mm and 8mm,
]

\node[box] (input) {Input Data};
\node[accent, right=of input] (proc) {Processing};
\node[accent, right=of proc] (model) {GNN Model};
\node[box, right=of model] (output) {Detection};

\draw[arrow] (input) -- (proc);
\draw[arrow] (proc) -- (model);
\draw[arrow] (model) -- (output);

\end{tikzpicture}
```

### Design Rules
- **2–3 accent colors max**; rest neutral gray/black
- Use `fill=acBlue!8` (very light) for key modules, not saturated fills
- Consistent box dimensions: all boxes same height unless semantically different
- Arrow style: uniform across entire diagram
- Font: sans-serif, ≥ 7pt
- **No Chinese text** in submission version
- Fit within column width (single or double)
- Left-to-right (Western reading) or top-to-bottom flow
- Group related modules with a dashed bounding box or background shade

---

## 11. Network / Graph Visualization

### When to Use
- Attack graph / provenance graph examples
- SO-ACG structure illustration
- Network topology

### TikZ Template

```latex
\begin{tikzpicture}[
    font=\sffamily\scriptsize,
    hps/.style={circle, draw=acBlue, fill=acBlue!15, minimum size=8mm, line width=0.5pt},
    nfr/.style={diamond, draw=acVermillion, fill=acVermillion!15, minimum size=8mm, line width=0.5pt},
    subj/.style={-Latex, acBlue, line width=0.7pt},
    obj/.style={-Latex, acOrange, dashed, line width=0.7pt},
    chain/.style={-Latex, acPurple, dotted, line width=0.7pt},
]

\node[hps] (h1) at (0,0) {$h_1$};
\node[nfr] (n1) at (2,0) {$n_1$};
\node[hps] (h2) at (4,0) {$h_2$};

\draw[subj] (h1) -- node[above, font=\sffamily\tiny] {subj} (n1);
\draw[obj] (n1) -- node[above, font=\sffamily\tiny] {obj} (h2);
\draw[chain] (h1) to[bend left=30] node[above, font=\sffamily\tiny] {chain} (h2);
\end{tikzpicture}
```

### Design Rules
- Node shape encodes node type (circle, diamond, rectangle, etc.)
- Node color from the paper's palette
- Edge style (solid/dashed/dotted) encodes relation type
- Edge thickness or color intensity encodes weight/confidence
- Legend box explaining node types and edge types (mandatory)
- Force-directed layout for organic graphs; hierarchical for DAGs

---

## 12. Timeline / Attack Progression Diagram

### When to Use
- Kill chain / attack phase visualization
- Temporal sequence of events
- Multi-stage attack illustration

### TikZ Template

```latex
\begin{tikzpicture}[
    font=\sffamily\footnotesize,
    phase/.style={draw=black!50, rounded corners=1pt, minimum height=7mm,
                  minimum width=18mm, inner sep=2pt, line width=0.5pt},
]
\node[phase, fill=acSky!30] (recon) at (0,0) {Recon};
\node[phase, fill=acOrange!30, right=4mm of recon] (exploit) {Exploit};
\node[phase, fill=acPurple!30, right=4mm of exploit] (c2) {C2};
\node[phase, fill=acVermillion!30, right=4mm of c2] (exfil) {Exfil};

\draw[-Latex, thick] (recon) -- (exploit);
\draw[-Latex, thick] (exploit) -- (c2);
\draw[-Latex, thick] (c2) -- (exfil);

% Time axis
\draw[->] ([yshift=-8mm]recon.south west) -- ([yshift=-8mm]exfil.south east)
    node[right, font=\sffamily\scriptsize] {Time};
\end{tikzpicture}
```

### Design Rules
- Color intensity increases with severity/stage progression
- Time axis always present with arrow and label
- Duration proportional to segment length (if data available)
- Causal arrows between phases

---

## 13. Waterfall / Incremental Contribution Chart

### When to Use
- Showing how each component contributes to final performance
- Ablation study visualization (alternative to table)

### Design Rules
- Start bar: full model performance
- Subsequent bars: show delta (positive = add, negative = remove)
- Positive delta: acGreen fill; Negative delta: acVermillion fill
- Connecting lines between bar tops
- Final bar: acBlue (the model's actual performance)
- Value labels on each bar showing the delta

---

## 14. Stacked Area Chart

### When to Use
- Showing composition over time (e.g., traffic type breakdown)
- Temporal trends of multiple components

### Design Rules
- Largest component at bottom for stability
- Semi-transparent fills (alpha 0.6–0.8)
- Legend order matches visual stacking order (bottom to top)
- Include total line on top (optional, solid black)
- X-axis: time with appropriate resolution

---

## 15. Bubble Chart / Multi-Dimensional Comparison

### When to Use
- Comparing methods on 3+ dimensions simultaneously
- X = Metric A, Y = Metric B, Size = Metric C (e.g., F1 vs Speed vs Params)

### Design Rules
- Bubble color by method (consistent with palette)
- Bubble size proportional to third variable (include size legend)
- Add method name labels near bubbles
- Grid for reference; logarithmic axes if ranges are wide
- Your method: slightly larger outline or glow effect for emphasis

---

## 16. Parallel Coordinates Plot

### When to Use
- Comparing methods across many metrics simultaneously (>5)
- Alternative to radar chart for higher dimensions

### Design Rules
- Each vertical axis = one metric, normalized to [0,1] or [min,max]
- One polyline per method
- Your method: thicker line (1.5pt) + full opacity
- Baselines: thinner (0.8pt) + reduced opacity (0.5)
- Axis labels at top; values at bottom
- Colorblind-safe line colors from palette

---

## 17. Matplotlib Export Settings (for Python-Generated Figures)

When generating figures with matplotlib for LaTeX inclusion:

```python
import matplotlib.pyplot as plt
import matplotlib as mpl

# Publication-quality settings
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'Helvetica'],
    'font.size': 8,
    'axes.labelsize': 9,
    'axes.titlesize': 9,
    'xtick.labelsize': 7,
    'ytick.labelsize': 7,
    'legend.fontsize': 7,
    'figure.figsize': (3.5, 2.5),  # single column width in inches
    'figure.dpi': 300,
    'savefig.dpi': 600,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.02,
    'pdf.fonttype': 42,  # embed fonts as TrueType
    'ps.fonttype': 42,
    'lines.linewidth': 1.0,
    'lines.markersize': 4,
    'axes.linewidth': 0.5,
    'grid.linewidth': 0.3,
    'grid.alpha': 0.3,
})

# Save as PDF (vector) for LaTeX
fig.savefig('figure.pdf', format='pdf')
```

### Double-Column Figure

```python
plt.rcParams['figure.figsize'] = (7.0, 3.0)  # double-column width
```
