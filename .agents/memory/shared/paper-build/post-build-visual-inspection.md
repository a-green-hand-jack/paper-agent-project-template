---
name: post-build-visual-inspection
date: 2026-10-20
source: Issues #156 §7 and #263; visual-inspection records of the downstream paper repositories, including figure labels judged legible from an asset render that printed at half the caption size on the page
applies_to: repositories that build a paper, poster or other typeset product whose layout a person will read
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
   headers that are wrong for the form. Three more show only on the page:
   - **stretched vertical space**: a style's `\flushbottom` stretches the space
     around headings, paragraphs and floats so that columns end level, which
     opens blank lines under a caption or between paragraphs; whether the body
     is `\raggedbottom` is the paper's choice, recorded in its publication
     record;
   - **a heading moved to the next column**: with `\raggedbottom`, a heading
     that cannot keep two lines under it at the column foot moves on and leaves
     the column short; the repair is wording (cut until it fits, or add a true
     sentence that fills the column), and it moves everything after it;
   - **floats stacked or off their page**: two floats on top of each other in
     one column, a column float directly under a page-wide one, a `[h]` float
     splitting a column, or a float on another page than its first reference;
     a page-wide float lands at the earliest at the top of the next page, so
     its source is declared a page ahead.
   A justified line can also be stretched by material that does not break,
   such as a boxed citation: list lines whose spacing exceeds `MAX_WORD_SPACE`.
6. **Measure a last line, do not judge it by eye.** Take the line boxes from the
   **blind** build (comments in `main` move the breaks), compute
   `(line right − column left) / column width` for every body line that stops
   short of the right edge, and list those below `LAST_LINE_FILL`. Fix by cutting
   words so the paragraph ends a line earlier, by rewording, or by adding
   content. A repair moves every break after it, so measure again — and again —
   until no paragraph is listed. Two-column main text and one-column appendix
   have different column widths; measure each on its own pages.
7. **Never move text with a spacing command.** `\looseness`, `\vspace`,
   `\linebreak`, a negative `\parfillskip` or a stretched `\emergencystretch`
   buys a line at the cost of a layout the other rendering of the same source
   will not reproduce; every repair is a wording or content change. Lines that
   end in inline mathematics, headings and footnotes are misjudged by extracting
   boxes and are settled by looking at the page.
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

Each project fills three parameters in the `## In this repository` section at the
end of this record (see `template-adoption` step 5):

- `MIN_FIGURE_TEXT`: the smallest in-figure text relative to the caption, for
  example `1.0` (as large as the caption).
- `LAST_LINE_FILL`: the shortest acceptable last line of a paragraph, for
  example "no line of one or two words", or a fill such as two thirds of the
  column. A stub is fixed by rewording, cutting or adding content, never by
  padding or spacing commands, and a word added to fill a line is content that
  must be true and is reported to the Human.
- `MAX_WORD_SPACE`: the widest acceptable median space in a justified line,
  as a multiple of the page's median space, for example `1.8`.

Then:

1. Render to `.project/build/inspect/<build>/`, for example
   `pdftoppm -r 110 -png .project/build/blind.pdf .project/build/inspect/blind/page`,
   or one page at higher resolution with `-f N -l N -r 240`.
2. After a local change, render again and compare the page images by hash to
   show which pages changed; look again at the changed ones.
3. `pdftotext -layout` helps find text, but merges adjacent paragraphs and
   keeps line numbers of an anonymous build; do not measure layout from it
   alone.
4. Measure with `.agents/scripts/shared/paper-build/page_measure.py`, which reads
   the line boxes of `pdftotext -bbox-layout` from the blind build and takes
   its page range from the build's `.aux` (`--part main` ends at
   `PaperMainTextEnd`, `--part appendix` starts at appendix A):
   `last-lines --below <LAST_LINE_FILL>`, `word-spacing --factor
   <MAX_WORD_SPACE>`, `column-gaps` (columns more than 1.5 lines short of the
   text area; the last page is judged by eye) and `section-height --from
   <heading>` (the column height a section takes against a length the author
   set). Its output is a list of candidates to confirm on the page, not a
   check, and `make check` does not run it. Measure again after every repair.
5. Compare each float's page, from its `\newlabel` in the build's `.aux`, with
   the page of its first reference in the text; list the floats that differ.
6. Float placement, last-line targets and spacing preferences differ between
   papers and venues; a paper records its own in its publication record, and
   never changes a venue kit's margins or spacing to win space.
