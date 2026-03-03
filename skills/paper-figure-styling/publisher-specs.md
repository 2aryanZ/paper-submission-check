# Publisher-Specific Specifications

Detailed per-publisher requirements for figures, tables, fonts, and file formats. Referenced by [SKILL.md](SKILL.md).

Covers the major publishers used in cybersecurity and computer science research.

## Contents

- [Validation Note](#validation-note)
- [1. Elsevier](#1-elsevier-computers--security-jisa-information-sciences-etc)
- [2. IEEE](#2-ieee-tdsc-tifs-sp-infocom-etc)
- [3. Springer](#3-springer-lncs-nature-journals-jsac-etc)
- [4. ACM](#4-acm-ccs-asia-ccs-imc-etc)
- [5. USENIX](#5-usenix-security-osdi-nsdi-etc)
- [6. Cross-Publisher Quick Reference](#6-cross-publisher-quick-reference)
- [7. Template Switching Checklist](#7-template-switching-checklist)

## Validation Note

- Publisher policies change frequently. Treat numeric constraints (page limits, dimensions, submission formats) as starting points, not immutable truth.
- Before submission, verify the current author instructions/CFP for your exact venue and year.
- Snapshot reviewed on 2026-03-03 against official sources listed at the end of this file.

---

## 1. Elsevier (Computers & Security, JISA, Information Sciences, etc.)

### Document Classes
- `elsarticle` (legacy, still widely used)
- `cas-sc` (Complex Article Service, single column)
- `cas-dc` (Complex Article Service, double column)

### Figure Dimensions

| Layout | Width | Notes |
|--------|-------|-------|
| Single column | 90 mm (3.54 in) | `\columnwidth` in cas-dc |
| 1.5 column | 140 mm (5.51 in) | `1.5\columnwidth` (rarely used) |
| Double column | 190 mm (7.48 in) | `\textwidth` in cas-dc |
| Maximum height | 240 mm | Leave space for caption |

### Font Requirements

| Element | Font | Size |
|---------|------|------|
| Body text | Times / STIX Two | 10pt (template default) |
| Figure text | Arial or Helvetica (sans-serif) | 7–10pt after scaling |
| Table text | Same as body | `\small` or `\footnotesize` |
| Caption | Template-controlled | Auto; typically `\small` |
| Math | STIX Two Math / Times Math | Matches body |

### Caption Style
- Figures: **Fig. 1.** Description text.
- Tables: **Table 1** Description text.
- Separator: period + space for figures; no period for tables (template-dependent)
- Handled automatically by `cas-dc.cls`; do not manually format

### File Format Requirements

| Type | Preferred | Acceptable | Never |
|------|-----------|------------|-------|
| Line art | EPS, PDF | TIFF (1000 DPI) | JPEG |
| Photographs | TIFF (300 DPI) | JPEG (max quality) | PNG |
| Plots (pgfplots) | PDF (auto from LaTeX) | — | — |
| Combined | PDF | TIFF (600 DPI) | — |

### Color Policy
- RGB color space accepted for online publication
- Print journals: verify CMYK rendering in proof
- Color charges vary by journal and print workflow; confirm in the target journal's Guide for Authors

### Hyperlink Colors

```latex
% Elsevier review version
\hypersetup{colorlinks=true,
  linkcolor={blue!70!black},
  citecolor={green!50!black},
  urlcolor={purple!70!black}}

% Elsevier camera-ready (check specific journal)
% Some require hidelinks, some allow colored links
```

### Table Style
- `booktabs` required; no vertical rules
- `threeparttable` for table notes
- Elsevier templates support `\tnote{}` for in-table markers
- `\resizebox{\columnwidth}{!}{...}` for wide tables

### Special Requirements
- **Graphical abstract**: Required for many Elsevier journals (530 × 300 pixels, or proportional)
- **Highlights**: 3–5 bullet points
- **CRediT author statement**: Required

---

## 2. IEEE (TDSC, TIFS, S&P, INFOCOM, etc.)

### Document Classes
- `IEEEtran` (journal and conference)
- Conference variants: `\documentclass[conference]{IEEEtran}`
- Journal variants: `\documentclass[journal]{IEEEtran}`

### Figure Dimensions

| Layout | Width | Notes |
|--------|-------|-------|
| Single column | 88.9 mm (3.5 in) | `\columnwidth` |
| Double column | 182 mm (7.16 in) | `\textwidth` |
| Maximum height | 234 mm (9.19 in) | Including caption |

### Font Requirements

| Element | Font | Size |
|---------|------|------|
| Body text | Times New Roman | 10pt (journal), 9pt (conf) |
| Figure text | Arial or Helvetica | 8–10pt at print size |
| Table text | Same as body | `\footnotesize` to `\small` |
| Caption | Template-controlled | `\footnotesize` |
| Minimum any text | 6pt | After all scaling |

### Caption Style
- Figures: **Fig. 1.** Description text.
- Tables: **TABLE I** — all caps Roman numerals, centered
- IEEE is strict about this format; template handles it
- Use `\caption{}` normally; IEEEtran formats automatically

### File Format Requirements

| Type | Preferred | Notes |
|------|-----------|-------|
| All figures | EPS or PDF | Vector strongly preferred |
| Photographs | TIFF or PNG | 300 DPI minimum |
| Line art | EPS, PDF | 600 DPI if raster |
| Screen captures | PNG | 300 DPI minimum |

### Color Policy
- Color figures are free for online
- **Print**: Color may incur charges; design for grayscale compatibility
- IEEE strongly recommends figures work in both color and grayscale
- Include statement: "Color versions of one or more figures are available online"

### Hyperlink Colors

```latex
% IEEE review: colored links acceptable
\hypersetup{colorlinks=true,
  linkcolor=blue, citecolor=blue, urlcolor=blue}

% IEEE camera-ready: typically hidelinks
\hypersetup{hidelinks}
```

### Table Style
- `booktabs` recommended but not mandatory
- IEEE traditionally uses more horizontal rules than booktabs minimalism
- TABLE caption above, centered, ALL CAPS
- Roman numeral numbering (TABLE I, TABLE II)

### Special Requirements
- **IEEE Access**: Requires LaTeX source with all figures as separate files
- **Conference papers**: Page limits vary by venue/year; verify the active CFP
- **Journal**: Figure quality checked during proof stage
- References in IEEE style commonly use abbreviated journal titles; follow the required `.bst`/author guide

---

## 3. Springer (LNCS, Nature journals, JSAC, etc.)

### Document Classes
- `llncs` (Lecture Notes in Computer Science — conferences like ACSAC, RAID)
- `svjour3` (Springer journals)
- `nature` (Nature family journals)
- `sn-jnl` (newer Springer Nature template)

### Figure Dimensions

| Layout | Width | Notes |
|--------|-------|-------|
| Single column | 84 mm (3.31 in) | `\columnwidth` |
| Double column | 174 mm (6.85 in) | `\textwidth` |
| Maximum height | 240 mm | Springer; 170 mm for Nature |
| LNCS text width | 122 mm | Single-column format |

### Font Requirements

| Element | Font | Size |
|---------|------|------|
| Body text | Computer Modern / Times | 10pt |
| Figure text | Arial / Helvetica | 7–9pt at final size |
| LNCS body | Computer Modern | 10pt |
| Nature body | Custom Nature font | Set by template |

### Caption Style
- Figures: **Fig. 1** Description text (no period after number for some templates)
- Tables: **Table 1** Description text
- Springer journals: sentence case in captions
- LNCS: template handles format
- Nature: bold figure label, then regular text

### File Format Requirements (Nature)

| Type | Preferred | Resolution |
|------|-----------|------------|
| Line art / graphs | PDF, EPS | Vector preferred; 1000+ DPI if raster |
| Photographs | TIFF | 300–600 DPI |
| Mixed (line + photo) | PDF, TIFF | 600 DPI |

### Color Policy
- Springer: color free for online; may charge for print (journal-dependent)
- Nature: color free everywhere
- LNCS proceedings: color free (PDF only)
- Always design for grayscale as fallback

### Hyperlink Colors

```latex
% Springer review
\hypersetup{colorlinks=true,
  linkcolor=blue!80!black, citecolor=blue!80!black}

% Springer camera-ready: usually hidelinks
\hypersetup{hidelinks}
```

### Special Requirements
- **LNCS page limits**: venue-dependent; verify current CFP
- **Nature**: Figure panels labeled **a**, **b**, **c** (lowercase bold, no parentheses)
- Nature figures: submit as separate high-resolution files
- Nature display-item limits depend on article type; verify current Nature formatting guide

---

## 4. ACM (CCS, ASIA CCS, IMC, etc.)

### Document Classes
- `acmart` with format options:
  - `sigconf` (conference — CCS, IMC)
  - `acmlarge` (journal — TOPS, TISSEC)
  - `acmsmall` (shorter journal)

### Figure Dimensions

| Layout | Width | Notes |
|--------|-------|-------|
| Single column | 84 mm (3.31 in) | `\columnwidth` |
| Double column | 178 mm (7.01 in) | `\textwidth` |
| sigconf text width | 178 mm | Double-column conference |

### Font Requirements

| Element | Font | Size |
|---------|------|------|
| Body text | Linux Libertine | 10pt (acmart default) |
| Figure text | Arial / Helvetica or match body | 7–9pt |
| Code | Inconsolata | Template-set |

### Caption Style
- Figures: **Figure 1:** Description text.
- Tables: **Table 1:** Description text.
- Note: ACM uses "Figure" not "Fig." and includes colon
- acmart template handles this; use `\caption{}` normally

### File Format Requirements
- PDF or EPS for vector graphics
- PNG or TIFF for raster (300+ DPI)
- acmart auto-includes `graphicx`

### Color Policy
- Color free for all ACM publications (digital library is online-only)
- Still recommended to test grayscale for printed reading

### Hyperlink Colors
- acmart sets hyperlink colors automatically
- Default: dark blue for all links
- Override: `\hypersetup{...}` after `\documentclass`

### Special Requirements
- **CCS page limit**: varies by year/track; verify current CFP
- DOI fields: include DOI when available; do not fabricate missing DOIs
- ACM template: `\begin{teaserfigure}` for the teaser/hero figure
- **ACM computing classification**: Required in frontmatter
- ACM accessibility: provide `\Description{...}` for figures as required by `acmart`

---

## 5. USENIX (Security, OSDI, NSDI, etc.)

### Document Classes
- `usenixatc2024` or annual variants
- Based on modified `article` class
- Single-column for some workshops; typically double-column

### Figure Dimensions

| Layout | Width | Notes |
|--------|-------|-------|
| Single column | ~86 mm | `\columnwidth` |
| Double column | ~178 mm | `\textwidth` |

### Font Requirements

| Element | Font | Size |
|---------|------|------|
| Body text | Times | 10pt |
| Figure text | Helvetica / Arial | 7–9pt |
| Minimum | Venue/template-specific | Keep labels legible at final size |

### Caption Style
- Figures: **Figure 1:** Description text.
- Tables: **Table 1:** Description text.
- "Figure" in full (not "Fig.") in USENIX style

### Color and Format
- Color free (proceedings are digital)
- PDF figures preferred
- Grayscale recommended as courtesy

### Hyperlink Colors

```latex
% USENIX: no strong policy; hidelinks safest
\hypersetup{hidelinks}
```

### Special Requirements
- **Page limit**: venue/year-specific. Example: USENIX Security 2026 allows 13 pages in review, with final papers up to 20 pages.
- No author kit modifications (margin hacking = desk rejection)
- Appendix goes after references (some allow, some don't)

---

## 6. Cross-Publisher Quick Reference

### Dimension Summary

| Publisher | 1-col (mm) | 2-col (mm) | Max H (mm) |
|-----------|-----------|-----------|------------|
| Elsevier | 90 | 190 | 240 |
| IEEE | 88.9 | 182 | 234 |
| Springer | 84 | 174 | 240 |
| Nature | 89 | 183 | 170 |
| ACM | 84 | 178 | — |
| USENIX | ~86 | ~178 | — |

### Caption Format Summary

| Publisher | Figure | Table |
|-----------|--------|-------|
| Elsevier | Fig. 1. text. | Table 1 text. |
| IEEE | Fig. 1. text. | TABLE I text |
| Springer | Fig. 1 text | Table 1 text |
| Nature | **a** text (panel) | Table 1 text |
| ACM | Figure 1: text. | Table 1: text. |
| USENIX | Figure 1: text. | Table 1: text. |

### Hyperlink Policy Summary

| Publisher | Review | Camera-Ready |
|-----------|--------|-------------|
| Elsevier | Colored OK | Journal-dependent |
| IEEE | Colored links often acceptable | PDF eXpress venues: no active links/bookmarks |
| Springer | Colored OK | `hidelinks` |
| ACM | Auto by template | Auto by template |
| USENIX | Any | `hidelinks` safest |

### Journal Name Format in References

| Publisher | Rule | Example |
|-----------|------|---------|
| IEEE | **Abbreviated** (ISO 4) | IEEE Trans. Inf. Forensics Security |
| Elsevier | **Full name** | Computers & Security |
| ACM | **Full name** | ACM Computing Surveys |
| Springer | Journal-dependent | Varies |

### Figure File Format Priority

| Publisher | 1st Choice | 2nd Choice | Avoid |
|-----------|-----------|-----------|-------|
| Elsevier | EPS / PDF | TIFF (1000 DPI) | JPEG for plots |
| IEEE | EPS / PDF | TIFF / PNG | Low-res JPEG |
| Springer | PDF / EPS | TIFF (600 DPI) | — |
| ACM | PDF | PNG / TIFF | — |
| USENIX | PDF | PNG | — |

---

## 7. Template Switching Checklist

When migrating a paper between publishers:

```
Template Migration Checklist:
- [ ] Change \documentclass to new template
- [ ] Verify column widths (figures auto-scale if using \columnwidth/\textwidth)
- [ ] Check figure heights (relative sizing avoids issues)
- [ ] Update caption style (usually automatic with new class)
- [ ] Change \journal{} to target journal name
- [ ] Update bibliography style (.bst)
- [ ] Verify journal name format (abbreviated vs. full) in .bib
- [ ] Check hyperlink color policy (colored vs. hidelinks)
- [ ] Verify page limit compliance
- [ ] Ensure DOI is included where available (no fabricated DOI)
- [ ] Update abstract word count to new limit
- [ ] Verify font rendering (compile and check PDF)
- [ ] Run figure quality checklist from SKILL.md Phase 11
```

## Official Sources (Snapshot)

- Elsevier artwork instructions: https://www.elsevier.com/authors/policies-and-guidelines/artwork-and-media-instructions
- IEEE graphics quality guidelines: https://procomm.ieee.org/trans-journal-graphics-guidelines/
- IEEE PDF eXpress warning on links/bookmarks: https://ras.papercept.net/conferences/support/files/IEEEPDFExpressInstructions.pdf
- ACM `acmart` authoring and accessibility (`\Description`): https://authors.acm.org/proceedings/production-information/preparing-your-article-with-latex
- Nature formatting guide: https://www.nature.com/nature/for-authors/formatting-guide
- Nature image integrity/figure guidance: https://research-figure-guide.nature.com/figures/preparing-figures-our-specifications/
- USENIX Security 2026 CFP (page limits): https://www.usenix.org/conference/usenixsecurity26/call-for-papers
