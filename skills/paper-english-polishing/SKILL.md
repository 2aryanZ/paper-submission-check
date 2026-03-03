---
name: paper-english-polishing
description: Paragraph-by-paragraph academic English polishing for LaTeX papers. Handles Chinese-to-English translation and native English refinement. Outputs structured diff tables (original/revised/reason) per paragraph, eliminates Chinglish patterns, enforces academic register, maintains terminology consistency, and avoids AI-generated text markers. Supports multi-paper workflows with venue-adaptive conventions. Use when the user mentions polishing, refining, improving English,润色, translation, native English, academic writing, paragraph editing, or sentence-level revision.
---

# Academic English Polishing

Paragraph-level polishing for academic papers targeting top-tier venues (IEEE S&P, USENIX Security, NeurIPS, ICML, TDSC, TIFS, etc.). Handles both Chinese-to-English translation and English-to-English refinement.

**Relationship to `paper-submission-check`**: That skill *detects* issues; this skill *rewrites* text. Run this skill first (polishing), then run `paper-submission-check` (validation).

## Execution Safety [CRITICAL]

Before any rewrite, lock these invariants:

- Never change technical facts: numbers, theorem statements, equations, symbols, citations, table/figure references.
- Never invent claims, datasets, baselines, or citations that are not in source text.
- Preserve author intent; when wording is ambiguous, keep a conservative rewrite and flag a question.
- Preserve all LaTeX commands and labels (`\label{}`, `\ref{}`, `\cite{}`) exactly unless user explicitly asks to refactor LaTeX.

## Workflow

```
Polishing Progress:
- [ ] Phase 0: Pre-Analysis (scope lock, language, venue, structure, terminology, bilingual setup)
- [ ] Phase 0b: Bilingual Scaffolding (if Chinese source: inject preamble, remove global CJK safely)
- [ ] Phase 1: Title & Abstract
- [ ] Phase 2: Introduction
- [ ] Phase 3: Related Work
- [ ] Phase 4: Method / Approach
- [ ] Phase 5: Experiments / Evaluation
- [ ] Phase 6: Discussion / Limitations
- [ ] Phase 7: Conclusion
- [ ] Phase 8: Appendix (if any)
- [ ] Phase 9: Cross-Section Consistency Verification
- [ ] Phase 10: Final AI-Style Sweep
- [ ] Phase 11: Submission Toggle (set \showchinesefalse, verify zero Chinese in PDF)
```

---

## Phase 0: Pre-Analysis

Before polishing, determine:

### 0. Scope Lock

- Confirm task granularity: sentence, paragraph, section, or full paper.
- For full papers, use chunked execution (3-8 paragraphs per batch) and keep a running terminology ledger.
- Decide rewrite strength: conservative (camera-ready), standard, or aggressive (translation-heavy draft).

### 1. Source Language & Task Type

| Scenario | Action |
|----------|--------|
| Chinese source → English target | Full translation + polishing (most aggressive rewriting) |
| Draft English by non-native speaker | Chinglish elimination + register upgrade |
| English revision / camera-ready | Light polishing, preserve author voice |

### 2. Target Venue

Read `\documentclass{}` and any `\journal{}` / `\conference{}` to identify the venue. Adapt tone:

| Venue Type | Style Notes |
|------------|-------------|
| Security (S&P, USENIX, CCS, NDSS) | Direct, precise; threat model must be crystal clear; avoid overclaiming |
| ML (NeurIPS, ICML, ICLR) | Formal but accessible; emphasize novelty and theoretical grounding |
| Systems (OSDI, SOSP, EuroSys) | Engineering-focused; reproducibility details matter |
| Journal (TDSC, TIFS, TKDE) | More thorough literature positioning; detailed experimental methodology |

### 3. Initialize Terminology Ledger

Create and maintain a terminology table throughout polishing. Pick ONE term per concept and enforce globally:

```
Terminology Ledger (update as polishing proceeds):
| Concept | Chosen Term | Rejected Alternatives |
|---------|-------------|----------------------|
| (fill during polishing) | | |
```

**Rules**: First occurrence defines full name + (ABBREVIATION). All subsequent occurrences use abbreviation only. Abstract defines abbreviations independently from body.

### 4. Bilingual Comparison Mode (Chinese → English only)

When source is Chinese, inject bilingual scaffolding into the LaTeX preamble so the PDF shows both languages during review, and hides Chinese with a single flag change before submission.

**Step 1: Add to preamble** (after existing `\usepackage` block):

