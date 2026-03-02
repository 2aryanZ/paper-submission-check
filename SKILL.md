---
name: paper-submission-check
description: Pre-submission quality check for academic papers in LaTeX. Detects and removes AI-generated writing style (em dashes, focal words, -ing chains, negative parallelism, inflated significance), first-person pronoun overuse, symbol errors, capitalization inconsistencies, mixed Chinese/English punctuation, citation format issues, BIB file errors, and formatting problems. Supports Elsevier, IEEE, Springer, ACM templates. Use when reviewing papers before journal or conference submission, removing AI writing traces, or when the user mentions paper checking, proofreading, submission preparation, quality review, or AI style removal.
---

# Paper Pre-Submission Quality Check

Systematic quality inspection for academic papers before journal/conference submission. Covers language, formatting, symbols, AI-style detection, LaTeX issues, citation correctness, BIB integrity, and content structure.

## Workflow

Track progress through all phases:

```
Pre-Submission Check Progress:
- [ ] Phase 0: Pre-Check (detect citation style, count authors, identify template)
- [ ] Phase 1: Pronoun & Subjectivity Check (with quantitative thresholds)
- [ ] Phase 2: AI-Generated Style Detection & Removal
- [ ] Phase 3: Symbol & Punctuation Errors
- [ ] Phase 4: Capitalization Consistency
- [ ] Phase 5: LaTeX-Specific Issues (citation-style-aware)
- [ ] Phase 6: Grammar & Language Quality
- [ ] Phase 7: Tables, Figures & Numbers (with cross-reference verification)
- [ ] Phase 8: Content Structure & Completeness
- [ ] Phase 9: BIB File Integrity Check
- [ ] Phase 10: Final Pre-Submission Checklist
```

---

## Phase 0: Pre-Check

Before starting, determine these properties (they affect later phases):

### 1. Detect Citation Style

Search for `\bibliographystyle{}`:

| Style | Type | Citation Appearance | Sentence-Start Rule |
|-------|------|--------------------|--------------------|
| `elsarticle-num`, `IEEEtran`, `unsrt`, `plain` | **Numbered** | [1], [2] | Use `Author et al.~\cite{key}` or `The work in~\cite{key}` |
| `elsarticle-harv`, `apalike`, `natbib` | **Author-Year** | (Smith, 2024) | Can start with `\citet{key}` directly |

**CRITICAL for numbered style**: Do NOT write `the work of Author et al.~\cite{key}, who...` — this creates redundancy. Use one of:
- `Author et al.~\cite{key} proposed...` (author + number)
- `The work in~\cite{key} proposed...` (work-in-number reference)
- `In~\cite{key}, the authors proposed...` (in-number format)

### 2. Count Authors

Search for `\author{}`:
- **Single author**: "we/our" should be avoided, use passive or "this paper"
- **Two+ authors**: "we/our" is acceptable but should be used sparingly (see Phase 1 thresholds)

### 3. Identify Template & Journal

Search for `\documentclass{}` and `\journal{}`:
- Check if `\journal{}` still contains a **template default** value (e.g., "Nuclear Physics B" in elsarticle template — must be changed)
- Verify the document class matches the target journal

---

## Phase 1: Pronoun & Subjectivity Check

### Quantitative Thresholds

Count total occurrences of `\bwe\b` and `\bour\b` (excluding comments and code):

| Pronoun | Recommended Max (full paper) | Action if exceeded |
|---------|-----------------------------|--------------------|
| "we" | ≤15 | Replace excess with passive voice or "this paper" |
| "our" | ≤8 | Replace with "the proposed" / "the" |
| "us" | ≤3 | Replace with passive constructions |

### Section-Specific Rules

