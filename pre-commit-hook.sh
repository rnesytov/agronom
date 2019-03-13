#!/usr/bin/env bash

# Run without arguments for checking files added to commit with 'git add'
# Run with --all for checking all modified files

set -eu  # Enable strict sh mode

ARG=${1:-}  # assign empty string if not defined
case "$ARG" in
    --install)
        # install git hook. If file exists, script fails.
        # Existing file should be manually removed before installing hook
        ln -s "../../pre-commit-hook.sh" "$(dirname "$0")/.git/hooks/pre-commit"
        exit 0
        ;;
    --all)
        # for scanning all changed files (for Pycharm external tool)
        COMPARE_ARG=HEAD
        ;;
    *)
        # for scanning only staged for commit files (for git hook)
        COMPARE_ARG='--cached'
        ;;
esac

set +eu  # Disable strict sh before sourcing 3rd-party script
. myvenv/bin/activate
set -eu  # Reenable strict mode

exec ./flake8.sh "agronom/" "$COMPARE_ARG"
