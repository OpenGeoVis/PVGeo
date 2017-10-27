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
  ITAL="$(tput sitm)"
  NORMAL="$(tput sgr0)"
else
  RED=""
  GREEN=""
  YELLOW=""
  BLUE=""
  BOLD=""
  NORMAL=""
fi

printf "${BLUE}%s${NORMAL}\n" "Updating ParaViewGeophysics..."

if git pull --rebase --stat origin master
then
  pushd ./src
  sh ./clean_out.sh
  sh ./build_plugins.sh
  popd
  popd
  printf "${GREEN}%s${NORMAL}\n" "Tsjakka!! ParaViewGeophysics has been updated and/or is at the current version."
  printf "${GREEN}%s${NORMAL}\n" "All plugins should be up to date and installed."
  printf "${BLUE}${BOLD}%s${ITAL}%s${NORMAL}\n" "To learn more about updates and featuresto come, check out the Read the Docs page at:"," http://paraviewgeophysics.readthedocs.io"
else
  printf "${RED}%s${NORMAL}\n" 'There was an error updating. Try again later?'
fi

# Pull from github
#git pull origin master
