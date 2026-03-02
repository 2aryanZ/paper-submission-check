# Multi-Model Review Strategy

## Why Multi-Model Matters

Using a single LLM for all reviewer roles creates systematic problems that undermine the review's value. This is not a theoretical concern — it has been empirically validated:

### The Single-Model Problem (Research Evidence)

| Problem | Evidence | Impact on Review Quality |
|---------|----------|--------------------------|
| **Echo Chamber** | "LLMs Are Echo Chambers" (ACL 2024): Single model outputs across personas are highly correlated | All "independent" reviews share the same blind spots; weaknesses missed by one persona are missed by all |
| **Bias Amplification** | "Judging with Many Minds" (EMNLP 2025): Multi-agent debate AMPLIFIES initial biases after first round | Review → Rebuttal → Re-Review loops become self-congratulatory; model accepts its own fixes too easily |
| **Weakness Detection Gap** | ICLR/NeurIPS review study (2025): LLMs produce 59% fewer weakness entities than human reviewers | Single model's weakness-finding limitation compounds across all roles — no diversity to compensate |
| **LLM-Style Preference** | LLM-REVal (ICLR 2026 submission): LLM reviewers systematically inflate scores for LLM-authored text | If the same model that assisted with writing also reviews, it will be biased toward its own style |
| **Score Clustering** | Empirical observation: Single-model multi-persona scores cluster in narrow range (e.g., all 5-6/10) | Fails to produce the natural reviewer variance (3-8/10 range) that signals genuine disagreement areas |

### Why Different Models Have Genuine Diversity

Different LLMs are trained on different data mixtures, with different RLHF preferences, and different architectural biases. This creates naturally different "personalities" that mirror real reviewer diversity:

- Claude tends toward diplomatic, balanced assessments — may under-flag critical issues
- GPT/Codex tends toward more direct critiques — may over-focus on formal correctness
- Gemini tends toward information-dense responses — may miss subtle logical issues

This diversity is a **feature**, not a bug — it produces the same type of productive disagreement that makes real peer review valuable.

---

## Model Capability Map (2025-2026)

### Detailed Strengths by Task Type

| Task | Claude Opus 4+ | GPT-5 / Codex | Gemini 3 Pro |
|------|----------------|---------------|--------------|
| **Formula verification** | Good | Best (AIME 100%) | Adequate |
| **Code/algorithm checking** | Best (SWE-bench 80.9%) | Good | Adequate |
| **Long document comprehension** | Good (200K context) | Good (400K) | Best (1M context) |
| **Writing quality assessment** | Best (most natural style sense) | Good | Adequate |
| **Literature search / fact-check** | Adequate (no native search) | Adequate | Best (native search) |
| **Systematic checklist execution** | Best (thorough, methodical) | Good | Good |
| **Adversarial critique** | Tends diplomatic | Most direct/harsh | Middle ground |
| **Cross-reference consistency** | Best (attention to detail) | Good | Good |
| **Novelty assessment** | Good | Good | Good (can search for prior work) |
| **Cost per review** | High ($15/$75 per M tokens) | High ($15/$60 per M tokens) | Low ($1.25/$5 per M tokens) |

---

## Recommended Model-Role Assignment

### Primary Assignment (Multi-Model Available)

| Role | Recommended Model | Rationale |
|------|-------------------|-----------|
| **Reviewer A: Domain Expert** | **Gemini 3 Pro** | 1M context reads full paper + cited references simultaneously; native web search verifies dataset claims, checks for missing baselines, and finds competing recent papers the authors may have missed |
| **Reviewer B: Methods Expert** | **GPT-5 / Codex** | Strongest mathematical reasoning (AIME 100%); best at verifying equation correctness, complexity analysis, gradient flow issues, and formal proofs; more direct critique style suitable for technical issues |
| **Reviewer C: Methodology Expert** | **Claude Opus** | Most systematic at executing structured checklists (10 pitfalls audit); excellent at identifying logical inconsistencies across sections; thorough attention to detail for data leakage detection |
| **Reviewer D: Presentation Expert** | **Claude Opus** | Best writing quality perception; most nuanced understanding of academic style, clarity, and logical flow; strong at identifying claim-evidence mismatches |
| **Meta-Reviewer (AC)** | **GPT-5** | Needs strong reasoning to synthesize 4 reviews from different models, identify genuine consensus vs. superficial agreement, and prioritize revision items; GPT's direct style suits the decision-making role |
| **Devil's Advocate** | **Whichever model was NOT used for the most critical reviewer** | The adversarial critic must use a different model than the primary reviewers to find blind spots they all share |

### Cost-Optimized Assignment

For budget-constrained scenarios, use a tiered approach:

| Tier | Roles | Model | Cost |
|------|-------|-------|------|
| **Deep review** | Rev B (math), Rev C (methodology) | Claude Opus or GPT-5 | High — these are highest-value reviews |
| **Broad review** | Rev A (domain), Rev D (writing) | Gemini 3 Pro | Low — leverages search and long context at 1/10 cost |
| **Synthesis** | Meta-Reviewer, Devil's Advocate | Claude Sonnet or GPT-4o | Medium — synthesis tasks don't require frontier models |

---

## §Devil: The Devil's Advocate Role

### Purpose

The Devil's Advocate is NOT a balanced reviewer. Its sole purpose is to **attack the paper's strongest claims** and find potential fatal flaws that diplomatic reviewers might soften or miss.

### Activation Criteria

Run the Devil's Advocate when:
- All 4 reviewers give Overall ≥ 6/10 (suspiciously unanimous positive)
- No Critical weaknesses were identified (may indicate shared blind spot)
- The paper claims "first" or "novel" or "state-of-the-art" without strong evidence

