#!/bin/bash
pushd "$(dirname "$0")"
#------ INSTALL TO PARAVIEW ------#
if [ ! -d $PVPLUGINPATH ]; then
    mkdir $PVPLUGINPATH
fi
for filename in ../build/*.xml; do
    cp $filename $PVPLUGINPATH
done
popd
