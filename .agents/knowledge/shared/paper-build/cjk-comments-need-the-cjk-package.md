---
name: cjk-comments-need-the-cjk-package
date: 2026-11-15
source: Issue #256 and the v0.10.1 CI runs; `dpkg-deb -c latex-cjk-common_4.8.5-1` (Ubuntu noble) and `texlive-lang-cjk`'s recommends on Ubuntu resolute
applies_to: any build that typesets an author comment written in Chinese, and the CI install lists that build runs on Ubuntu
---

# A Chinese comment needs CJKutf8, which the minimal TeX install lacks

## Fact

`paper/style/author-comments.sty` loads `CJKutf8` only when `\ifPaperNotes` is
true, so only the build that shows comments — `main` — needs it. That package is
not in a minimal Ubuntu TeX install, and the package that looks like the fix does
not provide it:

- `CJKutf8.sty` ships in **`latex-cjk-common`** (`/usr/share/texmf/tex/latex/CJK/CJKutf8.sty`).
- `texlive-lang-cjk` is a metapackage; the packages that carry the files
  (`latex-cjk-all`, `texlive-lang-chinese`) are its **recommends**, so
  `apt-get install --no-install-recommends texlive-lang-cjk` leaves the file
  absent and the build fails at the `\RequirePackage{CJKutf8}` line.
- Chinese **glyphs** need the arphic fonts, which `latex-cjk-chinese` pulls in
  (`latex-cjk-chinese-arphic-bsmi00lp`, `-bkai00mp`, `-gbsn00lp`, `-gkai00mp`).
  Without them the build succeeds and the PDF shows empty boxes.

A build on a machine that has these installed passes whether or not the CI list
names them, so a green local `make check` proves nothing about the CI install.

## Evidence

The template's `check` and `paper-only` jobs install a bounded list with
`--no-install-recommends`. Both failed at `author-comments.sty:17` with
`File CJKutf8.sty not found` on 2026-11-15 until `latex-cjk-common` and
`latex-cjk-chinese` were named explicitly (v0.10.1, runs 43714882562 and
43715128983); with them the `paper-only` job logs
`(/usr/share/texmf/tex/latex/CJK/CJKutf8.sty ...)` and builds all three forms
(run 43716539326). `dpkg-deb -c latex-cjk-common_4.8.5-1` lists that exact path,
and `apt-cache show texlive-lang-cjk` shows `latex-cjk-all` and
`texlive-lang-chinese` only as Recommends.

## Apply

- A repository whose authors write Chinese comments names both packages in every
  CI step that installs TeX, or its `main` build fails before any check runs.
- Do not treat `texlive-lang-cjk` as sufficient; name `latex-cjk-common` (the
  file) and `latex-cjk-chinese` (the fonts).
- To tell a missing-glyph failure from a missing-package failure: a missing
  package stops the build at `CJKutf8.sty`; missing fonts build fine and leave
  visible empty boxes, with `Missing character` lines in the log.

## Refresh

Recheck this when the Ubuntu TeX packaging, the CJK package contents or the
notes build changes, and before relying on it for another distribution: another
release may move `CJKutf8.sty` into a different package or pull the arphic fonts
in by default.
