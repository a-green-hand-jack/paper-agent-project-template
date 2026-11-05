# Paper Agent Project Template

这是一个将科研论文写作作为软件开发来组织的模板，由编码 Agent（Claude Code、Codex、OpenCode 或普通 shell）完成大量工作。它基于 [`coding-agent-project-template`](https://github.com/a-green-hand-jack/coding-agent-project-template)，分为三个层面：

- **产品面**：`paper/` 中的论文，是一棵自包含的 LaTeX 文件树。单独复制 `paper/` 即可编译，Overleaf 也只接收这个目录。
- **开发面**：`AGENTS.md` 和 `.agents/`，包含 Agent 规则、技能、记忆和知识记录、参考文献台账、脚本与检查。
- **Human 面**：`README.md`、`PAPER.md`（论文契约）、`DEV.md` 和 `RELEASE_NOTES.md`，以及 Issue 和 PR。

默认在 `dev` 开发，按任务风险决定 Issue、审阅和 PR；如需派出 Herdr worktree，先确认是否派遣、coding agent、具体模型和 thinking level。构建即测试：`make check` 遇到未定义的引用或引文、缺失文件、重复定义的标签和损坏的接口宏时会失败。每次发布都对应 `main` 上的一个标签；论文报告的每个数字都可追溯到产生它的代码仓库、提交和运行。

模板支持两种运行模式，由论文在 `PAPER.md` 中声明。**协作**模式下，Human 与 Agent 一起完成每个实质性步骤。**自主**模式下，Human 提供简报和材料，Agent 自行起草、审阅和构建；修改锁定项、发布或提交之前仍需停下来征求 Human 的决定。

## 开始一篇论文

1. 在 GitHub 上使用 **Use this template** 创建论文仓库，论文公开之前建议选择 **Private**。如需可复现的起点，也可以克隆一个发布标签（见下方“模板版本”）。
2. 在新仓库运行 `bash .agents/scripts/shared/init-branches.sh`。该命令创建并推送 `dev`，并将其设为默认分支。工作分支从 `dev` 开始；发布时合并到 `main`。
3. 在每个 worktree 中，首先运行 `bash .agents/scripts/shared/setup-worktree.sh`。
4. 移除仅属于本模板的内容：
   - 在 `.agents/content-registry.yaml` 中保留 `template.repository` 和 `template.version`（本模板及其起始版本），删除 `upstream` 块。
   - 删除 registry 标记为 `scope: template` 的文件，将对应 registry 条目移到 `omitted`（记录 `id`、`path` 和原因 `Upstream template-only content; not adopted.`，与 `upgrade-template.sh` 记录的文本一致），然后用 `bash .agents/scripts/shared/check-development.sh --write-indexes` 重新生成索引。需删除的内容包括 `.agents/memory/project/template-maintenance/` 中本模板专有的记录，以及 `.agents/tests/project/` 中 registry 标为 `scope: template` 的测试；以 registry 的完整清单为准。在 `AGENTS.md` 中，将关于本模板 case 分支的规则替换为论文自己的列表，或删除该规则。
   - 将 `RELEASE_NOTES.md` 替换为论文自己的发布记录；初始为空，每个发布标签对应一个 `## <tag>` 标题。
   - 将本 README 改写为论文说明：介绍论文及构建方法。
5. 填写模板留给论文的槽位：在 `.agents/memory/shared/paper-build/page-budget-on-blind-build.md`（`PAGE_MARGIN`）和 `.agents/memory/shared/paper-build/post-build-visual-inspection.md`（`MIN_FIGURE_TEXT`、`LAST_LINE_FILL`）末尾分别添加含 Slot/Value 表格的 `## In this repository` 小节。在两者都填写之前，`diagnose-environment.sh` 会发出警告。
6. 将论文简报交给 Agent。`paper-foundation` 技能会验证简报，并填写 `PAPER.md` 中已决定的字段；未决定的内容保持为 `unresolved`。没有简报时，与 Agent 一起填写 `PAPER.md`。
7. 确定投稿场所后，将其官方套件原样放入 `paper/`，在根目录 `Makefile` 中设置 `PAGE_BUDGET`，并在 `.agents/memory/project/paper-publication/publication.md` 中记录投稿场所（`paper-publication`）。将作者写入 `paper/authors.tex`，用每位真实作者的姓名、电子邮箱和机构对应的 `\PaperIdentity` 替换模板占位身份（`Template-Author-Name` 等）。在此之前，`make release-check` 的 `identity` 步骤会因占位身份失败，`leftovers` 会因模板的 `\PaperTODO` 文本失败，而 `pages` 在设置 `PAGE_BUDGET` 之前会失败；`make check` 则可以通过。占位文本不会匹配任何投稿套件的文本。
8. 在 `paper/` 中写作。将每张结果表、每个图数据文件和每个报告的数字登记到 `assets/MANIFEST.yaml`，并且只通过 `paper/macros.tex` 中的接口宏将数字写入正文。

Agent 首先读取 `AGENTS.md`，将每项任务路由到一个技能，并只加载该任务需要的记录。

## 构建

根目录的 `Makefile` 是公开构建入口。输出和中间文件写入 worktree 的 `.project/build/`，不写入 `paper/` 或仓库根目录。

| 命令 | 构建或检查的内容 |
| --- | --- |
| `make pdf` | `main`：署名并保留作者注释（`.project/build/main.pdf`） |
| `make submission` | `submission`：署名，移除注释 |
| `make blind` | `blind`：匿名，移除作者身份、致谢和注释 |
| `make check` | 构建 `main` 和 `blind`；遇到未定义的引用或引文、缺失文件、重复定义的标签、接口宏或参考文献台账错误、无效技能或记录 front matter，以及失败的单元测试时失败；报告 `blind` 的正文页数与 `PAGE_BUDGET` 的比较 |
| `make release-check` | 构建 `blind` 和 `submission`；匿名 PDF 或其源文件中存在作者身份（或模板占位身份）、`submission` 中留有注释或 TODO、页数超预算、参考文献未达到发布强度，或完整在线元数据审计未通过时失败（需要 `uv` 和网络） |
| `make clean` | 清理构建输出 |

三个版本来自同一份源：`paper/main.tex` 对应 `main`，单行的 `paper/submission.tex` 和 `paper/blind.tex` 只关闭部分层次。TeX 从 `PATH` 获取；如果排在前面的 `latexmk` 属于其他安装，则可设置 `TEXBIN=<TeX Live bin directory>`。构建需要 `latexmk`、`pdflatex` 和 `bibtex`；检查还需要 `pdftotext`、`pdfinfo`、PyYAML 和 markdown-it-py。

单独复制 `paper/` 后，可用 `make -C <copy> main`（或 `blind`、`submission`）构建，输出写入 `<copy>/build/`。

## 目录

| 路径 | 层面 | 用途 |
| --- | --- | --- |
| `paper/` | 产品 | 论文：`main.tex`、`submission.tex`、`blind.tex`、`authors.tex`、`macros.tex`、`refs.bib`、`sections/`、`figures/`、`tables/`、`algorithms/`、`style/` 和其中的 `Makefile` |
| `assets/` | 证据 | `MANIFEST.yaml`：每个报告数字、表格和图数据文件的源仓库、提交、运行、校验和及重新生成命令；大型文件的本地链接 |
| `Makefile` | 构建入口 | 上述 `make` 目标 |
| `.project/` | worktree 本地状态 | 构建输出、日志和截图；Git 忽略此目录 |
| `.agents/` | 开发 | 技能、记忆和知识记录、参考文献台账、脚本和测试；见 `.agents/AGENTS.md` |
| `.github/` | 开发 | CI 及 Issue、PR 模板 |
| `AGENTS.md`、`CLAUDE.md` | Agent 入口 | 规则和任务路由；`CLAUDE.md` 是指向 `AGENTS.md` 的符号链接 |
| `README.md` | Human | 本页面 |
| `PAPER.md` | Human | 论文契约：论文主张、叙事和风格，不得静默更改的内容，以及尚未决定的问题 |
| `DEV.md` | Human | 论文的开发方式：Issue、构建、Overleaf、证据和发布 |
| `RELEASE_NOTES.md` | Human | 每个发布标签对应一个标题 |

`paper/refs.bib` 是论文实际引用的文献，`.agents/references/ledger.json`
记录各处引用的身份和论断支持。`.agents/references/exemplars/` 保存写作、
图表和海报范例的来源与学习记录；范例不会自动成为论文引用。第三方下载材料
放在 `.project/artifacts/` 或登记的外部资产中。

## 发布与 Overleaf

发布（投稿版本、arXiv 版本或终稿版本）通过从 `dev` 到 `main` 的 PR 完成：通过 `make release-check` 后，在 `main` 上创建例如 `submit-<venue>-<yyyy>`、`arxiv-v1` 或 `camera-ready` 的标签，并记录到 `RELEASE_NOTES.md`。

Overleaf 通过 `.agents/scripts/shared/paper-publication/overleaf-sync.sh` 镜像 `dev` 上的 `paper/`：`status` 比较两边，`push` 将 `HEAD:paper` 快进推送到 Overleaf，`pull` 将 Overleaf 编辑拉到 `sync/overleaf-*` 分支供 PR 使用。两个方向都会检查文件树相等，仓库根目录不会发送到 Overleaf。具体说明见 `DEV.md`。

## 为什么使用这个模板

普通 LaTeX 仓库说明源文件在哪里、如何编译。本模板还回答：

- 论文希望读者相信什么，哪些决定 Agent 不得静默更改；
- 每个主张由哪些实验问题和解释边界支持，每个报告数字从何而来；
- 每条引文是否支持其所在句子；
- 哪些术语、结果、图和表必须在全文及三个构建版本中保持一致；
- 当前任务应使用哪个技能；
- 发布所依据的确切源文件及其检查。

它不承诺让科学研究变得更好，也不取代 Human 的研究决策。它让论文变化过程中的意图、证据、作者身份和交付保持关联，并留下证据，表明交付的论文就是经过审阅的论文。

## 模板版本

**Use this template** 会复制默认分支的最新状态。如需可复现的起点，请克隆发布标签（将 `<TEMPLATE_TAG>` 替换为 Releases 页面中的标签）：

```bash
git clone --branch <TEMPLATE_TAG> --depth 1 \
  https://github.com/a-green-hand-jack/paper-agent-project-template.git my-paper
cd my-paper
git remote remove origin
git remote add origin https://github.com/OWNER/PAPER.git
git push -u origin main
```

先阅读该标签上的 `RELEASE_NOTES.md`。之后可通过 `template-upgrade` 技能升级：`bash .agents/scripts/shared/upgrade-template.sh --check <TEMPLATE_TAG>` 输出计划，`upgrade-template.sh <TEMPLATE_TAG>` 应用计划；标记为 **Command only.** 且没有冲突的版本不需要其他操作（轻量路径）。采用 `.agents/scripts/shared/` 布局之前的论文，需要按 `template-upgrade` 的 `## In this repository` 小节所示，运行一次目标版本的完整命令目录。模板缺陷通过 `template-feedback` 反馈。现有论文仓库通过 `template-adoption` 接入；使用过 `template-sync` 的论文遵循 `RELEASE_NOTES.md` 中 v0.4.0 的说明。
