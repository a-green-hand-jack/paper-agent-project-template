# 发布说明

本文件只描述当前发布；历史版本保留在各自的标签里（例如 `git show v0.7.1:RELEASE_NOTES.md`）。
基于本模板创建的论文维护自己的发布说明，不复制此历史。

## v0.10.2 — 2026-11-15

把中文批注的 CI 依赖写成可查的事实，而不是发布说明里的一句附注。

- 新知识记录 `.agents/knowledge/shared/paper-build/cjk-comments-need-the-cjk-package.md`：
  `CJKutf8.sty` 在 Ubuntu 上由 `latex-cjk-common` 提供；`texlive-lang-cjk` 是 metapackage，
  真正的文件在 Recommends 里，`--no-install-recommends` 装不到；中文字形要 `latex-cjk-chinese`
  （arphic 字体），缺字体时构建成功但 PDF 是空框，日志里有 `Missing character`。
  证据是 v0.10.1 的三次 CI 运行与 `dpkg-deb -c` 的文件清单。
- `paper/style/author-comments.sty` 头部注明这两包与记录位置，论文抄这段样式时能直接看到。

### Adoption states

以下状态通过 `make check`；`make release-check` 对尚未填写的论文在表中步骤失败，原因见 v0.4.2。模板中的占位内容不是投稿论文。

| State | `make release-check` fails on |
| --- | --- |
| fresh paper | `identity`, `leftovers`, `pages` |
| existing bibliography, no ledger | `identity`, `leftovers`, `pages`, `references` |
| existing bibliography, migrated ledger | `identity`, `leftovers`, `pages`, `references` |
| venue kit | `identity`, `leftovers`, `pages` |

### Upgrading a paper from v0.10.1

**Command only.** 知识记录随升级进入 `.agents/`；`paper/style/author-comments.sty` 那两行注释
属产品面，需要时照抄。CI 的安装清单加 `latex-cjk-common` 与 `latex-cjk-chinese`（若本仓库用中文批注）。

## Starting from this template

1. 用 GitHub 的 **Use this template** 创建论文仓库，公开之前建议选 **Private**；需要可复现的起点时，克隆一个发布标签。
2. 运行 `bash .agents/scripts/shared/init-branches.sh`：创建并推送 `dev`，把它设为默认分支。工作分支从 `dev` 开始，发布时合并到 `main`。
3. 每个 worktree 先运行 `bash .agents/scripts/shared/setup-worktree.sh`。
4. 把采用工作交给 agent（`template-adoption`）：删除 registry 标记 `scope: template` 的文件并记为 `omitted`，把 `template` 块改成论文仓库，把本文档换成论文自己的发布说明，重写 README。
5. 让 agent 填写留给论文的槽位：`page-budget-on-blind-build.md` 的 `PAGE_MARGIN`，`post-build-visual-inspection.md` 的 `MIN_FIGURE_TEXT` 与 `LAST_LINE_FILL`。
6. 把论文简报交给 agent（`paper-foundation`）：`brief.md` 中未决定的内容保持 `unresolved`。

模板升级：`bash .agents/scripts/shared/upgrade-template.sh --check <tag>` 输出计划，去掉 `--check` 应用；
标记 **Command only.** 且没有冲突的版本不需要其他操作。
