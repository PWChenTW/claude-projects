#!/bin/bash

# Claude Code Statusline Script for General Project Template
# This script generates a rich, informative statusline for Claude Code

# Read JSON input from stdin
input=$(cat)

# Extract data from JSON
model_name=$(echo "$input" | jq -r '.model.display_name // "Claude"')
current_dir=$(echo "$input" | jq -r '.workspace.current_dir // ""')
session_id=$(echo "$input" | jq -r '.session_id // ""')

# Get short directory name (last 2 components if path is long)
if [[ -n "$current_dir" ]]; then
    # Replace home directory with ~
    short_dir=${current_dir/#$HOME/\~}
    # If path has more than 2 components, show only last 2
    IFS='/' read -ra PATH_PARTS <<< "$short_dir"
    if [[ ${#PATH_PARTS[@]} -gt 3 ]]; then
        short_dir=".../${PATH_PARTS[-2]}/${PATH_PARTS[-1]}"
    fi
else
    short_dir="~"
fi

# Get git branch if in a git repository
git_info=""
if git rev-parse --git-dir >/dev/null 2>&1; then
    branch=$(git branch --show-current 2>/dev/null || echo "detached")
    # Get git status indicators
    if [[ -n $(git status --porcelain 2>/dev/null) ]]; then
        git_status="●"  # Has changes
    else
        git_status=""   # Clean
    fi
    git_info="🌿 $branch$git_status"
fi

# Detect framework type if CLAUDE.md exists
framework_info=""
if [[ -f "CLAUDE.md" && -f "CLAUDE_OPTIMIZED.md" ]]; then
    # Check which one was modified more recently or has more lines
    if [[ "CLAUDE_OPTIMIZED.md" -nt "CLAUDE.md" ]] || [[ $(wc -l < "CLAUDE_OPTIMIZED.md") -lt $(wc -l < "CLAUDE.md") ]]; then
        framework_info="⚡ Optimized"
    else
        framework_info="🏗️ Original"
    fi
elif [[ -f "CLAUDE_OPTIMIZED.md" ]]; then
    framework_info="⚡ Optimized"
elif [[ -f "CLAUDE.md" ]]; then
    framework_info="🏗️ Original"
fi

# Session status indicator (based on session ID length/format)
session_status="🟢"  # Default to active
if [[ -z "$session_id" ]]; then
    session_status="🔴"
elif [[ ${#session_id} -lt 8 ]]; then
    session_status="🟡"
fi

# Get current time
current_time=$(date '+%H:%M')

# Build statusline with colors and emojis
statusline=""

# Time at the beginning
statusline+="$(printf '\033[1;33m%s\033[0m' "$current_time")"

# Model info with icon
statusline+=" 🤖 $(printf '\033[1;36m%s\033[0m' "$model_name")"

# Current directory
statusline+=" 📁 $(printf '\033[1;32m%s\033[0m' "$short_dir")"

# Git info (if available)
if [[ -n "$git_info" ]]; then
    statusline+=" $git_info"
fi

# Framework info (if available)
if [[ -n "$framework_info" ]]; then
    statusline+=" $framework_info"
fi

# Session status
statusline+=" $session_status"

# Output the statusline
printf "%s" "$statusline"