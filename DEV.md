# 论文开发

## 边界

`paper/` 是产品面，`.agents/` 是 Agent 开发面，根目录文档（`README.md`、`PAPER.md`、本文件、`RELEASE_NOTES.md`）是 Human 面。每个主题只在一个权威位置详述，其他位置链接到它。运行状态、日志、截图和构建输出放在当前 worktree 的 `.project/`，不得放入跟踪文件或未知的全局目录。

`paper/` 是自包含的：单独复制即可构建，不读取 `.agents/`；构建写入 `.project/build/`（单独复制 `paper/` 时写入其 `build/`），不写回 `paper/` 或根目录。

## Issue、分支与 PR

默认直接在现有 `dev` checkout 工作，先检查并保留无关改动和运行中的任务。按任务风险及 Human 要求决定是否需要 Issue、审阅和 PR；运行适用检查并报告证据。提交和推送仍需明确授权。

Issue 分支从其声明的目标（默认为 `dev`）开始，命名为 `fix/issue-<N>-<slug>`、`feat/issue-<N>-<slug>`、`docs/issue-<N>-<slug>` 或 `chore/issue-<N>-<slug>`。简单 Issue 通过 PR 返回 `dev`。父任务需要联合验收时，`issue-workflow` 记录父集成分支、子 PR 目标和最终到 `dev` 的 PR；合并子任务不结束父任务的验收职责。`main` 只保存发布状态。Overleaf 编辑通过 `overleaf-sync.sh pull` 创建的 `sync/overleaf-<commit>` 分支进入仓库。

PR 描述说明修改内容和原因，列出验收及 CI 要求的每项检查命令与结果，以及过程中修复的相关缺陷。只有维护者能完成的步骤应写成具体阻塞，说明维护者需要做什么。构建和发布证据放在 Issue 或 PR 中；Agent 自己的摘要不能代替它。

需要派遣 Herdr worktree 时，事先询问 Human 是否派遣，并确认本次 coding agent、具体模型和 thinking level；不得自动选择或静默 fallback。经确认后使用 Herdr 原生命令创建，新会话首先运行 setup。交接提示包含 Issue 链接、分支、阅读范围和验收要求：

```bash
bash .agents/scripts/shared/new-agent-prompt.sh 123 feat/issue-123-example dev \
  .project/state/coordinator-handoff.md
```

需要经授权的隔离工作而 Herdr 不可用时报告阻塞，不以原始 Git 创建替代 worktree。`issue-workflow` 技能涵盖开始、合并与收尾。

Issue、PR、评论和提交使用 [`development-writing`](.agents/skills/shared/development-writing/SKILL.md)：解释具体变更，使当前描述与最终范围一致，并说明证据对应的版本和条件。既有 Issue 字段和 PR 小节仍是入口；建议性提示不增加新的必填字段。registry 没有 `writing:` 声明，因此每个文件保持自身语言。发布叙事使用 `release-doc-audit` 并保留本模板自身的发布历史。

## 会话身份与交付

遵循 `issue-workflow` 处理调用者身份和派发。控制 Herdr 前，将工具进程允许的 Herdr 变量和原生线程与实时 workspace、pane、Agent 和 Git 公共目录/worktree 身份匹配。新的 Codex 派发应先检查已安装 CLI 支持 `--no-daemon`，再隔离启动；随后由 worker 独立验证身份并明确确认范围。上下文缺失或过期时只能进行已授权的只读诊断，不得猜测 ID 或修改共享服务。每次派遣前确认 agent、具体模型和 thinking level，并在 Dispatch 中记录实际选择及启动模式。

将任务键、角色、尝试次数和实际返回的 ID，与领取任务的协调者地址、允许的联系人/事件及恢复职责一起放入 `.project/state/` 的本地交接文件。将该文件作为上面命令的第四个参数；私人地址不得写入 Issue、PR 或跟踪内容。[`agent-communication`](.agents/skills/shared/agent-communication/SKILL.md) 负责传输预检及区分已提交、已确认和已完成状态。原生队列的实际可达性应与启动或提交成功分开检查。发送前检查目标的实时状态和输入；目标阻塞或存在实际草稿时停止发送。

