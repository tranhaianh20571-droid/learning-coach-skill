#!/usr/bin/env bash

set -euo pipefail

force=0
source_dir=""
codex_home="${CODEX_HOME:-$HOME/.codex}"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --source)
      source_dir="$2"
      shift 2
      ;;
    --codex-home)
      codex_home="$2"
      shift 2
      ;;
    --force)
      force=1
      shift
      ;;
    -h|--help)
      cat <<'EOF'
用法：
  ./tools/install-learning-coach.sh [--force] [--source PATH] [--codex-home PATH]

说明：
  将仓库内的 learning-coach skill 安装到 ~/.codex/skills/learning-coach
EOF
      exit 0
      ;;
    *)
      echo "未知参数：$1" >&2
      exit 1
      ;;
  esac
done

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "$script_dir/.." && pwd)"

if [[ -z "$source_dir" ]]; then
  source_dir="$repo_root"
fi

if [[ ! -d "$source_dir" ]]; then
  echo "找不到 skill 源目录：$source_dir" >&2
  exit 1
fi

skills_root="$codex_home/skills"
target_dir="$skills_root/learning-coach"

mkdir -p "$skills_root"

if [[ -e "$target_dir" ]]; then
  if [[ "$force" -ne 1 ]]; then
    echo "目标目录已存在：$target_dir" >&2
    echo "如需覆盖，请重新执行并加上 --force。" >&2
    exit 1
  fi
  rm -rf "$target_dir"
fi

mkdir -p "$target_dir"
for name in SKILL.md agents assets references scripts; do
  if [[ -e "$source_dir/$name" ]]; then
    cp -R "$source_dir/$name" "$target_dir/$name"
  fi
done
find "$target_dir" -type d -name "__pycache__" -prune -exec rm -rf {} +

echo
echo "安装完成。"
echo "skill 目录：$target_dir"
echo
echo "推荐下一步："
echo '1. 在 Codex 里直接说：使用 $learning-coach 帮我开始一个新的学习项目'
echo "2. 或手动运行：python \"$target_dir/scripts/learn.py\""
