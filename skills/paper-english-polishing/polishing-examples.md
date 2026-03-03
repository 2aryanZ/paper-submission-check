# Polishing Examples

Complete before/after examples demonstrating the output format and polishing quality expected for each section type. All examples are from the security + ML domain.

## Contents

- [Example 1: Abstract (Chinese → English)](#example-1-abstract-chinese--english)
- [Example 2: Introduction Opening (Chinese → English)](#example-2-introduction-opening-chinese--english)
- [Example 3: Method Paragraph (Chinese → English)](#example-3-method-paragraph-chinese--english)
- [Example 4: Results Paragraph (Chinese → English)](#example-4-results-paragraph-chinese--english)
- [Example 5: Limitation Paragraph (Chinese → English)](#example-5-limitation-paragraph-chinese--english)
- [Example 6: Special Cases](#example-6-special-cases)
- [Common Transformation Patterns Summary](#common-transformation-patterns-summary)

---

## Example 1: Abstract (Chinese → English)

### Chinese Source

> 高级持续性威胁（APT）的检测与归因长期被割裂为两个阶段：先由黑盒模型输出告警，再以事后解释方法追溯决策依据。然而，事后解释主要捕捉输入与输出间的统计关联，难以保证与模型真实推理路径一致，因此可能给安全响应带来误导。

### Diff Table

| # | Original Sentence (Chinese) | Revised (English, changes **bolded**) | Reason |
|---|---------------------------|---------------------------------------|--------|
| 1 | 高级持续性威胁（APT）的检测与归因长期被割裂为两个阶段：先由黑盒模型输出告警，再以事后解释方法追溯决策依据。 | **Detection and attribution of Advanced Persistent Threats (APTs) have long been treated as two separate stages: a black-box model first raises alerts, and post-hoc explanation methods then trace the decision rationale.** | Restructure: main clause first; define APT at first use; natural English word order |
| 2 | 然而，事后解释主要捕捉输入与输出间的统计关联，难以保证与模型真实推理路径一致，因此可能给安全响应带来误导。 | **However, post-hoc explanations primarily capture statistical correlations between inputs and outputs and do not guarantee alignment with the model's actual reasoning. This mismatch can mislead security response.** | Split Chinese compound into two English clauses; remove ambiguous participial tail |

### Bilingual LaTeX Output

```latex
\zhpara{高级持续性威胁（APT）的检测与归因长期被割裂为两个阶段：先由黑盒模型输出告警，再以事后解释方法追溯决策依据。然而，事后解释主要捕捉输入与输出间的统计关联，难以保证与模型真实推理路径一致，因此可能给安全响应带来误导。}
Detection and attribution of Advanced Persistent Threats (APTs) have long been treated as two separate stages: a black-box model first raises alerts, and post-hoc explanation methods then trace the decision rationale. However, post-hoc explanations primarily capture statistical correlations between inputs and outputs and do not guarantee alignment with the model's actual reasoning. This mismatch can mislead security response.
```

**PDF rendering (comparison mode)**: Chinese appears in small blue text above, English in normal black below.

---

## Example 2: Introduction Opening (Chinese → English)

### Chinese Source

> 2020 年曝光的 SolarWinds 供应链攻击是一个典型案例：攻击者在目标网络中潜伏长达 9 个月，仅使用合法系统管理工具即完成了从初始入侵到数据窃取的完整攻击链。事后调查显示，这些恶意行为混杂在每天数亿条审计日志中，与正常运维活动几乎无法区分。

### Diff Table

| # | Original Sentence (Chinese) | Revised (English, changes **bolded**) | Reason |
|---|---------------------------|---------------------------------------|--------|
| 1 | 2020 年曝光的 SolarWinds 供应链攻击是一个典型案例：攻击者在目标网络中潜伏长达 9 个月... | **The SolarWinds supply-chain compromise disclosed in 2020 exemplifies this threat: the adversary persisted in the target network for nine months, completing the full kill chain from initial access to data exfiltration using only legitimate system administration tools.** | "曝光" → "disclosed"; "攻击者" → "adversary" (security standard); "潜伏" → "persisted" (ATT&CK terminology); spell out "nine" at non-sentence-start; "攻击链" → "kill chain" (standard term) |
| 2 | 事后调查显示，这些恶意行为混杂在每天数亿条审计日志中，与正常运维活动几乎无法区分。 | **Post-incident investigation revealed that these malicious activities were interleaved with hundreds of millions of daily audit log entries. As a result, analysts could hardly distinguish them from normal operations.** | Convert Chinese compound into two explicit clauses with clear causal relation |

### Bilingual LaTeX Output

```latex
\zhpara{2020 年曝光的 SolarWinds 供应链攻击是一个典型案例：攻击者在目标网络中潜伏长达 9 个月，仅使用合法系统管理工具即完成了从初始入侵到数据窃取的完整攻击链。事后调查显示，这些恶意行为混杂在每天数亿条审计日志中，与正常运维活动几乎无法区分。}
The SolarWinds supply-chain compromise disclosed in 2020~\cite{fireeye2020sunburst} exemplifies this threat: the adversary persisted in the target network for nine months and completed the full kill chain from initial access to data exfiltration using only legitimate system administration tools. Post-incident investigation revealed that these malicious activities were interleaved with hundreds of millions of daily audit log entries. As a result, analysts could hardly distinguish them from normal operations.
```

---

## Example 3: Method Paragraph (Chinese → English)

### Chinese Source

> 选择 GRU 而非 Transformer 基于两个考量：其一，尽管当前设定 T=128，但实际部署中实体的原始事件序列可达数千条，GRU 的 O(T) 时间复杂度在扩展至更长序列时更具优势；其二，HARP 的三视图机制需要在同一组编码隐藏状态上进行三次不同掩码的池化操作，GRU 的逐步序列编码天然支持这种共享上下文下的选择性池化。

### Diff Table

| # | Original Sentence (Chinese) | Revised (English, changes **bolded**) | Reason |
|---|---------------------------|---------------------------------------|--------|
| 1 | 选择 GRU 而非 Transformer 基于两个考量 | **We choose GRU over Transformer for two reasons.** | Restructure: English states the main choice first as a short topic sentence |
| 2 | 其一，...GRU 的 O(T) 时间复杂度在扩展至更长序列时更具优势 | **First, although the current setting uses $T=128$, raw entity sequences in production can span thousands of events; the $O(T)$ time complexity of GRU scales more favorably to longer inputs.** | "其一" → "First,"; single Chinese sentence split at semicolon; "更具优势" → "scales more favorably" (precise) |
| 3 | 其二，...GRU 的逐步序列编码天然支持这种共享上下文下的选择性池化 | **Second, the three-view mechanism requires three masked pooling operations over the same set of hidden states. The step-wise encoding of GRU naturally supports this selective pooling under shared context, whereas the pairwise interactions in Transformer self-attention complicate reusing representations after masking.** | Break one long Chinese sentence into two English sentences; add explicit contrast with Transformer (implied in Chinese) |

### Bilingual LaTeX Output

```latex
\zhpara{选择 GRU 而非 Transformer 基于两个考量：其一，尽管当前设定 $T=128$，但实际部署中实体的原始事件序列可达数千条，GRU 的 $O(T)$ 时间复杂度在扩展至更长序列时更具优势；其二，HARP 的三视图机制需要在同一组编码隐藏状态上进行三次不同掩码的池化操作，GRU 的逐步序列编码天然支持这种共享上下文下的选择性池化。}
We choose GRU over Transformer for two reasons. First, although the current setting uses $T=128$, raw entity sequences in production can span thousands of events; the $O(T)$ time complexity of GRU scales more favorably to longer inputs. Second, the three-view mechanism requires three masked pooling operations over the same set of hidden states. The step-wise encoding of GRU naturally supports this selective pooling under shared context, whereas the pairwise interactions in Transformer self-attention complicate reusing representations after masking.
```

**Note**: The Chinese `\zhpara{}` preserves inline math (`$T=128$`, `$O(T)$`) exactly as in the original.

---

## Example 4: Results Paragraph (Chinese → English)

### Chinese Source

> 在 SAGA 上，HARP 的 AP（0.9957）和 F1（0.9962）均为所有方法中最高，AUC 与 SeqGRU、SeqAttn 在显示精度内持平（均为 0.9997，全精度差异 <3×10^-5）。

### Diff Table

| # | Original Sentence (Chinese) | Revised (English, changes **bolded**) | Reason |
|---|---------------------------|---------------------------------------|--------|
| 1 | 在 SAGA 上，HARP 的 AP（0.9957）和 F1（0.9962）均为所有方法中最高 | **On SAGA, HARP achieves the highest AP (0.9957) and F1 (0.9962) among all methods.** | "在...上" → "On"; active voice "achieves" instead of Chinese passive structure |
| 2 | AUC 与 SeqGRU、SeqAttn 在显示精度内持平（均为 0.9997，全精度差异 <3×10^-5） | **Its AUC ties with SeqGRU and SeqAttn at the reported precision (all 0.9997; full-precision difference $<3\times10^{-5}$).** | "显示精度内持平" → "ties at the reported precision" (concise); merge into one sentence with semicolon |

### Bilingual LaTeX Output

```latex
\zhpara{在 SAGA 上，HARP 的 AP（0.9957）和 F1（0.9962）均为所有方法中最高，AUC 与 SeqGRU、SeqAttn 在显示精度内持平（均为 0.9997，全精度差异 $<3\times10^{-5}$）。}
On SAGA, HARP achieves the highest AP (0.9957) and F1 (0.9962) among all methods. Its AUC ties with SeqGRU and SeqAttn at the reported precision (all 0.9997; full-precision difference $<3\times10^{-5}$).
```

---

## Example 5: Limitation Paragraph (Chinese → English)

### Chinese Source

> 序列长度限制。为控制计算复杂度，长序列需要截断或采样（当前限制为 128 个事件）。这可能导致对持续数月的低频攻击的早期信号丢失。

### Diff Table

| # | Original Sentence (Chinese) | Revised (English, changes **bolded**) | Reason |
|---|---------------------------|---------------------------------------|--------|
| 1 | 序列长度限制。 | **Sequence length constraint.** | Section-label translation; "限制" → "constraint" (more formal than "limitation" for a technical bound) |
| 2 | 为控制计算复杂度，长序列需要截断或采样（当前限制为 128 个事件）。 | **To keep computational cost tractable, long sequences are truncated or subsampled to a maximum of 128 events.** | "为控制" → "To keep...tractable" (avoid "in order to"); merge parenthetical into main clause |
| 3 | 这可能导致对持续数月的低频攻击的早期信号丢失。 | **This truncation may discard early-stage indicators of low-and-slow campaigns that span months.** | "持续数月的低频攻击" → "low-and-slow campaigns that span months" (security terminology); "信号丢失" → "discard early-stage indicators" (active, precise) |

### Bilingual LaTeX Output

```latex
\noindent\textbf{Sequence length constraint.}
\zhpara{为控制计算复杂度，长序列需要截断或采样（当前限制为 128 个事件）。这可能导致对持续数月的低频攻击的早期信号丢失。}
To keep computational cost tractable, long sequences are truncated or subsampled to a maximum of 128 events. This truncation may discard early-stage indicators of low-and-slow campaigns that span months.
```

**Note**: Section-label headings (like `\noindent\textbf{...}`) are placed BEFORE `\zhpara{}`, since both Chinese and English share the same heading.

---

## Example 6: Special Cases

### Figure/Table Caption (bilingual)

```latex
\caption{Entity-level detection performance. Best in each column is bolded.
\protect\zhcaption{实体级检测性能。各列最优加粗。}}
\label{tab:main_detection}
```

### Equation-Heavy Paragraph

When a paragraph is mostly equations with brief connective text, keep `\zhpara{}` for the connective text only. Equations are language-neutral and need no bilingual treatment:

```latex
\zhpara{总损失由检测损失与归因质量损失加权组合：}
The total loss combines the detection loss and attribution quality loss:
\begin{equation}
\mathcal{L} = \mathcal{L}_{\text{det}} + \lambda_{\text{attr}}\,\mathcal{L}_{\text{attr}}
\end{equation}
```

### Itemized Contributions

```latex
\zhpara{本文的主要贡献如下：}
The main contributions of this paper are as follows:
\begin{itemize}
\item \zhpara{\textbf{三视图反事实训练范式。}现有可微选择方法要么仅约束充分性...}
\textbf{Three-view counterfactual training.} Existing differentiable selection methods either constrain only sufficiency...
\end{itemize}
```

---

## Common Transformation Patterns Summary

| Chinese Pattern | English Transformation |
|----------------|----------------------|
| 由于A，所以B。 | B because A. / B, as A. |
| 首先...，其次...，最后... | First, ... Second, ... Finally, ... (each a new sentence) |
| ...的...的...的+名词 (noun stacking) | Break into "X of Y" or relative clause |
| One 60+ word Chinese sentence | 2-3 English sentences of 15-25 words each |
| 从而/进而 (resultative) | ", thereby" / "; this enables" / split into two sentences |
| ...的关键在于... | "The key to ... lies in ..." / "... critically depends on ..." |
| 本文主要贡献如下 | "The main contributions of this paper are as follows:" / "This paper makes the following contributions:" |
