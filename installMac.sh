#!/bin/bash
# FOR MAC OS X OPERATING SYSTEM
# ONLY RUN THIS SCRIPT ONCE (at time of installation)

pushd "$(dirname "$0")"
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

#if [ "$EUID" -ne 0 ]
#  then echo "Please run as root. Run script as: sudo sh./installMac.sh"
#  exit
#fi

pvplist="/Library/LaunchAgents/pvgp.PV_PLUGIN_PATH.plist"
pyplist="/Library/LaunchAgents/pvgp.PYTHONPATH.plist"

# check if the .plist files exits. Remove if so.
if [ -f ${pvplist} ]; then
    printf "${YELLOW}%s${NORMAL}\n" "${pvplist} Currently exists. Overwiting..."
    printf "${RED}%s${NORMAL}\n" "You will need to log out and back in after this script executes."
    sudo rm -f $pvplist
fi
if [ -f ${pyplist} ]; then
    printf "${YELLOW}%s${NORMAL}\n" "${pyplist} Currently exists. Overwiting..."
    printf "${RED}%s${NORMAL}\n" "You will need to log out and back in after this script executes."
    sudo rm -f $pyplist
fi

# Unsetting the PV_PLUGIN_PATH variable
printf "${RED}"
launchctl unsetenv PV_PLUGIN_PATH
printf "${NORMAL}"
printf "${GREEN}%s${NORMAL}\n" "Setting environmental variables immediate use..."
printf "${RED}"
launchctl setenv PV_PLUGIN_PATH ${PVGP}/plugins
launchctl setenv PYTHONPATH $PYTHONPATH:${PVGP}/
printf "${NORMAL}"

# Write plst files to LaunchAgents so Paths are always set at login
printf "${GREEN}%s${NORMAL}\n" "Writing environmental variables to '/Library/LaunchAgents/'..."
cat << EOF | sudo tee ${pvplist}
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
  <plist version="1.0">
  <dict>
  <key>Label</key>
  <string>setenv.PV_PLUGIN_PATH</string>
  <key>ProgramArguments</key>
  <array>
    <string>/bin/launchctl</string>
    <string>setenv</string>
    <string>PV_PLUGIN_PATH</string>
    <string>${PVGP}/plugins</string>
  </array>
  <key>RunAtLoad</key>
  <true/>
  <key>ServiceIPC</key>
  <false/>
</dict>
</plist>
EOF

cat << EOF | sudo tee ${pyplist}
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
  <plist version="1.0">
  <dict>
  <key>Label</key>
  <string>setenv.PYTHONPATH</string>
  <key>ProgramArguments</key>
  <array>
    <string>/bin/launchctl</string>
    <string>setenv</string>
    <string>PYTHONPATH</string>
    <string>${PYTHONPATH}:${PVGP}/</string>
  </array>
  <key>RunAtLoad</key>
  <true/>
  <key>ServiceIPC</key>
  <false/>
</dict>
</plist>
EOF

printf "${GREEN}%s${NORMAL}\n" "All Finished! Any version of ParaView will launch with the PVGP plugins and Python Module."

printf "${YELLOW}%s${NORMAL}\n" "Virtual Reality Users: Beware that your version of ParaView has Python included as errors/crashes will occur if you use these plugins without Python."

popd
