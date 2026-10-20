---
name: post-build-visual-inspection
date: 2026-10-20
source: Issue #156 §7; visual-inspection records of the downstream paper repositories, including figure labels judged legible from an asset render that printed at half the caption size on the page
scope: shared
applies_to: repositories that build a paper, poster or other typeset product whose layout a person will read
status: active
supersedes: null
superseded_by: null
---

# Look at the rendered pages before calling a build done

## Decision

1. **A clean build proves nothing about layout.** Compiling without errors, an
   empty warning list or a high-resolution view of a figure file does not show
   that the pages read well. Render the affected pages and look at them at
   reading size before calling a layout change done.
2. **Judge figures on the compiled page.** Text inside a figure is measured
   against the caption on the page, never on the asset file; in-figure text is
   at least `MIN_FIGURE_TEXT` of the caption size.
3. **Check the known failure classes:** floats far from the text that cites
   them, lines holding one character or word, paragraph last lines shorter than
   `LAST_LINE_FILL`, paragraphs split without need, overfull lines, and running
   headers that are wrong for the form.
4. **Report what was inspected.** Name the build, the pages looked at and what
   was not checked. Never claim visual approval without looking at the
   rendered pages.
5. **Keep the build's output whole.** Redirect build output to a file; never
   pipe a build into `head` or another command that can stop reading early.

## Why

Reviewers given a 300 dpi render of a figure file called its labels legible;
on the compiled page they printed at about half the caption size. Global
settings such as `\sloppy`, a large `\emergencystretch` or `\hbadness=10000`
remove the warnings that would point at bad lines, so a quiet log says nothing.
Piping a build into `head` ended it with SIGPIPE and left a truncated PDF that
looked like a finished one.

## Apply

Each project fills two parameters in the `## In this repository` section at the
end of this record (see `template-adoption` step 5):

- `MIN_FIGURE_TEXT`: the smallest in-figure text relative to the caption, for
  example `1.0` (as large as the caption).
- `LAST_LINE_FILL`: the shortest acceptable last line of a paragraph, for
  example "no line of one or two words". A stub is fixed by rewording, never by
  padding.

Then:

1. Render to `.project/build/inspect/<build>/`, for example
   `pdftoppm -r 110 -png .project/build/blind.pdf .project/build/inspect/blind/page`,
   or one page at higher resolution with `-f N -l N -r 240`.
2. After a local change, render again and compare the page images by hash to
   show which pages changed; look again at the changed ones.
3. `pdftotext -layout` helps find text, but merges adjacent paragraphs and
   keeps line numbers of an anonymous build; do not measure layout from it
   alone.
4. Float placement, last-line targets and spacing preferences differ between
   papers and venues; a paper records its own in its publication record, and
   never changes a venue kit's margins or spacing to win space.