Worker 应及时向获授权的协调者报告失败、阻塞和职责转移。在同一检查点和版本上汇总实现/验收、PR 创建和确切 head 证据；日常进度留在本地。纯 ACK 结束其回执链。未确认事件保留负责人、恢复指针和有界下一步，不要重复轮询或发送心跳。这些事件不授予提交、合并或发布权限。

每个活动检查点先读取当前摘要和回执，再在查询、回复或派发前分类收到的事件。将重复事件、已覆盖的早期里程碑及没有新职责的终态事件归入本地记录，不重复检查或报告完成。head 匹配不代表覆盖了新失败：变化的风险和未完成职责应各保留一次，并附证据、负责人和下一步。真正的新用户指令仍有其效力；事件中引用的旧授权不构成新的批准。这是会话工作流，而不是队列过滤器或后台消费者。

## 验收期间的写入责任

在检查读取共享 checkout 之前，在 `.project/state/` 中记录确切输入、验收负责人、所有写入者、受保护路径及允许的日志/产物输出。未提交工作须保存 diff/内容身份；仅有 HEAD 不足以识别它。所有写入者明确暂停修改这些输入，验收负责人确认固定版本后再检查。在此期间负责人和写入者均不得编辑受保护输入。本论文使用的现有命令是 `make check`、诊断和状态检查；构建/检查输出保留在 `.project/`。单独的不可变快照则记录其来源和隔离方式，不必冻结 checkout。

检查退出后，验收负责人记录结果并明确交还写入责任；接收方确认接回后才能编辑、提交或切换分支。新请求、漂移、重启或时间流逝都不会解除暂停。发生变更须先结束或使旧验收失效，停止或隔离其检查，再转移责任并重新检查。实时交接回执应与重复事件、过期输入和传输失败的场景评审分开；两者互不证明。

## Worktree 生命周期

每个 worktree 是具有独立状态的工作单元。创建后在其中运行：

```bash
bash .agents/scripts/shared/setup-worktree.sh
```

Setup 写入 `.project/home` 和 `.project/worktree.env`，创建本地状态目录，检查工具和资产清单，并运行 `.agents/scripts/project/setup-project.sh`，后者创建 `.project/build/` 并报告 TeX 工具。不要复用其他 worktree 的 `.project/`。

PR 合并后不要直接删除目录。先核对后台验收、审计和承诺的后续事项。职责未完成时保留 worktree，或在既有授权下明确转移并取得接任者确认。在 `.project/state/` 将当前或终态摘要与回执放在一起：确切版本、已覆盖事件和证据、剩余职责/负责人、风险、待收回执、用户报告状态和恢复位置。检查和所属进程退出后，协调者迁移并验证状态、记录恢复目的地，然后才进行受管移除。仅凭合并或空闲状态不能证明这些职责已完成。

然后运行：

```bash
bash .agents/scripts/shared/teardown-worktree.sh --migrate-to <canonical checkout>
```

该命令检查被忽略的状态、复制应保留的内容并写入迁移记录；它不会删除 worktree。`.agents/scripts/project/migrate-project.rules` 规定丢弃可由 `make` 重建的 `.project/build/`。只有资产迁移完成且其中不再有唯一副本后，才使用 worktree 管理器销毁 worktree 和分支。

## 构建与检查

根目录 `Makefile` 是唯一构建入口；`README.md` 列出其目标。两个变量可调整构建：

- `TEXBIN=<TeX Live bin directory>` 将该目录放到 `PATH` 最前，以应对其他 `latexmk` 排在前面的机器。不要将机器路径写入跟踪文件。
- `PAGE_BUDGET=<pages>` 是投稿场所的正文页数上限，在 `blind` 上计算至 `\label{PaperMainTextEnd}`。确定投稿场所后在 `Makefile` 中设置；`PAGE_BUDGET=none` 表示发布没有页数限制，例如 arXiv 版本。`make check` 报告页数，`make release-check` 在没有预算或超出预算时失败。

