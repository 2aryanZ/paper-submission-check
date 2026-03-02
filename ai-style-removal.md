# AI Writing Style Removal Guide for Academic Papers

Remove signs of AI-generated writing to make text sound natural, human-written, and suitable for top-tier journal publication. Based on Wikipedia's "Signs of AI writing" guide, the PNAS study on LLM writing styles (Carnegie Mellon, 2025), ACL research on lexical overrepresentation, and real-world journal editor feedback.

---

## Severity Classification for Journal Submission

From a journal editor's perspective, AI writing signs carry different risk levels:

| Severity | Risk | Editor's Reaction | Action |
|----------|------|-------------------|--------|
| **S1: Desk Rejection Risk** | Very High | "This reads like ChatGPT output" — immediate flag to ethics committee | Must fix every instance |
| **S2: Major Revision / Suspicion** | High | "The writing quality is inconsistent" — reviewer flags AI use | Fix all instances |
| **S3: Minor Revision** | Medium | "The language could be more precise" — noted but not fatal | Fix most instances |
| **S4: Stylistic** | Low | Reviewers notice but don't explicitly flag | Fix if time permits |

---

## Pattern 1: Em Dash Overuse [S1]

**Why it matters**: The em dash (—) has become the single most recognizable marker of AI-generated academic text. LLMs are "addicted" to em dashes because their training data from NYT and academic journals associates them with sophisticated writing. Multiple em dashes in one paragraph is a near-certain AI tell.

**Detection**: Search for `—` or `---` in LaTeX.

**Threshold**: Max 2-3 em dashes in the entire paper. Zero in the abstract.

| AI Pattern | Human Rewrite |
|-----------|---------------|
| "The method — which uses sketch structures — achieves high accuracy" | "The method, which uses sketch structures, achieves high accuracy" |
| "SBEAD — a sketch-based approach — outperforms baselines" | "SBEAD, a sketch-based approach, outperforms baselines" |
| "anomaly detection — particularly in streaming graphs — remains challenging" | "Anomaly detection in streaming graphs remains challenging" |

**Rewriting strategies**:
- Replace with commas for parenthetical clauses
- Replace with colons for explanations
- Restructure into two sentences
- Use "namely" or "specifically" for appositive phrases

---

## Pattern 2: The 21 Focal Words [S1]

**Why it matters**: A 2025 ACL study identified 21 words whose frequency in scientific abstracts surged after ChatGPT's release. Journal editors and reviewers have been trained to spot these.

**The list** (ordered by suspicion level):

| Tier | Words | Frequency Spike |
|------|-------|----------------|
| **Extreme** | delve, tapestry, landscape (figurative), nuanced, multifaceted | 50-150x normal |
| **Very High** | intricate, meticulous, pivotal, underscore, commendable | 20-50x normal |
| **High** | noteworthy, groundbreaking, innovative, comprehensive, paramount | 10-20x normal |
| **Moderate** | crucial, vital, significant, remarkable, exceptional, navigate | 5-10x normal |

**Replacements**:

| AI Word | Context-Appropriate Replacements |
|---------|--------------------------------|
| delve (into) | examine, analyze, investigate, study |
| tapestry | combination, mixture, set of factors |
| landscape (figurative) | field, area, domain, context |
| nuanced | detailed, subtle, fine-grained |
| multifaceted | complex, compound, multi-component |
| intricate | complex, detailed, fine-grained |
| meticulous | careful, thorough, systematic |
| pivotal | important, key, central |
| underscore | show, demonstrate, confirm, indicate |
| commendable | good, strong, high, effective |
| noteworthy | notable, important, interesting |
| groundbreaking | new, first, important, significant |
| innovative | new, proposed, novel (sparingly) |
| comprehensive | thorough, detailed, extensive, complete |
| paramount | important, essential, critical |
| crucial | important, necessary, key |
| vital | important, essential, necessary |
| navigate | address, handle, manage, work with |

