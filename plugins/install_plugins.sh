
PVPATH="/Applications/ParaView-5.4.0.app/Contents/MacOS/plugins/"
rm -rf $PVPATH
mkdir $PVPATH
cp -r ./xml_plugins/ $PVPATH
