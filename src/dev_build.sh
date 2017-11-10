pushd "$(dirname "$0")"
# This script will build up all of the in development plugins, then call the
#   build script for the other filters which calls the install script.
#   Only use this script if you have filters with the './filters/dev_*.py' prefix

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

# filters under development:
printf "${BLUE}%s${NORMAL}\n" "--> Attempting to wrap DEV FILTERS in XML..."
printf "${RED}" # Change printout color to red to signify errors
for filename in ./filters/dev_*.py; do
    filtername="${filename%.*}"
    python2 python_filter_generator.py $filename "../build/$(basename "$filtername").xml"
done
printf "${NORMAL}"
sh ./build_plugins.sh
popd