**Rule**: If the word could be removed or replaced with a simpler word without losing meaning, replace it.

---

## Pattern 3: Present Participial Clause Chains [S1]

**Why it matters**: The PNAS study found LLMs use present participial (-ing) clauses 2-5x more than humans. These are the most statistically distinctive marker of instruction-tuned LLMs. They appear as trailing "-ing" phrases that add superficial analysis.

**Detection**: Search for patterns like `, highlighting`, `, underscoring`, `, emphasizing`, `, demonstrating`, `, showcasing`, `, reflecting`, `, contributing`, `, ensuring`, `, fostering`, `, enabling`, `, facilitating`.

| AI Pattern | Human Rewrite |
|-----------|---------------|
| "The method achieves 0.99 AUC, demonstrating its effectiveness across diverse datasets" | "The method achieves 0.99 AUC on all four datasets" |
| "CMS reduces memory usage, enabling real-time processing of streaming data" | "CMS reduces memory usage. This enables real-time processing of streaming data" |
| "The results confirm the approach, highlighting its potential for practical applications" | "The results confirm the approach is effective in practice" |
| "SP-SBEAD outperforms baselines, underscoring the importance of sketch-based methods" | "SP-SBEAD outperforms all baselines (Table 3)" |

**Rewriting strategies**:
- Delete the -ing clause entirely if it adds no new information
- Split into two sentences if it does add information
- Replace with a specific number or reference
- Convert to a direct statement: "This demonstrates X" (but use sparingly)

**Threshold**: Max 3 participial -ing clauses in the entire paper. Zero chains (one -ing clause followed by another).

---

## Pattern 4: Negative Parallelism / Contrastive Pairs [S2]

**Why it matters**: A 2025 peer-reviewed study found that LLMs produce "emphatic epanorthosis" (the "not X, but Y" pattern) at rates far exceeding human corpora. This is an RLHF artifact — models are rewarded for perceived clarity and persuasive impact.

**Patterns to detect**:

```
not only ... but also
not just ... but (also/rather)
not merely ... but
not X, but rather Y
goes beyond ... to
more than just ... it is
rather than ... instead
```

| AI Pattern | Human Rewrite |
|-----------|---------------|
| "This is not just a detection method, but a comprehensive framework for network security" | "This detection method addresses three types of network anomalies" |
| "The results not only validate the approach but also underscore its potential for broader applications" | "The approach achieves the best AUC on three of four datasets" |
| "SP-SBEAD goes beyond simple detection to provide real-time analysis" | "SP-SBEAD detects anomalies in real time" |
| "The method is more than just efficient — it is transformative" | "The method processes 1M edges in 12 seconds" |

**Threshold**: Max 1 "not only...but also" per paper. Zero instances of "not just...but rather" or "goes beyond...to".

---

## Pattern 5: Rule of Three [S2]

**Why it matters**: LLMs consistently group descriptors, benefits, or features in threes. This creates an unnaturally rhythmic, persuasive cadence that is more characteristic of marketing copy than scientific writing.

**Detection**: Search for three-item lists joined by commas and "and":

```
X, Y, and Z  (where X, Y, Z are adjectives or abstract nouns)
accuracy, efficiency, and robustness
precision, recall, and F1-score  ← this one is fine (technical terms)
```

| AI Pattern (Suspicious Threes) | Human Rewrite |
|-------------------------------|---------------|
| "achieving high accuracy, efficiency, and robustness" | "achieving 0.998 AUC with 12-second processing time" |
| "demonstrating effectiveness, scalability, and adaptability" | "effective on datasets ranging from 4.5M to 22M edges" |
| "precision, reliability, and innovation" | (delete — meaningless in context) |
| "the method's accuracy, speed, and generalizability" | "the method achieves high AUC (>0.95) across all datasets" |

