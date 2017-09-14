#!/bin/bash

# Pull from github
git pull origin master

pushd ./src
sh ./clean_out.sh
sh ./build_plugins.sh
popd
