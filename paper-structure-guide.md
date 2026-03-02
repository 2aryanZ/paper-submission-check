# Paper Structure & Writing Quality Guide

Structural and writing quality standards for academic papers targeting top-tier journals. Covers abstract construction, introduction structure (CARS model), paragraph and sentence length, keyword optimization, section-specific rules, and conclusion requirements. Based on Swales' CARS model, Elsevier/IEEE/Springer author guidelines, and empirical analysis of 9,830+ research papers.

---

## 1. Abstract Writing Standards

The abstract is the first thing editors read. A poorly written abstract can result in desk rejection before the paper reaches reviewers.

### Word Count Requirements by Publisher

| Publisher | Article Type | Abstract Limit | Notes |
|-----------|-------------|---------------|-------|
| **Elsevier** | Research Article | 150–300 words (varies by journal) | Check specific journal's Guide for Authors |
| **Elsevier** | Short Communication | 100–150 words | |
| **IEEE** | Transactions/Access | ≤200 words | Strict limit |
| **IEEE** | Conference | 150–200 words | |
| **Springer** | Research Article | 150–250 words | Varies by journal |
| **ACM** | Conference | 150–250 words | |

**How to count**: In LaTeX, extract the abstract text and use any word counter. Exclude LaTeX commands from the count.

### Abstract Structure (the "PRKS" Framework)

A strong abstract follows four parts in order:

| Part | Content | Approximate Share |
|------|---------|-------------------|
| **P — Problem** | What problem does this paper address? | 15–20% |
| **R — Response** | What does this paper propose/do? | 25–30% |
| **K — Key Results** | What are the main quantitative results? | 35–40% |
| **S — Significance** | Why do these results matter? | 10–15% |

**Common errors**:

| Error | Example | Fix |
|-------|---------|-----|
| Problem section too long (>50%) | 5 sentences on background before mentioning the method | Compress to 1–2 sentences |
| Missing specific numbers | "achieves superior performance" | "achieves 0.998 AUC on CICIDS2019" |
| Undefined abbreviations | "AUC" used without expansion | "Area Under the Curve (AUC)" at first use |
| Generic opening sentence | "With the exponential growth of..." | Start with the specific problem or contribution |
| Citations in abstract | "\cite{xxx}" appearing in abstract | Remove — abstracts should be self-contained |

### Abstract Opening Sentence

The opening sentence is critical. Editors immediately recognize generic AI-style openings.

| Bad Opening (Generic) | Good Opening (Specific) |
|-----------------------|------------------------|
| "With the rapid development of..." | "Detecting anomalous edges in streaming graphs requires O(1) per-edge methods" |
| "In recent years, X has attracted significant attention" | "This paper proposes SBEAD, a sketch-based method for real-time graph anomaly detection" |
| "The exponential growth of data has made X increasingly important" | "Existing graph-based anomaly detection methods require complete graph structures, limiting real-time applicability" |

**Rule**: If the opening sentence could apply to any paper in the field, it is too generic. Start with your specific problem or contribution.

### Abstract Self-Containment Rule

The abstract must be understandable without reading the paper. This means:
- Every abbreviation must be defined in the abstract, even if defined again in the body
- No references to figures, tables, equations, or sections
- No citations (most publishers prohibit this)
- All claimed numbers must be verifiable from the paper's results

---

## 2. Introduction Structure: Swales' CARS Model

The **CARS (Create A Research Space)** model, developed by linguist John Swales (1990), is the standard framework for writing research introductions. Editors and reviewers unconsciously expect this structure.

### The Three Moves

| Move | Purpose | What to Write | Typical Length |
|------|---------|--------------|---------------|
| **Move 1: Establish Territory** | Show the research area is important and active | General background + importance + cite key works | 1–2 paragraphs |
| **Move 2: Establish Niche** | Identify the gap/problem in existing research | Limitations of current methods + what is missing | 1 paragraph |
| **Move 3: Occupy Niche** | State what this paper does to fill the gap | Proposed approach + contributions + paper outline | 1–2 paragraphs + contributions list |

### Move 1: Establish Territory (3 optional steps)

| Step | Example |
|------|---------|
| **1a. Claim centrality** | "Graph-based anomaly detection has been extensively studied..." |
| **1b. Make topic generalizations** | "Graph data structures capture rich structural information while preserving content-related details" |
| **1c. Review previous work** | "Approaches include deep learning-based [refs] and structure-based methods [refs]" |

### Move 2: Establish Niche (4 strategies, pick one)

