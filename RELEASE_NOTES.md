# 发布说明

本文件只描述当前发布；历史版本保留在各自的标签里（例如 `git show v0.4.13:RELEASE_NOTES.md`）。
基于本模板创建的论文维护自己的发布说明，不复制此历史。

## v0.6.0 — 2026-11-14

本版跟随 coding template v0.1.36 → v0.1.37：registry 与 memory/knowledge 只保留当前记录，`retention` 机制被移除（上游 #179）。其余行为、`paper/` 自包含、三种构建和 Overleaf 投影不变。

- **只留当前记录。** `status: superseded|retired` 的 memory/knowledge 记录连同文件一起删除，历史交给 git；`retention`、`retention_reason` 字段消失。替换链只要求"当前记录之间的指向不成环"，被替换的身份可以已不存在（作为 provenance）。
- **升级会失败的地方。** 论文仓库若仍有 `retention*` 字段或 `status: superseded|retired` 条目，升级后 `check-development.sh` 会失败并指出具体记录；发布前删除这些记录即可，内容仍在 git 里。
- **继承状态。** 继承脚本与 v0.1.37 逐字节一致；本仓已无 `retention` 或历史状态条目。

### Adoption states

以下状态通过 `make check`；`make release-check` 对尚未填写的论文在表中步骤失败，原因见 v0.4.2。模板中的占位内容不是投稿论文。

| State | `make release-check` fails on |
| --- | --- |
| fresh paper | `identity`, `leftovers`, `pages` |
| existing bibliography, no ledger | `identity`, `leftovers`, `pages`, `references` |
| existing bibliography, migrated ledger | `identity`, `leftovers`, `pages`, `references` |
| venue kit | `identity`, `leftovers`, `pages` |

### Upgrading a paper from v0.5.0

1. 运行 `bash .agents/scripts/shared/upgrade-template.sh v0.6.0`（本版为 **Command only.**）。
2. 删除 registry 中所有 `retention`/`retention_reason` 字段与 `status: superseded|retired` 的条目及其文件；需要保留的说法写进当前记录，历史留在 git。
3. 运行 `bash .agents/scripts/shared/check-development.sh --write-indexes`，再运行 `make check`。
