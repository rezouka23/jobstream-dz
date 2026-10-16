#!/usr/bin/env bash
set -Eeuo pipefail

REMOTE_HOST="${JOBSTREAM_DEPLOY_HOST:-45.154.98.205}"
REMOTE_USER="${JOBSTREAM_DEPLOY_USER:-root}"
REMOTE_PORT="${JOBSTREAM_DEPLOY_PORT:-22}"
REMOTE_PATH="${JOBSTREAM_DEPLOY_PATH:-/opt/jobstreamdz}"
API_PM2_NAME="${JOBSTREAM_API_PM2_NAME:-jobstreamdz-api}"
PUBLISHER_PM2_NAME="${JOBSTREAM_PUBLISHER_PM2_NAME:-jobstreamdz-publisher}"

MODE="dry-run"
DELETE_REMOTE=true
AUTO_RESTART=true

usage() {
  cat <<'EOF'
Usage: scripts/deploy-changed.sh [--dry-run|--apply] [--no-delete] [--no-restart]

Compares this checkout against the deployed server and uses rsync to transfer
only changed files. Runtime data and secrets are intentionally excluded.

Default mode is --dry-run.

Environment overrides:
  JOBSTREAM_DEPLOY_HOST        default: 45.154.98.205
  JOBSTREAM_DEPLOY_USER        default: root
  JOBSTREAM_DEPLOY_PORT        default: 22
  JOBSTREAM_DEPLOY_PATH        default: /opt/jobstreamdz
  JOBSTREAM_API_PM2_NAME       default: jobstreamdz-api
  JOBSTREAM_PUBLISHER_PM2_NAME default: jobstreamdz-publisher

Authentication:
  Prefer SSH keys. If using password auth, install sshpass and run with:
  SSHPASS='your-password' scripts/deploy-changed.sh --apply
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run|--check)
      MODE="dry-run"
      ;;
    --apply|--deploy)
      MODE="apply"
      ;;
    --no-delete)
      DELETE_REMOTE=false
      ;;
    --no-restart)
      AUTO_RESTART=false
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
  shift
done

if [[ ! -d jobstreamdz || ! -d landing || ! -f requirements.txt ]]; then
  echo "Run this script from the project root." >&2
  exit 1
fi

if ! command -v rsync >/dev/null 2>&1; then
  echo "rsync is required locally." >&2
  exit 1
fi

if ! command -v ssh >/dev/null 2>&1; then
  echo "ssh is required locally." >&2
  exit 1
fi

use_sshpass=false
if [[ -n "${SSHPASS:-}" ]]; then
  if ! command -v sshpass >/dev/null 2>&1; then
    echo "SSHPASS is set but sshpass is not installed." >&2
    exit 1
  fi
  use_sshpass=true
fi

REMOTE="${REMOTE_USER}@${REMOTE_HOST}"
SSH_ARGS=(-p "$REMOTE_PORT" -o StrictHostKeyChecking=accept-new)
RSYNC_RSH="ssh -p ${REMOTE_PORT} -o StrictHostKeyChecking=accept-new"

run_ssh() {
  if [[ "$use_sshpass" == true ]]; then
    sshpass -e ssh "${SSH_ARGS[@]}" "$REMOTE" "$@"
  else
    ssh "${SSH_ARGS[@]}" "$REMOTE" "$@"
  fi
}

run_rsync() {
  local -a rsync_cmd=(rsync)
  rsync_cmd+=(
    --archive
    --checksum
    --human-readable
    --itemize-changes
    --no-owner
    --no-group
    --omit-dir-times
    --out-format=%i\ %n%L
    -e "$RSYNC_RSH"
  )

  if [[ "$DELETE_REMOTE" == true ]]; then
    rsync_cmd+=(--delete)
  fi

  if [[ "$MODE" == "dry-run" ]]; then
    rsync_cmd+=(--dry-run)
  fi

  rsync_cmd+=(
    --exclude '/.*'
    --exclude '.env'
    --exclude '.venv/'
    --exclude 'venv/'
    --exclude '__pycache__/'
    --exclude '*.pyc'
    --exclude '*.pyo'
    --exclude '*.pyd'
    --exclude '*.bak'
    --exclude 'google-service-account.json'
    --exclude 'seen_telegram_jobs.json'
    --exclude 'seen_telegram_jobs.json.bak.*'
    --exclude 'digest_history/'
    --exclude 'latest_digest.json'
    --exclude 'latest_remote_digest.json'
    --exclude 'landing/PROJECT_SUMMARY.md'
    --exclude 'landing/product-intro*/'
    --exclude 'bin/'
    --exclude 'docs/'
    --exclude 'skills/'
    --exclude 'skills-lock.json'
    ./
    "${REMOTE}:${REMOTE_PATH}/"
  )

  if [[ "$use_sshpass" == true ]]; then
    sshpass -e "${rsync_cmd[@]}"
  else
    "${rsync_cmd[@]}"
  fi
}

echo "Checking remote ${REMOTE}:${REMOTE_PATH} ..."
run_ssh "command -v rsync >/dev/null && test -d '$REMOTE_PATH' && test -d '$REMOTE_PATH/.venv' && command -v pm2 >/dev/null"

plan_file="$(mktemp)"
trap 'rm -f "$plan_file"' EXIT

run_rsync | tee "$plan_file"

if [[ ! -s "$plan_file" ]]; then
  echo "No deployable file changes detected."
  exit 0
fi

requirements_changed=false
python_changed=false

if grep -Eq '(^| )requirements\.txt($| )' "$plan_file"; then
  requirements_changed=true
fi

if grep -Eq '(^| )(main\.py|jobstreamdz/.*\.py)($| )' "$plan_file"; then
  python_changed=true
fi

if [[ "$MODE" == "dry-run" ]]; then
  echo
  echo "Dry run only. Re-run with --apply to deploy these changes."
  exit 0
fi

if [[ "$AUTO_RESTART" != true ]]; then
  echo "Deployment complete. PM2 restart skipped by --no-restart."
  exit 0
fi

if [[ "$requirements_changed" == true || "$python_changed" == true ]]; then
  echo "Refreshing Python runtime and restarting PM2 apps ..."
  run_ssh bash -s -- "$REMOTE_PATH" "$API_PM2_NAME" "$PUBLISHER_PM2_NAME" "$requirements_changed" <<'REMOTE_SCRIPT'
set -Eeuo pipefail
remote_path="$1"
api_pm2_name="$2"
publisher_pm2_name="$3"
requirements_changed="$4"

cd "$remote_path"

if [[ "$requirements_changed" == true ]]; then
  .venv/bin/pip install -r requirements.txt
fi

.venv/bin/python -m compileall -q jobstreamdz main.py
pm2 restart "$api_pm2_name"
pm2 restart "$publisher_pm2_name"
pm2 save
curl -fsS http://127.0.0.1:8000/healthz >/dev/null
REMOTE_SCRIPT
  echo "Deployment complete. API and publisher restarted."
else
  echo "Deployment complete. No Python/runtime restart needed."
fi
