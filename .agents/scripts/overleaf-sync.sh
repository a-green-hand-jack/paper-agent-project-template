#!/usr/bin/env bash
# Sync the paper tree with an Overleaf project through Overleaf's Git remote.
#
#   overleaf-sync.sh status [options]  compare the Overleaf project with HEAD:<tree>
#   overleaf-sync.sh push [options]    put HEAD:<tree> on Overleaf as a fast-forward
#   overleaf-sync.sh pull [options]    put Overleaf's edits on a branch sync/overleaf-<commit>
#                                      for a PR
#
# Options:
#   --remote NAME  the Overleaf remote (default: overleaf)
#   --branch NAME  its branch (default: $OVERLEAF_BRANCH, git config remote.NAME.overleafBranch,
#                  the remote's HEAD, then main)
#   --tree DIR     the directory that is the Overleaf project (default: paper)
#   --replace      push even though Overleaf holds content that HEAD never had
#
# The Overleaf project holds the contents of DIR only, never the repository root. Trees
# are compared instead of commits because Overleaf rewrites the commits it receives.
# push and pull never touch the working tree; a PR merges what pull brings. Add the remote
# without a token in its URL and keep the token in a Git credential helper:
#   git remote add overleaf https://git.overleaf.com/<project-id>
set -euo pipefail

usage() { awk 'NR > 1 && /^#/ { sub(/^# ?/, ""); print; next } NR > 1 { exit }' "$0"; }
die() { printf 'ERROR %s\n' "$*" >&2; exit 1; }
short() { printf '%s' "${1:0:12}"; }

command=${1:-}
case $command in
  status | push | pull) shift ;;
  -h | --help) usage; exit 0 ;;
  *) usage >&2; exit 2 ;;
esac

remote=overleaf branch='' tree=paper replace=0
while (($#)); do
  case $1 in
    --remote) remote=${2:?--remote needs a name}; shift 2 ;;
    --branch) branch=${2:?--branch needs a name}; shift 2 ;;
    --tree) tree=${2:?--tree needs a directory}; shift 2 ;;
    --replace) replace=1; shift ;;
    -h | --help) usage; exit 0 ;;
    *) die "unknown option $1" ;;
  esac
done

