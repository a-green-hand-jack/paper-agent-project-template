# 发布说明

本文件记录本模板自身的发布历史，每个版本使用一个 `## <tag>` 标题。
基于本模板创建的论文维护自己的发布说明，不复制此历史。

## v0.4.6 — 2026-11-04

本版本将跟随的 coding template 从 `v0.1.13` 升至 `v0.1.26`（#185 升至
`v0.1.19`、#187 升至 `v0.1.25`、#189 升至 `v0.1.26`），原样继承升级命令，
并将开发面迁移到 v0.1.26 的布局：六个类别各含 `shared/` 和 `project/` 分组，
schema 2 registry 是内容的唯一目录。本模板的 `template.version` 设为 `v0.4.6`（#191）。

### 变更

- `template.upstream.version` 为 `v0.1.26`，`template.version` 为 `v0.4.6`。
  跨越的十三个 coding template 版本（v0.1.14 至 v0.1.26）中，截至 v0.1.19（#185）
  新增升级命令及轻量路径（v0.1.14）、Issue 会话中“小规模真实运行即可”的规则和
  `actions/checkout@v5`（v0.1.15）、凭据清单（v0.1.16 和 v0.1.17）、
  `migrate-project.rules` 的通配符规则、`<LOCAL_CHECK>` 槽位和分阶段子 Issue
  （v0.1.18），以及 hook 审查、实现与交付门禁、`agent-communication` 和 Herdr
  收尾恢复（v0.1.19）。截至 v0.1.25（#187）还增加包含协调者和任务身份的交接、
  交付事件、通过明确暂停和归还保护验收输入、接收时对已覆盖结果和新职责的核对；
  可选且须明确声明的父集成分支（普通 Issue 仍以 `dev` 为目标）；以及
  `development-writing` skill、`release-doc-audit` 的发布类型指导、
  `agent-session-messaging` knowledge 记录和 `project-positioning-before-layout`
  memory 记录。Issue 和 PR 模板增加写作与验收建议，没有新增必填字段。v0.1.26
  （#189）是下述布局变更。
- `.agents/scripts/shared/upgrade-template.sh`（至 v0.4.5 的路径为
  `.agents/scripts/upgrade-template.sh`）与 coding template v0.1.26 逐字节相同，
  同目录的 `content_registry.py` 也是如此；旧的平铺路径不再存在。本模板自己的副本
  （#177、#182）及其差异已移除：克隆和合并提案位于
  `.project/state/template-upgrade/`（原为 `.project/build/template-upgrade/`）；
  仓库省略的 `optional: true` 路径继续省略，新增的可选路径留待人工决定；registry
  逐键合并，`entry_fields:` 取代顶层 `upgrade:`；未使用 `## In this repository`
  段落适配的 Markdown 文件采用三方合并，“Review”不再建议为其添加段落；标题使用
  “project”而非“paper”。
- 新增共享内容：`agent-communication` 和可选的 `credential-setup` skill、可选的
  `credential-inventory` knowledge 记录、`probe-credentials.sh`，以及 memory 记录
  `host-files-owned-by-running-user`、`look-at-the-artifact-before-concluding`、
  `provider-cost-routing`、`screen-with-scriptable-fakes` 和
  `speed-and-parallelism-by-measurement`。`issue-workflow`、`worktree-lifecycle`、
  `asset-lifecycle`、`llm-credentials`、三个 `issue-*` 记录和四个脚本的本地段落以上
  内容已替换。
- 本仓库的决定记录在各自的段落和 `rebuild-on-coding-template` 中：`<CI>` 保持
  `yes`，`<LOCAL_CHECK>` 为 `make check` 加工作流中的两个脚本步骤；不设置 `writing:`
  块；没有 `credentials.yaml`，因此 `probe-credentials.sh --check` 跳过；继续拒绝
  `serve-the-coding-agent`、`docker-objects-prefixed-and-removed`、
  `long-running-supervision` 和产品发布骨架。
- `template-adoption`：继承文本现已说明，从非 `main` 分支采用时，三项分支模型诊断
  发出警告；本模板原先称其为预期失败的段落已删除。`test_agent_content.py` 检查新行为。
- `test_upgrade_template.py` 和 `test_adoption_states.py` 跟随上游命令的措辞、状态
  目录及新增可选内容；升级中的论文手工采用可选内容，新建论文则已包含它们。
- v0.1.26 布局（#189）：继承脚本和本模板脚本均位于 `.agents/scripts/shared/`，
  Python 模块使用 snake_case：`check_paper_build.py`、`check_paper_interfaces.py`、
  `check_agent_content.py`、`check_reference_integrity.py`、`reference_evidence.py`、
  `check_bibtex_format.py`、`check_reference_metadata.py`、`check_reference_corrections.py`，
  以及辅助模块 `bib_identity.py`、`bounded_run.py`、`citation_occurrences.py`、
  `reference_env.py`、`validate_bibtex_correction.py` 和 `validate_bibtex_with_pybtex.py`；
  锁定依赖位于 `shared/reference-integrity/`。`setup-project.sh` 和
  `migrate-project.rules` 位于 `.agents/scripts/project/`。共享脚本测试位于
  `.agents/tests/shared/`，`test_adoption_states.py` 位于 `.agents/tests/project/`。
  `ENTRY_TEMPLATE.md` 改为 `entry-template.md`，`VENUE_TEMPLATE.md` 改为
  `.agents/knowledge/shared/venue-template.md`。`paper-brief-ingest` 脚本为
  `scripts/paper_brief.py`。每个类别及分组都有 `AGENTS.md` 和 `CLAUDE.md` 链接；
  `.agents/references/` 是已声明的根条目。
