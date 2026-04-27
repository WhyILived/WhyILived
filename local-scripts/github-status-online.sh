#!/bin/bash
# Marks you as Online on your GitHub profile badge.
# Called by hypridle on-resume (when you come back from idle).
# Requires: ~/.config/github-status/config with GIST_ID and GITHUB_TOKEN set.

CONFIG="$HOME/.config/github-status/config"
if [[ ! -f "$CONFIG" ]]; then
  echo "Missing config at $CONFIG" >&2
  exit 1
fi
source "$CONFIG"

PAYLOAD=$(printf '{"files":{"status.json":{"content":"{\"schemaVersion\":1,\"label\":\"status\",\"message\":\"Online \\u00b7 Arch Linux / Hyprland\",\"color\":\"brightgreen\",\"namedLogo\":\"linux\",\"logoColor\":\"white\"}"}}}')

curl -s -o /dev/null -X PATCH \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  "https://api.github.com/gists/$GIST_ID" \
  -d "$PAYLOAD"
