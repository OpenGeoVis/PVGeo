#!/bin/bash
# This script will build up all of the XML server manager plugins from the .py
#   files that describe the plugins. There are 4 stages to this script. It will
#   build the filters, then the sources, then the readers, and then it will call
#   the install_plugins script to install the built plugins.
#   NOTE: this will only build plugins with specific prefixes to control the
#       the development/deployment process.
#       The prefixes are as follows:
#           Filters     ->      './filters/filter_*.py'
#           Sources     ->      './artificial_sources/create_*.py'
#           Readers     ->      './readers/read_*.py'

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

# Jump to this directory so we can execute relative scripts
pushd "$(dirname "$0")"

#------ WRAP FILTERS IN XML ------#
printf "${BLUE}${BOLD}%s${NORMAL}\n" "--> Attempting to wrap FILTERS in XML..."

for filename in ./filters/filter_*.py; do
    filtername="${filename%.*}"
    printf "${YELLOW}%s${NORMAL}\n" "    --> $(basename "$filtername")"
    printf "${RED}" # Change printout color to red to signify errors
    python2 python_filter_generator.py $filename "../build/$(basename "$filtername").xml"
done
printf "${NORMAL}"

#------ WRAP SOURCES IN XML ------#
printf "${BLUE}${BOLD}%s${NORMAL}\n" "--> Attempting to wrap SOURCES in XML..."
for filename in ./artificial_sources/create_*.py; do
    filtername="${filename%.*}"
    printf "${YELLOW}%s${NORMAL}\n" "    --> $(basename "$filtername")"
    printf "${RED}" # Change printout color to red to signify errors
    python2 python_filter_generator.py $filename "../build/$(basename "$filtername").xml"
done
printf "${NORMAL}"
#------ WRAP READERS IN XML ------#
printf "${BLUE}${BOLD}%s${NORMAL}\n" "--> Attempting to wrap READERS in XML..."
for filename in ./readers/read_*.py; do
    filtername="${filename%.*}"
    printf "${YELLOW}%s${NORMAL}\n" "    --> $(basename "$filtername")"
    printf "${RED}" # Change printout color to red to signify errors
    python2 python_filter_generator.py $filename "../build/$(basename "$filtername").xml"
done
printf "${NORMAL}"
#------ INSTALL ------#
sh ./install_plugins.sh
popd