| Strategy | Signal Phrases | Example |
|----------|---------------|---------|
| **Counter-claiming** | "However, ...", "Despite this, ..." | "However, most methods focus on static graphs, which cannot capture temporal dynamics" |
| **Indicating a gap** | "No study has...", "Little attention has been paid to..." | "Few methods address real-time detection in streaming graphs with bounded memory" |
| **Question-raising** | "The question remains...", "It is unclear whether..." | "It remains unclear whether sketch-based methods can achieve both accuracy and efficiency" |
| **Continuing a tradition** | "Building upon...", "Extending..." | "Building upon sketch-based streaming methods, this paper aims to enhance..." |

**Critical**: Move 2 is where many papers fail. The gap statement must be specific and directly motivate Move 3.

### Move 3: Occupy Niche (3 components)

| Component | Format | Notes |
|-----------|--------|-------|
| **State purpose** | "This paper proposes X and Y" | 1 sentence, clear and direct |
| **List contributions** | Numbered \begin{enumerate} list | 3–5 items, each measurable and specific |
| **Paper outline** | "The remainder of this paper..." | 1 paragraph mapping sections to content |

### Introduction Checklist

```
Introduction Checklist:
- [ ] Move 1 present: field importance established with citations
- [ ] Move 2 present: specific gap/limitation identified (not vague)
- [ ] Move 3 present: clear statement of what this paper does
- [ ] Contributions: 3–5 numbered items, each specific and measurable
- [ ] Paper outline: all sections referenced with \ref{}
- [ ] Length: 1.5–2.5 pages (including contributions and figure, if any)
- [ ] Flow: Move 1 → Move 2 → Move 3 transition is natural
- [ ] No "orphan" paragraphs (unrelated to the three moves)
```

---

## 3. Paragraph Structure & Length

### Empirical Standards (from analysis of 9,830 research papers)

| Metric | Median | Healthy Range | Problematic |
|--------|--------|---------------|-------------|
| Words per paragraph | 109 | 65–200 | <30 or >250 |
| Sentences per paragraph | 4 | 3–6 | 1 or >8 |
| By section — Methods | 92 words | 60–150 | >200 |
| By section — Discussion | 131 words | 80–200 | >250 |
| By section — Introduction | 120 words | 80–200 | >250 |

### Paragraph Rules

**Rule 1: One idea per paragraph**

Each paragraph should make one clear point. If a paragraph covers two distinct ideas, split it.

**Rule 2: Topic sentence first**

The first sentence of each paragraph should state the paragraph's main point. The remaining sentences provide evidence, elaboration, or examples.

| Weak Opening | Strong Opening |
|-------------|---------------|
| "There are many methods..." | "Sketch-based methods reduce memory from O(n) to O(d×b)" |
| "It is important to consider..." | "CMS maintains d independent hash rows for robustness" |

**Rule 3: No single-sentence paragraphs**

A paragraph with only one sentence indicates an underdeveloped idea. Either expand it or merge it with an adjacent paragraph.

Exception: The paper outline paragraph ("The remainder of this paper...") is often a single long sentence and is acceptable.

**Rule 4: No giant paragraphs**

Paragraphs exceeding 250 words should be split. Common locations for giant paragraphs:
- The first Introduction paragraph (trying to cover too much background)
- Dataset descriptions (listing all features in one block)
- The Conclusion (restating everything in one paragraph)

**Rule 5: Conclusion must be multi-paragraph**

For papers >6 pages, the conclusion should contain 2–4 short paragraphs:
1. Summary of contributions and key findings
2. Main significance or implications
3. Limitations (if not in Discussion)
4. Future work directions

### Detection Method

Count words per paragraph by searching for blank lines between `\par` or double newlines. Flag:
- Paragraphs with >250 words → suggest split
- Paragraphs with only 1 sentence → suggest merge or expand
- 3+ consecutive short paragraphs (<50 words each) → suggest consolidation

---

## 4. Sentence Length Standards

### Ideal Ranges

| Range | Assessment | Action |
|-------|-----------|--------|
| 8–14 words | Too short — may sound simplistic | Combine with adjacent sentence if appropriate |
| **15–25 words** | **Ideal range** | No action needed |
| 25–35 words | Acceptable but watch clarity | Review for readability |
| **>35 words** | **Too long** — comprehension drops significantly | Must split into 2 sentences |

### Sentence Length Variation

Good academic writing varies sentence length naturally. If 5+ consecutive sentences are all the same length (±3 words), the prose feels mechanical (an AI marker).

| Monotonous (AI-like) | Varied (Human-like) |
|----------------------|-------------------|
| "The method processes edges. The method assigns scores. The method detects anomalies. The method uses CMS." (all ~5-7 words) | "The method processes edges in O(1) time. For each edge, it queries d hash rows and computes the IQR-based boundary. Edges exceeding this boundary receive high anomaly scores." (7, 15, 9 words) |

