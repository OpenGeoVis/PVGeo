#!/bin/bash
# This script will clean out all the built plugins in the build/ driectory as
#   well as remove ALL XML plugins in the PVPLUGINPATH directory. Be careful
#   using this script unless you know what you are doing. I use this script to
#   clean out depricated plugins or for making sure there are no leftovers when
#   renaming a filter.
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

pushd "$(dirname "$0")"
printf "${BLUE}%s${NORMAL}\n" "Jumping to the PVPLUGINPATH..."
pushd $PVPLUGINPATH
# Removes all of the XML files from th ParaView plugin path
printf "${BLUE}%s${NORMAL}\n" "Cleaning out old plugins..."
rm -f *.xml
popd
# Removes all XML files in th ../build/ directory
printf "${BLUE}%s${NORMAL}\n" "Back to ParaViewGeophysics repo."
printf "${BLUE}%s${NORMAL}\n" "Cleaning out old plugins..."
rm -f ../build/*.xml
popd
