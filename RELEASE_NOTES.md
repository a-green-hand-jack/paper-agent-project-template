# 发布说明

本文件只描述当前发布；历史版本保留在各自的标签里（例如 `git show v0.7.1:RELEASE_NOTES.md`）。
基于本模板创建的论文维护自己的发布说明，不复制此历史。

## v0.9.0 — 2026-11-15

两个下游论文从 v0.4.12 升到 v0.8.0 时暴露的三处升级链路缺陷。

- **构建入口不再被自动合并。** 三方合并把论文本地已有的 `ifneq ($(wildcard …venv…))` 块再插一份，
  重复运行还会累加（`RSI_light_paper` 升完后同一段有三份）。`Makefile` 改为 `upgrade: review`：
  升级只打印本版的差异，合并由论文决定（#245）。
- **uv 不再被钉死在一个补丁版本。** `reference-integrity/uv.toml` 从 `==0.11.23` 改成 `>=0.11.23`；
  依赖由 `uv.lock` 固定，宿主 uv 更新不该让 `make release-check` 的元数据审计直接拒跑（#246）。
- **退役的根目录文档收尾。** v0.5.0 删掉 `PAPER.md`/`DEV.md` 后，13 个技能与索引文件里还有 28 处
  指向 `PAPER.md`，现在都改指 `paper-foundation/brief.md` 与相关记录；`.agents/memory/AGENTS.md`、
  `.agents/memory/shared/AGENTS.md`、`development-writing` 改为 `shared`（不再要求论文写本地适配段，
  消掉下游诊断的三条 warning）；路径检查现在也扫技能自带的 `sources/**/*.md`，并拒绝任何指向
  `PAPER.md`、`DEV.md` 的引用——只读共享技能里那处合法的 `DEV.md`（指被采用项目的检查命令）走 allow 文件（#247）。

### Adoption states

以下状态通过 `make check`；`make release-check` 对尚未填写的论文在表中步骤失败，原因见 v0.4.2。模板中的占位内容不是投稿论文。

| State | `make release-check` fails on |
| --- | --- |
| fresh paper | `identity`, `leftovers`, `pages` |
| existing bibliography, no ledger | `identity`, `leftovers`, `pages`, `references` |
| existing bibliography, migrated ledger | `identity`, `leftovers`, `pages`, `references` |
| venue kit | `identity`, `leftovers`, `pages` |

### Upgrading a paper from v0.8.0

**Command only.** 没有必须手动完成的步骤，但有三件事值得顺手做：

1. 升级计划里 `Makefile` 现在显示为 “the project's own (upgrade: review)” 并打印本版差异；命令不再改写它。
   如果上一次升级已经给 `Makefile` 插入了重复的 `ifneq ($(wildcard …venv…))` 块（`RSI_light_paper` 是三份），
   删掉多余副本。
2. 升级后 `diagnose-environment.sh` 不应再报 `warn adaptation section missing`（那三个文件已改为 `shared`）；
   若还报，说明本地的 registry 仍是旧 scope，跑一次 `check-development.sh --write-indexes`。
3. 路径检查现在会扫技能自带的 `sources/**/*.md`：如果你的仓库里还有指向已退役根目录文档的引用，
   `check-development.sh` 或项目检查脚本会指出它；改为指向 `paper-foundation/brief.md`。

## Starting from this template

1. 用 GitHub 的 **Use this template** 创建论文仓库，公开之前建议选 **Private**；需要可复现的起点时，克隆一个发布标签。
2. 运行 `bash .agents/scripts/shared/init-branches.sh`：创建并推送 `dev`，把它设为默认分支。工作分支从 `dev` 开始，发布时合并到 `main`。
3. 每个 worktree 先运行 `bash .agents/scripts/shared/setup-worktree.sh`。
4. 把采用工作交给 agent（`template-adoption`）：删除 registry 标记 `scope: template` 的文件并记为 `omitted`，把 `template` 块改成论文仓库，把本文档换成论文自己的发布说明，重写 README。
5. 让 agent 填写留给论文的槽位：`page-budget-on-blind-build.md` 的 `PAGE_MARGIN`，`post-build-visual-inspection.md` 的 `MIN_FIGURE_TEXT` 与 `LAST_LINE_FILL`。
6. 把论文简报交给 agent（`paper-foundation`）：`brief.md` 中未决定的内容保持 `unresolved`。

模板升级：`bash .agents/scripts/shared/upgrade-template.sh --check <tag>` 输出计划，去掉 `--check` 应用；
标记 **Command only.** 且没有冲突的版本不需要其他操作。
