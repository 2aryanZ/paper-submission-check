# Paper Skills Repository

[English](#english) | [中文](#中文)

---

## English

This repository uses a flat multi-skill layout under `skills/`.

## Skills

| Skill | Type | Purpose |
|---|---|---|
| `paper-submission-check` | submission | Pre-submission quality checks for LaTeX papers (language, AI-style cleanup, references, formatting, checklist). |
| `paper-multi-round-review` | review | Multi-round peer-review simulation (reviewers, meta-review, rebuttal and revision loop). |

## Repository Structure

```text
paper-submission-check/
├── skills/
│   ├── paper-submission-check/
│   │   ├── SKILL.md
│   │   ├── ai-phrases.md
│   │   ├── ai-style-removal.md
│   │   ├── checklist.md
│   │   ├── paper-structure-guide.md
│   │   ├── reference-format-guide.md
│   │   └── LICENSE
│   └── paper-multi-round-review/
│       ├── SKILL.md
│       ├── reviewer-profiles.md
│       ├── review-dimensions.md
│       ├── ml-security-pitfalls.md
│       ├── multi-model-strategy.md
│       └── review-examples.md
├── README.md
└── LICENSE
```

## Installation

Most AI platforms load one skill per folder (`<skill-name>/SKILL.md`).
Copy the skill folder(s) you want from `skills/`.

### Cursor

```bash
cd ~
git clone git@github.com:zhousodo/paper-submission-check.git paper-skills
cp -r ~/paper-skills/skills/paper-submission-check ~/.cursor/skills/
cp -r ~/paper-skills/skills/paper-multi-round-review ~/.cursor/skills/
```

### OpenAI Codex

```bash
cd ~
git clone git@github.com:zhousodo/paper-submission-check.git paper-skills
cp -r ~/paper-skills/skills/paper-submission-check ~/.agents/skills/
cp -r ~/paper-skills/skills/paper-multi-round-review ~/.agents/skills/
```

### Claude Code

```bash
cd ~
git clone git@github.com:zhousodo/paper-submission-check.git paper-skills
cp -r ~/paper-skills/skills/paper-submission-check ~/.claude/skills/
cp -r ~/paper-skills/skills/paper-multi-round-review ~/.claude/skills/
```

---

## 中文

仓库已改为你要求的扁平多 Skill 结构：所有 Skill 直接放在 `skills/` 下。

## Skill 列表

| Skill | 类型 | 用途 |
|---|---|---|
| `paper-submission-check` | submission | 投稿前终检（语言、AI痕迹清理、参考文献、格式、检查清单）。 |
| `paper-multi-round-review` | review | 多轮同行评审模拟（评审、Meta-Review、rebuttal/revision 循环）。 |

## 仓库结构

```text
paper-submission-check/
├── skills/
│   ├── paper-submission-check/
│   └── paper-multi-round-review/
├── README.md
└── LICENSE
```

## 安装方式

大多数平台按“一个文件夹 = 一个 Skill（必须有 `SKILL.md`）”加载。
按需把 `skills/` 下的目标 Skill 目录复制到平台技能目录。

### Cursor

```bash
cd ~
git clone git@github.com:zhousodo/paper-submission-check.git paper-skills
cp -r ~/paper-skills/skills/paper-submission-check ~/.cursor/skills/
cp -r ~/paper-skills/skills/paper-multi-round-review ~/.cursor/skills/
```

### OpenAI Codex

```bash
cd ~
git clone git@github.com:zhousodo/paper-submission-check.git paper-skills
cp -r ~/paper-skills/skills/paper-submission-check ~/.agents/skills/
cp -r ~/paper-skills/skills/paper-multi-round-review ~/.agents/skills/
```

### Claude Code

```bash
cd ~
git clone git@github.com:zhousodo/paper-submission-check.git paper-skills
cp -r ~/paper-skills/skills/paper-submission-check ~/.claude/skills/
cp -r ~/paper-skills/skills/paper-multi-round-review ~/.claude/skills/
```