**Distinguish from legitimate threes**:
- Technical term lists are fine: "precision, recall, and F1-score"
- Specific items are fine: "DARPA, CICIDS2017, and TON_IoT"
- Abstract quality triples are suspicious: "accuracy, efficiency, and robustness"

---

## Pattern 6: Inflated Significance [S2]

**Why it matters**: LLMs statistically regress toward positive, important-sounding language. Everything becomes "crucial", "pivotal", or a "watershed moment". Editors recognize this as the AI equivalent of shouting louder while saying less.

**Detection keywords**: `pivotal`, `crucial`, `vital`, `watershed`, `landmark`, `seminal`, `groundbreaking`, `transformative`, `revolutionary`, `paradigm shift`, `indelible mark`, `lasting impact`.

| AI Pattern | Human Rewrite |
|-----------|---------------|
| "This represents a pivotal advancement in anomaly detection" | "This method improves AUC by 5% over the strongest baseline" |
| "a groundbreaking approach that transforms the field" | "a new approach using sketch data structures" |
| "This work has a lasting impact on cybersecurity research" | "This approach reduces memory usage from O(n^2) to O(d*w)" |
| "a paradigm shift in streaming graph analysis" | "a method that processes streaming graphs in constant memory" |

**Rule**: Replace every claim of significance with a specific, verifiable fact.

---

## Pattern 7: Vague Attributions [S2]

**Why it matters**: LLMs attribute opinions to unnamed authorities instead of citing specific sources. This is both an AI marker and a scientific writing flaw.

**Detection keywords**: `researchers have shown`, `studies indicate`, `experts argue`, `it is widely recognized`, `the literature suggests`, `industry experts`, `some critics argue`, `scholars note`, `it has been demonstrated that`.

| AI Pattern | Human Rewrite |
|-----------|---------------|
| "Researchers have shown that sketch-based methods are effective" | "Cormode and Muthukrishnan~\cite{cormode2005improved} showed that CMS achieves sub-linear space complexity" |
| "Studies indicate that anomaly detection remains challenging" | "Existing methods such as MIDAS~\cite{bhatia2022midas} require O(n) memory per timestamp" |
| "It is widely recognized that streaming graphs pose unique challenges" | "Streaming graphs generate up to 10^6 edges per second~\cite{specific_ref}" |

**Rule**: Every claim must cite a specific paper or present specific data. If you cannot cite it, either find the source or remove the claim.

---

## Pattern 8: Nominalization Overuse [S3]

**Why it matters**: The PNAS study found LLMs use nominalizations (turning verbs into nouns) 1.5-2x more than humans. This creates dense, passive prose that is harder to read.

| AI (Nominalized) | Human (Active Verb) |
|-------------------|-------------------|
| "The utilization of sketch structures enables..." | "Using sketch structures enables..." |
| "The implementation of the algorithm requires..." | "Implementing the algorithm requires..." |
| "The optimization of parameters involves..." | "Optimizing parameters involves..." |
| "Through the application of CMS..." | "By applying CMS..." |
| "The investigation of anomaly patterns reveals..." | "Investigating anomaly patterns reveals..." |
| "The facilitation of real-time detection..." | "To facilitate real-time detection..." |

**Detection**: Search for words ending in `-tion`, `-ment`, `-ness`, `-ity` that have simpler verb forms. Common offenders: `utilization`, `implementation`, `optimization`, `facilitation`, `investigation`, `examination`, `establishment`, `enhancement`, `improvement`.

---

## Pattern 9: Conjunctive Phrase Saturation [S3]

**Why it matters**: AI text starts nearly every paragraph with a transition word. Human writing varies paragraph openings naturally.

**Detection**: Check consecutive paragraph openings. If 3+ paragraphs in a row start with transition words, this is an AI marker.

**Overused transitions** (with frequency thresholds for a full paper):

