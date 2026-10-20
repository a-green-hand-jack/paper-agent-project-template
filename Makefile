# Public build entry for the paper in paper/. Output and intermediates go to
# this worktree's .project/build/; nothing is written into paper/ or the root.
#   make pdf | blind | submission   build one form (.project/build/<job>.pdf)
#   make check                      builds main and blind and runs every check
#   make release-check              release gates for blind and submission
#   make clean                      remove the build output
# TEXBIN=<TeX Live bin directory> selects the TeX binaries when the right
# latexmk is not first on PATH. PAGE_BUDGET is the venue's main-text page
# limit, measured on the blind build (.agents/memory/shared/page-budget-on-blind-build.md);
# PAGE_BUDGET=none declares a release without a page limit, such as arXiv.
PAGE_BUDGET ?=
TEXBIN ?=
BUILD_DIR := $(CURDIR)/.project/build
export PAGE_BUDGET TEXBIN BUILD_DIR

.PHONY: pdf blind submission check release-check clean

pdf:
	@$(MAKE) --no-print-directory -C paper main
blind submission:
	@$(MAKE) --no-print-directory -C paper $@
check:
	@bash .agents/scripts/paper-check.sh
release-check:
	@bash .agents/scripts/release-check.sh
clean:
	@$(MAKE) --no-print-directory -C paper clean
