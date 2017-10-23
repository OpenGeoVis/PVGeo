#!/bin/bash
# This script will install all of the plugins currently built and sitting in
#   the build/ directory. It performs a simple copy of those plugins into the
#   PVPLUGINPATH directory for ParaView which you should set up according to
#   the README
pushd "$(dirname "$0")"
#------ INSTALL TO PARAVIEW ------#
if [ ! -d $PVPLUGINPATH ]; then
    mkdir $PVPLUGINPATH
fi
for filename in ../build/*.xml; do
    cp $filename $PVPLUGINPATH
done
popd
