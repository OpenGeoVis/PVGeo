#!/bin/bash
# This script will clean out all the built plugins in the build/ driectory as
#   well as remove ALL XML plugins in the PVPLUGINPATH directory. Be careful
#   using this script unless you know what you are doing. I use this script to
#   clean out depricated plugins or for making sure there are no leftovers when
#   renaming a filter.

pushd "$(dirname "$0")"
pushd $PVPLUGINPATH
# Removes all of the XML files from th ParaView plugin path
rm -f *.xml
popd
# Removes all XML files in th ../build/ directory
rm -f ../build/*.xml
popd
