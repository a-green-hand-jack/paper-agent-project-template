#!/usr/bin/env bash
# make check: build main and blind, fail on undefined references or citations,
# missing files and multiply defined labels, report the main-text pages of the
# blind build against PAGE_BUDGET, and run the repository's static checks, the
# development registry check and the unit tests. Build output and logs stay in
# BUILD_DIR (.project/build/).
set -uo pipefail

root=$(git rev-parse --show-toplevel)
cd "$root"
build=${BUILD_DIR:-$root/.project/build}
mkdir -p "$build/logs"
export PYTHONPYCACHEPREFIX="$build/cache"
failed=()

step() { printf '\n== %s\n' "$1"; }
run() { # run NAME COMMAND...: run a check and remember a failure
  local name=$1
  shift
  "$@" || failed+=("$name")
}

for job in main blind; do
  step "build $job"
  if make -C paper "$job" BUILD_DIR="$build" TEXBIN="${TEXBIN:-}" >"$build/logs/$job.log" 2>&1; then
    echo "OK $job: .project/build/$job.pdf"
  else
    echo "ERROR $job: the build failed; the full output is in .project/build/logs/$job.log"
    failed+=("build $job")
  fi
  run "log $job" python3 .agents/scripts/shared/paper-build/check_paper_build.py --build-dir "$build" log "$job"
done

step 'page budget (blind)'
run 'pages' python3 .agents/scripts/shared/paper-build/check_paper_build.py --build-dir "$build" pages blind --budget "${PAGE_BUDGET:-}"

step 'PDF text layer (main)'
run 'underscores' python3 .agents/scripts/shared/paper-build/check_paper_build.py --build-dir "$build" underscores main

step 'reference integrity (draft)'
run 'references' python3 .agents/scripts/shared/paper-references/check_reference_integrity.py --profile draft

step 'interface macros'
run 'interfaces' python3 .agents/scripts/shared/paper-build/check_paper_interfaces.py

step 'development registry and layout'
run 'development registry' bash .agents/scripts/shared/check-development.sh

step 'skills, memory and knowledge records'
run 'agent content' python3 .agents/scripts/shared/check_agent_content.py

step 'unit tests'
for group in shared project; do
  for directory in ".agents/tests/$group" ".agents/tests/$group"/*/; do
    [[ -d "$directory" ]] || continue
    compgen -G "$directory/test_*.py" >/dev/null || continue
    run "unit tests ($directory)" python3 -m unittest discover -s "$directory" -p 'test_*.py'
  done
done

echo
if ((${#failed[@]})); then
  printf 'FAILED make check: %s\n' "$(IFS=,; echo "${failed[*]}" | sed 's/,/, /g')"
  exit 1
fi
echo 'OK make check'
