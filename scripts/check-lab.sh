#!/usr/bin/env bash
set -euo pipefail

script_dir=$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
repository_root=$(CDPATH= cd -- "$script_dir/.." && pwd)
lab_root=${GROW_IDEAS_ROOT:-$repository_root}
requested=${1:-}
errors=0

fail() {
  echo "ERROR: $*" >&2
  errors=$((errors + 1))
}

require_file() {
  [[ -f "$1" ]] || fail "missing file: $1"
}

for relative in \
  AGENTS.md \
  README.md \
  docs/operating-model.md \
  docs/methods.md \
  .agents/skills/refine-product-idea/SKILL.md \
  .agents/skills/refine-product-idea/references/discovery.md \
  .agents/skills/refine-product-idea/references/decision.md \
  .agents/skills/refine-product-idea/references/definition.md \
  .agents/skills/refine-product-idea/references/readiness.md \
  scripts/new-idea.sh \
  scripts/check-lab.sh \
  ideas/_template/README.md \
  ideas/_template/source.md \
  ideas/_template/discovery.md \
  ideas/_template/product.md \
  ideas/_template/specification.md \
  ideas/_template/handoff.md \
  ideas/_template/retrospective.md; do
  require_file "$repository_root/$relative"
done

check_idea() {
  local idea_dir=$1
  local status verdict expected_verdict owner_decisions gate_counts gate_total gate_valid

  for file in README.md source.md discovery.md product.md specification.md handoff.md retrospective.md; do
    require_file "$idea_dir/$file"
  done

  [[ -f "$idea_dir/README.md" ]] || return

  status=$(awk -F': ' '/^status: / {gsub(/"/, "", $2); print $2; exit}' "$idea_dir/README.md")
  verdict=$(awk -F': ' '/^verdict: / {gsub(/"/, "", $2); print $2; exit}' "$idea_dir/README.md")

  case "$status" in
    captured|discovering|deciding|defining|auditing|waiting-for-owner|experiment-ready|adopt-ready|build-ready|parked|stopped) ;;
    *) fail "$idea_dir has invalid status: ${status:-missing}" ;;
  esac

  case "$verdict" in
    undecided|build|validate-first|use-existing|park|stop) ;;
    *) fail "$idea_dir has invalid verdict: ${verdict:-missing}" ;;
  esac

  if rg -q '\{\{(DATE|TITLE|RAW_IDEA)\}\}' "$idea_dir"; then
    fail "$idea_dir contains unresolved template placeholders"
  fi

  if [[ "$status" == build-ready ]]; then
    [[ "$verdict" == build ]] || fail "$idea_dir is build-ready but verdict is not build"
    rg -q '^Applicability: required$' "$idea_dir/specification.md" || fail "$idea_dir build-ready specification is not marked required"
    rg -q '^Applicability: required$' "$idea_dir/handoff.md" || fail "$idea_dir build-ready handoff is not marked required"
    gate_counts=$(awk -F'|' '
      /^## Gates$/ { inside=1; next }
      /^## / { if (inside) exit }
      inside && /^\|/ {
        name=$2; status=$3; evidence=$4
        gsub(/^[[:space:]]+|[[:space:]]+$/, "", name)
        gsub(/^[[:space:]]+|[[:space:]]+$/, "", status)
        gsub(/^[[:space:]]+|[[:space:]]+$/, "", evidence)
        if (name == "gate" || name ~ /^-+$/) next
        total++
        if ((status == "passed" || status == "not-applicable") && evidence != "") valid++
      }
      END { print total + 0, valid + 0 }
    ' "$idea_dir/README.md")
    read -r gate_total gate_valid <<< "$gate_counts"
    [[ "$gate_total" == 6 && "$gate_valid" == 6 ]] || fail "$idea_dir build-ready README needs exactly six passed or justified not-applicable gates with evidence"
    rg -q '^- Verdict: build$' "$idea_dir/handoff.md" || fail "$idea_dir build-ready handoff verdict is not build"
    rg -q '^- Status: build-ready$' "$idea_dir/handoff.md" || fail "$idea_dir build-ready handoff status is not build-ready"
    rg -q '^- P0 open count: 0$' "$idea_dir/handoff.md" || fail "$idea_dir build-ready handoff does not report zero open P0 findings"
    rg -q '^- P1 open count: 0$' "$idea_dir/handoff.md" || fail "$idea_dir build-ready handoff does not report zero open P1 findings"
    rg -q '^- Owner decisions remaining: 0$' "$idea_dir/handoff.md" || fail "$idea_dir build-ready handoff has owner decisions"
    if rg -q '^\| .+ \| .+ \| .+ \| .+ \| .+ \| open \|$' "$idea_dir/handoff.md"; then
      fail "$idea_dir build-ready handoff still contains an open audit finding"
    fi
    if rg -q '^\| (E-001|H-001|T-01|RULE-001|C-001|R-001|A-001) \|[[:space:]]*\|' "$idea_dir"; then
      fail "$idea_dir build-ready artifacts still contain an empty template row"
    fi
    if rg -q '^\|[[:space:]]+\|' "$idea_dir"; then
      fail "$idea_dir build-ready artifacts still contain a blank first-column row"
    fi
    owner_decisions=$(awk '/^## Owner decisions$/ { capture=1; next } /^## / { if (capture) exit } capture { print }' "$idea_dir/README.md")
    printf '%s\n' "$owner_decisions" | rg -q '^なし[。]?$' || fail "$idea_dir build-ready README Owner decisions must be exactly なし"
  fi

  expected_verdict=''
  case "$status" in
    experiment-ready) expected_verdict=validate-first ;;
    adopt-ready) expected_verdict=use-existing ;;
    parked) expected_verdict=park ;;
    stopped) expected_verdict=stop ;;
  esac

  if [[ -n "$expected_verdict" ]]; then
    [[ "$verdict" == "$expected_verdict" ]] || fail "$idea_dir $status status requires $expected_verdict verdict"
    rg -q '^Applicability: not-applicable — .+' "$idea_dir/specification.md" || fail "$idea_dir non-build specification needs a not-applicable reason"
    rg -q '^Applicability: not-applicable — .+' "$idea_dir/handoff.md" || fail "$idea_dir non-build handoff needs a not-applicable reason"
  fi
}

if [[ -n "$requested" ]]; then
  if [[ "$requested" = /* ]]; then
    idea_dir=$requested
  else
    idea_dir="$lab_root/$requested"
  fi
  [[ -d "$idea_dir" ]] || fail "idea directory not found: $idea_dir"
  [[ -d "$idea_dir" ]] && check_idea "$idea_dir"
elif [[ -d "$lab_root/ideas" ]]; then
  while IFS= read -r idea_dir; do
    check_idea "$idea_dir"
  done < <(find "$lab_root/ideas" -mindepth 1 -maxdepth 1 -type d ! -name '_template' | sort)
fi

if (( errors > 0 )); then
  echo "Lab check failed with $errors error(s)." >&2
  exit 1
fi

echo 'Lab check passed.'
