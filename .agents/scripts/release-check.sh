#!/usr/bin/env bash
# make release-check: build blind and submission and fail when the blind build
# shows an author identity (PDF text, PDF metadata or any source it reads) or
# paper/authors.tex still declares the template's placeholder identity, when
# submission still has \PaperTODO, \PaperNote or TODO, when the main text of
# blind is over PAGE_BUDGET or no budget is set, when the references do not
# pass the release profile, or when the full online metadata audit of every
# bibliography entry does not pass (it needs uv and the network; a provider
# failure is an infrastructure outcome). Run make check first; this adds
# release gates.
set -uo pipefail

root=$(git rev-parse --show-toplevel)
cd "$root"
build=${BUILD_DIR:-$root/.project/build}
mkdir -p "$build/logs"
export PYTHONPYCACHEPREFIX="$build/cache"
failed=()

step() { printf '\n== %s\n' "$1"; }
run() {
  local name=$1
  shift
  "$@" || failed+=("$name")
}
check() { python3 .agents/scripts/check-paper-build.py --build-dir "$build" "$@"; }

for job in blind submission; do
  step "build $job"
  if make -C paper "$job" BUILD_DIR="$build" TEXBIN="${TEXBIN:-}" >"$build/logs/$job.log" 2>&1; then
    echo "OK $job: .project/build/$job.pdf"
  else
    echo "ERROR $job: the build failed; the full output is in .project/build/logs/$job.log"
    failed+=("build $job")
    continue
  fi
  run "log $job" check log "$job"
done

step 'anonymity (blind)'
run 'identity' check identity blind

step 'leftovers (submission)'
run 'leftovers' check leftovers submission

step 'page budget (blind)'
run 'pages' check pages blind --budget "${PAGE_BUDGET:-}" --require-budget --fail-over

step 'reference integrity (release)'
run 'references' python3 .agents/scripts/check-reference-integrity.py --profile release

step 'reference metadata (full online audit)'
run 'metadata' python3 .agents/scripts/check-reference-metadata.py

echo
if ((${#failed[@]})); then
  printf 'FAILED make release-check: %s\n' "$(IFS=,; echo "${failed[*]}" | sed 's/,/, /g')"
  exit 1
fi
echo 'OK make release-check'
