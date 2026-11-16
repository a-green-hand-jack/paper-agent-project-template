# 发布说明

本文件只描述当前发布；历史版本保留在各自的标签里（例如 `git show v0.7.1:RELEASE_NOTES.md`）。
基于本模板创建的论文维护自己的发布说明，不复制此历史。

## v0.11.0 — 2026-11-16

收下 #261–#264 四条下游反馈：两条写作偏好改为可填槽位，渲染页检查补三类版面失败并附共享测量命令，
悬空的技能名改正并由检查发现，过时的"标记 superseded"说法改为现行规则。

- **写作偏好改为槽位（#261）。** `experiments-argue-for-claims` 与 `writing-exemplar-archive` 改为
  `shared_with_adaptation`：前者保留"按主张组织、一节一证据一结论"，新增 `CLAIM_NAMING`
  （`named` 小节写明主张，默认；`implicit` 只陈述事实，主张留在引言）；后者保留"范文是写作模型、
  不是引文、学到的写成卡片"，新增 `EXEMPLAR_STORE`（默认被忽略的 `.project/artifacts/writing-exemplars/`；
  也可以是登记在 `policy.root_files` 里的 Git 路径），只是永不进 `paper/`。`paper-writing` 技能与
  `writing-reference-finder` 改为指向槽位。
- **渲染页检查补三类失败（#263）。** `post-build-visual-inspection` 第 3 条加入竖直空白被
  `\flushbottom` 拉伸、标题移栏留空、浮动体相邻或不在首次引用页，以及词距异常行；新槽位
  `MAX_WORD_SPACE`。新共享命令 `.agents/scripts/shared/paper-build/page_measure.py`（只用标准库与
  poppler）：`last-lines`、`word-spacing`、`column-gaps`、`section-height`，页范围默认从 blind 构建的
  `.aux` 读出（正文到 `PaperMainTextEnd`，附录从附录 A 起）。结果是待人眼确认的候选，不进 `make check`。
  浮动体页码与首次引用页的比对写进记录的 `Apply`。
- **悬空技能名（#262）。** 共享文本里的 `writing-router`、`figure-router`、`section-writing`、
  `paper-brief-ingest` 以及已删的图工具名改为现有的技能或 source。`check_development_paths.py`
  （`make check` 的 `paths` 步）新增一项：反引号里出现已退役的技能名（脚本内的清单加上本仓库
  `omitted:` 里的技能包名，减去仍存在的）时，模板仓库（registry 有 `template.upstream`）报错，论文仓库只警告。
- **过时的 superseded 说法（#264）。** `memory/project/AGENTS.md` 尾节、`decision-packet` 第 2–4 步与
  `venue-icml-2026` 的 Refresh 改为现行规则：被取代的记录连同注册表条目删除，后继在 `supersedes`
  里列旧 ID；尾节的起始记录列表注明由论文按实际改写。

### Adoption states

以下状态通过 `make check`；`make release-check` 对尚未填写的论文在表中步骤失败，原因见 v0.4.2。模板中的占位内容不是投稿论文。

| State | `make release-check` fails on |
| --- | --- |
| fresh paper | `identity`, `leftovers`, `pages` |
| existing bibliography, no ledger | `identity`, `leftovers`, `pages`, `references` |
| existing bibliography, migrated ledger | `identity`, `leftovers`, `pages`, `references` |
| venue kit | `identity`, `leftovers`, `pages` |

### Upgrading a paper from v0.10.2

1. 运行 `bash .agents/scripts/shared/upgrade-template.sh v0.11.0`。两条写作记录由 `shared` 变为
   `shared_with_adaptation`；本地未改过的记录整份替换。
2. 在三条记录末尾的 `## In this repository` 写下新槽位：`experiments-argue-for-claims` 的
   `CLAIM_NAMING`、`writing-exemplar-archive` 的 `EXEMPLAR_STORE`、`post-build-visual-inspection` 的
   `MAX_WORD_SPACE`。不写时取记录里的默认值（`named`、被忽略的 `.project/artifacts/writing-exemplars/`），
   但 `diagnose-environment.sh` 会对缺尾节的记录报警。已在项目技能里写"临时覆盖"的论文，把决定移进尾节后撤掉覆盖。
3. 运行 `make check`，看 `paths` 步的 `WARN`：论文自己的记录若还引用已退役的技能名，在本仓库的 Issue 里改掉。
4. 若本地有末行、词距、栏底空白或节长的测量脚本，改用 `page_measure.py` 后删除。
5. `memory/project/AGENTS.md` 尾节若仍写"marked superseded in the registry"，按模板新文字改写并保留本论文的起始记录列表。

## Starting from this template

1. 用 GitHub 的 **Use this template** 创建论文仓库，公开之前建议选 **Private**；需要可复现的起点时，克隆一个发布标签。
2. 运行 `bash .agents/scripts/shared/init-branches.sh`：创建并推送 `dev`，把它设为默认分支。工作分支从 `dev` 开始，发布时合并到 `main`。
3. 每个 worktree 先运行 `bash .agents/scripts/shared/setup-worktree.sh`。
4. 把采用工作交给 agent（`template-adoption`）：删除 registry 标记 `scope: template` 的文件并记为 `omitted`，把 `template` 块改成论文仓库，把本文档换成论文自己的发布说明，重写 README。
5. 让 agent 填写留给论文的槽位：`page-budget-on-blind-build.md` 的 `PAGE_MARGIN`，`post-build-visual-inspection.md` 的 `MIN_FIGURE_TEXT`、`LAST_LINE_FILL` 与 `MAX_WORD_SPACE`，`experiments-argue-for-claims.md` 的 `CLAIM_NAMING`，`writing-exemplar-archive.md` 的 `EXEMPLAR_STORE`。
6. 把论文简报交给 agent（`paper-foundation`）：`brief.md` 中未决定的内容保持 `unresolved`。

模板升级：`bash .agents/scripts/shared/upgrade-template.sh --check <tag>` 输出计划，去掉 `--check` 应用；
标记 **Command only.** 且没有冲突的版本不需要其他操作。
