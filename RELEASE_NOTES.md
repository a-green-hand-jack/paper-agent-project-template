# 发布说明

本文件只描述当前发布；历史版本保留在各自的标签里（例如 `git show v0.7.1:RELEASE_NOTES.md`）。
基于本模板创建的论文维护自己的发布说明，不复制此历史。

## v0.8.0 — 2026-11-15

`assets/` 退役。论文报告的是别人的运行，模板不再保留一个外部资产目录：结果来源改由记录承载。

- **结果台账换成记录。** `.agents/memory/project/paper-foundation/results-ledger.md` 一行一个上报值：id、类型、`observed`/`planned`、来源仓库与提交/运行、文件与 SHA-256、重生成命令、接口宏和使用位置。
- **`assets/` 删除。** 目录里只有一份 schema 和空的 `assets: []`，连一份真实资产都不该随模板发布；它的链接机制（`.project/assets.links`）在论文里没有用途——大文件（原始日志、checkpoint、数据集）留在产生它的代码仓库或受管存储，本仓库不保存指向它们的机器路径。小文件仍在 `paper/tables/`、`paper/figures/` 里提交。
- **规则、记录与技能同步。** `AGENTS.md`、`.agents/AGENTS.md`、`README.md`、`experiments.md`、`paper-interfaces.md`、`results-through-interface-macros.md`、`writing-exemplar-archive.md`、`paper-foundation`、`paper-figures` 与 `asset-lifecycle` 技能、`.gitignore` 的 `assets/*` 例外，以及路径检查的前缀表，全部改指台账。
- **一项已知的上游缺口。** 继承的 `diagnose-environment.sh` 仍要求 `assets/MANIFEST.yaml` 并报 `FAIL assets manifest`，`setup-worktree.sh` 每次运行都会警告，`migrate-assets.sh` 在 worktree 退休时会把 `assets/` 建回来。上游已报 #183；这些脚本保持逐字节继承，不在本仓库改。

### Adoption states

以下状态通过 `make check`；`make release-check` 对尚未填写的论文在表中步骤失败，原因见 v0.4.2。模板中的占位内容不是投稿论文。

| State | `make release-check` fails on |
| --- | --- |
| fresh paper | `identity`, `leftovers`, `pages` |
| existing bibliography, no ledger | `identity`, `leftovers`, `pages`, `references` |
| existing bibliography, migrated ledger | `identity`, `leftovers`, `pages`, `references` |
| venue kit | `identity`, `leftovers`, `pages` |

### Upgrading a paper from v0.7.1

本版删掉了一个目录，命令不会动论文自己拥有的路径，所以迁移要手动完成。

1. 取来本版的新记录：`git show <本版标签>:.agents/memory/project/paper-foundation/results-ledger.md > .agents/memory/project/paper-foundation/results-ledger.md`（它登记为 `optional`，升级命令只在计划里提示，不会替你写）。
2. 把 `assets/MANIFEST.yaml` 的每条条目改写成台账里的一行；论文正文与 `paper-interfaces.md` 里引用的 manifest id 一并改成台账 id。
3. 删除 `assets/` 目录。
4. 从 `.agents/content-registry.yaml` 删掉 `assets/README.md`、`assets/MANIFEST.yaml`、`assets/.gitkeep` 三条；留着会变成 dangling active entry，`make check` 会失败。
5. 运行 `bash .agents/scripts/shared/check-development.sh --write-indexes`，再运行 `make check`。

## Starting from this template

1. 用 GitHub 的 **Use this template** 创建论文仓库，公开之前建议选 **Private**；需要可复现的起点时，克隆一个发布标签。
2. 运行 `bash .agents/scripts/shared/init-branches.sh`：创建并推送 `dev`，把它设为默认分支。工作分支从 `dev` 开始，发布时合并到 `main`。
3. 每个 worktree 先运行 `bash .agents/scripts/shared/setup-worktree.sh`。
4. 把采用工作交给 agent（`template-adoption`）：删除 registry 标记 `scope: template` 的文件并记为 `omitted`，把 `template` 块改成论文仓库，把本文档换成论文自己的发布说明，重写 README。
5. 让 agent 填写留给论文的槽位：`page-budget-on-blind-build.md` 的 `PAGE_MARGIN`，`post-build-visual-inspection.md` 的 `MIN_FIGURE_TEXT` 与 `LAST_LINE_FILL`。
6. 把论文简报交给 agent（`paper-foundation`）：`brief.md` 中未决定的内容保持 `unresolved`。

模板升级：`bash .agents/scripts/shared/upgrade-template.sh --check <tag>` 输出计划，去掉 `--check` 应用；
标记 **Command only.** 且没有冲突的版本不需要其他操作。