### Long Sentence Splitting Strategies

| Long Sentence | Split Version |
|--------------|--------------|
| "The proposed method uses CMS to maintain count statistics for each node and edge, and then applies an IQR-based boundary detection mechanism that adapts to varying traffic patterns while maintaining sensitivity to sudden anomalies." (35 words) | "The proposed method uses CMS to maintain count statistics for each node and edge. An IQR-based boundary detection mechanism then adapts to varying traffic patterns while remaining sensitive to sudden anomalies." (17 + 16 words) |

---

## 5. Keywords Optimization

### Number Requirements by Publisher

| Publisher | Required | Recommended |
|-----------|---------|-------------|
| **Elsevier** | Varies by journal, typically max 6 | 4–6 |
| **IEEE** | Min 3, Max 10 | 5–7 |
| **Springer** | Varies by journal | 4–6 |
| **ACM** | Uses CCS concepts (separate system) | 3–5 keywords + CCS |

### Keyword Quality Checklist

| Check | Rule | Example |
|-------|------|---------|
| **Count** | At least 4, no more than 6 (Elsevier) or 10 (IEEE) | 4 keywords → consider adding 1–2 more |
| **Not all from title** | At least 1–2 keywords should NOT appear in the title | Title has "Anomaly Detection" and "Graph Stream" → add a keyword like "Count-Min Sketch" that isn't in the title |
| **Broad + Specific mix** | Include both general field terms and specific method/technique terms | Broad: "Network Security"; Specific: "Count-Min Sketch" |
| **No redundancy** | Each keyword should add unique discoverability | "Anomaly Detection" and "Anomalous Behavior Detection" are redundant |
| **Standard terms** | Use established terms from the field, not invented ones | "Graph Stream" ✓; "Stream-Graph Analysis" ✗ (non-standard) |
| **Separator** | Elsevier uses `\sep`; IEEE uses commas; check journal guide | |

### Keyword Discoverability Strategy

Think: "What would a researcher search for to find this paper?"

| Level | Purpose | Examples |
|-------|---------|---------|
| **Field** | Broad field terms for general discoverability | Network Security, Data Mining |
| **Topic** | Specific research topic | Anomaly Detection, Graph Stream |
| **Method** | Specific technique used | Count-Min Sketch, Sketch Data Structure |
| **Application** | Domain where it's applied | Intrusion Detection, Edge Stream |

Aim for 2 topic + 1–2 method + 1–2 field/application keywords.

---

## 6. Section-Specific Structural Rules

### Related Work

**Purpose**: Not a laundry list — must build a case for why your work is needed.

| Structure | Content |
|-----------|---------|
| **Opening** | Scope statement: "This section reviews X, Y, and Z" |
| **Thematic groups** | Organize by approach/theme, not chronologically |
| **Per-group analysis** | For each group: summarize methods → state limitations → cite key works |
| **Gap summary** | Final paragraph: synthesize what is missing across all groups → motivate your approach |

**Checklist**:
```
Related Work Checklist:
- [ ] Organized thematically (not just a list of papers)
- [ ] Each group has: summary + limitations + citations
- [ ] Final paragraph synthesizes the gap
- [ ] Gap directly connects to the proposed method
- [ ] Sufficient breadth (15–30 citations for a full paper)
- [ ] Recent references included (at least 3–5 from the past 2 years)
```

### Method

**Purpose**: Sufficient detail for reproduction.

| Component | Must Include |
|-----------|-------------|
| **Problem definition** | Formal notation, input/output specification |
| **Algorithm description** | Step-by-step, with pseudocode or algorithm block |
| **Mathematical formulation** | Key equations numbered and referenced |
| **Parameter explanation** | Every symbol defined at first use |
| **Complexity analysis** | Time and space complexity (can be in Experiments instead) |

**Checklist**:
```
Method Checklist:
- [ ] All symbols defined at first use
- [ ] Algorithm pseudocode provided
- [ ] Key equations numbered
- [ ] Input/output clearly specified
- [ ] Method is reproducible from description alone
```

### Experiments

**Purpose**: Convince reviewers that results are valid and reproducible.

**Recommended subsection order**:

| Order | Subsection | Content |
|-------|-----------|---------|
| 1 | Dataset | Description, statistics, preprocessing, why these datasets |
| 2 | Baselines | Which methods compared, why these, parameter settings |
| 3 | Experimental Settings | Hardware, software, hyperparameters, number of runs |
| 4 | Evaluation Metrics | Definition of each metric used |
| 5 | Results & Analysis | Tables/figures with interpretation |
| 6 | Ablation Study | Impact of each component (optional but strengthens paper) |
| 7 | Parameter Sensitivity | Effect of key parameters (optional) |
| 8 | Complexity Analysis | Time/space comparison (if not in Method) |

