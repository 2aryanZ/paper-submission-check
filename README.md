# Paper Pre-Submission Quality Check

[English](#english) | [中文](#中文)

---

## English

A systematic, 10-phase quality inspection workflow for academic LaTeX papers before journal/conference submission. Works with **Cursor, Claude Code, OpenAI Codex, GitHub Copilot, Windsurf**, and any AI coding assistant that reads markdown instructions.

### Supported Platforms

All major AI coding platforms now support a **skill directory** structure — a folder with a `SKILL.md` file that the agent auto-detects and loads.

| Platform | Personal Skills | Project Skills | Invocation |
|----------|----------------|----------------|------------|
| **Cursor** | `~/.cursor/skills/` | `.cursor/skills/` | Auto-detected; triggered by keywords |
| **Claude Code** | `~/.claude/skills/` | `.claude/skills/` | Auto-detected; or `/paper-submission-check` |
| **OpenAI Codex** | `~/.agents/skills/` | `.agents/skills/` | Auto-detected by Codex CLI/IDE/App |
| **GitHub Copilot** | — | `.github/copilot-instructions.md` or `AGENTS.md` | Referenced as custom instructions |
| **Windsurf** | Global rules (via UI) | `.windsurf/rules/` | Loaded as workspace rules |
| **Any LLM** | — | — | Copy `SKILL.md` content to system prompt |

### What It Does

This skill guides the AI agent through a 10-phase quality check of your LaTeX paper:

| Phase | Check | Examples |
|-------|-------|---------|
| 0 | **Pre-Check** | Detect citation style (numbered/author-year), template type, journal name |
| 1 | **Pronoun & Subjectivity** | "we/our" overuse with quantitative thresholds, "our proposed" redundancy |
| 2 | **AI-Style Detection & Removal** | 13 AI patterns with severity levels (S1-S4), 80+ phrases, em dash/focal word/-ing chain detection, rewriting strategies |
| 3 | **Symbol & Punctuation** | Chinese/English punctuation mixing, dash errors, space issues |
| 4 | **Capitalization** | Section title consistency, acronym definitions |
| 5 | **LaTeX Issues** | Citation format (style-aware), `~` before `\cite`/`\ref`, redundant formatting |
| 6 | **Grammar & Language** | Contractions, comma splices, duplicate content, tense consistency |
| 7 | **Tables, Figures & Numbers** | Number cross-reference verification, decimal precision |
| 8 | **Content Structure & Completeness** | Abstract (PRKS), introduction (CARS model), paragraph/sentence length, keywords, section rules, limitations, conclusion ≠ abstract |
| 9 | **BIB File Integrity** | Brace matching, nested entries, missing fields, cross-references |
| 10 | **Final Checklist** | Per-publisher requirements (Elsevier, IEEE, Springer, ACM) |

### Supported Publishers

- **Elsevier** (`elsarticle`): IPM, COMNET, JSA, KBS, ESWA, etc.
- **IEEE** (`IEEEtran`): Transactions, conferences
- **Springer** (`svjour3`, `llncs`): APIN, TOIT, LNCS, etc.
- **ACM** (`acmart`): Conferences

### Installation

#### Cursor

```bash
# macOS / Linux
cd ~/.cursor/skills
git clone https://github.com/zhousodo/paper-submission-check.git
```

```powershell
# Windows
cd $env:USERPROFILE\.cursor\skills
git clone https://github.com/zhousodo/paper-submission-check.git
```

Restart Cursor after cloning. The skill auto-activates when you mention "paper check", "submission", or "proofreading".

#### Claude Code

Claude Code uses `~/.claude/skills/` (personal) and `.claude/skills/` (project) — the same folder + `SKILL.md` convention.

**Personal skill (all projects):**

```bash
# macOS / Linux
cd ~/.claude/skills
git clone https://github.com/zhousodo/paper-submission-check.git
```

```powershell
# Windows
cd $env:USERPROFILE\.claude\skills
git clone https://github.com/zhousodo/paper-submission-check.git
```

**Project skill (one project):**

```bash
cd your-paper-project
mkdir -p .claude/skills
cd .claude/skills
git clone https://github.com/zhousodo/paper-submission-check.git
```

After installation, invoke with `/paper-submission-check` or let Claude auto-detect it.

#### OpenAI Codex

Codex uses `~/.agents/skills/` (user-level) and `.agents/skills/` (repository-level) for skills.

**User-level skill (all projects):**

```bash
# macOS / Linux
cd ~/.agents/skills
git clone https://github.com/zhousodo/paper-submission-check.git
```

```powershell
# Windows
cd $env:USERPROFILE\.agents\skills
git clone https://github.com/zhousodo/paper-submission-check.git
```

**Repository-level skill (one project):**

```bash
cd your-paper-project
mkdir -p .agents/skills
cd .agents/skills
git clone https://github.com/zhousodo/paper-submission-check.git
```

Works across Codex CLI, IDE extension, and Codex App.

#### GitHub Copilot

Copilot supports `AGENTS.md` for its coding agent. Add to your repository root's `AGENTS.md`:

```markdown
## Paper Quality Check

When reviewing LaTeX papers before submission, follow the 10-phase workflow in:
- .agents/skills/paper-submission-check/SKILL.md

Reference databases:
- AI phrase detection: .agents/skills/paper-submission-check/ai-phrases.md
- Publisher checklists: .agents/skills/paper-submission-check/checklist.md
```

Copilot also reads `.github/copilot-instructions.md` and path-specific `.github/instructions/*.instructions.md` files.

#### Windsurf

Windsurf uses `.windsurf/rules/` for workspace-level rules.

**Workspace rule:**

```bash
cd your-paper-project
mkdir -p .windsurf/rules
cd .windsurf/rules
git clone https://github.com/zhousodo/paper-submission-check.git
```

You can also reference the skill content in `.windsurf/context.md` for session-wide context.

#### Any Other LLM (ChatGPT, Gemini, etc.)

Copy the content of `SKILL.md` into your system prompt or conversation, then ask:

```
Based on the above instructions, check my paper: [paste LaTeX content]
```

### Usage Examples

#### Cursor

```
@SKILL.md Please check my paper @paper.tex and @refs.bib before submission.
```

#### Claude Code

```bash
# CLI mode
claude "Check my paper.tex and my.bib for submission to Elsevier"

# Interactive mode — invoke the skill directly
> /paper-submission-check
```

#### OpenAI Codex

```bash
codex "Review my paper.tex using the paper-submission-check workflow"
```

#### General Prompts (any platform)

```
Check my paper @paper.tex and @refs.bib before submitting to Elsevier.
```

```
Run a pre-submission quality check on @manuscript.tex.
```

```
Help me review @paper.tex for AI-generated style issues.
```

### File Structure

```
paper-submission-check/
├── SKILL.md                  # Main skill instructions (10-phase workflow)
├── ai-phrases.md             # AI-generated phrase database (5 tiers, 80+ phrases)
├── ai-style-removal.md       # AI style removal guide (13 patterns, severity levels, rewriting strategies)
├── paper-structure-guide.md  # Paper structure & writing quality guide (abstract, CARS, paragraphs, keywords, sections)
├── checklist.md              # Per-publisher requirements and regex search commands
├── README.md                 # This file
└── LICENSE                   # MIT License
```

### Output

The skill produces a structured report:

```markdown
# Paper Pre-Submission Check Report

## Paper Info
- Template: elsarticle
- Citation Style: numbered
- Target Journal: Information Processing & Management

## Summary
- Total issues found: 23
- Critical (must fix): 3
- Warning (should fix): 12
- Suggestion (optional): 8

## Pronoun Statistics
- "we" count: 18 (threshold: ≤15) [OVER]
- "our" count: 5 (threshold: ≤8) [OK]

## Critical Issues
1. [Line 42] BIB entry missing closing brace
2. [Line 156] AI-style phrase: "has garnered significant attention"
...
```

### Contributing

Issues and pull requests are welcome. If you find new AI-generated patterns or publisher-specific requirements, please contribute them.

### License

MIT License - see [LICENSE](LICENSE)

---

## 中文

一个系统化的 10 阶段学术 LaTeX 论文投稿前质量检查工作流。支持 **Cursor、Claude Code、OpenAI Codex、GitHub Copilot、Windsurf** 及所有能读取 Markdown 指令的 AI 编程助手。

### 支持的平台

主流 AI 编程平台均已支持 **skill 目录** 结构 —— 一个包含 `SKILL.md` 文件的文件夹，代理会自动检测并加载。

| 平台 | 个人 Skill 目录 | 项目 Skill 目录 | 调用方式 |
|------|----------------|----------------|---------|
| **Cursor** | `~/.cursor/skills/` | `.cursor/skills/` | 自动检测；关键词触发 |
| **Claude Code** | `~/.claude/skills/` | `.claude/skills/` | 自动检测；或 `/paper-submission-check` |
| **OpenAI Codex** | `~/.agents/skills/` | `.agents/skills/` | Codex CLI / IDE / App 自动检测 |
| **GitHub Copilot** | — | `AGENTS.md` 或 `.github/copilot-instructions.md` | 作为自定义指令引用 |
| **Windsurf** | 全局规则（通过 UI） | `.windsurf/rules/` | 作为工作区规则加载 |
| **其他 LLM** | — | — | 将 `SKILL.md` 内容复制到系统提示词 |

### 功能说明

此 skill 引导 AI 代理对 LaTeX 论文进行 10 阶段质量检查：

| 阶段 | 检查项 | 说明 |
|------|--------|------|
| 0 | **预检** | 检测引用风格（编号/作者-年份）、模板类型、期刊名称 |
| 1 | **代词和主观性** | "we/our" 过度使用（含量化阈值）、"our proposed" 冗余检测 |
| 2 | **AI 风格检测与移除** | 13 种 AI 模式（S1-S4 严重度分级）、80+ 短语、破折号/焦点词/-ing 链检测、改写策略 |
| 3 | **符号和标点** | 中英文标点混用、破折号错误、空格问题 |
| 4 | **大小写一致性** | 章节标题风格统一、缩写定义检查 |
| 5 | **LaTeX 问题** | 引用格式（区分编号/作者-年份）、`~` 不间断空格、重复格式化 |
| 6 | **语法和语言** | 缩写词、逗号拼接、重复内容、时态一致性 |
| 7 | **表格、图表和数字** | 正文与表格数字交叉验证、小数精度一致 |
| 8 | **内容结构与完整性** | 摘要（PRKS）、引言（CARS 模型）、段落/句子长度、关键词、各节规范、局限性、结论≠摘要 |
| 9 | **BIB 文件完整性** | 花括号配对、条目嵌套、缺失字段、交叉引用 |
| 10 | **最终清单** | 各出版商特定要求（Elsevier、IEEE、Springer、ACM） |

### 支持的出版商

- **Elsevier** (`elsarticle`)：IPM、COMNET、JSA、KBS、ESWA 等
- **IEEE** (`IEEEtran`)：期刊、会议
- **Springer** (`svjour3`, `llncs`)：APIN、TOIT、LNCS 等
- **ACM** (`acmart`)：会议

### 安装方法

#### Cursor

```powershell
# Windows
cd $env:USERPROFILE\.cursor\skills
git clone https://github.com/zhousodo/paper-submission-check.git
```

```bash
# macOS / Linux
cd ~/.cursor/skills
git clone https://github.com/zhousodo/paper-submission-check.git
```

克隆后重启 Cursor，skill 会自动识别。

#### Claude Code

Claude Code 使用 `~/.claude/skills/`（个人）和 `.claude/skills/`（项目）—— 与 Cursor 相同的文件夹 + `SKILL.md` 约定。

**个人 skill（所有项目可用）：**

```powershell
# Windows
cd $env:USERPROFILE\.claude\skills
git clone https://github.com/zhousodo/paper-submission-check.git
```

```bash
# macOS / Linux
cd ~/.claude/skills
git clone https://github.com/zhousodo/paper-submission-check.git
```

**项目 skill（单个项目）：**

```bash
cd 你的论文项目目录
mkdir -p .claude/skills
cd .claude/skills
git clone https://github.com/zhousodo/paper-submission-check.git
```

安装后，使用 `/paper-submission-check` 调用，或让 Claude 自动检测。

#### OpenAI Codex

Codex 使用 `~/.agents/skills/`（用户级）和 `.agents/skills/`（仓库级）存放 skill。

**用户级 skill（所有项目可用）：**

```powershell
# Windows
cd $env:USERPROFILE\.agents\skills
git clone https://github.com/zhousodo/paper-submission-check.git
```

```bash
# macOS / Linux
cd ~/.agents/skills
git clone https://github.com/zhousodo/paper-submission-check.git
```

**仓库级 skill（单个项目）：**

```bash
cd 你的论文项目目录
mkdir -p .agents/skills
cd .agents/skills
git clone https://github.com/zhousodo/paper-submission-check.git
```

适用于 Codex CLI、IDE 扩展和 Codex App。

#### GitHub Copilot

Copilot 编程代理支持 `AGENTS.md`。在仓库根目录的 `AGENTS.md` 中添加：

```markdown
## 论文质量检查

审查 LaTeX 论文时，遵循 .agents/skills/paper-submission-check/SKILL.md 中的工作流。
```

Copilot 也支持 `.github/copilot-instructions.md` 和路径级 `.github/instructions/*.instructions.md`。

#### Windsurf

Windsurf 使用 `.windsurf/rules/` 存放工作区规则。

```bash
cd 你的论文项目目录
mkdir -p .windsurf/rules
cd .windsurf/rules
git clone https://github.com/zhousodo/paper-submission-check.git
```

也可在 `.windsurf/context.md` 中引用 skill 内容作为会话上下文。

#### 其他 LLM（ChatGPT、Gemini 等）

将 `SKILL.md` 的内容复制到系统提示词或对话中，然后提问：

```
根据上述指令，检查我的论文：[粘贴 LaTeX 内容]
```

### 使用方法

#### Cursor

```
@SKILL.md 请帮我检查论文 @paper.tex 和 @refs.bib，准备投稿。
```

#### Claude Code

```bash
# CLI 模式
claude "检查 paper.tex 和 my.bib，准备投稿到 Elsevier"

# 交互模式 — 直接调用 skill
> /paper-submission-check
```

#### OpenAI Codex

```bash
codex "使用 paper-submission-check 工作流审查 paper.tex"
```

### 贡献

欢迎提交 Issue 和 Pull Request。如果发现新的 AI 生成模式或出版商要求，请贡献到此项目。

### 许可证

MIT 许可证 - 详见 [LICENSE](LICENSE)
