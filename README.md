# 论文标题

一句话说明这篇论文主张什么、现在到哪一步（草稿 / 准备投稿 <venue> / 已投稿 / 已发布）。

这是模板自带的占位论文。用本模板创建论文仓库后，把标题、这句话和下面各节改成论文自己的内容。

## 快速开始

需要 TeX Live 提供的 `latexmk`、`pdflatex`、`bibtex`，检查还需要 `pdftotext`、`pdfinfo`。
`uv` 可用时，worktree 初始化会把检查用的 Python 装进 `.project/venv`，`make check` 优先用它。

```bash
bash .agents/scripts/shared/setup-worktree.sh   # 每个 worktree 一次
make pdf                                         # 然后打开 .project/build/main.pdf
```

## 写作

- 正文写在 `paper/sections/`，附录写在 `paper/appendix/`，每个附录一个文件，`paper/main.tex`
  在 `\appendix` 之后按顺序 `\input`。
- 我定的事情：论文的主张、故事主线、实验公平性、重要结果解释、投稿与发布。
- 还没定的内容写进作者批注，不要写成正文里的结论；`submission` 与 `blind` 构建会自动去掉批注。
- 让 agent 改的时候说清改哪一节、改成什么。它会把决定记进 `.agents/memory/project/`；
  看不懂那些记录时，让它用平实的语言复述一遍。
- 论文里出现的每个数字都来自 `assets/MANIFEST.yaml` 登记的运行，并且只能经由
  `paper/macros.tex` 的接口宏写进正文；不要手抄数字。
- 引用只来自 `paper/refs.bib`，每条引用和它所支持的句子记在 `.agents/references/ledger.json`。

## 构建与检查

| 命令 | 得到什么 |
| --- | --- |
| `make pdf` | 署名、保留批注的全文，我审阅时看这份 |
| `make blind` | 匿名版本，用于投稿机检 |
| `make submission` | 署名、无批注的版本 |
| `make check` | 构建 `main` 与 `blind`，检查引用、引文、标签、接口宏、台账、记录与单元测试，并报告正文页数 |
| `make release-check` | 投稿门禁：匿名性、残留批注与占位身份、页预算、引文强度、元数据审计（需 `uv` 与网络） |

三个版本出自同一份源：`paper/main.tex` 是全文，`paper/submission.tex` 和 `paper/blind.tex`
各只有一行，只关闭其中的某些层次。`PAGE_BUDGET` 在根目录 `Makefile` 里设定，
无页数限制的发布（例如 arXiv）写 `PAGE_BUDGET=none`。TeX 不在 `PATH` 上时用
`TEXBIN=<TeX Live bin 目录>` 指定。

`paper/` 是自包含的：单独复制它，`make -C <复制目录> main` 仍然能构建（`blind`、`submission` 同理）。

## 仓库结构

| 路径 | 是什么 |
| --- | --- |
| `paper/` | 论文本身，自包含；单独复制也能构建，详见下面一行 |
| `assets/MANIFEST.yaml` | 每个数字、表格和图数据文件的来源仓库、提交、运行、校验和与重生成命令 |
| `Makefile` | 上面那些命令；输出写到 `.project/build/` |
| `.project/` | 构建输出、日志和截图；Git 忽略，不进论文 |
| `.agents/` | agent 的工作面：规则、技能、记录、台账、脚本与检查；入口 `.agents/AGENTS.md`，`notes/` 放工作笔记 |
| `.claude/`、`.pi/` | 指向 `.agents/` 的链接，让对应的 agent 找到同一份规则 |
| `AGENTS.md`、`CLAUDE.md` | agent 的规则与任务路由；`CLAUDE.md` 是指向 `AGENTS.md` 的链接 |
| `RELEASE_NOTES.md` | 每次发布的说明：当前版本一节，历史在标签里 |

`paper/` 里的内容：`main.tex` 是全文，`submission.tex`、`blind.tex` 各一行，另有
`authors.tex`、`macros.tex`、`refs.bib`，以及 `sections/`、`appendix/`、`figures/`、
`tables/`、`algorithms/`、`style/` 和它自己的 `Makefile`。

## 发布与 Overleaf

发布走从 `dev` 到 `main` 的 PR：`make release-check` 通过后合并，在 `main` 上创建
`submit-<venue>-<yyyy>`、`arxiv-v1` 或 `camera-ready` 这样的标签，并在 `RELEASE_NOTES.md`
里写一条记录。

Overleaf 只镜像 `paper/`：`bash .agents/scripts/shared/paper-publication/overleaf-sync.sh status`
比较两边，`push` 把 `HEAD:paper` 快进推过去，`pull` 把 Overleaf 上的编辑拉回
`sync/overleaf-*` 分支。仓库根目录永远不会发到 Overleaf；取舍与失败处理见 `paper-publication` 技能。

## 来源

本仓库由 [paper-agent-project-template](https://github.com/a-green-hand-jack/paper-agent-project-template)
生成。起步步骤（初始化 `dev`、删除模板专用内容、填写留给论文的槽位）在 `RELEASE_NOTES.md`
的 `## Starting from this template` 一节；升级与缺陷反馈交给 `template-upgrade`、`template-feedback`
技能。论文采用模板后，删掉本节和那一节。
