#!/usr/bin/env bash

# Used by CI and pre commit hook
# Should be called from repo root dir

set -eu

DIRECTORY="${1:-.}"

if [ "$#" = "2" ];
then
    # git hook mode, check changed files
    COMPARE_ARG="$2"
    function get_files {
        git diff "$COMPARE_ARG" --name-status "$DIRECTORY" | awk '$1 != "D" {print $2}' | grep -E '[.]py$'
    }
else
    # ci mode, check all files
    function get_files {
        find "$DIRECTORY" -iname '*.py'
    }
fi

# casual check for non-settings .py files
NON_SETTINGS_FAILED=false
IGNORED_PATHS_REGEX='/migrations/|/settings/|/thirdparty/|/myvenv/'
if FILES=`get_files | grep -vE "$IGNORED_PATHS_REGEX"`
then
    flake8 `realpath $FILES` || NON_SETTINGS_FAILED=true
fi

# more specific linter config for settings-related .py-files
SETTINGS_FAILED=false
if FILES=`get_files | grep -v /migrations/ | grep /settings/`
then
    [ "$FILES" = "" ] \
        || flake8 --append-config=bakend/settings/.flake8 `realpath $FILES` \
        || SETTINGS_FAILED=true
fi

if "$NON_SETTINGS_FAILED" || "$SETTINGS_FAILED"
then
    exit 1
else
    exit 0
fi
