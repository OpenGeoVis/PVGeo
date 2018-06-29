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

# Bump the version if asked to
if [ "$#" -eq 1 ]; then
    pushd ..
    if ! (bumpversion --no-tag $1) &> /dev/null; then
        # handle error
        echo "Git working directory is not clean."
        popd
        exit 1
    fi
    popd
fi

# Clean out the plugins directory
printf "${RED}"
for plugin in ../plugins/*.xml; do
    rm "${plugin}"
done
printf "${NORMAL}"

#------ PLUGINS IN A SUBDIRECTORY ------#
printf "${BLUE}${BOLD}%s${NORMAL}\n" "--> Attempting to build plugin categories..."
for directory in ./*/; do
    #dirname="${directory%.*}"
    printf "${YELLOW}%s${NORMAL}\n" "   |--> $(basename "$directory")"
    printf "${RED}" # Change printout color to red to signify errors
    python python_filter_generator.py $directory "../plugins"
done
printf "${NORMAL}"

# Commit the build for the new version
if [ "$#" -eq 1 ]; then
    sh _commit_bump.sh $1
fi

popd
