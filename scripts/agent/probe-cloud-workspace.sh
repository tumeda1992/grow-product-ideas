#!/usr/bin/env bash
# Read/write probe only. Never replay an interrupted operation here.
set -euo pipefail

task_repo=${1:?repository path required}
probe_token=${2:?probe token required}
expected_branch=${3:-}
[[ "$probe_token" =~ ^[a-zA-Z0-9_-]+$ ]] || exit 2
[[ -d "$task_repo" ]] || exit 20
task_repo=$(cd "$task_repo" && pwd -P)
actual_root=$(git -C "$task_repo" rev-parse --show-toplevel) || exit 20
[[ "$actual_root" == "$task_repo" ]] || exit 23
if [[ -n "$expected_branch" ]]; then
  [[ "$(git -C "$task_repo" branch --show-current)" == "$expected_branch" ]] || exit 23
fi
git -C "$task_repo" rev-parse --verify HEAD >/dev/null || exit 20
probe_file=$(mktemp "$task_repo/.cloud-readiness.XXXXXX") || exit 22
trap 'rm -f -- "$probe_file"' EXIT
printf '%s' "$probe_token" >"$probe_file"
[[ "$(cat "$probe_file")" == "$probe_token" ]] || exit 22
printf 'CLOUD_WORKSPACE_READY:%s\n' "$probe_token"
