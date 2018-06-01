#!/bin/bash
# This is the update script for the repository for those that are unfimliar with
#   using Git and do not want to mess with the scripts in this repo.

pushd "$(dirname "$0")"

# Use colors, but only if connected to a terminal, and that terminal
# supports them.
if which tput >/dev/null 2>&1; then
    ncolors=$(tput colors)
fi
if [ -t 1 ] && [ -n "$ncolors" ] && [ "$ncolors" -ge 8 ]; then
    RED="$(tput setaf 1)"
    GREEN="$(tput setaf 2)"
    YELLOW="$(tput setaf 3)"
    BLUE="$(tput setaf 4)"
    BOLD="$(tput bold)"
    UND="$(tput smul)"
    NORMAL="$(tput sgr0)"
else
    RED=""
    GREEN=""
    YELLOW=""
    BLUE=""
    BOLD=""
    NORMAL=""
fi

printf "${BLUE}${BOLD}%s${NORMAL}\n" "--> Updating PVGeophysics..."

#  Pull from github
if git pull --rebase --stat origin master
then
    # Succesful update from GitHub
    printf "${GREEN}${BOLD}%s${NORMAL}\n" "--> Tsjakka!! PVGeophysics has been updated and/or is at the current version."
    # Now lets clean out the old version
    pushd ./src
    # Now lets build and install everything (running a build incase user has their own plugins added to thier fork)
    sh ./build_plugins.sh
    popd
    printf "${GREEN}${BOLD}%s${NORMAL}\n" "--> All plugins should be up to date and installed."
    printf "${BLUE}${BOLD}%s${NORMAL}\n" "--> Learn more about updates and features to come on the Read the Docs page at:"
    printf "${BLUE}${BOLD}${UND}%s${NORMAL}\n" "https://banesullivan.github.io/PVGeophysics/"
else
  printf "${RED}${BOLD}%s${NORMAL}\n" '--> There was an error updating. Try again later or run a `git status` to see if you have unstaged changes. If you have made changes to files in the repo, you will need to stage them.'
fi

popd