`make check` 按顺序执行：`main` 和 `blind` 构建及其日志检查（未定义的引用或引文、缺失文件、重复定义的标签）、`blind` 页数、PDF 文本层下划线保留检查（T1 编码）、离线参考文献门槛、接口宏检查、开发 registry 检查（`check-development.sh`）、技能/记忆/知识结构检查，以及 `.agents/tests/shared/` 和 `.agents/tests/project/` 的单元测试。构建日志位于 `.project/build/logs/<build>.log`。

通过 `make check` 不代表页面视觉效果正确。宣布构建完成前，应渲染并查看受影响页面（[`post-build-visual-inspection`](.agents/memory/shared/paper-build/post-build-visual-inspection.md)）；渲染结果和截图放入 `.project/build/inspect/`。

依赖：

- 带 `latexmk`、`pdflatex`、`bibtex` 及论文和投稿套件所需宏包的 TeX Live；
- 用于 PDF 检查的 `pdftotext` 和 `pdfinfo`（poppler-utils）；
- 用于脚本的 Python 3、PyYAML 和 markdown-it-py。`setup-project.sh` 在 `uv` 可用时创建 `.project/venv` 并把这两项依赖装进去，根 `Makefile`、`paper-check.sh` 和 `release-check.sh` 在 venv 存在时优先使用它；设置 `AGENTS_PYTHON` 为解释器路径即完全改用它。开发面检查以隔离模式运行（忽略用户级 site-packages 和 `PYTHONPATH`），因此没有 venv 也没有 `AGENTS_PYTHON` 时，`PATH` 上的 `python3` 必须能导入这两项依赖，否则 `make check` 失败；`diagnose-environment.sh` 会检查并输出 `FAIL`；
- 可选的 `uv`，供使用 `.agents/scripts/shared/paper-references/reference-integrity/` 中锁定依赖的在线参考文献审计使用。

`bash .agents/scripts/shared/setup-worktree.sh` 会报告缺失项。

论文没有 Python 包、容器或安装器，因此本模板没有 `pyproject.toml`、`Dockerfile`、`.dockerignore` 或 `install.sh`，`diagnose-environment.sh` 会将其报告为缺失的可选文件。不要为论文添加它们。需要独立环境的工具将环境安装在 `.project/` 下。

## 可选 CLI 环境

可选 CLI 由项目内环境提供，不安装到用户级环境，也不进入 `paper/`、`make check` 或发布内容：

```bash
bash .agents/scripts/shared/tool-env.sh install benchmark-radar
bash .agents/scripts/shared/tool-env.sh run benchmark-radar status --json
```

声明在 `.agents/scripts/shared/tool-environments.json`，包含来源、固定提交、入口和环境变量。环境、数据和缓存位于当前 worktree 的 `.project/tools/<tool>/`；未安装时 `run` 明确失败，不回退到 `PATH` 上的全局命令。新增工具只需增加一条声明并运行 `install`；使用 CLI 自己的公共命令，不另建搜索、状态或监控层。凭据仍按 `llm-credentials` 政策注入，不写入声明或跟踪文件。

## 证据

结果来自代码仓库。将每张结果表、每个图数据文件和每个报告的数字登记在 `assets/MANIFEST.yaml`：源仓库、提交、运行或配置标识、校验和及重新生成命令。数字只能通过 `paper/macros.tex` 的接口宏进入正文；`.agents/memory/project/paper-foundation/paper-interfaces.md` 为每个宏记录含义、控制提示和 manifest ID。计划中的结果登记为 `planned`，绝不写成观察结果。大型文件（原始日志、checkpoint、数据集）保留在其代码仓库或受管存储中；通过 `.project/assets.links` 本地链接，绝不放入 Git。

图的来源：

- `paper/figures/` 保存 LaTeX 引用的导出文件，最好使用矢量 PDF，使 `paper/` 单独即可编译。
- 根据数据绘图的脚本位于代码仓库及其 manifest 条目中；若属于论文，也可与输出一起放在 `paper/figures/`。
- 不可重建的可编辑源文件（绘图、幻灯片或选定的生成草稿）属于资产：登记在 manifest，保存在受管存储或 `.project/artifacts/<topic>/`，不放入 `paper/`。
- 临时渲染和被拒草稿放入 `.project/build/figures/`。

`paper-figures` 应用此策略。

## 参考文献审计