- schema 2 registry 管理每个单元的 ID、范围、所有者、摘要、状态、替代关系和刷新条件；
  memory 与 knowledge 的 front matter 只保留 `name`、`date`、`source` 和 `applies_to`。
  分组 `AGENTS.md` 使用由 registry 生成的索引（`check-development.sh --write-indexes`）
  代替手写列表，本模板自己的文字移至 `## In this repository` 段落。`make check` 也运行
  `check-development.sh` 和两个分组的测试（无测试的分组会跳过）；
  `check_agent_content.py` 从 registry 读取 skill 和记录登记。
- 随附 skill 和标准文件通过带理由的 `policy.naming_exceptions` 保留名称。
  `long-running-supervision`、`run-settings-from-config`、`USER.md` 和 `src/` 在此登记为
  拒绝采用。上游命令曾将本模板的 skill 包、记录和注释迁为占位项；registry 已人工修正，
  并在 `migrations` 记录每次迁移。

### Adoption states

与 v0.4.2 相同。以下各状态均通过 `make check`；`make release-check` 仅在所列步骤
失败，原因见 v0.4.2。

| State | `make release-check` fails on |
| --- | --- |
| fresh paper | `identity`, `leftovers`, `pages` |
| existing bibliography, no ledger | `identity`, `leftovers`, `pages`, `references` |
| existing bibliography, migrated ledger | `identity`, `leftovers`, `pages`, `references` |
| venue kit | `identity`, `leftovers`, `pages` |

### Upgrading a paper from v0.4.5

1. 按 `template-upgrade` 的“In this repository”说明运行一次本版本的完整命令目录
   （用 `git archive` 将 `.agents/scripts/shared` 放到
   `.project/state/template-upgrade/target-command/`；命令需要同目录的
   `content_registry.py`，不能只流式执行单个文件）：先加 `--check`，再不加该参数运行。
   命令将 registry 迁移到 schema 2，把脚本、测试和记录模板移至新路径，替换各 skill、
   记录和脚本中 `## In this repository` 之前的部分，并把 registry 字段从记录的 front
   matter 移出。后续运行的克隆位于 `.project/state/template-upgrade/`；旧的
   `.project/build/template-upgrade/` 可以删除。
2. 命令会拒绝 `.agents/memory/project/AGENTS.md`：因为“Start a paper”要求论文删除
   这里的模板索引行，而本版本将手写索引替换成生成索引。将论文在该文件添加的规则移至
   本版本文件尾部的 `## In this repository` 段落（通过
   `git -C .project/state/template-upgrade/paper-agent-project-template.git show v0.4.6:.agents/memory/project/AGENTS.md`
   取得），再以 `--resolved .agents/memory/project/AGENTS.md` 重跑。首次运行已将论文
   自己的 registry 索引写入各分组 `AGENTS.md`；此次重跑会把只在 `registry-index` 标记
   内与发布版不同的文件报告为冲突（继承自 coding-agent-project-template v0.1.26）。
   用 `diff` 核对，为每个此类文件添加 `--resolved <path>` 并再次运行，然后命令会设置
   `template.version`。运行 `make check`。
3. 更新论文自身对旧路径的调用（其 `Makefile` 增补、工作流、脚本、记录及
   `assets/README.md`；命令会列出这些文件供人工比较）：`.agents/scripts/<name>` 现为
   `.agents/scripts/shared/<name>`，Python 名称使用上述 snake_case；
   `.agents/tests/<test>` 现为 `.agents/tests/shared/<test>`。命令移入 `project/`
   分组的论文自有脚本或记录保留原内容；以真实摘要替换命令登记的占位摘要，并将非
   snake_case 的 Python 模块重命名或登记带理由的命名例外，直到 `check-development.sh` 通过。
4. 命令列出两个须人工处理的新可选项：`credential-setup` 和 `credential-inventory`。
   已采用 `llm-credentials` 的论文应使用命令输出的 `git show` 采用两者，因为前者的
   步骤和格式现由这两项提供；未采用 `llm-credentials` 的论文则省略两者。不调用 LLM
   provider 的论文无需为清单添加 `credentials.yaml`，此时 `probe-credentials.sh --check`
   会跳过。
5. 在论文自己的 `issue-workflow` 段落中，将 `<POST_MERGE_CHECK>` 改名为
   `<LOCAL_CHECK>`，无论 `<CI>` 的值为何都填入 `DEV.md` 检查命令；增加新槽位
   `<AGENT_KINDS>`、`<PROVIDER_ARGS>`、`<MODEL_SELECTION>`、`<EXCLUDED_MODELS>`、
   `<FALLBACK_AGENT>`、`<WORKSPACE_PREFIX>`、`<MERGE_METHOD>` 和 `<PRE_MERGE_GATE>`。
   对“Phased work”第 3 或第 4 步的补充移至第 4 或第 5 步；“在 dev checkout 解决
   冲突”的补充改到 PR 自己的 worktree。检查没有补充覆盖 hook 审查、实现和交付门禁、
   PR 就绪门禁或使用 Herdr 自身 reopen 和 remove 命令的 Close-out 恢复。`gh pr checks`
   合并门禁改为 `<LOCAL_CHECK>`，CI 只作说明。
6. 在 `llm-credentials` 段落中，将针对旧 Apply 步骤的补充改为针对 `credential-setup`
   同一步骤的补充（第 1 至第 5 步编号不变）。
7. 在 `template-adoption` 段落中，删除将三项分支模型诊断称为预期失败的段落；现在它们
   是警告。`release-doc-audit` 段落对第 3 步的补充可以删去新升级段检查已覆盖的内容。
   命令还会列出 `asset-lifecycle` 供核对，因为新文本有第二个编号列表；其第 2 步不变。
8. 如果 `migrate-project.rules` 中一行的 `NAME` 含 `*`、`?` 或 `[`，请阅读一次
   `migrate-assets.sh` 的文件头：此类 `NAME` 现在是通配符。

## v0.4.5 — 2026-10-21