cd "$(git rev-parse --show-toplevel)"
tree=${tree%/}
tree=${tree#./}
case /$tree/ in
  // | /./ | //* | */../*) die "--tree must name a directory inside the repository, never its root: '$tree'" ;;
esac
[[ $replace == 0 || $command == push ]] || die "--replace applies only to push"

url=$(git remote get-url "$remote" 2>/dev/null) ||
  die "no Git remote named '$remote'; add it with: git remote add $remote https://git.overleaf.com/<project-id>"
if [[ $url =~ ^[A-Za-z][A-Za-z0-9+.-]*://[^/@]*:[^/@]*@ ]]; then
  die "the URL of remote '$remote' holds a password or token; remove it (git remote set-url $remote https://git.overleaf.com/<project-id>) and keep the token in a credential helper"
fi

if [[ -z $branch ]]; then
  branch=${OVERLEAF_BRANCH:-$(git config --get "remote.$remote.overleafBranch" || true)}
fi
if [[ -z $branch ]]; then
  branch=$(git ls-remote --symref "$remote" HEAD 2>/dev/null |
    sed -n 's|^ref: refs/heads/\([^[:space:]]*\)[[:space:]]*HEAD$|\1|p' || true)
fi
branch=${branch:-main}
tracking=refs/remotes/$remote/$branch

fetch() {
  git fetch --quiet --no-tags "$remote" "+refs/heads/$branch:$tracking" ||
    die "cannot fetch branch '$branch' of remote '$remote'; check the remote, its credentials and --branch"
  tip=$(git rev-parse --verify "$tracking^{commit}")
  tip_tree=$(git rev-parse "$tip^{tree}")
}

# "<commit> <tree>" for every commit reachable from $1 whose <tree> directory exists.
local_trees() {
  paste -d' ' <(git rev-list "$1") <(git rev-list "$1" | awk -v t="$tree" '{ print $0 ":" t }' |
    git cat-file --batch-check='%(objectname) %(objecttype)') | awk '$3 == "tree" { print $1, $2 }'
}

# The trees of every commit reachable from the Overleaf tip.
overleaf_trees() {
  git rev-list "$tip" | awk '{ print $0 "^{tree}" }' | git cat-file --batch-check='%(objectname)'
}

head=$(git rev-parse --verify 'HEAD^{commit}')
paper_tree=$(git rev-parse --verify -q "HEAD:$tree") || die "HEAD has no directory $tree"
[[ $(git cat-file -t "$paper_tree") == tree ]] || die "HEAD:$tree is not a directory"

# Classify the Overleaf tip against HEAD: in-sync, overleaf-behind (Overleaf holds a state of
# <tree> that HEAD's history had), overleaf-ahead or diverged (Overleaf holds edits HEAD lacks;
# base is the newest local commit whose <tree> Overleaf had), or unrelated (no shared state).
classify() {
  base=''
  if [[ $tip_tree == "$paper_tree" ]]; then state=in-sync; return; fi
  local trees
  trees=$(local_trees HEAD)
  if awk -v t="$tip_tree" '$2 == t { found = 1 } END { exit !found }' <<<"$trees"; then
    state=overleaf-behind
    return
  fi
  base=$(awk 'NR == FNR { seen[$1] = 1; next } ($2 in seen) { print $1; exit }' \
    <(overleaf_trees) <(printf '%s\n' "$trees"))
  if [[ -z $base ]]; then
    state=unrelated
  elif [[ $(git rev-parse "$base:$tree") == "$paper_tree" ]]; then
    state=overleaf-ahead
  else
    state=diverged
  fi
}

dirty_note() {
  if [[ -n $(git status --porcelain -- "$tree") ]]; then
    echo "NOTE uncommitted changes in $tree/ are not part of HEAD and are not synced"
  fi
}

fetch
classify
printf 'remote %s, branch %s, tree %s/\n' "$remote" "$branch" "$tree"
printf 'Overleaf  %s  tree %s\n' "$(short "$tip")" "$(short "$tip_tree")"
printf 'HEAD      %s  tree %s\n' "$(short "$head")" "$(short "$paper_tree")"

case $command in
  status)
    case $state in
      in-sync) echo "STATE in-sync: Overleaf holds HEAD:$tree" ;;
      overleaf-behind) echo "STATE overleaf-behind: HEAD has changes Overleaf lacks; push sends them" ;;
      overleaf-ahead) echo "STATE overleaf-ahead: Overleaf has edits made after $(short "$base"); pull puts them on a branch" ;;
      diverged) echo "STATE diverged: both sides changed after $(short "$base"); pull, merge the branch, then push" ;;
      unrelated) echo "STATE unrelated: Overleaf and HEAD share no state of $tree/; push --replace overwrites Overleaf" ;;
    esac
    dirty_note
    ;;
  push)
    dirty_note
    if [[ $state == in-sync ]]; then
      echo "OK nothing to push: Overleaf already holds HEAD:$tree"
      exit 0
    fi
    if [[ $state != overleaf-behind && $replace == 0 ]]; then
      die "Overleaf holds edits that HEAD does not have (state $state); run 'pull', merge the sync branch and push again, or push --replace to overwrite them"
    fi
    commit=$(git commit-tree "$paper_tree" -p "$tip" -m "Update from Git: $tree/ of $(short "$head")" -m "Paper-Source-Commit: $head")
    git push --quiet "$remote" "$commit:refs/heads/$branch" ||
      die "the push was rejected; Overleaf may have changed meanwhile, so run status and try again"
    fetch
    [[ $tip_tree == "$paper_tree" ]] ||
      die "after the push Overleaf holds tree $(short "$tip_tree"), not HEAD:$tree $(short "$paper_tree")"
    echo "OK pushed HEAD:$tree to $remote/$branch; Overleaf now holds tree $(short "$tip_tree")"
    ;;
  pull)
    case $state in
      in-sync) echo "OK nothing to pull: Overleaf holds HEAD:$tree"; exit 0 ;;
      overleaf-behind) echo "OK nothing to pull: Overleaf holds an older state of $tree/; push updates it"; exit 0 ;;
      unrelated) die "Overleaf and HEAD share no state of $tree/, so there is no base to merge from; compare by hand" ;;
    esac
    sync_branch=sync/overleaf-$(short "$tip")
    if existing=$(git rev-parse --verify -q "refs/heads/$sync_branch"); then
      [[ $(git rev-parse "$existing:$tree" 2>/dev/null) == "$tip_tree" ]] ||
        die "branch $sync_branch exists and does not hold Overleaf's tree; delete or rename it first"
      echo "OK $sync_branch already holds Overleaf's edits; merge it: git merge $sync_branch"
      exit 0
    fi
    index=$(mktemp "$(git rev-parse --absolute-git-dir)/overleaf-sync-index.XXXXXX")
    trap 'rm -f "$index"' EXIT
    GIT_INDEX_FILE=$index git read-tree "$base"
    GIT_INDEX_FILE=$index git ls-files -z -- "$tree/" | GIT_INDEX_FILE=$index git update-index -z --force-remove --stdin
    GIT_INDEX_FILE=$index git read-tree --prefix="$tree/" "$tip_tree"
    root_tree=$(GIT_INDEX_FILE=$index git write-tree)
    commit=$(git commit-tree "$root_tree" -p "$base" -m "Overleaf edits to $tree/ after $(short "$base")" -m "Overleaf-Commit: $tip")
    git update-ref "refs/heads/$sync_branch" "$commit" ''
    [[ $(git rev-parse "$sync_branch:$tree") == "$tip_tree" ]] || die "$sync_branch does not hold Overleaf's tree"
    echo "OK $sync_branch holds Overleaf's $tree/ on top of $(short "$base"), the last state both sides had"
    echo "   review: git diff $(short "$base") $sync_branch -- $tree"
    echo "   deliver it through a PR into the integration branch, never by merging onto it directly:"
    echo "   git push -u origin $sync_branch && gh pr create --base dev --head $sync_branch"
    ;;
esac