| Section | "we/our" Guidance |
|---------|-------------------|
| Abstract | Max 1-2; prefer "this paper proposes" |
| Introduction | Max 2-3 for contributions; "This paper proposes..." preferred for opening |
| Contributions list | "We propose..." is standard and acceptable |
| Method | Keep for formula derivations ("we compute..."); replace elsewhere with passive |
| Experiments | Prefer passive: "Experiments were conducted..." |
| Results/Discussion | Replace "our method" → "the proposed method" or method name |
| Conclusion | Prefer "This paper proposed..." or passive |
| Future Work | "we" is acceptable for describing future plans |

### The "our proposed X" Rule

**"our proposed X" is always redundant** — either "our X" or "the proposed X", never both. Search for and replace:

```
our proposed method   → the proposed method
our proposed approach → the proposed approach  
our proposed algorithm → the proposed algorithm
```

### Subjective Language (always replace)

| Subjective | Objective |
|------------|-----------|
| We believe that X | The results indicate X |
| In our opinion | Based on the experimental evidence |
| We feel this is important | This is significant because |
| Our method is the best | The proposed method outperforms |

---

## Phase 2: AI-Generated Style Detection & Removal

**This is the most critical phase.** Journal editors and reviewers increasingly detect AI-generated text. Major publishers (Elsevier, Springer Nature, IEEE) require disclosure of AI use, and undisclosed AI-generated text can lead to desk rejection or ethics investigation.

This phase has two parts: **Detection** (find AI patterns) and **Removal** (rewrite to sound human).

### Step 2a: Detect AI Patterns by Severity

Scan for patterns in order of severity (S1 = desk rejection risk, S2 = major revision risk):

**S1 — Desk Rejection Risk (fix every instance):**

| Pattern | What to Search | Threshold |
|---------|---------------|-----------|
| Em dash overuse | `—` or `---` | ≤3 total, 0 in abstract |
| 21 focal words | `delve`, `tapestry`, `landscape` (figurative), `nuanced`, `multifaceted`, `intricate`, `meticulous`, `pivotal`, `underscore`, `commendable` | 0 instances |
| Participial -ing chains | `, highlighting`, `, underscoring`, `, demonstrating`, `, showcasing`, `, reflecting`, `, contributing`, `, ensuring`, `, fostering` | ≤3 total |
| Tier-1 AI phrases | `garnered attention`, `pave the way`, `testament to`, `realm of`, `myriad of`, `plethora of`, `poised to revolutionize` | 0 instances |

**S2 — Major Revision Risk (fix all instances):**

| Pattern | What to Search | Threshold |
|---------|---------------|-----------|
| Negative parallelism | `not only...but also`, `not just...but`, `goes beyond...to` | ≤1 total |
| Rule of Three | Three abstract adjectives joined by "and" (e.g., "accuracy, efficiency, and robustness") | Replace with data |
| Inflated significance | `pivotal`, `crucial`, `vital`, `watershed`, `groundbreaking`, `transformative`, `paradigm shift` | Replace with specifics |
| Vague attributions | `researchers have shown`, `studies indicate`, `experts argue`, `it is widely recognized` | Replace with citations |
| Positivity bias | Missing limitations section, no failure cases discussed | Add honest limitations |

**S3 — Minor Revision (fix most):**

| Pattern | What to Search | Threshold |
|---------|---------------|-----------|
| Nominalizations | `utilization`, `implementation`, `optimization`, `facilitation` | Convert to verbs |
| Conjunctive saturation | `Furthermore`, `Moreover`, `Additionally` starting consecutive paragraphs | ≤3 each total |
| Formulaic transitions | "Having discussed X, we now turn to Y" | 0 instances |
| Correlative conjunctions | `whether...or`, `both...and`, `neither...nor` | ≤2 total |
| Hedge stacking | "could potentially suggest that it might" | ≤1 hedge per sentence |

### Step 2b: Rewrite with Human Style

Apply these golden rules when rewriting:

1. **Specific beats impressive**: Replace every adjective with a number
2. **Active beats nominal**: "X uses Y" not "the utilization of Y by X"
3. **Short beats long**: If a sentence has >30 words, split it
4. **Direct beats hedged**: "X improves Y" not "X could potentially improve Y"
5. **Cited beats claimed**: "Smith et al. showed X" not "researchers have shown X"
6. **Honest beats promotional**: Include real limitations, not vague future work
7. **Varied beats formulaic**: Don't start every paragraph with "Furthermore"
8. **Simple beats ornate**: "use" not "utilize", "show" not "underscore"

### Quick Before/After Reference

| AI-Generated | Human-Written |
|-------------|---------------|
| "This paper delves into the intricate challenges of anomaly detection" | "This paper addresses anomaly detection in streaming graphs" |
| "The method — leveraging sketch structures — achieves remarkable performance across diverse datasets" | "The method uses sketch structures and achieves 0.998 AUC on CICIDS2019" |
| "These findings not only validate the effectiveness but also underscore the potential, demonstrating superior adaptability" | "The method outperforms all baselines on three of four datasets (Table 3)" |
| "Furthermore, the comprehensive evaluation demonstrates both efficiency and robustness" | "The method processes 1M edges in 12 seconds with constant memory" |

For the complete AI phrase database, see [ai-phrases.md](ai-phrases.md).
For the detailed AI style removal guide with 13 patterns and rewriting strategies, see [ai-style-removal.md](ai-style-removal.md).

---

## Phase 3: Symbol & Punctuation Errors

### Mixed Chinese/English Punctuation (Critical for CJK authors)

Search for Chinese characters in English text:

| Chinese | English Correct | Search Pattern |
|---------|----------------|---------------|
| （ ） | ( ) | `\uff08`, `\uff09` |
| ， | , | `\uff0c` |
| 。 | . | `\u3002` |
| ； | ; | `\uff1b` |
| ： | : | `\uff1a` |
| " " | " " or `` '' (LaTeX) | `\u201c`, `\u201d` |
| ' ' | ' ' or ` ' (LaTeX) | `\u2018`, `\u2019` |
| 、 | , | `\u3001` |
| — | --- (LaTeX em-dash) | `\u2014` |

**All Chinese punctuation in English papers is an error. Zero tolerance.**

### Dash Errors in LaTeX

| Usage | Correct LaTeX | Wrong |
|-------|--------------|-------|
| Hyphen (compound words) | `-` | |
| En-dash (number ranges) | `--` (e.g., pages 1--10) | `-` for ranges |
| Em-dash (parenthetical) | `---` | `--` for parenthetical |
| Minus sign (math) | `$-$` | `-` outside math mode |

### Space Errors

Search with regex for these patterns:

| Error | Correct | Regex |
|-------|---------|-------|
| Double space in text | Single space | `  +` (two or more spaces) |
| Missing space after period | `method. The` | `\.\w` |
| Space before comma | `method,` | ` ,` |
| No space after comma | `method, which` | `,[^ \\$~\n}]` |
| No space before `(` | `method (CMS)` | `\w\(` |

### Bracket Consistency

- All parentheses must be English `( )`, not Chinese `（ ）`
- Check for unmatched brackets
- Abbreviation pattern: full name + (ABBR) at first mention, then ABBR only

---

## Phase 4: Capitalization Consistency

### Section Titles

Check that ALL section/subsection titles follow ONE consistent style:

| Style | Example | Check |
|-------|---------|-------|
| Title Case | `\section{Related Work}` | First letter of major words capitalized |
| Sentence case | `\section{Related work}` | Only first word capitalized |
| ALL CAPS | `\section{EXPERIMENTS}` | Every letter capitalized |

**Error**: Mixing styles (e.g., "Related Work" + "EXPERIMENTS" + "method"). Pick one and apply consistently.

### Method/Model Names

- Consistency: same capitalization everywhere (e.g., "SBEAD" not "Sbead" or "sbead")
- First mention: full name + abbreviation
- After first mention: abbreviation only

### Acronyms

- Define every acronym at first use (including in the abstract separately from body)
- Never start a sentence with an undefined acronym
- Create a mental or explicit list of all acronyms; verify each is defined

---

## Phase 5: LaTeX-Specific Issues

### Non-Breaking Spaces Before Citations and References

```latex
% WRONG — line break may separate text from citation/reference
as shown in previous work \cite{smith2024}
as shown in Fig. \ref{fig:demo}
as shown in Table \ref{tab:results}

% CORRECT — non-breaking space prevents separation
as shown in previous work~\cite{smith2024}
as shown in Fig.~\ref{fig:demo}
as shown in Table~\ref{tab:results}
```

**Rule**: Always use `~` before `\cite{}`, `\ref{}`, `\eqref{}`.

Also check: `Table` or `Fig.` on one line with `\ref{}` on the next line → must be on same line with `~`.

### Citation at Sentence Beginning (Style-Dependent)

**For NUMBERED citation style** (`elsarticle-num`, `IEEEtran`):

```latex
% WRONG — renders as "[5] pioneered..."
\cite{lo2022graphsage} pioneered the application...

% CORRECT options for numbered style:
Lo et al.~\cite{lo2022graphsage} pioneered...     % Author + [number]
The work in~\cite{lo2022graphsage} pioneered...    % "work in [number]"
In~\cite{lo2022graphsage}, the authors pioneered...% "In [number],"

% WRONG — redundant construction
the work of Author et al.~\cite{key}, who employed... 
% "the work of Author [15], who" is awkward and redundant

% CORRECT
Author et al.~\cite{key} employed...
% OR
The work in~\cite{key} employed...
```

**For AUTHOR-YEAR style** (`elsarticle-harv`, `natbib`):

```latex
% Use \citet for textual citation at sentence start:
\citet{lo2022graphsage} pioneered...  % → "Lo et al. (2022) pioneered..."
```

### Redundant Formatting

Search for doubled commands:
```
\textbf{\textbf{...}}    → \textbf{...}
\textit{\textit{...}}    → \textit{...}
\emph{\emph{...}}        → \emph{...}
```

### Float Placement

- `[htbp]` is recommended for general use
- `[H]` (from float package) forces exact placement — use sparingly
- `[t]` is preferred for top-of-page figures in two-column layouts
- Check that ALL figures and tables have `\label` and are referenced in text

### Common LaTeX Errors

| Error | Fix |
|-------|-----|
| `\textit` for math variables | Use `$x$` not `\textit{x}` |
| Bare `%` in text | Use `\%` |
| Bare `_` in text | Use `\_` (e.g., `TON\_IoT`) |
| `\fontsize` without `\selectfont` | Always pair them |
| Missing `\label` after `\caption` | Add `\label` right after `\caption` |
| `\journal{}` still has template default | Change to target journal name |

---

## Phase 6: Grammar & Language Quality

### Contractions (Forbidden in Academic Writing)

```
don't → do not       can't → cannot        won't → will not
it's → it is         that's → that is      there's → there is
we've → we have      we're → we are        isn't → is not
```

### Duplicate Content Detection

Search for repeated phrases within the same paragraph or section:
- Repeated sentence openings within a paragraph
- Same phrase appearing twice in the same paragraph (e.g., "To formally define the problem... To formally define the problem...")
- Same idea restated in different words back-to-back

### Comma Splice Detection

A comma splice is two independent clauses joined only by a comma. Search for patterns like:
```
, When → . When  (or ; When)
, This → . This  (or ; This)  
, It   → . It    (or ; It)
, The  → . The   (if both clauses are complete sentences)
```

### Tense Consistency

| Section | Recommended Tense |
|---------|-------------------|
| Abstract | Past (what was done) + Present (what results show) |
| Introduction | Present (general facts) + Past (prior work) |
| Methods | Past (what was done) or Present (the algorithm does X) |
| Results | Past (experiments showed) |
| Discussion | Present (results suggest) + Future (future work will) |

### Redundant Phrases

| Verbose | Concise |
|---------|---------|
| in order to | to |
| due to the fact that | because |
| it can be seen that | (delete, start with the observation) |
| a large number of | many |
| in the case of | for / when |
| with respect to | for / regarding |
| on the other hand | however / alternatively |
| it is well-established that | (delete, state the fact directly) |
| it is important to note that | (delete, state the fact directly) |

### Common Grammar Errors in Non-Native English

| Error | Correct |
|-------|---------|
| "researches" (as plural noun) | "studies" or "research efforts" |
| "an anomaly detection" | "anomaly detection" (uncountable) |
| "datas" | "data" (already plural) |
| "informations" | "information" (uncountable) |
| "the Equation 1" | "Equation 1" or "Eq.~(1)" |
| "as shown in the Fig. 1" | "as shown in Fig.~1" |
| "in network environment" | "in the network environment" (missing article) |

---

## Phase 7: Tables, Figures & Numbers

### Tables

- Bold the best result in each column: `\textbf{0.9982}` — NOT double bold `\textbf{\textbf{...}}`
- Consistent decimal precision (e.g., all 4 decimal places in same table)
- Direction indicators: ↑ (higher is better), ↓ (lower is better)
- Use `booktabs` package (`\toprule`, `\midrule`, `\bottomrule`)
- Every table must be referenced in text

### Figures

- Vector format (PDF/EPS) for plots, not PNG/JPG
- Captions should be self-contained (understandable without reading main text)
- Font size in figures should be readable (not too small after scaling)
- Every figure must be referenced in text
- Consistent color scheme across all figures

### Number Cross-Reference Verification

**CRITICAL**: Verify that every number mentioned in the text matches its source:

- Numbers in abstract must match numbers in tables/results
- Dataset statistics in text (e.g., "4,554,344 communications") must match Table values
- Claimed improvements in text ("49 percentage points higher") must be verifiable from tables
- Model names and their associated numbers must be consistent

| Check | Example Error |
|-------|---------------|
| Text vs Table mismatch | Text says "4,554,343" but Table says "4,554,344" |
| Abstract vs Results mismatch | Abstract says "0.998 AUC" but table shows "0.9982" |
| Percentage claim errors | "49 percentage points" from 0.51 to 0.998 = 0.488, not 0.49 |

### Number Formatting Rules

| Rule | Wrong | Correct |
|------|-------|---------|
| Spell out numbers < 10 at sentence start | "4 datasets were used" | "Four datasets were used" |
| Numbers with units together | "5 %" | "5\%" |
| Thousands separator | "4554344" | "4,554,344" |
| Decimal consistency | "0.997" and "0.9984" | Same decimal places in same table |

---

## Phase 8: Content Structure & Completeness

### Abstract Check

- [ ] Length: 150--300 words (check journal requirements)
- [ ] Contains: problem, approach, key results with numbers, significance
- [ ] No citations in abstract
- [ ] No undefined abbreviations (define in abstract even if defined in body)
- [ ] First sentence is NOT a generic statement ("With the rapid development of...")
- [ ] Numbers in abstract match numbers in results tables

### Contribution Check

- [ ] Contributions are specific and measurable
- [ ] Each contribution maps to a section in the paper
- [ ] Number of contributions: 3--5 (not too many)

### Terminology Consistency

Pick one term and use throughout:

| Inconsistent | Pick One |
|-------------|----------|
| "anomaly detection" / "anomalous detection" / "AD" | Pick one form after definition |
| "graph stream" / "streaming graph" / "graph streams" | Pick one form |
| "dataset" / "data set" / "benchmark" | Be consistent |
| "TON_IoT" / "TON-IoT" / "TON\_IoT" | Match the original paper's name with `\_` in LaTeX |

### Self-Citation Anonymization (for blind review)

- No author names in text if double-blind
- Replace "In our previous work [X]" with "In prior work [X]"
- Check PDF metadata (author field)

---

## Phase 9: BIB File Integrity Check

**This phase was added based on real-world errors found in submissions.**

### Structural Integrity

Check every BIB entry for:

1. **Matching braces**: Every `@type{key,` must have a closing `}`
2. **No nested entries**: One entry must be fully closed before the next begins
3. **Required fields present**: Check `title`, `author`, `year` at minimum
4. **No trailing comma after last field** (some BibTeX implementations fail)

### Common BIB Errors

| Error | Description |
|-------|-------------|
| Missing closing `}` | An entry's `}` is missing, causing the next entry to nest inside |
| Duplicate keys | Two entries with the same citation key |
| Unused entries | Entries in .bib that are never `\cite{}`d (not an error, but cleanup) |
| Missing fields | Conference papers without `booktitle`, articles without `journal` |
| Encoding issues | Non-ASCII characters in fields (use `{\"o}` not `ö`) |

### Cross-Reference Check

- Every `\cite{key}` in .tex has a matching entry in .bib
- No "Citation undefined" warnings
- Author names in text match BIB entries (e.g., if you write "Lo et al.", verify the BIB has `Lo` as first author)

---

## Phase 10: Final Pre-Submission Checklist

```
Final Submission Checklist:
- [ ] All figures are referenced in text
- [ ] All tables are referenced in text  
- [ ] All equations are numbered (if referenced) and referenced
- [ ] All acronyms defined at first use
- [ ] All \label{} have corresponding \ref{} (and vice versa)
- [ ] \journal{} contains correct target journal name (not template default)
- [ ] Page limit satisfied
- [ ] Bibliography formatted per journal style
- [ ] No orphan/widow lines (single line at top/bottom of page)
- [ ] No overfull hbox warnings (text overflowing margins)
- [ ] Author information correct (for non-blind submissions)
- [ ] Author information removed (for blind submissions)
- [ ] Supplementary materials prepared if required
- [ ] Cover letter prepared if required
- [ ] Highlights / graphical abstract if required (Elsevier)
- [ ] CRediT author statement (Elsevier)
- [ ] Data availability statement
- [ ] Declaration of competing interests
- [ ] All co-authors have approved the manuscript
- [ ] LaTeX compiles with zero errors and minimal warnings
- [ ] Spell check completed
- [ ] BIB file compiles without errors
```

---

## Report Format

After running all checks, produce a structured report:

```markdown
# Paper Pre-Submission Check Report

## Paper Info
- Template: [elsarticle / IEEEtran / ...]
- Citation Style: [numbered / author-year]
- Authors: [count]
- Target Journal: [name]

## Summary
- Total issues found: XX
- Critical (must fix): XX
- Warning (should fix): XX  
- Suggestion (optional): XX

## Pronoun Statistics
- "we" count: XX (threshold: ≤15) [OK/OVER]
- "our" count: XX (threshold: ≤8) [OK/OVER]

## Critical Issues
1. [Line XX] BIB entry missing closing brace → fix brace structure
2. [Line XX] Chinese bracket found: （ACCURACY）→ (ACCURACY)
3. [Line XX] AI-style phrase: "has garnered significant attention" → "has been widely studied"
4. ...

## Warnings
1. [Line XX] Inconsistent capitalization: "EXPERIMENTS" vs "Related Work"
2. [Line XX] Missing ~ before \cite: "work \cite{}" → "work~\cite{}"
3. [Line XX] Number mismatch: text says "4,554,343" but Table says "4,554,344"
4. ...

## Suggestions  
1. [Line XX] Consider replacing "novel" (used 4 times) with specific descriptors
2. [Line XX] Abstract opens with generic statement — consider starting with contribution
3. ...
```

## Additional Resources

- For the complete AI-generated phrase database, see [ai-phrases.md](ai-phrases.md)
- For the detailed AI style removal guide (13 patterns, severity levels, rewriting strategies), see [ai-style-removal.md](ai-style-removal.md)
- For the detailed pre-submission checklist with per-publisher requirements, see [checklist.md](checklist.md)