让 `upgrade-template.sh` 能在真实论文中完成轻量升级：不再拒绝论文重写的 Human 文档或没有 `## In this repository` 段落的适配文件，也能在人工解决冲突后完成升级（#182）。

### 修复

- 由于 README 的“Start a paper”要求论文重写 `README.md` 和 `DEV.md`，命令曾在每篇论文中拒绝这两个文件，也拒绝不带适配段落的共享文件，如 `.agents/scripts/AGENTS.md`，即使发布版改动未触及本地文字。人工合并后仍被拒绝，命令不设置 `template.version`，因此 agent 需要手工编辑 registry。
  - 论文自有的 Human 文档：registry 条目可使用其 `upgrade:` 键下说明的 `upgrade: review`。`README.md`、`PAPER.md` 和 `DEV.md` 使用该字段；`RELEASE_NOTES.md` 保持 `scope: template` 并跳过。命令绝不修改这些文件，仅在“Review”中打印发布版差异，不作为冲突；审查项不阻塞轻量路径。
  - 不带段落的适配文件：以源标签为基础三方合并；不重叠的修改直接应用，仅重叠视为冲突。对 Markdown 文件，“Review”建议将本地文字移入段落，见 `template-upgrade` 第 5 步。
  - 已解决冲突：`--resolved <path>` 可重复使用，也可用于 registry；文件人工解决且无冲突标记后，命令接受该文件并设置 `template.version`。
- `test_upgrade_template.py` 检查拥有自有 README、DEV 和无段落适配 `AGENTS.md` 的论文夹具能无冲突升级并设置版本；真实重叠仍会被拒绝，使用 `--resolved` 后完成。从 v0.4.1 升级的采用状态测试现以重写过 README 的论文开始，保留论文自行编写的 `upgrade: review` 文档。

### Adoption states

与 v0.4.2 相同。以下各状态均通过 `make check`；`make release-check` 仅在所列步骤失败，原因见 v0.4.2。

| State | `make release-check` fails on |
| --- | --- |
| fresh paper | `identity`, `leftovers`, `pages` |
| existing bibliography, no ledger | `identity`, `leftovers`, `pages`, `references` |
| existing bibliography, migrated ledger | `identity`, `leftovers`, `pages`, `references` |
| venue kit | `identity`, `leftovers`, `pages` |

### Upgrading a paper from v0.4.4

**Command only.** 仅需命令即可完成从 v0.4.4 的升级，但必须使用本发布版的副本：v0.4.4 副本会拒绝论文自行添加内容的 `.agents/scripts/AGENTS.md`，因为本版本修改了该文件。按 `template-upgrade` 的“In this repository”运行一次本发布版副本：先用 `--check`，再不加该参数，最后运行 `make check`。“Review”列表可能建议为无段落适配的 `AGENTS.md` 添加 `## In this repository`；可留待后续 Issue。

## v0.4.4 — 2026-10-20

新增轻量升级路径：一个命令完成模板升级的机械部分，每个版本说明是否还有其他步骤（#177）。

### 新增

- `.agents/scripts/upgrade-template.sh [--check] <TARGET_TAG>` 将论文从 registry 中的 `template.version` 升级到目标标签，一次可跨越任意数量版本。命令将两个标签抓取到 `.project/build/template-upgrade/`（已有后可离线），并针对两者间变化的每个路径，依据目标版本 registry 执行 `template-upgrade` 第 5 步：
  - 跳过 `scope: template`，不改变项目自有路径；
  - 共享文件通过检查 1 后替换 `## In this repository` 之前的部分，若无该段落则整体替换；新增共享路径会被添加，已移除路径仅在本地未变时删除；
  - registry 逐项合并；无冲突时将 `template.version` 设置为目标版本；
  - 不触碰 `assets/`、`.project/` 和 `.env`。

  本地编辑视为冲突，绝不覆盖；命令用 `git merge-file` 报告三方合并提案并以 1 退出。输出包括已应用、跳过、拒绝和需人工处理的内容：槽位或对应步骤发生变化的段落，以及跨越的每个版本的升级段落。`--check` 输出相同计划但不修改文件。
- 轻量路径（`template-upgrade` 的“In this repository”）：跨越的所有版本都标记 **Command only.** 且 `--check` 未报告冲突或人工步骤时，升级由一个 Issue、一个 worktree、该命令、`make check` 和一个 PR 构成；否则从命令计划开始执行完整流程。
- 每个发布条目的 `### Upgrading a paper from <tag>` 以 **Command only.** 开头或列出剩余人工步骤。`release-doc-audit` 要求此格式，`test_adoption_states.py` 检查 v0.4.0 之后每个条目。它还用候选版本自身命令将 v0.4.1 新论文升级到候选版本：除论文自有文件外，结果与候选版本新论文相同，并通过 `make check`。
- `.agents/tests/test_upgrade_template.py` 对带三个标签的模板仓库夹具运行命令。CI 的 `check` 任务检出完整历史，确保包含 v0.4.1 标签。

### Adoption states

与 v0.4.2 相同。以下各状态均通过 `make check`；`make release-check` 仅在所列步骤失败，原因见 v0.4.2。

| State | `make release-check` fails on |
| --- | --- |
| fresh paper | `identity`, `leftovers`, `pages` |
| existing bibliography, no ledger | `identity`, `leftovers`, `pages`, `references` |
| existing bibliography, migrated ledger | `identity`, `leftovers`, `pages`, `references` |
| venue kit | `identity`, `leftovers`, `pages` |

### Upgrading a paper from v0.4.3

**Command only.** 命令在此版本首次加入，因此按 `template-upgrade` 的“In this repository”运行一次本发布版副本：先用 `--check`，再不加该参数，最后运行 `make check`。

## v0.4.3 — 2026-10-20