| Word/Phrase | Max Occurrences | Alternative |
|-------------|----------------|-------------|
| Furthermore | 3 | (delete, or restructure) |
| Moreover | 3 | (delete, or restructure) |
| Additionally | 3 | (delete) |
| Notably | 3 | Specifically / In particular |
| In particular | 3 | (vary with "Specifically") |
| Consequently | 2 | (start with the consequence directly) |
| It is worth noting that | 0 | (delete entirely, state the fact) |
| Interestingly | 0 | (delete, explain why it's interesting) |

**Rewriting strategy**: Start paragraphs with the subject or finding directly:
- AI: "Furthermore, the experimental results demonstrate..."
- Human: "On DARPA, SP-SBEAD achieves 0.90 AUC..."

---

## Pattern 10: Positivity Bias and Missing Limitations [S2]

**Why it matters**: LLMs trained with RLHF exhibit systematic positivity bias. Everything is described positively. An honest academic paper must discuss limitations, failure cases, and trade-offs. Absence of genuine limitations is a strong AI marker.

**Signs**:
- Limitations section is vague, generic, or suspiciously short
- "Future work" substitutes for real limitations
- Results section contains no discussion of failure cases or weak performance
- Every comparison is favorable; no dataset where the method performs poorly

**What editors expect to see**:
- Specific failure cases: "On TON_IoT with attack ratio below 0.1%, the method's precision drops to 0.72"
- Honest trade-offs: "While SBEAD achieves lower memory usage, SP-SBEAD requires 2x more computation"
- Scope limitations: "The method was tested only on network traffic; applicability to other domains is unknown"
- Comparison nuance: "MIDAS outperforms SBEAD on the DARPA dataset by 0.02 AUC"

---

## Pattern 11: Formulaic Section Transitions [S3]

**Why it matters**: LLMs produce nearly identical transition sentences between sections. Each section starts with a summary of what came before and a preview of what comes next. This "recap-preview" pattern rarely appears in well-written human papers.

| AI Pattern | Human Approach |
|-----------|---------------|
| "Having discussed the related work, we now turn to the proposed methodology" | (just start the methodology section) |
| "In the previous section, we presented the experimental setup. In this section, we discuss the results" | (just present the results) |
| "Building upon the theoretical framework established above, we now present..." | (just present) |

**Rule**: Sections should start with content, not meta-commentary about the paper's structure.

---

## Pattern 12: Correlative Conjunction Overuse [S3]

**Why it matters**: LLMs overuse paired constructions that create artificial symmetry.

**Patterns**: `whether...or`, `either...or`, `neither...nor`, `both...and`, `the more...the more`.

| AI Pattern | Human Rewrite |
|-----------|---------------|
| "Whether in real-time detection or offline analysis, the method proves effective" | "The method works in both real-time and offline settings" |
| "Both the accuracy and the efficiency of the approach exceed expectations" | "The approach achieves 0.998 AUC and processes 1M edges/sec" |
| "Neither the memory overhead nor the computational cost is prohibitive" | "Memory usage is O(d*w) and computation is O(1) per edge" |

**Threshold**: Max 2 correlative constructions per paper.

---

## Pattern 13: False Ranges and Hedge Stacking [S3]

**Why it matters**: LLMs insert ranges that sound sophisticated but convey no real information. They also stack hedging words to avoid commitment.

**False ranges**:

| AI Pattern | Problem | Fix |
|-----------|---------|-----|
| "from traditional methods to cutting-edge approaches" | Meaningless range | "methods including X, Y, and Z" |
| "ranging from small to large-scale networks" | Vague | "networks with 10K to 22M edges" |
| "across various domains and applications" | Unspecific | "in network intrusion detection" |

**Hedge stacking**:

| AI Pattern | Fix |
|-----------|-----|
| "This could potentially suggest that it might be possible to..." | "This suggests..." |
| "It appears that the results may indicate a possible trend toward..." | "The results show a trend toward..." |
| "The method seems to possibly offer some improvement" | "The method improves AUC by 3%" |

---

## Systematic Removal Workflow

When removing AI style from a paper, follow this order:

### Step 1: Scan for S1 patterns (Desk Rejection Risk)
1. Count em dashes → reduce to ≤3 total, 0 in abstract
2. Search for all 21 focal words → replace every instance
3. Count -ing participial chains → reduce to ≤3 total
4. Check for direct ChatGPT artifacts (markdown, "I hope this helps", "Let me know")

### Step 2: Scan for S2 patterns (Major Revision Risk)
5. Count "not only...but also" and contrastive pairs → reduce to ≤1 total
6. Count abstract triple adjectives (Rule of Three) → replace with specifics
7. Find inflated significance claims → replace with data
8. Find vague attributions → replace with specific citations
9. Check for positivity bias → add genuine limitations

### Step 3: Scan for S3 patterns (Minor Revision)
10. Count nominalizations → convert to active verbs
11. Check paragraph opening variety → vary transition words
12. Remove formulaic section transitions
13. Reduce correlative conjunctions to ≤2
14. Eliminate false ranges and hedge stacking

### Step 4: Final humanization pass
14. Read each paragraph aloud — does it sound like a human expert wrote it?
15. Verify: every claim has a number or citation backing it
16. Verify: the Limitations section is honest and specific
17. Verify: the abstract starts with a specific problem, not a generic statement

---

## Quick Reference: Sentence-Level Before/After

| # | AI-Generated | Human-Written |
|---|-------------|---------------|
| 1 | "This paper delves into the intricate challenges of anomaly detection in streaming graphs" | "This paper addresses anomaly detection in streaming graphs" |
| 2 | "The proposed method — leveraging sketch-based data structures — achieves remarkable performance across diverse datasets" | "The proposed method uses sketch-based data structures and achieves 0.998 AUC on CICIDS2019" |
| 3 | "These findings not only validate the effectiveness of our approach but also underscore its potential for real-world applications, demonstrating superior performance and adaptability" | "The method outperforms all baselines on three of four datasets (Table 3)" |
| 4 | "Furthermore, the comprehensive experimental evaluation demonstrates that the method is both efficient and robust, highlighting its suitability for practical deployment" | "The method processes 1M edges in 12 seconds with constant memory usage" |
| 5 | "It is worth noting that the results reveal a nuanced interplay between accuracy and computational efficiency, suggesting a promising avenue for future research" | "Accuracy increases with sketch width (Table 4), but so does memory usage — a trade-off controlled by parameter w" |
| 6 | "The intricate nature of modern network traffic necessitates innovative approaches that can navigate the evolving landscape of cybersecurity threats" | "Modern network traffic generates 10^6 edges/second, requiring O(1)-per-edge detection methods" |
| 7 | "Researchers have increasingly recognized the pivotal role of sketch-based methods in addressing the multifaceted challenges inherent in real-time anomaly detection" | "Sketch-based methods such as CMS~\cite{cormode2005} reduce memory from O(n) to O(d*w)" |
| 8 | "The experimental results compellingly demonstrate the method's remarkable ability to achieve exceptional accuracy while maintaining commendable computational efficiency" | "SBEAD achieves 0.998 AUC on CICIDS2019 and processes each edge in O(d) time" |

---

## The Golden Rules

1. **Specific beats impressive**: Replace every adjective with a number
2. **Active beats nominal**: "X uses Y" not "the utilization of Y by X"
3. **Short beats long**: If a sentence has >30 words, split it
4. **Direct beats hedged**: "X improves Y" not "X could potentially improve Y"
5. **Cited beats claimed**: "Smith et al. showed X" not "researchers have shown X"
6. **Honest beats promotional**: Include real limitations, not vague future work
7. **Varied beats formulaic**: Don't start every paragraph with "Furthermore"
8. **Simple beats ornate**: "use" not "utilize", "show" not "underscore"
