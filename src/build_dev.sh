pushd "$(dirname "$0")"
# This script will build up all of the in development plugins, then call the
#   build script for the other filters which calls the install script.
#   Only use this script if you have filters with the './filters/dev_*.py' prefix

# filters under development:
for filename in ./filters/dev_*.py; do
    filtername="${filename%.*}"
    python2 python_filter_generator.py $filename "../build/$(basename "$filtername").xml"
done
sh ./build_plugins.sh
popd