```latex
% === Bilingual comparison mode ===
% Set \showchinesefalse before submission to hide all Chinese text
\usepackage{xcolor}
\usepackage{iftex}
\ifPDFTeX
  \usepackage{CJKutf8}
  \newcommand{\zhtext}[1]{\begin{CJK*}{UTF8}{gbsn}#1\end{CJK*}}
\else
  % XeLaTeX/LuaLaTeX: assume CJK-capable engine/font setup already exists
  \newcommand{\zhtext}[1]{#1}
\fi

\newif\ifshowchinese
\showchinesetrue

\newcommand{\zhpara}[1]{%
  \ifshowchinese
    \par\noindent{\small\color{blue!40!black}\zhtext{#1}}\par\vspace{0.3em}%
  \fi
}
\newcommand{\zhcaption}[1]{%
  \ifshowchinese
    {\small\color{blue!40!black}\zhtext{#1}}%
  \fi
}
```

**Step 2: Remove global CJK wrapper only if present**. If the document body is wrapped by one global `CJK*` environment, remove that wrapper and localize Chinese with `\zhpara{}`. If there is no global wrapper, skip this step.

**Step 3: Convert each section**. For every paragraph:
```latex
\zhpara{原始中文段落完整保留在此，包括所有公式和引用。}
Polished English paragraph here, with all formulas and citations.
```

**Design rationale**: Paragraph-level alignment, NOT sentence-level. Good translation restructures sentence order and count; forcing 1:1 sentence alignment produces Chinglish.

**Scope of `\zhpara{}`**: Use for body paragraphs. Section titles (`\section{}`) switch directly to English without bilingual pairing. For figure/table captions, use `\protect\zhcaption{}` inside `\caption{}`.

**Compile sanity check**: After adding bilingual scaffolding, compile once to verify no caption/macro errors before batch polishing.

**Submission checklist item**: Before submission, change `\showchinesetrue` → `\showchinesefalse` and verify the PDF contains zero Chinese characters.

### 5. Pronoun Budget (Soft Constraint)

Before starting, set target ranges (advisory, not hard bans):

| Section | "we" budget | "our" budget |
|---------|-------------|-------------|
| Abstract | 0-1 | 0 |
| Introduction | 2-3 | 1-2 |
| Contributions list | 1-3 (standard) | 0 |
| Method | 3-5 (for derivations) | 0-1 |
| Experiments | 1-2 | 0-1 |
| Discussion | 1-2 | 0-1 |
| Conclusion | 1-2 | 0 |
| **Total (preferred)** | **≤20** | **≤10** |

---

## Output Format (Default + Long-Document Mode)

Use one of two modes:

- Default mode: apply full diff-table output for sentence/paragraph requests and short sections.
- Long-document mode: for full-paper polishing, process 3-8 paragraphs per batch with the same structure, then continue sequentially.

### Long-Document Mode Rules

- Keep a running paragraph index (`Sec.2-P3`, `Sec.2-P4`, ...); never skip paragraphs silently.
- At the end of each batch, output terminology updates and unresolved author decisions.
- If user asks for "final text only", provide polished text first and a compact change log second.

For each paragraph in a batch, use this structure:

### Step 1: Sentence-Level Diff Table

| # | Original Sentence | Revised (changes in **bold**) | Reason |
|---|-------------------|-------------------------------|--------|
| 1 | (full original) | (full revised, changed parts **bolded**) | (concise reason) |
| 2 | ... | ... | ... |

### Step 2: Bilingual LaTeX Output (Chinese → English mode)

When bilingual mode is active (Chinese source), output LaTeX code with `\zhpara{}`:

```latex
\zhpara{完整的中文原始段落，逐字保留，包括行内公式如 $f_\theta$ 和引用如 \cite{key}。}
Full polished English paragraph here, ready for the final paper.
```

When bilingual mode is NOT active (English-only source), output plain English:

> Full polished paragraph as continuous text, ready to paste into LaTeX.

### Step 3: Terminology Updates (if any)

Add new entries to the Terminology Ledger.

**Rules for the diff table**:
- Every sentence that changes MUST appear in the table
- Unchanged sentences MAY be omitted (note "No change" if listing them)
- **Bold** marks ONLY the changed portions, not the entire sentence
- Reason column: max 15 words; cite the specific rule (e.g., "Chinglish: missing article", "AI-style: remove em dash", "Register: nominalization → verb")

**Rules for bilingual LaTeX output**:
- `\zhpara{}` content is the EXACT original Chinese text (no edits, no reordering)
- Preserve all LaTeX commands, math, and citations inside `\zhpara{}`
- If Chinese text contains literal LaTeX special chars (`# $ % & _ { } ~ ^`) that are not intended commands, escape them.
- One `\zhpara{}` per paragraph — never split a Chinese paragraph across multiple `\zhpara{}`
- The English paragraph immediately follows with no blank line between `\zhpara{}` and English

---

## Polishing Rules (apply in priority order)

### Rule 1: Eliminate Chinglish [CRITICAL for CJK authors]