在线参考文献审计现在按继承的 `llm-credentials` 记录，从设备的共享凭据文件读取密钥（#176）。

### 修复

- 参考文献审计以前只从根目录 `.env` 读取密钥，遇到 `BIBTEX_CHECK_MAILTO`、`OPENALEX_API_KEY`、`S2_API_KEY` 以外的键就失败（`.env:<n> unsupported key`）。论文因此只能将密钥复制到项目 `.env`（`llm-credentials` 禁止），或将共享文件链接为 `.env`（又会因其他键失败）。`_reference_env.py` 现在也读取 `.project/credentials/.env`，即共享文件的链接（在 worktree 中通过 `.project/credentials` 链接访问）；仅导出上述三个键，其他键全部跳过，不导出也不打印。进程环境优先于根 `.env`，根 `.env` 优先于共享文件。根 `.env` 保持严格允许列表，仍可作为后备。`.env.example`、`DEV.md`（“Reference audits”）、`bibliographic-metadata-services` 和 `llm-credentials` 的本地段落均将共享文件列为首选路径。

### Adoption states

与 v0.4.2 相同。以下各状态均通过 `make check`；`make release-check` 仅在所列步骤失败，原因见 v0.4.2。

| State | `make release-check` fails on |
| --- | --- |
| fresh paper | `identity`, `leftovers`, `pages` |
| existing bibliography, no ledger | `identity`, `leftovers`, `pages`, `references` |
| existing bibliography, migrated ledger | `identity`, `leftovers`, `pages`, `references` |
| venue kit | `identity`, `leftovers`, `pages` |

### Upgrading a paper from v0.4.2

**Manual steps.** 使用 `template-upgrade` 获取此版本，然后：

1. 若设备有共享凭据文件，将规范 checkout 的 `.project/credentials/.env` 链接至该文件（论文尚无 `.project/credentials/` 时先创建目录）。不要复制文件或其中的值。
2. 在每个现有 worktree 重跑 `bash .agents/scripts/setup-worktree.sh`，使规范 checkout 创建 `.project/credentials/` 之前建立的 worktree 也获得 `.project/credentials` 链接。
3. 仅含这些键的根 `.env` 仍可使用，且优先于共享文件；密钥来自共享文件后删除它，避免过期副本遮蔽轮换后的密钥。

## v0.4.2 — 2026-10-20

修复下游论文采用 v0.4.1 后报告的问题（#173），并在每次发布前测试本模板记录的采用状态，以便今后首先在这里发现此类缺陷。

### 修复

- 有参考文献策略但没有 ledger 的论文未通过 `make check`，而 Draft 门禁接受这种状态（#169）：出厂状态参考文献测试读取了仓库自身的 `.agents/references/ledger.json`。现在测试自行创建空 v2 ledger、策略和标记。
- 新采用模板且未修改 ICML 2026 模板包时，`make release-check` 的 `identity` 步骤失败（#170）。原占位符 `Author Name` 匹配了模板包自己的文字（`icml2026.sty` 中的“author names”“author name”），因为该步骤按子串匹配 blind 构建读取的每行中每个 `\PaperIdentity` 字符串。现在使用合成占位符（`Template-Author-Name`、`template-author@example.invalid`、`Template-Institution`）；只要 `paper/authors.tex` 仍声明它，`identity` 就给出专门的失败信息。对 blind 读取的所有源文件进行子串搜索的逻辑不变，因此对真实姓名仍同样严格。
- 在线参考文献审计无法在其时限或 `references` 任务的 30 分钟内完成现实规模的书目（#171）。以下原因均在修复前确认：
  - **时限没有传递给检查器。** 它只结束 `uv`；`uv run` 启动的检查器继续运行，在审计返回后仍查询服务、写入报告和缓存。现在两个审计均在独立进程组运行工具，到时结束整个进程组，从而限制包括重试在内的完整运行。
  - **达到时限时没有报告。** `bibtex-check` 为每个条目流式输出一条记录，但审计此前将其丢弃。元数据运行达到时限后以 `incomplete`（退出码 2）结束，`run.json` 包含 `checked_keys` 和 `unfinished_keys`；已检查条目的确定问题仍以 `reference_problem` 失败。修正审计达到时限时以 `incomplete`（仍为建议）结束，不再记为 `provider_unavailable`。
  - **CI 缓存每次均为冷缓存。** 每次运行都再次查询所有条目。
  - **无密钥服务会让工具停滞。** OpenAlex 无密钥时每个地址每天约允许 100 次搜索，之后返回 429 和数小时的 `Retry-After`：`bibtex-check` 1.6.1 不设上限地等待，`bibtex-update` 对每个请求重试数分钟，使两个审计均达到时限。无密钥 Semantic Scholar 对大量请求返回 429，而工具只缓存 `200` 响应；即使暖缓存，100 条目的完整无密钥审计仍无法在 30 分钟内完成（实测约每条 18 秒）。

  根据维护者在 #171 的决定，在线审计拆为三个层级（`DEV.md`，“Reference audits”）：

  | 何时 | 运行内容 | 门禁 |
  | --- | --- | --- |
  | 每次 pull request 和 push（`references`） | 相对基础提交新增、变更或 ledger 指纹不再匹配的条目 | 必需；通常数秒 |
  | 合入 `main` 的 pull request、推送至 `main`、`make release-check` | 完整元数据审计（CI 还运行修正审计） | 必需 |
  | 每周及 `workflow_dispatch`（`references-full`） | 两项完整审计并行运行，保留缓存 | 报告；不阻塞合并 |

  - **Ledger 指纹。** `check-reference-metadata.py --record` 为每个验证通过的条目写入 `verification.bibtex_fingerprint`，对有确定问题的条目删除该字段。在变更层（`--scope changed --base <commit>`），未变且有指纹的条目不发起查询；无待审计内容时不启动工具。
  - **服务失败**（故障、限流、机器人验证）属于基础设施结果，会列出未完成的条目（`unfinished_keys`），不将其记为条目失败。
  - **缓存。** 每次 CI 运行都恢复并保存 `.project/build/reference-integrity/cache/` 中各审计的 HTTP 缓存，包括失败或超时的运行，重跑可继续。保存前审计会删除含 API key 的行；OpenAlex 通过 URL 参数接收该值。
  - **跳过无密钥的 OpenAlex。** 缺少 `OPENALEX_API_KEY` 时，审计打开工具自身的 OpenAlex 熔断器并记录 `skipped_services`。
  - **默认值。** 两项审计使用四个共享各服务速率限制的 worker（对 20 个公开条目，冷缓存用时 201 秒，单 worker 为 519 秒），时限为 3600 秒；CI 对变更层设 600 秒、发布路径设 1800 秒、每周任务设 5400 秒。

  未修改锁定的 `bibtex-updater` 1.6.1；其当时最新版本仍会不设上限地等待 429 的 `Retry-After`。

