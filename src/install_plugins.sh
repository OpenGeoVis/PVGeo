#!/bin/bash
# This script will install all of the plugins currently built and sitting in
#   the build/ directory. It performs a simple copy of those plugins into the
#   PVPLUGINPATH directory for ParaView which you should set up according to
#   the README

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
printf "${BLUE}%s${NORMAL}\n" "Installing all the plugins..."
#------ INSTALL TO PARAVIEW ------#
if [ ! -d $PVPLUGINPATH ]; then
    mkdir $PVPLUGINPATH
fi
for filename in ../build/*.xml; do
    cp $filename $PVPLUGINPATH
done
popd