These are the highest-priority fixes. See [chinglish-patterns.md](chinglish-patterns.md) for the complete pattern database.

**Top 10 patterns to check every sentence**:

| # | Pattern | Wrong | Correct |
|---|---------|-------|---------|
| 1 | Missing/wrong article | "in network environment" | "in **the** network environment" |
| 2 | Uncountable plurals | "researches", "datas", "informations" | "studies", "data", "information" |
| 3 | Dangling modifier | "Using GRU, the accuracy is improved" | "Using GRU, **we improve** the accuracy" |
| 4 | Redundant twins | "help and assist", "method and approach" | Keep one |
| 5 | "in order to" | "in order to achieve" | "to achieve" |
| 6 | Subject-verb disagreement | "the data shows" | "the data **show**" or "the dataset **shows**" (choose one style and stay consistent) |
| 7 | Wrong preposition | "based on ..., we propose" (dangling) | "Based on ..., we propose" or restructure |
| 8 | "respectively" misuse | "A and B are 0.9 and 0.8 respectively" | "A and B achieve 0.9 and 0.8, respectively" (comma!) |
| 9 | "the + Figure/Table/Equation" | "as shown in the Fig. 1" | "as shown in Fig.~1" |
| 10 | Noun stacking (>3 nouns) | "entity behavior attribution learning system" | "a system for entity-level behavioral attribution" |

### Rule 2: Avoid AI-Generated Style [CRITICAL]

The polished text MUST NOT introduce AI markers. During rewriting:

**Hard bans (zero tolerance)**:
- Invented facts/citations/metrics introduced during style rewriting.
- Tier-1 AI phrases: "garnered attention", "pave the way", "testament to", "in the realm of", "myriad of", "plethora of".
- Generic abstract openings: "In recent years...", "With the rapid development of...", "In the era of...".

**Style controls (soft, context-dependent)**:
- Em dashes (—): prefer comma/colon/split sentence; keep only when clearly improving readability.
- Participial clause endings (e.g., ", demonstrating ..."): allow only when referent is unambiguous; otherwise rewrite.
- High-risk adjectives/adverbs (e.g., "comprehensive", "remarkable", "significant"): keep only if backed by concrete evidence or numbers.
- "not only...but also": prefer <=2 per paper.
- "Furthermore/Moreover/Additionally" paragraph openers: prefer <=3 each per paper.
- Nominalizations (utilization, implementation): prefer verb forms when natural.

See [ai-phrases.md](../paper-submission-check/ai-phrases.md) in `paper-submission-check` for the complete phrase database. If unavailable, continue with the rules above (do not block polishing).

### Rule 3: Academic Register

| Informal | Formal |
|----------|--------|
| a lot of | numerous / many |
| big | substantial / large |
| get | obtain / achieve |
| show | demonstrate / indicate |
| kind of / sort of | (delete or rephrase) |
| thing | aspect / factor / component |
| good / bad | effective / ineffective; advantageous / detrimental |
| don't / can't / won't | do not / cannot / will not |

