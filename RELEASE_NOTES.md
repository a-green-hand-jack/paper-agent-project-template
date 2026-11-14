# 发布说明

本文件只描述当前发布；历史版本保留在各自的标签里（例如 `git show v0.7.0:RELEASE_NOTES.md`）。
基于本模板创建的论文维护自己的发布说明，不复制此历史。

## v0.7.1 — 2026-11-14

跟随 coding template v0.1.37 → v0.1.38。上一版已经把起步步骤搬进本文件的
`## Starting from this template`；本版接过上游对其余问题的修正，`paper/`、三种构建
与 Overleaf 投影不变。

- **凭据的说法不再是空头承诺。** 上游把"项目在根目录登记 `credentials.yaml`"改成"采用后由
  `llm-credentials` 建立"；本模板的 `AGENTS.md` 同步，并写明模板自身不调用 LLM、没有这个文件。
- **README 的归属写对。** 上游 registry 把 `README.md` 从 `scope: project` 改成
  `shared_with_adaptation` + `upgrade: review`：升级命令不改写已采用项目的 README，只在计划里
  打印本版差异。本仓的 README 已是论文形状，按 review 处理即可。
- **继承状态。** 继承脚本与 v0.1.38 逐字节一致；`check_agent_content.py` 与 `tool-env.sh` 是本地适配。

### Adoption states

以下状态通过 `make check`；`make release-check` 对尚未填写的论文在表中步骤失败，原因见 v0.4.2。模板中的占位内容不是投稿论文。

| State | `make release-check` fails on |
| --- | --- |
| fresh paper | `identity`, `leftovers`, `pages` |
| existing bibliography, no ledger | `identity`, `leftovers`, `pages`, `references` |
| existing bibliography, migrated ledger | `identity`, `leftovers`, `pages`, `references` |
| venue kit | `identity`, `leftovers`, `pages` |

### Upgrading a paper from v0.7.0

1. 运行 `bash .agents/scripts/shared/upgrade-template.sh v0.7.1`（本版为 **Command only.**）。
2. 若论文仓库的 `AGENTS.md` 仍写着"项目在根目录登记 `credentials.yaml`"，改成"采用后由 `llm-credentials` 建立"；这是上游唯一的正文改动。
3. 运行 `bash .agents/scripts/shared/check-development.sh --write-indexes`，再运行 `make check`。

## Starting from this template

1. 用 GitHub 的 **Use this template** 创建论文仓库，公开之前建议选 **Private**；需要可复现的起点时，克隆一个发布标签。
2. 运行 `bash .agents/scripts/shared/init-branches.sh`：创建并推送 `dev`，把它设为默认分支。工作分支从 `dev` 开始，发布时合并到 `main`。
3. 每个 worktree 先运行 `bash .agents/scripts/shared/setup-worktree.sh`。
4. 把采用工作交给 agent（`template-adoption`）：删除 registry 标记 `scope: template` 的文件并记为 `omitted`，把 `template` 块改成论文仓库，把本文档换成论文自己的发布说明，重写 README。
5. 让 agent 填写留给论文的槽位：`page-budget-on-blind-build.md` 的 `PAGE_MARGIN`，`post-build-visual-inspection.md` 的 `MIN_FIGURE_TEXT` 与 `LAST_LINE_FILL`。
6. 把论文简报交给 agent（`paper-foundation`）：`brief.md` 中未决定的内容保持 `unresolved`。

模板升级：`bash .agents/scripts/shared/upgrade-template.sh --check <tag>` 输出计划，去掉 `--check` 应用；
标记 **Command only.** 且没有冲突的版本不需要其他操作。
