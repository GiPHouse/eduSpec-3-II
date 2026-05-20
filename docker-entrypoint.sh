#!/bin/sh
set -eu

DATA_DIR="${EDUSPEC_DATA_DIR:-${DATA_DIR:-/data}}"
export EDUSPEC_DATA_DIR="$DATA_DIR"

if [ -n "${EDUSPEC_DATA_GIT_URL:-}" ]; then
    if [ -d "$DATA_DIR" ] && [ "$(find "$DATA_DIR" -mindepth 1 -maxdepth 1 | head -n 1)" ]; then
        echo "EDUSPEC_DATA_GIT_URL is set, but EDUSPEC_DATA_DIR '$DATA_DIR' is not empty." >&2
        echo "Use an empty directory for Git mode, or mount an existing datasource without EDUSPEC_DATA_GIT_URL." >&2
        exit 1
    fi

    mkdir -p "$DATA_DIR"

    if [ -n "${EDUSPEC_DATA_GIT_REF:-}" ]; then
        git clone --depth 1 --branch "$EDUSPEC_DATA_GIT_REF" "$EDUSPEC_DATA_GIT_URL" "$DATA_DIR"
    else
        git clone --depth 1 "$EDUSPEC_DATA_GIT_URL" "$DATA_DIR"
    fi
fi

exec "$@"
