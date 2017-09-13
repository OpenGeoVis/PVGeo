#------ INSTALL TO PARAVIEW ------#
# NOTE: Change this path if needed:
PVPATH="/Applications/ParaView-5.4.0.app/Contents/MacOS/plugins/"
if [ ! -d $PVPATH ]; then
    mkdir $PVPATH
fi
for filename in ../build/*.xml; do
    cp $filename $PVPATH
done