### 新增

- `.agents/tests/test_adoption_states.py`（#172）在临时目录中用发布文件构造以下每种采用状态，实际运行 `make check` 和 `make release-check`，将失败项与下表比较，并用 stub 检查器对 100 条目书目运行限时完整元数据审计及变更层审计。它属于本模板（`scope: template`）；`DEV.md` 的“Releases”和 `release-doc-audit` 要求发布前运行它。
- `.agents/tests/test_reference_tool_contract.py` 在锁定环境中检查审计写入的缓存格式和熔断状态。

### Adoption states

以下所有状态均通过 `make check`。`make release-check` 只在所列步骤失败；`identity` 失败仅因 `paper/authors.tex` 仍声明模板占位身份。服务验证每个条目时，完整元数据审计（`metadata`）通过；测试使用 stub 检查器。

| State | `make release-check` fails on |
| --- | --- |
| fresh paper | `identity`, `leftovers`, `pages` |
| existing bibliography, no ledger | `identity`, `leftovers`, `pages`, `references` |
| existing bibliography, migrated ledger | `identity`, `leftovers`, `pages`, `references` |
| venue kit | `identity`, `leftovers`, `pages` |

新论文指执行 README 的“Start a paper”第 4、5 步后的模板。已有书目状态加入被引用的 `paper/refs.bib`，无 ledger，或具有经 `reference-evidence.py migrate` 迁移的 v1 ledger；直到 ledger 以 Release 强度记录每条参考文献和每次引用，`references` 才会通过。venue kit 状态在 `paper/style/` 加入由 blind 构建加载的未修改模板包。论文声明作者后 `identity` 通过，模板的 `\PaperTODO` 文字消失后 `leftovers` 通过，设置 `PAGE_BUDGET` 后 `pages` 通过。

在线元数据审计中，冷缓存上的限时完整审计以 `incomplete` 结束并列出未完成条目，下次运行从保留的缓存继续；完整审计记录指纹后，未改变的 100 条目书目在变更层不产生查询。

### Upgrading a paper from v0.4.1

使用 `template-upgrade` 获取此版本，然后：

1. 如果 `paper/authors.tex` 仍保留 v0.4.1 占位身份（`Author Name`、`author@example.org`、`Example Institution`），声明论文的真实身份；该占位符会匹配某些 venue kit 的文字。
2. 完整采用 `.github/workflows/reference-validation.yml`：分层的 `references` 任务（现检出完整历史以与基础提交比较）、每周 `references-full` 任务、缓存步骤和契约测试。保留分支保护所需的任务名称；`references` 保持必需检查。
3. 记录一次指纹：在分支上运行 `python3 .agents/scripts/check-reference-metadata.py --record`（完整审计，需要 `uv` 和网络，`.env` 中的密钥有帮助），审查报告，并通过 PR 提交 `.agents/references/ledger.json`。在此之前，变更层仅审计 PR 新增或修改的条目。没有 ledger 的论文没有指纹；其变更层只与基础提交比较。
4. `make release-check` 现在运行完整元数据审计；在有 `uv` 和网络的环境中运行。
5. 审计缓存已迁至 `.project/build/reference-integrity/cache/`。旧的 `metadata-cache.db`、`corrections/http-cache.db` 和 `corrections/resolution-cache.json` 不再读取，可删除。如有条件，将 `OPENALEX_API_KEY` 和 `S2_API_KEY` 设为仓库 secret（`bibliographic-metadata-services`）；可信运行即可使用 OpenAlex 和经认证的 Semantic Scholar，pull request 运行仍不使用密钥。
6. 仅为使 `make check` 通过而初始化的 Draft 强度 ledger（#169）可保留或移除；`make check` 不再需要它。
7. 不要采用 `.agents/tests/test_adoption_states.py`，它属于 `scope: template`。若升级复制了它，请删除。

## v0.4.1 — 2026-10-20

修复下游论文采用 v0.4.0 后报告的参考文献工具和采用顺序问题（#166）。

### 修复

