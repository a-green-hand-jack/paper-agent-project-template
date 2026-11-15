# 发布说明

本文件只描述当前发布；历史版本保留在各自的标签里（例如 `git show v0.7.1:RELEASE_NOTES.md`）。
基于本模板创建的论文维护自己的发布说明，不复制此历史。

## v0.10.0 — 2026-11-15

从 `ResearchWorld_paper` 11 月的三轮作者评审里收下三条经验。#251 改了一条现有规则，属行为变更。

- **未决内容改为可见占位。** 新记录 `shared/paper-writing/undecided-content-visible-placeholder.md` 取代原来那条"未决内容写在作者批注里"：稿件里用 `\PaperTODO{...}`（每个构建都可见、发布门禁必拦），原文与"在等什么"进 `.agents/notes/` 的工作笔记与拥有它的 Issue；作者批注只承载一轮评审的话，答复它的改动删除它。`AGENTS.md` 与 `paper-writing` 技能同步。
- **批注宏必须走 `\AuthorComment`。** 同一记录写明：批注命令声明在 `paper/style/author-comments.sty` 且是 `\AuthorComment` 的调用，否则 `make release-check` 枚举不到——下游的盒子式宏（`\annote`/`\cnote`）正是这样躲过门禁的（#251）。
- **一轮评审是一个可测量的流程。** 新参考 `paper-writing/sources/revision-rounds/reference.md`：作者标出的是习惯样本，先按节计数再计划，before/after 计划等批准，改完重量并报告前后计数；修一个口头禅不能装上另一个（#252）。
- **结果未定稿的处置。** `claims-set-expected-results` 增一节：新快照只改数字、不动主张措辞，差异报告给作者并记进 Issue；实验侧撤掉的实验不删描述，改可见占位并写清 owner（#252）。
- **末行修复的操作细节。** `post-build-visual-inspection` 补第 6、7 条：在 blind 构建上量末行、修一处要重量到全过、两栏与单栏分别量；**禁止**用 `\looseness`、`\vspace`、`\linebreak` 或负 `\parfillskip` 凑行，为凑行加的词必须是真内容并报告（#253）。
- **路径检查容忍"已删未提交"的文件**：`git ls-files` 仍列出、工作区已删除的文档不再让它崩。

### Adoption states

以下状态通过 `make check`；`make release-check` 对尚未填写的论文在表中步骤失败，原因见 v0.4.2。模板中的占位内容不是投稿论文。

| State | `make release-check` fails on |
| --- | --- |
| fresh paper | `identity`, `leftovers`, `pages` |
| existing bibliography, no ledger | `identity`, `leftovers`, `pages`, `references` |
| existing bibliography, migrated ledger | `identity`, `leftovers`, `pages`, `references` |
| venue kit | `identity`, `leftovers`, `pages` |

### Upgrading a paper from v0.9.1

**Command only，但行为有变更：**

1. 运行 `bash .agents/scripts/shared/upgrade-template.sh v0.10.0`。
2. 若论文仍按旧规则把未决事项停在作者批注里，本版之后应改成 `\PaperTODO{...}` + 一份 `.agents/notes/` 笔记；论文自己的记录若写了更强的本地规则（例如作者原话逐字保留），保留它并在记录里说明未决项怎样标记。
3. 检查 `paper/style/author-comments.sty` 里的每个批注命令是否都是 `\AuthorComment` 的调用；`make release-check` 只枚举它能看见的命令。

## Starting from this template

1. 用 GitHub 的 **Use this template** 创建论文仓库，公开之前建议选 **Private**；需要可复现的起点时，克隆一个发布标签。
2. 运行 `bash .agents/scripts/shared/init-branches.sh`：创建并推送 `dev`，把它设为默认分支。工作分支从 `dev` 开始，发布时合并到 `main`。
3. 每个 worktree 先运行 `bash .agents/scripts/shared/setup-worktree.sh`。
4. 把采用工作交给 agent（`template-adoption`）：删除 registry 标记 `scope: template` 的文件并记为 `omitted`，把 `template` 块改成论文仓库，把本文档换成论文自己的发布说明，重写 README。
5. 让 agent 填写留给论文的槽位：`page-budget-on-blind-build.md` 的 `PAGE_MARGIN`，`post-build-visual-inspection.md` 的 `MIN_FIGURE_TEXT` 与 `LAST_LINE_FILL`。
6. 把论文简报交给 agent（`paper-foundation`）：`brief.md` 中未决定的内容保持 `unresolved`。

模板升级：`bash .agents/scripts/shared/upgrade-template.sh --check <tag>` 输出计划，去掉 `--check` 应用；
标记 **Command only.** 且没有冲突的版本不需要其他操作。