离线参考文献门槛在 `make check`（Draft）和 `make release-check`（Release）中运行。在线审计包括元数据审计（`check_reference_metadata.py`）和更正候选项（`check_reference_corrections.py`），分三级运行：

| 时机 | 运行范围 | 门槛 |
| --- | --- | --- |
| 每次 PR 和推送（`references` job） | 相对于基准提交新增或变更的条目，以及台账指纹不再匹配的条目 | 必须通过；通常只需数秒 |
| 向 `main` 的 PR、推送到 `main`，以及 `make release-check` | 所有条目的完整元数据审计（CI 还运行更正审计） | 必须通过 |
| 每周及 `workflow_dispatch`（`references-full` job） | 两项完整审计并行运行，缓存跨运行保留 | 报告结果；不阻塞合并 |

已验证条目的指纹通过 `python3 .agents/scripts/shared/paper-references/check_reference_metadata.py --record` 记录在台账（`verification.bibtex_fingerprint`）。采用分级机制后，对完整范围运行一次并提交台账。provider 故障、限流或机器人验证属于基础设施结果，应列出因此未完成的条目，不能算作条目失败。规则见 [`reference-integrity`](.agents/memory/shared/paper-references/reference-integrity.md)，服务、密钥和缓存见 [`bibliographic-metadata-services`](.agents/knowledge/shared/paper-references/bibliographic-metadata-services.md)。

本地审计优先从环境读取 `BIBTEX_CHECK_MAILTO`、`OPENALEX_API_KEY` 和 `S2_API_KEY`。首选文件来源是设备的共享凭据文件：将规范 checkout 的 `.project/credentials/.env` 链接到该文件，每个 worktree 再通过 `setup-worktree.sh` 创建的 `.project/credentials` 链接访问。只导出这三个键，跳过其他键。仅含这三个键的项目专用根目录 `.env` 仍是后备来源，且优先于共享文件。

## Overleaf

Overleaf 镜像 `dev` 上的 `paper/`，且只镜像 `paper/`（[`overleaf-paper-tree-only`](.agents/memory/shared/paper-publication/overleaf-paper-tree-only.md)）。每个 checkout 添加一次 remote，URL 中不含 token；token 存在 Git credential helper 中：

```bash
git remote add overleaf https://git.overleaf.com/<project-id>
```

分支从 remote 的 `HEAD` 查找；`--branch`、`OVERLEAF_BRANCH` 或 `git config remote.overleaf.overleafBranch` 可覆盖。然后：

```bash
bash .agents/scripts/shared/paper-publication/overleaf-sync.sh status   # in-sync, overleaf-behind, overleaf-ahead, diverged or unrelated
bash .agents/scripts/shared/paper-publication/overleaf-sync.sh pull     # Overleaf edits -> branch sync/overleaf-<commit>, for a PR into dev
bash .agents/scripts/shared/paper-publication/overleaf-sync.sh push     # HEAD:paper -> Overleaf, as a fast-forward
```

- 编辑前运行 `status`（[`sync-overleaf-before-editing`](.agents/memory/shared/paper-publication/sync-overleaf-before-editing.md)）。如果 Overleaf 有 `dev` 缺少的编辑，`pull` 将其放到从双方最后共同状态创建的分支；通过 PR 合并到 `dev` 后再 `push`。
- `push` 在 Overleaf tip 之上提交 `HEAD:paper` 并非强制推送。如果 Overleaf 包含 `HEAD` 缺少的编辑，命令会拒绝执行；推送后重新 fetch 并检查文件树相等。`push --replace` 会覆盖这些编辑；只在首次发布到与 `paper/` 没有共同状态的项目，或 Human 明确允许时使用。
- 比较的是文件树而非提交，因为 Overleaf 会重写收到的提交。
- 实际运行 Overleaf 需要维护者的项目及凭据；单元测试以本地裸仓库代替。

## 可选的第二产品：`poster/`

会议海报是与 `paper/` 并列的第二个产品树 `poster/`。它与 `paper/` 一样自包含，构建到 `.project/build/poster/`，内容及其 `macros.tex` 副本只来自论文，并使用另一个 remote 上的独立 Overleaf 项目（`--remote overleaf-poster --tree poster`）。`paper-publication` 技能对此有说明。模板本身不提供 `poster/`。

