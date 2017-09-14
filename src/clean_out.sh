#!/bin/bash

PVPATH="/Applications/ParaView-5.4.0.app/Contents/MacOS/plugins/"
pushd $PVPATH
rm -f *.xml
popd
rm -f ../build/*.xml
