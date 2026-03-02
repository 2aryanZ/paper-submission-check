# Paper Skills Repository

[English](#english) | [中文](#中文)

---

## English

This repository now uses a strict categorized multi-skill layout.

## Skills

| Category | Skill | Purpose |
|---|---|---|
| `submission` | `paper-submission-check` | Pre-submission quality checks for LaTeX papers (language, AI-style cleanup, references, formatting, checklist). |
| `review` | `paper-multi-round-review` | Multi-round peer-review simulation (reviewers, meta-review, rebuttal and revision loop). |

## Repository Structure

```text
paper-submission-check/
├── skills/
│   ├── submission/
│   │   └── paper-submission-check/
│   │       ├── SKILL.md
│   │       ├── ai-phrases.md
│   │       ├── ai-style-removal.md
│   │       ├── checklist.md
│   │       ├── paper-structure-guide.md
│   │       ├── reference-format-guide.md
│   │       └── LICENSE
│   └── review/
│       └── paper-multi-round-review/
│           ├── SKILL.md
│           ├── reviewer-profiles.md
│           ├── review-dimensions.md
│           ├── ml-security-pitfalls.md
│           ├── multi-model-strategy.md
│           └── review-examples.md
├── README.md
└── LICENSE
```

## Installation

Most AI platforms load one skill per folder (`<skill-name>/SKILL.md`).
Copy whichever skills you want from this repo.

### Cursor

```bash
cd ~
git clone git@github.com:zhousodo/paper-submission-check.git paper-skills
cp -r ~/paper-skills/skills/submission/paper-submission-check ~/.cursor/skills/
cp -r ~/paper-skills/skills/review/paper-multi-round-review ~/.cursor/skills/
```

### OpenAI Codex

```bash
cd ~
git clone git@github.com:zhousodo/paper-submission-check.git paper-skills
cp -r ~/paper-skills/skills/submission/paper-submission-check ~/.agents/skills/
cp -r ~/paper-skills/skills/review/paper-multi-round-review ~/.agents/skills/
```

### Claude Code

```bash
cd ~
git clone git@github.com:zhousodo/paper-submission-check.git paper-skills
cp -r ~/paper-skills/skills/submission/paper-submission-check ~/.claude/skills/
cp -r ~/paper-skills/skills/review/paper-multi-round-review ~/.claude/skills/
```

---

## 中文

仓库已切换为严格的“分类多 Skill 结构”。

## Skill 列表

| 分类 | Skill | 用途 |
|---|---|---|
| `submission` | `paper-submission-check` | 投稿前终检（语言、AI痕迹清理、参考文献、格式、检查清单）。 |
| `review` | `paper-multi-round-review` | 多轮同行评审模拟（评审、Meta-Review、rebuttal/revision 循环）。 |

## 仓库结构

```text
paper-submission-check/
├── skills/
│   ├── submission/
│   │   └── paper-submission-check/
│   └── review/
│       └── paper-multi-round-review/
├── README.md
└── LICENSE
```

## 安装方式

大多数平台按“一个文件夹 = 一个 Skill（必须有 `SKILL.md`）”加载。
按需把本仓库里的 skill 目录复制到平台技能目录。

### Cursor

```bash
cd ~
git clone git@github.com:zhousodo/paper-submission-check.git paper-skills
cp -r ~/paper-skills/skills/submission/paper-submission-check ~/.cursor/skills/
cp -r ~/paper-skills/skills/review/paper-multi-round-review ~/.cursor/skills/
```

### OpenAI Codex

```bash
cd ~
git clone git@github.com:zhousodo/paper-submission-check.git paper-skills
cp -r ~/paper-skills/skills/submission/paper-submission-check ~/.agents/skills/
cp -r ~/paper-skills/skills/review/paper-multi-round-review ~/.agents/skills/
```

### Claude Code

```bash
cd ~
git clone git@github.com:zhousodo/paper-submission-check.git paper-skills
cp -r ~/paper-skills/skills/submission/paper-submission-check ~/.claude/skills/
cp -r ~/paper-skills/skills/review/paper-multi-round-review ~/.claude/skills/
```
