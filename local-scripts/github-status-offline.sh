#!/bin/bash
# Marks you as Offline on your GitHub profile badge.
# Called by hypridle on-timeout (after 10 minutes of inactivity).
# Requires: ~/.config/github-status/config with GIST_ID and GITHUB_TOKEN set.

CONFIG="$HOME/.config/github-status/config"
if [[ ! -f "$CONFIG" ]]; then
  echo "Missing config at $CONFIG" >&2
  exit 1
fi
source "$CONFIG"

PAYLOAD='{"files":{"status.json":{"content":"{\"schemaVersion\":1,\"label\":\"status\",\"message\":\"Offline\",\"color\":\"555555\",\"namedLogo\":\"linux\",\"logoColor\":\"white\"}"}}}'

curl -s -o /dev/null -X PATCH \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  "https://api.github.com/gists/$GIST_ID" \
  -d "$PAYLOAD"
