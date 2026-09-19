#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo 'Usage: ./scripts/new-idea.sh <kebab-case-slug> <title> [raw idea]' >&2
  exit 2
}

slug=${1:-}
title=${2:-}
raw_idea=${3:-$title}

[[ -n "$slug" && -n "$title" ]] || usage
[[ "$slug" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]] || {
  echo "Error: slug must be lowercase kebab-case: $slug" >&2
  exit 2
}

script_dir=$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
repository_root=$(CDPATH= cd -- "$script_dir/.." && pwd)
lab_root=${GROW_IDEAS_ROOT:-$repository_root}
template_dir="$repository_root/ideas/_template"
idea_dir="$lab_root/ideas/$slug"

[[ -d "$template_dir" ]] || {
  echo "Error: template directory not found: $template_dir" >&2
  exit 1
}

[[ ! -e "$idea_dir" ]] || {
  echo "Error: idea already exists: $idea_dir" >&2
  exit 1
}

mkdir -p "$lab_root/ideas"
cp -R "$template_dir" "$idea_dir"

export LAB_TEMPLATE_DATE
export LAB_TEMPLATE_TITLE=$title
export LAB_TEMPLATE_RAW_IDEA=$raw_idea
LAB_TEMPLATE_DATE=$(date +%F)

find "$idea_dir" -type f -name '*.md' -exec perl -pi -e '
  s/\{\{DATE\}\}/$ENV{LAB_TEMPLATE_DATE}/g;
  s/\{\{TITLE\}\}/$ENV{LAB_TEMPLATE_TITLE}/g;
  s/\{\{RAW_IDEA\}\}/$ENV{LAB_TEMPLATE_RAW_IDEA}/g;
' {} +

echo "$idea_dir"