**But avoid over-formalization**: "use" is fine (don't change to "utilize"); "show" is acceptable in results.

### Rule 4: Sentence Structure

| Rule | Threshold |
|------|-----------|
| Max sentence length | Prefer <=35 words; split when >40 unless technically necessary |
| Min sentence length | Avoid repeated fragments under 6 words |
| Paragraph length | Usually 3-8 sentences; allow 1-2 sentence paragraphs for transitions, contributions, or limitations |
| Single-sentence paragraphs | Allowed when rhetorically justified; avoid repeated one-liners |
| Sentence length variation | Alternate long and short; avoid all-same-length |
| One idea per sentence | Split multi-idea sentences |

### Rule 5: Tense Consistency

| Section | Primary Tense | When to Switch |
|---------|---------------|----------------|
| Abstract | Past ("proposed", "achieved") | Present for general claims ("show that") |
| Introduction | Present (field facts) | Past (specific prior work) |
| Related Work | Past ("proposed", "used") | Present (still-true facts) |
| Method | Present ("computes", "outputs") | Past is also acceptable |
| Experiments | Past ("conducted", "achieved") | Present for table references ("Table X shows") |
| Results/Discussion | Present ("suggest", "indicate") | Past for what was done |
| Conclusion | Past ("proposed", "demonstrated") | Future for future work |

### Rule 6: Hedging & Precision

| Over-claimed | Appropriately hedged |
|-------------|---------------------|
| "proves that" | "provides evidence that" / "demonstrates that" |
| "dramatically improves" | "improves by 12 percentage points" (use numbers!) |
| "the best method" | "the best-performing method among those evaluated" |
| "solves the problem" | "addresses the problem" / "mitigates the issue" |
| "novel" (if used >2×) | Replace excess with: "new", or describe what's actually new |

---

## Section-Specific Conventions

See [section-conventions.md](section-conventions.md) for detailed per-section writing patterns (Abstract PRKS structure, Introduction CARS model, Related Work thematic organization, etc.).

**Quick reference**:

| Section | Key Convention |
|---------|---------------|
| Abstract | PRKS: Problem → Response → Key results (with numbers) → Significance |
| Introduction | CARS: Territory → Niche (gap) → Occupy (contributions) |
| Contributions | 3-5 numbered items; each specific + measurable; verb-led ("We propose...") |
| Related Work | Thematic groups, NOT laundry list; each group ends with gap/limitation |
| Method | Define all symbols at first use; notation table if >10 symbols |
| Experiments | Dataset stats table; baselines with published defaults stated; interpret results |
| Conclusion | NOT abstract copy; strongest takeaway first; honest limitations |

---

## Phase 9: Cross-Section Consistency Verification

After all sections are polished, verify:

```
Consistency Checklist:
- [ ] Numbers in Abstract match Results tables exactly
- [ ] Each contribution maps to a specific section
- [ ] Introduction gap == Method solution
- [ ] Method symbols == Experiment parameters
- [ ] Conclusion claims ⊆ Results data (no overclaiming)
- [ ] Terminology Ledger: every concept uses chosen term only
- [ ] Pronoun counts within target range (advisory, not hard rejection criterion)
- [ ] "the proposed method" / method name used consistently (not "our proposed method")
```

---

## Phase 10: Final AI-Style Sweep

After all polishing, do a final pass. Count:

| Marker | Count | Threshold | Status |
|--------|-------|-----------|--------|
| Tier-1 AI phrases | | 0 | |
| Generic abstract openers | | 0 | |
| Em dashes (—) | | Prefer 0; max 2 outside abstract | |
| -ing chains at clause boundary | | Prefer ≤5; each must be unambiguous | |
| High-risk adjectives/adverbs | | Keep only when evidence-backed | |
| "not only...but also" | | ≤2 | |
| Furthermore/Moreover/Additionally | | ≤3 each | |
| "we" total | | Preferred ≤20 | |
| "our" total | | Preferred ≤10 | |

---

## Chinese-to-English: Translation Principles

When translating from Chinese source, follow these principles (NOT word-by-word translation):

### 1. Restructure, Don't Translate

Chinese academic writing front-loads conditions and background before the main point. English prefers: main point first, then conditions.

| Chinese structure | English structure |
|-------------------|-------------------|
| 由于A，因此B | B because A / B, as A |
| 在...方面，本文提出... | This paper proposes... for... |
| 针对...问题，我们... | To address..., we... / We address... by... |

### 2. Break Long Chinese Sentences

A single Chinese sentence often maps to 2-3 English sentences. If a translated sentence exceeds 40 words, split it unless technical precision requires one sentence.

### 3. Convert Chinese Logical Connectors

| Chinese | English (varies by context) |
|---------|----------------------------|
| 然而 | However, / Yet, / In contrast, |
| 此外 | In addition, / Moreover, (use sparingly) |
| 因此 | Therefore, / Thus, / Consequently, |
| 首先...其次...最后 | First, ... Second, ... Finally, |
| 一方面...另一方面 | On one hand, ... On the other hand, (use sparingly; prefer direct contrast) |

### 4. Handle Domain-Specific Terms

Security/ML terms have established English translations:

| Chinese | Standard English |
|---------|-----------------|
| 溯源图 | provenance graph |
| 高级持续性威胁 | Advanced Persistent Threat (APT) |
| 可解释性 | interpretability / explainability |
| 归因 | attribution |
| 反事实 | counterfactual |
| 梯度解耦 | gradient decoupling |
| 多示例学习 | multiple instance learning (MIL) |

---

## Polishing Examples

See [polishing-examples.md](polishing-examples.md) for complete before/after examples for each section type, including bilingual LaTeX output format.

---

## Report Format

After completing all phases, produce a summary:

```markdown
# Polishing Report

## Paper Info
- Source language: [Chinese / English draft]
- Target venue: [name]
- Template: [NeurIPS / IEEE / Elsevier / ...]

## Statistics
- Paragraphs polished: XX
- Sentences modified: XX / YY total
- Chinglish patterns fixed: XX
- AI markers avoided/removed: XX

## Terminology Ledger (final)
| Concept | Chosen Term | Rejected Alternatives |
|---------|-------------|----------------------|
| ... | ... | ... |

## Pronoun Usage (final)
| Pronoun | Count | Budget | Status |
|---------|-------|--------|--------|
| we | | Preferred ≤20 | |
| our | | Preferred ≤10 | |

## Remaining Concerns
- (Any issues that need author decision)
```