## 记忆与知识

`.agents/memory/` 保存持久决策，`.agents/knowledge/` 保存带来源和刷新条件的时效性事实。每个目录的 `AGENTS.md` 保存规则和从 registry 生成的索引；每条记录是 `shared/` 或 `project/` 下独立的 Markdown 文件，front matter 遵循该目录的 `entry-template.md`。投稿场所记录从 `.agents/knowledge/shared/paper-publication/venue-template.md` 开始。范围、状态、替代关系和刷新条件放在 `.agents/content-registry.yaml`，而非 front matter。新增或移动记录时，在 registry 登记并运行 `bash .agents/scripts/shared/check-development.sh --write-indexes`。`make check` 检查 registry、布局和索引、每条记录的 front matter 和小节，以及每个技能的 registry 条目。

论文需要填写 `.agents/memory/project/` 中的初始记录（`brief.md`、`experiments.md`、`paper-interfaces.md`、`publication.md`），并为每项持久决策增加一条记录。

## 分支模型与可见性

`dev` 是集成分支，`main` 是发布分支。新仓库的首次 setup 在 GitHub CLI 可用时创建并推送 `dev`，并将其设为 GitHub 默认分支；`bash .agents/scripts/shared/init-branches.sh` 也可显式完成此操作。诊断命令报告缺失内容及修复方法。

论文公开前建议使用 **Private** 仓库。公开前检查凭据、私人数据、Issue、PR、日志和机器路径。本模板仓库公开：向其反馈时只提供通用、去标识化的复现步骤，并说明论文仓库是私有还是公开；只有论文仓库公开且维护者同意时才指明其名称。

## 验证

测试应覆盖真实风险、历史缺陷和接口边界，不为覆盖率添加测试。论文变更通过公开入口——构建——验证：

```bash
bash .agents/scripts/shared/diagnose-environment.sh
bash .agents/scripts/shared/inspect-state.sh
make check
```

`make check` 运行除模板自有测试（`.agents/tests/project/test_template_*.py`）之外的所有单元测试；单独运行一个文件可使用 `python3 -m unittest discover -s <该测试所在目录> -p 'test_<name>.py'`（例如 `.agents/tests/shared/paper-references`）。`check-development.sh` 本身是继承脚本，因此“文档里点名的路径必须存在”这一步由本模板自己的 `.agents/scripts/project/check_development_paths.py` 在 `make check` 中完成：它检查 `AGENTS.md`、`README.md`、`DEV.md`、`.agents/{AGENTS,memory,knowledge,execution,scripts,notes}` 与非 vendored `SKILL.md` 里出现的 `.agents/…`、`paper/…` 路径，校验 `CLAUDE.md`、`.claude`、`.pi` 的链接目标，并按 `check-development-paths.allow` 列出显式豁免。开发面变更后还应运行 `bash .agents/scripts/shared/check-shells.sh`；使用 `bash .agents/scripts/shared/check-development.sh --write-indexes` 重新生成 registry 索引。通过单元测试不能代替 `make check`，二者也不能代替查看页面。

## 发布

论文发布（投稿版本、arXiv 版本、终稿版本）：

1. 在 `dev` 为该版本设置 `PAGE_BUDGET`，运行 `make check` 和 `make release-check`，并查看 `blind` 和 `submission` 页面。
2. 运行 `paper-publication`，为 Human 批准准备发布；对候选版本运行 `release-doc-audit`。
3. 创建从 `dev` 到 `main` 的 PR。合并后在 `main` 上创建并推送标签，例如 `submit-<venue>-<yyyy>`、`arxiv-v1` 或 `camera-ready`。
4. 在 `RELEASE_NOTES.md` 中添加 `## <tag>` 条目，记录发布内容、所用构建及检查结果。

