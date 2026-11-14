# 发布说明

本文件只描述当前发布；历史版本保留在各自的标签里（例如 `git show v0.4.13:RELEASE_NOTES.md`）。
基于本模板创建的论文维护自己的发布说明，不复制此历史。

## v0.5.0 — 2026-11-14

本版把模板收敛为“`paper/` 是唯一的人类展示面，`.agents/` 是唯一的开发面”，并跟随 coding template v0.1.34 → v0.1.36。论文正文、`paper/` 自包含、三种构建和 Overleaf 投影不变。

- **人类面收敛（[#221](https://github.com/a-green-hand-jack/paper-agent-project-template/issues/221)）。** 删除 `PAPER.md` 和 `DEV.md`：论文的决定进 `.agents/memory/project/`，`README.md` 是唯一的人类入口；取消 `Mode: collaborative|autonomous`，写作即 human-agent co-work。`paper_brief.py`、brief-ingest 卡片与其测试随 `PAPER.md` 退役。
- **附录独立（[#238](https://github.com/a-green-hand-jack/paper-agent-project-template/issues/238)）。** 每个附录一个文件，位于 `paper/appendix/`；`paper/main.tex` 在 `\appendix` 之后按主文引用顺序 `\input`，`sections/` 只放正文。
- **开发面结构（[#224](https://github.com/a-green-hand-jack/paper-agent-project-template/issues/224)）。** `.claude` 与 `.pi` 是指向 `.agents/` 的符号链接；新增 `.agents/notes/` 存放进行中的计划与图稿；写作范例只放 `.project/artifacts/writing-exemplars/` 或登记为外部资产。
- **引用检查（[#227](https://github.com/a-green-hand-jack/paper-agent-project-template/issues/227)）。** `make check` 新增 `paths` 一步：文档里点名的 `.agents/…`、`paper/…`、`assets/…` 路径必须存在，`CLAUDE.md`/`.claude`/`.pi` 必须是约定目标的符号链接；豁免逐条写在 `check-development-paths.allow` 并打印。
- **技能裁剪（[#229](https://github.com/a-green-hand-jack/paper-agent-project-template/issues/229)）。** 删除 15 个未被使用或已被取代的 vendored 包（29 → 2），`.agents/skills/shared` 从 4.7 MB 降到 0.6 MB；`agent-communication`、`cli-first-operations`、`engineering-change` 降为 `optional`，论文默认不继承。
- **环境（[#226](https://github.com/a-green-hand-jack/paper-agent-project-template/issues/226)）。** `setup-project.sh` 在 `uv` 可用时创建 `.project/venv` 并安装 PyYAML 与 markdown-it-py，`make check`/`make release-check` 优先使用它；`.project/venv` 与 `.project/tools` 有了 teardown 规则。
- **记录（[#228](https://github.com/a-green-hand-jack/paper-agent-project-template/issues/228)）。** 两篇下游论文的九条过程经验进入 `.agents/memory/shared/`（claims→预期结果、不防御性写作、实验一节一表一图、符号开销、作者批注承载未定内容、图稿 deck、Overleaf 以树为准、凭据路线、合作者内容逐字节保留）。
- **修复（[#220](https://github.com/a-green-hand-jack/paper-agent-project-template/issues/220)）。** v0.4.13 分组记录 `llm-credentials` 中重复的适配段；内容检查拒绝重复标题与畸形标题。
- **跟随上游 v0.1.35 → v0.1.36。** registry 只记录当前状态：`legacy_inventory`、`local_legacy_inventory`、`migrations` 被移除，新增 `minimum_upgrade_source: v0.4.12`；`RELEASE_NOTES.md` 只描述当前版本，升级命令按标签逐个读取；继承脚本与上游逐字节一致（上游 #162–#168、#174、#177）。
- **发布顺序。** 发布先经 `dev` → `main` 的 PR，合并后只在 `main` 上创建标签（`paper-publication` 技能已写明）。

### Adoption states

以下状态通过 `make check`；`make release-check` 对尚未填写的论文在表中步骤失败，原因见 v0.4.2。模板中的占位内容不是投稿论文。

| State | `make release-check` fails on |
| --- | --- |
| fresh paper | `identity`, `leftovers`, `pages` |
| existing bibliography, no ledger | `identity`, `leftovers`, `pages`, `references` |
| existing bibliography, migrated ledger | `identity`, `leftovers`, `pages`, `references` |
| venue kit | `identity`, `leftovers`, `pages` |

### Upgrading a paper from v0.4.13

命令完成机械部分，以下步骤留给论文：

1. 删除 `PAPER.md` 和 `DEV.md`；仍需要的决定移入 `.agents/memory/project/`（`paper-foundation/brief.md`、`experiments.md`、`paper-interfaces.md`、`paper-publication/publication.md`）。这两个文件的条目带 `upgrade: review`，命令不会替你删除。
2. 把附录从 `paper/sections/` 移到 `paper/appendix/`，每个附录一个文件；模板新增的 `paper/appendix/a-example.tex` 只是起点，可删除或替换。
3. 升级后运行 `bash .agents/scripts/shared/check-development.sh --write-indexes`，再运行 `make check` 并查看受影响的页面。
4. 论文早于 `v0.4.12` 时必须用 `template-adoption` 重新接入：registry 不再携带迁移表，升级只支持 `minimum_upgrade_source` 及之后的来源。
5. 可选：采用 `.agents/notes/` 存放进行中的计划与图稿；删除论文侧的 `RELEASE_NOTES.md` 历史，只保留当前发布。