- `reference-evidence.py inventory` 曾从引用命令处而非句首记录 `claim_text`，导致记录及其指纹缺少论断（#159）。现在记录完整句子；引用前或后的部分超过 600 字符时在单词边界截断，并标记 `claim_text_truncated`。
- 被引句子变化时，`inventory` 为其创建新 occurrence，却让证据指向旧 occurrence，Draft 门禁因此拒绝（`points to unknown occurrence`）。现在证据会移动到相同位置、相同键的新 occurrence 并保留旧指纹，因此成为过期证据：Draft 发出警告，Release 失败，符合参考文献契约。
- 随模板提供的测试曾对仓库本身运行 Release 参考文献门禁，导致 ledger 仍为 Draft 强度的论文无法通过 `make check`（#160）。现在测试在临时目录中测试出厂状态，`make check` 再次成为 Draft 门禁。
- 从 `main` 采用且尚未建立 `dev` 时，`diagnose-environment.sh` 无法通过（#161）。v0.4.0 发布说明（第 8、10 步）和 `template-adoption` 现指出在维护者合并后运行 `init-branches.sh` 之前预期失败的三行分支模型诊断。继承脚本未变；脚本问题已向上游报告。
- `reference-evidence.py migrate` 写出的证据被 Draft 门禁拒绝（`source_identity lacks a stable identifier or source_hash`）（#162）。现在它和 `record` 一样，将参考文献标识符及 `source_hash` 复制进 `source_identity`。
- 有策略而无 ledger 的仓库能通过 Draft 门禁，但 `references` CI 任务失败（#163）。其 `status` 和 `inventory` 步骤现在只在 `.agents/references/ledger.json` 存在时运行。
- 标题规范化把 LaTeX 重音（`Caf{\'e}`）当成措辞变化，使修正审计与 Unicode 候选标题比较时失败（#164）。现在 NFKC 之前使用锁定的 `bibtex-updater` 自带解码器将重音解码为 Unicode。
- 在线元数据审计无法验证一条 COLM 引文（#165）：
  - DBLP `202` 机器人验证页现在是基础设施结果（`bot_challenged_services`；`unverified` 运行转为 `provider_unavailable`），而非“无匹配”；
  - 当检查器匹配到 OpenReview 记录、仅年份或 venue 名称不同，且 ledger 将该参考文献记录为来自 `openreview` 的 `verified` 和 `agent-resolved` 或 `human-confirmed` 时，现在报告而不判失败（`ledger_reviewed_openreview_keys`）。

  锁定的 `bibtex-updater` 1.6.1 未打补丁。其后续版本已映射 `COLM`（1.11.0）并把 DBLP 的 202 报为未完成查询（1.12.0）；从 `venueid` 读取 OpenReview 记录年份的问题已报告上游（[rpatrik96/bibtexupdater#82](https://github.com/rpatrik96/bibtexupdater/issues/82)）。

### Upgrading a paper from v0.4.0

使用 `template-upgrade` 获取此版本，然后：

1. 运行 `python3 .agents/scripts/reference-evidence.py inventory`。每次引用的论断指纹和 occurrence id 均会改变（#159）；运行前，Draft 门禁因 ledger 中缺少 occurrence 而失败。运行后每个 occurrence 均为 `pending`，其证据过期（Draft 警告，Release 失败）。使用 `packet` 和 `record`（`citation-support-review` skill）重新记录支持证据，并在 `make release-check` 前请 Human 再次确认。
2. 已用 v0.4.0 迁移 v1 ledger 并人工修复 `source_identity` 的论文继续正常工作。由于 v2 新增 occurrence 级审查，`migrate` 写出的每个 occurrence 最初均为 `pending`，在 `make release-check` 前需 Human 重新确认（#162）。
3. 删除针对 #160（跳过 Release 子测试）或 #163（仅为使 `references` 任务通过而初始化 ledger）的本地变通方案。
4. 对审计无法验证的 COLM 或其他仅有 OpenReview 的引文，在 ledger 中将其身份记录为 `verified`，在来源中列出 `openreview`，提供 `openreview` 标识符和 `agent-resolved`（或由 Human 填写的 `human-confirmed`）。

## v0.4.0 — 2026-10-20

这是一个破坏性发布。本模板基于 [`coding-agent-project-template`](https://github.com/a-green-hand-jack/coding-agent-project-template) `v0.1.13` 重建并更名为 `paper-agent-project-template`（#156）。现在像开发代码一样开发论文：自包含的 `paper/` 产品树、从 `dev` 发起的 Issue 和 PR、作为测试套件的构建、`main` 上带标签的发布，以及每个报告数字的来源记录。`.agents/memory/project/rebuild-on-coding-template.md` 记录了每个旧路径、工具、测试、skill 和决定的新位置。

### 变更

- **继承。** 模板原样采用 coding template 的脚本、共享 skill（`issue-workflow`、`worktree-lifecycle`、`template-adoption`、`template-upgrade`、`template-feedback`、`release-doc-audit`、`asset-lifecycle`、`cli-first-operations`、`project-memory-governance`）和共享 memory 记录；适配只写在尾部的 `## In this repository` 段落。registry 在 `template` 中记录本模板，在 `template.upstream` 中记录 coding template。
- **分支。** `dev` 是默认分支和集成分支，`main` 是发布分支。`template-dev` 已退役，其最后提交保留为 `archive/template-dev` 标签。
- **产品面。** `paper/` 包含 `main.tex`、`submission.tex`、`blind.tex`、`authors.tex`、`macros.tex`、`refs.bib`、`sections/`、`figures/`、`tables/`、`algorithms/`、`style/` 和 `Makefile`，构建不依赖 `paper/` 外的文件。一份源文件按固定顺序生成三个构建，每一步移除一层：`main`（具名、含注释）、`submission`（移除注释）和 `blind`（再移除身份及致谢）。
- **构建。** 根目录 `Makefile` 提供 `pdf`、`blind`、`submission`、`check`、`release-check` 和 `clean`。TeX 从 `PATH` 或 `TEXBIN` 获取，所有输出写入 worktree 的 `.project/build/`。
  - 未定义的引用或引文、缺失文件、重复定义的标签、PDF 文本中丢失的下划线、参考文献 ledger 错误、接口宏错误、无效的 skill 或记录结构、测试失败都会使 `make check` 失败；它还报告 `blind` 正文页数与 `PAGE_BUDGET` 的比较。
  - 匿名 PDF、其元数据或源文件中出现作者身份，`submission` 中留下注释或 TODO，页数预算缺失或超限，或参考文献低于发布强度，都会使 `make release-check` 失败。
- **Human 面。** 根目录包含 `README.md`、`PAPER.md`、`DEV.md`、`RELEASE_NOTES.md` 和 `AGENTS.md`，`CLAUDE.md` 是后者的符号链接。`EXPERIMENTS.md`、`PAPER_INTERFACES.md`、`PUBLICATION.md`、`BRIEF.md`、`DECISIONS.md` 成为 `.agents/memory/` 下的分类记录；`REFERENCES.md` 和 `LATEX_TEMPLATES.md` 成为 memory 和 knowledge 记录。
- **证据。** `assets/MANIFEST.yaml` 为每个结果表、图数据文件和报告数字登记源仓库、提交、运行、校验和及再生成命令。数字只能通过接口宏进入正文；每个宏在 `paper/macros.tex` 中有 `% Interface:` 标记，并在 `.agents/memory/project/paper-interfaces.md` 有条目。
- **Overleaf。** `.agents/scripts/overleaf-sync.sh` 提供 `status`、`push` 和 `pull`。`push` 将 `HEAD:paper` 快进到 Overleaf 分支顶端；`pull` 将 Overleaf 修改带到 `sync/overleaf-<commit>` 分支以创建 PR。两者均检查树相等，仓库根目录绝不会发送到 Overleaf。远端来自本地 Git 配置，凭据留在 Git 凭据通道。
- **发布。** 一个发布包括从 `dev` 到 `main` 的 PR、如 `submit-<venue>-<yyyy>`、`arxiv-v1` 或 `camera-ready` 的标签，以及论文自身 `RELEASE_NOTES.md` 的条目。
- **CI。** `template-check`（继承：`structure`）、`paper-check`（`check`、`paper-only`）和 `reference-validation`（`references`）。`main` 上的必需检查变为 `structure`、`check`、`paper-only` 和 `references`。
- **Skills。** 所有 skill 位于 `.agents/skills/shared/`。从下游论文归纳并泛化的有 `writing-router`、`writing-reference-finder`、`openreview-review-collector`、`figure-router`、`scientific-figure-workflow` 和 `poster-build`。固定在指定提交并随附许可证及含哈希的 `PROVENANCE.md` 的有 `scientific-writing`、`scientific-english-editor`、`better-usage`、`academic-voice`、`proofread`、`lieflat-less-ai-tone`、`scipilot-figure-skill`、`icarus-figures`、`thesis-figure-skill`、`tikz-figure-code` 和 `image-to-editable-ppt`（最后一项已打补丁，确保不读取其他工具的登录）。
- **记录。** 新的共享 memory 记录保存下游论文共有经验：一份源文件生成三个构建、Overleaf 只接收论文树、编辑前同步 Overleaf、构建后目视检查、有效的 skill front matter、对 blind 构建执行页数预算、官方 venue kit 保持原样、从 `TEXBIN` 获取 TeX、通过接口宏传递结果，以及参考文献完整性。新的共享 knowledge 记录保存 ICLR 2027、ICML 2026、NeurIPS 2026 海报、官方 LaTeX 模板包和书目元数据服务的有日期事实，各自带有刷新条件。
- **仓库。** 仓库描述为“Paper template built on coding-agent-project-template: develop a paper like code”。

### 修复

- `paper-brief.py ingest` 曾将多行列表项拆为多个列表项，包括 `PAPER.md` 的 locked 段落（#154）；现在保留每个列表项的续行。
- `reference-evidence.py inventory --location` 曾删除所有其他位置的 occurrence 记录；现在保留。
- `reference-evidence.py record --origin` 曾静默将未知来源记录为 `agent-pdf`；现在拒绝未知来源。
- `check-reference-integrity.py` 现在验证 `.agents/references/policy.json` 中的 `bibliography_origin`。
- 八个 `SKILL.md` 文件（七个 `ccf-*` 包装器和 `writing-dna-skill`）的 front matter 无法解析。它们已退役，`make check` 现在解析每个 `SKILL.md`。
- reference-validation 工作流不再回退到个人邮箱，而读取仓库变量 `BIBTEX_CHECK_MAILTO`。
- 已移除指向本模板自身 Overleaf 项目的受跟踪配置。

### 退役

`template-sync`、`paper-init.py`、`template-inheritance.json`、`template-sync.json`、旧 `template-adoption` 工具和 skill、`paper/variants/`、`paper/generated/`、构建配置（`paper-build.json`、`external-latex`）、发布实例与记录（`release.py`、`releases/`、`build-release.yml`）、文档一致性检查器、`verify.sh` 和旧布局检查、CCFA-Skills 套件及带包装器的 writing-dna-skill，以及根目录文档 `AGENT_GUIDE.md`、`ANATOMY.md`、`CONTRIBUTING.md`、`WHY_THIS_TEMPLATE.md`、`LATEX_TEMPLATES.md` 和 `REFERENCES.md`。#155（被 canonical variant 夹具阻塞的 `external-latex` 采用）随之过时。

### 从 `template-sync` 迁移论文

`template-sync` 无法将论文跨越此版本迁移，因为本版本改变了它自身依赖的布局。请按采用流程迁移一次，后续每次升级使用 `template-upgrade`。

1. **创建 Issue。** 在论文仓库创建 Issue，并像其他较大变更一样在独立 worktree 的分支中迁移。`.agents/template-sync.json` 记录论文上次审查的模板提交；其下游本地路径属于论文自己添加的内容，迁移时必须保留。
2. **阅读发布版。** 不改变当前 checkout，例如在 worktree 的 `.project/` 中运行 `git clone --branch v0.4.0 --depth 1 https://github.com/a-green-hand-jack/paper-agent-project-template.git`。遵循其 `template-adoption` skill，在改动之前写出迁移映射。发布版中的 `.agents/memory/project/rebuild-on-coding-template.md` 说明每个旧路径的去向。
3. **采用开发面。** 从发布版获取 `AGENTS.md` 和 `CLAUDE.md` 符号链接、`.agents/`（脚本、skill、记录、测试、registry）、`.github/`、根 `Makefile`、`assets/`、`.env.example` 和 `.gitignore` 规则。然后按 `README.md` 的“Start a paper”第 4、5 步删除仅属于模板的内容，并填写留给论文的槽位。保留 `template.repository`，设置 `template.version: v0.4.0`，不设置 `upstream` 块。
4. **将论文移入新的 `paper/` 布局：**
   - 保留 `sections/`、`figures/`、`tables/`、`refs.bib`、`macros.tex` 和 `style/`，以发布版的 `main.tex`、`submission.tex`、`blind.tex`、`authors.tex` 和 `Makefile` 为框架。
   - 将变体映射到三个构建：`draft` 对应 `main`，`camera-ready` 和 `arxiv` 对应 `submission`，`anonymous` 对应 `blind`。
   - 将作者块放入 `paper/authors.tex`，匿名构建不得包含的每个姓名、邮箱、机构或 URL 分别用一个 `\PaperIdentity{...}`。
   - 作者注释写为 `\PaperNote{...}`。致谢保留在 `main.tex` 中 `blind` 不包含的部分。
   - 超出移除一层范围的变体差异（如 camera-ready 样式选项）由 Human 决定；记录在 `.agents/memory/project/publication.md`。
   - 将 `paper/venue_preamble.tex` 移至 `main.tex`。将 `paper/generated/` 中每个数字移入 `macros.tex` 的接口宏，并在 `assets/MANIFEST.yaml` 中登记。
   - 在每个接口宏上方添加 `% Interface: <Name>` 标记。
5. **将根目录契约迁入记录：**
   - `EXPERIMENTS.md` 改为 `.agents/memory/project/experiments.md`。
   - `PAPER_INTERFACES.md` 改为 `paper-interfaces.md`。
   - `PUBLICATION.md` 改为 `publication.md`，其参考文献策略块改为 `.agents/references/policy.json`。
   - `BRIEF.md` 改为 `brief.md`，`DECISIONS.md` 的每个活动条目各自成为一条项目记录。
   - 保留 `PAPER.md`，替换其中对变体的提及。
   - 将 `references/ledger.json` 移至 `.agents/references/ledger.json`，并将 `paper/refs.bib` 顶部的标记行改为该路径。
6. **删除本版本退役的内容：**
   - `.agents/` 下的 `template-sync.json`、`template-inheritance.json`、`paper-build.json`、`documentation-consistency.json`、`init-state.json`、`template-origin.json`、`ANATOMY.md`、`runtime/`、`tools/`、`dependencies/` 和 `vendor/`，以及 `ccf-*` 和 `writing-dna-skill` 包装器；
   - `releases/`；
   - 根目录的 `AGENT_GUIDE.md`、`ANATOMY.md`、`CONTRIBUTING.md`、`LATEX_TEMPLATES.md`、`REFERENCES.md` 和 `WHY_THIS_TEMPLATE.md`；
   - `.github/workflows/pr-validation.yml` 和 `build-release.yml`。

   删除 `.agents/overleaf-sync.json` 前，将其项目 URL 添加为不含 token 的本地远端：`git remote add overleaf https://git.overleaf.com/<project-id>`。
7. **保留发布历史。** `releases/records/` 中每条记录在论文自身 `RELEASE_NOTES.md` 中成为一个 `## <tag>` 条目；已知发布提交时为其打标签。
8. **验证。** 运行 `bash .agents/scripts/setup-worktree.sh`、`bash .agents/scripts/diagnose-environment.sh`、`make pdf`、`make blind`、`make submission` 和 `make check`，之后确认 `git status --short` 为空。第 10 步创建 `dev` 前，`diagnose-environment.sh` 在且仅在三行分支模型诊断上以 1 退出：`FAIL local dev branch`、`FAIL origin/dev branch` 和 `FAIL GitHub default branch: main`（未认证 `gh` 时为 `skip`）。这是预期行为；其他各行必须通过。按页数和 `pdftotext` 文本将 `blind`、`submission` 与之前的 anonymous 和 camera-ready PDF 比较：迁移改变论文构建方式，不改变论文内容。
9. **Overleaf。** `bash .agents/scripts/overleaf-sync.sh status` 报告 `overleaf-behind`（Overleaf 持有较早的 `paper/` 状态）或 `in-sync`；若报告 Overleaf 修改，先执行 `pull`。PR 合并进 `dev` 后执行 `push`。
10. **GitHub。** 合并后，维护者将 `dev` 设为默认分支（若尚未设置，运行 `bash .agents/scripts/init-branches.sh`），并将 `main` 的必需检查调整为 `structure`、`check`、`paper-only` 和 `references`。此后 `diagnose-environment.sh` 的三行分支模型诊断也会通过。

## 更早的版本

v0.4.0 之前模板名为 `agent-writing-harness`（v0.3.x），更早之前名为 `ccfa-writing-paper-template`。各标签的 GitHub release 或提交中有详细信息。

- **v0.3.1 — 2026-09-02**：可在 Draft 强度下离线引用提供的只读书目（#153）。
- **v0.3.0 — 2026-08-28**：仓库更名为 `agent-writing-harness`（#151）。
- **v0.2.1 — 2026-08-25**：隔离模板仓库测试夹具。
- **v0.2.0 — 2026-08-24**：模板开发面迁至 `template-dev`，并打包 CCFA-Skills 套件与 writing-dna-skill。
- **v0.1.0 — 2026-08-09**：加强模板生命周期验证（#91）。
- **v0.0.5 — 2026-07-17**：第一个带标签的发布，包含显示宏、带编号的文件名、扁平化 arXiv 导出、Overleaf 发布和 venue kit 验证门禁。