本模板自身的发布使用 `main` 上的 `v<major>.<minor>.<patch>` 标签，每个标签在 `RELEASE_NOTES.md` 中有一个 `## <tag>` 标题。模板发布前运行 `release-doc-audit`、`make check` 和模板自有测试（`python3 -m unittest discover -s .agents/tests/project -p 'test_template_*.py'`，约十几分钟；CI 的 `check` job 也会运行）；`main` 要求 CI job `structure`、`check`、`paper-only` 和 `references` 通过。发布条目包含 “Adoption states” 表：对按 README “Start a paper” 到达的每个状态（新论文、没有台账的现有参考文献或已迁移台账、投稿套件），列出该状态下预期失败的 `make release-check` 步骤。模板自有测试中的 `.agents/tests/project/test_template_adoption_states.py` 从交付文件构建每种状态，分别运行 `make check` 和 `make release-check` 并将失败项与表格比较，还会对真实规模的参考文献运行在线元数据审计；发布需要该测试通过。升级小节 `### Upgrading a paper from <previous tag>` 在 `upgrade-template.sh` 单独完成升级时以 **Command only.** 开头，否则列出剩余手动步骤；同一测试检查 v0.4.0 之后的每个条目，并用候选版本自身的命令将 v0.4.1 的新论文升级到候选版本。

CI 的 Ubuntu 镜像 DNS 预检和 TeX 安装步骤各有独立超时，apt 也设置连接超时和有限重试；runner 的瞬时 DNS/网络故障会在数分钟内显式失败，而不是耗尽 job 超时。遇到该失败时读取安装日志并重跑 failed jobs，不使用管理员权限绕过必需检查。

## 与模板的关系

跟随 coding template v0.1.34。继承的命令和记录与该版本没有本地差异：`.agents/scripts/shared/` 中来自上游的脚本（包括 `upgrade-template.sh` 和 `content_registry.py`）与 v0.1.34 逐字节相同，继承的技能和记录在 `## In this repository` 小节之上与上游原文相同。本模板早先携带的升级命令和 registry 检查修改已全部进入上游（v0.1.33，上游 #155）。每次跟随新的上游版本后重新核对：用 `cmp` 比较上游脚本，比较各记录在小节之上的正文；出现必须保留的本地差异时，在此逐块列出原因、引入它的 Issue 和上游状态。

本仓库是 `coding-agent-project-template` 的派生模板：在其基础上构建，并供论文使用。它的 registry `.agents/content-registry.yaml` 在 `template` 中记录本模板，在 `template.upstream` 中记录其遵循的 coding template：

| 仓库 | `template.repository` / `template.version` | `template.upstream` |
| --- | --- | --- |
| `coding-agent-project-template` | 自身及其当前版本 | 无 |
| 本模板 | 自身及其发布版本（v0.4.13） | coding template 及其所遵循的标签（v0.1.34） |
| 由本模板创建的论文 | 本模板及采用的标签 | 无 |

仓库有 `template.upstream` 字段时遵循该字段，否则遵循 `template`。

- 本模板通过 `template-upgrade` 接收 coding template 发布，更新 `template.upstream.version`。继承文件保持原文，本模板的适配只放在末尾的 `## In this repository` 小节。
- 论文通过 `template-upgrade` 接收本模板发布，阅读目标标签的 `RELEASE_NOTES.md`，并延续本模板编写的 `## In this repository` 小节。`bash .agents/scripts/shared/upgrade-template.sh [--check] <TARGET_TAG>` 执行流程的机械部分（步骤 5）并输出其余步骤；如果没有冲突且跨过的每个版本都标记 **Command only.**，则采用 `template-upgrade` 的 `## In this repository` 小节定义的轻量路径。
- 论文发现的缺陷或缺口通过 `template-feedback` 反馈给本模板。本模板将继承内容中的缺陷转发给 coding template，并链接两个 Issue。
- 从 v0.4.0 之前布局的迁移记录在 `.agents/memory/project/template-maintenance/rebuild-on-coding-template.md`，使用过 `template-sync` 的论文的迁移步骤在 `RELEASE_NOTES.md` 的 v0.4.0 条目中。

## 操作

Setup、构建、检查、Overleaf 同步和发布通过 `make` 目标和 `.agents/scripts/` 完成，不使用私有函数、临时包装器或第二套脚本（`cli-first-operations`）。论文没有长时间运行的产品任务；实验在各自代码仓库中运行和监督。
