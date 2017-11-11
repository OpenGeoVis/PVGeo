#!/bin/bash
# FOR WINDOWS OPERATING SYSTEM
# ONLY RUN THIS SCRIPT ONCE (at time of installation)

pushd "$(dirname "$0")"
export CYGWIN=winsymlinks:native
# The PVGP Path:
PVGP="$( cd "$(dirname "$0")" ; pwd -P )"

# Use colors if connected to a terminal, and that terminal supports them.
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

#### BEGIN INSTALLATION

#- Check that PVPATH exists: The path to ParaView installation
if [ -z ${PVPATH+x} ]; then
    printf "${RED}%s${NORMAL}\n" "PVPATH is unset. Please set this path in your ~/.bash_profile and re-source."
    return -1
else
    # Path exists so lets get to installing!
    ##### Link PVGPpy to ParaView Python
    # Create symbolic link between PVGPpy and ParaView's Python library
    printf "${PVGP} \n"
    printf "${RED}\n" # Change printout color to red to signify errors

    link_name="${PVGP}/PVGPpy"
    target_dir="${PVPATH}/bin/Lib/site-packages/PVGPpy"
    cmd /c mklink /d "`cygpath -w \"$link_name\"`" "`cygpath -w \"$target_dir\"`"
    #ln -s $PVGP/PVGPpy $PVPATH/bin/Lib/site-packages
    printf "${NORMAL}"

    #### Link the build folder to the Plugins folder in ParaView
    # Create symbolic link for plugins in ParaView's 3rd party plugin folder
    printf "${RED}" # Change printout color to red to signify errors
    link_name="${PVPATH}/bin/plugins"
    target_dir="${PVGP}/plugins"

    printf "trying: %s\n" "`cygpath -w \"$link_name\"`" "`cygpath -w \"$target_dir\"`"

    cmd /c mklink /d "`cygpath -w \"$link_name\"`" "`cygpath -w \"$target_dir\"`"
    # TODO: this will not work for windows or linux users
    #ln -s $PVGP/plugins $PVPATH/bin/
    printf "${NORMAL}"
fi


popd