### Devil's Advocate Prompt Template

```
You are a hostile reviewer who has been asked to find fatal flaws in this paper.
Your job is NOT to be balanced. Assume the paper has a critical weakness and find it.

Focus on:
1. The single strongest claim in the paper — try to falsify it
2. The experimental result that seems "too good" — find the methodological reason
3. The novelty claim — find the most similar prior work that undermines it
4. The assumption most likely to be violated in real deployment
5. The evaluation gap that, if exposed, would change the conclusion

You must identify at least 3 potential fatal flaws with specific evidence.
If you cannot find fatal flaws, explain exactly what you checked and why the paper survives.
```

### Why a Different Model

The Devil's Advocate MUST use a different model than the main reviewers because:
- Same-model adversarial prompting is less effective (model tends to soften its own criticisms)
- A genuinely different model has different blind spots → it can find issues the others literally cannot see
- Cross-model adversarial checking produces more diverse and surprising findings

---

## Cross-Model Review-Rebuttal Protocol

### The Self-Satisfied Rebuttal Problem

When Model X writes a review, then Model X evaluates the rebuttal to its own review, it tends to accept the rebuttal too easily. This is because:
1. The model recognizes patterns it would have generated itself
2. It has implicit memory of what it considered "sufficient" when writing the review
3. It lacks the fresh perspective needed to evaluate whether a fix is truly adequate

### Solution: Cross-Model Rebuttal Verification

```
Phase 1: Review              → Model A writes review
Phase 3: Author drafts fix   → (human or any model)
Phase 5: Re-Review           → Model B evaluates the fix

Model A ≠ Model B (CRITICAL)
```

### Cross-Model Re-Review Matrix

| Original Review By | Re-Review By | Why This Pairing |
|--------------------|-------------|------------------|
| Gemini (Rev A) | Claude or GPT | Claude/GPT verifies domain claims with different knowledge base |
| GPT (Rev B) | Claude | Claude re-checks math with different reasoning approach |
| Claude (Rev C) | GPT | GPT's directness catches methodology fixes that Claude might accept too diplomatically |
| Claude (Rev D) | Gemini | Gemini can search for comparison points; fresh eyes on writing quality |

---

## Single-Model Fallback Protocol

When only one model is available (most common scenario in practice), mitigate the echo chamber through these mandatory measures:

### Mitigation 1: Forced Independence

Run each reviewer in a **separate conversation/context** — do NOT let the model see previous reviews when writing the next one. This prevents explicit opinion leakage.

Implementation:
- Use separate sub-agent invocations (Cursor Task tool) for each reviewer
- Each sub-agent gets ONLY the paper text + its specific reviewer profile
- Reviews are collected and synthesized only in Phase 2

### Mitigation 2: Explicit Disagreement Mandate

In each reviewer prompt, add:

```
IMPORTANT: You MUST identify at least 2 weaknesses that you believe OTHER 
reviewers might MISS. Think about what blind spots a [domain/methods/methodology/
writing] expert would have, and focus your unique contribution there.

Your review will be compared against 3 other independent reviews. If your 
weaknesses list is >70% overlapping with theirs, your review has failed to 
add unique value.
```

### Mitigation 3: Temperature Variation

If the model supports temperature control:
- Reviewer A: temperature 0.3 (focused, conservative)
- Reviewer B: temperature 0.5 (balanced)
- Reviewer C: temperature 0.2 (systematic, precise)
- Reviewer D: temperature 0.7 (more creative, catches unusual issues)
- Devil's Advocate: temperature 0.8 (aggressive, unexpected angles)

### Mitigation 4: Adversarial Self-Check

After all 4 reviews are collected, run a final pass:

```
Here are 4 reviews of the same paper. Identify:
1. Points where ALL reviewers agree — these are likely real issues
2. Points where NO reviewer raised concerns — these are potential blind spots
3. For each blind spot area, generate a NEW critique that none of the 
   reviewers thought of

Focus blind spot search on: data leakage, hidden assumptions, missing 
baselines from 2024-2026, unfair evaluation advantages, overclaiming.
```

### Mitigation 5: Web Search Augmentation

For the Domain Expert role (Rev A), always use web search to:
- Verify dataset claims against original dataset papers
- Find papers published in the last 12 months that should be cited
- Check if claimed "novelty" has been independently achieved elsewhere
- Verify that baseline methods haven't been superseded

This partially compensates for the model's training data cutoff.

---

## Quality Assurance: Review Diversity Metrics

After collecting all reviews, compute these diversity metrics to check review quality:

### Metric 1: Weakness Overlap Ratio

```
overlap = |W_shared| / |W_union|
where W_shared = weaknesses mentioned by 2+ reviewers
      W_union = all unique weaknesses across all reviews

Target: overlap < 0.5 (less than half of weaknesses are shared)
Red flag: overlap > 0.7 (echo chamber likely)
```

### Metric 2: Score Variance

```
score_std = std([overall_A, overall_B, overall_C, overall_D])

Target: score_std ≥ 1.5 (healthy disagreement)
Red flag: score_std < 0.5 (suspiciously unanimous)
```

### Metric 3: Unique Contribution Count

Each review should contain at least 1 weakness or question that NO other review mentions. If a review has zero unique contributions, it failed to leverage its specialized perspective.

### If Metrics Indicate Echo Chamber

1. Re-run the least diverse review with a different model (if available) or different temperature
2. Add the Devil's Advocate pass
3. Force a "what are we all missing?" synthesis step