**Checklist**:
```
Experiments Checklist:
- [ ] All baselines use their published default parameters (state this explicitly)
- [ ] Number of experimental runs stated (e.g., "averaged over 5 runs")
- [ ] Hardware and software environment specified
- [ ] Best results bolded in tables
- [ ] Results discussed, not just presented
- [ ] Statistical significance reported if applicable
```

### Discussion & Limitations

**Purpose**: Interpret results, acknowledge weaknesses, establish credibility.

**Discussion must include**:

| Component | Content | Why It Matters |
|-----------|---------|---------------|
| **Result interpretation** | What do the numbers mean? Why does method X outperform Y? | Shows understanding, not just measurement |
| **Comparison with prior work** | How do findings relate to/contradict existing results? | Places work in context |
| **Limitations** | Specific weaknesses of the study | Absence is a red flag for reviewers |
| **Broader implications** | What does this mean for the field? | Adds value beyond the paper |

**Limitations subsection requirements** (based on reviewer feedback research):

Limitations must be **specific, not vague**:

| Vague Limitation (Rejected) | Specific Limitation (Accepted) |
|----------------------------|-------------------------------|
| "The method has some limitations" | "The method was tested only on four datasets; generalizability to other network types is unverified" |
| "Future work will address limitations" | "CMS hash collisions may reduce accuracy for low-volume attack patterns, as observed on the DARPA dataset where AUC drops to 0.89" |
| "The approach may not work in all scenarios" | "SP-SBEAD's weighted aggregation (a=0.4, b=0.3, c=0.3) was tuned on CICIDS2017; optimal weights may differ for other datasets" |

**If no separate Limitations subsection**: Limitations can appear in the Discussion section, but they MUST appear somewhere. A paper with zero limitations acknowledged has a higher rejection risk.

### Conclusion

**Purpose**: Synthesize (not summarize), state significance, point forward.

**Conclusion ≠ Abstract**:

| Abstract | Conclusion |
|----------|-----------|
| Standalone summary for someone who hasn't read the paper | Synthesis for someone who has read the paper |
| States: what, how, results | States: what it means, why it matters, what's next |
| Includes problem background | No background needed — reader already knows |
| Quantitative (specific numbers) | Can be more qualitative (implications) |

**Conclusion Structure** (2–4 paragraphs for full papers):

| Paragraph | Content |
|-----------|---------|
| **1. Summary** | "This paper proposed X and Y. Experiments on N datasets showed..." (2–3 sentences) |
| **2. Key findings & significance** | Most important result + what it means for the field |
| **3. Limitations** | If not already in Discussion (1–2 sentences) |
| **4. Future work** | Specific directions, not vague promises |

**Red flags**:
- Conclusion is a single giant paragraph (>200 words) → must split
- Conclusion repeats the abstract nearly word-for-word → must rewrite
- Conclusion makes claims not supported by the paper's data
- Conclusion introduces new information not discussed earlier
- "Paving the way for future advancements" → too vague, be specific

**Conclusion length**: Typically 5–7% of total paper word count. For an 8,000-word paper: 400–560 words.

---

## 7. Cross-Section Consistency Checks

| Check | What to Verify |
|-------|---------------|
| Abstract numbers = Table numbers | Every number in the abstract must match a table or figure |
| Contribution list = Paper content | Each numbered contribution must map to a specific section |
| Introduction gap = Method solution | The gap identified in Move 2 must be directly addressed by the proposed method |
| Related Work gap = Contribution novelty | The novelty claimed must not be already done by cited papers |
| Method symbols = Experiment parameters | Mathematical symbols (d, b, w) must match parameter names in experiments |
| Discussion = Results interpretation | Discussion should interpret results, not repeat the numbers |
| Conclusion claims ⊆ Results data | No claim in the conclusion that isn't supported by the experiments |
| Keywords ⊆ Paper content | Every keyword should appear in the paper's actual content |

---

## Quick Reference: Section Length Guidelines

For a typical 8,000–10,000 word research paper:

| Section | Approximate Share | Pages (single-column) |
|---------|------------------|-----------------------|
| Abstract | 2–3% (150–300 words) | — |
| Introduction | 12–15% | 1.5–2 |
| Related Work | 15–20% | 2–2.5 |
| Problem Definition | 5–8% | 0.5–1 |
| Method | 20–25% | 2.5–3 |
| Experiments | 25–30% | 3–4 |
| Discussion | 5–10% | 0.5–1 |
| Conclusion | 5–7% | 0.5–1 |

These are guidelines, not rigid rules. The key is that Method + Experiments should be the longest combined section (the "meat" of the paper).
