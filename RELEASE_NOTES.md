# 发布说明

本文件只描述当前发布；历史版本保留在各自的标签里（例如 `git show v0.7.1:RELEASE_NOTES.md`）。
基于本模板创建的论文维护自己的发布说明，不复制此历史。

## v0.10.1 — 2026-11-15

作者用中文写批注，模板却排不出来（#256）。

- `paper/style/author-comments.sty` 现在在显示批注的构建里加载 `CJKutf8`，并把批注正文包进
  `CJK` 环境；`submission` 与 `blind` 不加载 CJK，依赖面不变。
- 之前 `main` 会在第一个中文字符处失败（`Unicode character 标`）；`RSI_light_paper` 2026-11-15
  同步作者新批注时撞上，PR #21 在论文侧修了一次。
- 加了一条测试：`author-comments.sty` 必须在 `\ifPaperNotes` 下加载 CJK，并且批注正文包在
  `CJK` 环境里——这条约束靠构建发现不了，只能靠断言。

### Adoption states

以下状态通过 `make check`；`make release-check` 对尚未填写的论文在表中步骤失败，原因见 v0.4.2。模板中的占位内容不是投稿论文。

| State | `make release-check` fails on |
| --- | --- |
| fresh paper | `identity`, `leftovers`, `pages` |
| existing bibliography, no ledger | `identity`, `leftovers`, `pages`, `references` |
| existing bibliography, migrated ledger | `identity`, `leftovers`, `pages`, `references` |
| venue kit | `identity`, `leftovers`, `pages` |

### Upgrading a paper from v0.10.0

**Command only，但 `paper/` 属产品面，升级命令不动它：**

1. 运行 `bash .agents/scripts/shared/upgrade-template.sh v0.10.1`（开发面与 v0.10.0 相同）。
2. 若本仓库要用中文批注，把模板本版的 `paper/style/author-comments.sty` 里那三行（`\ifPaperNotes\RequirePackage{CJKutf8}\fi` 与批注正文的 `CJK` 环境）照抄进自己的 sty；抄完 `make pdf`、`make submission`、`make blind` 三个构建都要过。
3. 改了 `paper/` 之后按 `paper-publication` 的流程 push 到 Overleaf，让作者那边也能编译。

## Starting from this template

1. 用 GitHub 的 **Use this template** 创建论文仓库，公开之前建议选 **Private**；需要可复现的起点时，克隆一个发布标签。
2. 运行 `bash .agents/scripts/shared/init-branches.sh`：创建并推送 `dev`，把它设为默认分支。工作分支从 `dev` 开始，发布时合并到 `main`。
3. 每个 worktree 先运行 `bash .agents/scripts/shared/setup-worktree.sh`。
4. 把采用工作交给 agent（`template-adoption`）：删除 registry 标记 `scope: template` 的文件并记为 `omitted`，把 `template` 块改成论文仓库，把本文档换成论文自己的发布说明，重写 README。
5. 让 agent 填写留给论文的槽位：`page-budget-on-blind-build.md` 的 `PAGE_MARGIN`，`post-build-visual-inspection.md` 的 `MIN_FIGURE_TEXT` 与 `LAST_LINE_FILL`。
6. 把论文简报交给 agent（`paper-foundation`）：`brief.md` 中未决定的内容保持 `unresolved`。

模板升级：`bash .agents/scripts/shared/upgrade-template.sh --check <tag>` 输出计划，去掉 `--check` 应用；
标记 **Command only.** 且没有冲突的版本不需要其他操作。
