#!/bin/bash
pushd "$(dirname "$0")"
pushd $PVPLUGINPATH
rm -f *.xml
popd
rm -f ../build/*.xml
popd
