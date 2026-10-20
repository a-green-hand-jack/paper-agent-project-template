# Builds this paper with latexmk. It needs nothing outside this directory: in a
# copy of paper/ alone the output goes to build/; inside a set-up worktree it
# goes to the worktree's .project/build/ (BUILD_DIR overrides both). Set TEXBIN
# to a TeX Live bin directory when the right latexmk is not first on PATH.
TEXBIN ?=
LATEXMK ?= latexmk
BUILD_DIR ?= $(if $(wildcard ../.project/home),../.project/build,build)
LATEXMK_FLAGS ?= -pdf -interaction=nonstopmode -halt-on-error -file-line-error

ifneq ($(strip $(TEXBIN)),)
export PATH := $(TEXBIN):$(PATH)
endif
# Keep log lines whole so checks can read file names and keys.
export max_print_line := 10000

BUILDS := main blind submission
.PHONY: all $(BUILDS) clean

all: main

$(BUILDS):
	$(LATEXMK) $(LATEXMK_FLAGS) -outdir=$(BUILD_DIR) -auxdir=$(BUILD_DIR)/aux/$@ $@.tex

clean:
	rm -f $(foreach b,$(BUILDS),$(BUILD_DIR)/$(b).pdf)
	rm -rf $(BUILD_DIR)/aux
