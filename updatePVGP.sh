#!/bin/bash
# This is the update script for the repository for those that are unfimliar with
#   using Git and do not want to mess with the scripts in this repo.

pushd "$(dirname "$0")"

# Pull from github
git pull origin master

pushd ./src
sh ./clean_out.sh
sh ./build_plugins.sh
popd
popd
