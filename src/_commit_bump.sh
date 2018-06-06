#!/bin/bash
VERSION="0.3.0"

# Build on bumped version
if [ "$#" -eq 1 ]; then
    # Jump to this directory so we can execute relative scripts
    pushd "$(dirname "$0")"
    git add ..
    git commit -m "Build on version: ${VERSION}"
    popd
fi
