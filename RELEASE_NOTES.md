# 发布说明

本文件只描述当前发布；历史版本保留在各自的标签里（例如 `git show v0.6.0:RELEASE_NOTES.md`）。
基于本模板创建的论文维护自己的发布说明，不复制此历史。

## v0.7.0 — 2026-11-14

README 只写给论文。模板自己的起步、版本与升级不再占据人类入口。

- **README 变成论文文档。** 标题与阶段、快速开始、写作、构建与检查、仓库结构、发布与 Overleaf；一屏能扫完，命令先于配置。
- **起步步骤换位置。** "Use this template" 之后要做的六件事，见本文件末尾的 `## Starting from this template`；完整流程仍由 `template-adoption` 技能执行。
- **版本与升级指向技能。** 模板版本、`upgrade-template.sh` 与缺陷反馈不再在 README 展开；每个发布的 `### Upgrading a paper from <tag>` 说明该版本怎么升，反馈走 `template-feedback`。
- **清掉陈旧指针。** 删除对已退役 `template-sync` 的引用；结构表补上 `.agents/notes/` 和 `.claude`、`.pi` 链接。
- **继承状态。** 升级命令为 **Command only.**；README 是 `upgrade: review` 文件，命令不会改写它，改写由论文自己决定。

### Adoption states

以下状态通过 `make check`；`make release-check` 对尚未填写的论文在表中步骤失败，原因见 v0.4.2。模板中的占位内容不是投稿论文。

| State | `make release-check` fails on |
| --- | --- |
| fresh paper | `identity`, `leftovers`, `pages` |
| existing bibliography, no ledger | `identity`, `leftovers`, `pages`, `references` |
| existing bibliography, migrated ledger | `identity`, `leftovers`, `pages`, `references` |
| venue kit | `identity`, `leftovers`, `pages` |

### Upgrading a paper from v0.6.0

1. 运行 `bash .agents/scripts/shared/upgrade-template.sh v0.7.0`（本版为 **Command only.**）。
2. 按本文件的 README 形状重写论文仓库的 `README.md`：保留构建命令与结构表，删掉模板专用步骤；命令不会替你改，因为这份文件被登记为 `upgrade: review`。
3. README 里若还有 `template-sync` 一类已退役命令的说明，删掉。
4. 运行 `bash .agents/scripts/shared/check-development.sh --write-indexes`，再运行 `make check`。

## Starting from this template

1. 用 GitHub 的 **Use this template** 创建论文仓库，公开之前建议选 **Private**；需要可复现的起点时，克隆一个发布标签。
2. 运行 `bash .agents/scripts/shared/init-branches.sh`：创建并推送 `dev`，把它设为默认分支。工作分支从 `dev` 开始，发布时合并到 `main`。
3. 每个 worktree 先运行 `bash .agents/scripts/shared/setup-worktree.sh`。
4. 把采用工作交给 agent（`template-adoption`）：删除 registry 标记 `scope: template` 的文件并记为 `omitted`，把 `template` 块改成论文仓库，把本文档换成论文自己的发布说明，重写 README。
5. 让 agent 填写留给论文的槽位：`page-budget-on-blind-build.md` 的 `PAGE_MARGIN`，`post-build-visual-inspection.md` 的 `MIN_FIGURE_TEXT` 与 `LAST_LINE_FILL`。
6. 把论文简报交给 agent（`paper-foundation`）：`brief.md` 中未决定的内容保持 `unresolved`。

模板升级：`bash .agents/scripts/shared/upgrade-template.sh --check <tag>` 输出计划，去掉 `--check` 应用；
标记 **Command only.** 且没有冲突的版本不需要其他操作。
