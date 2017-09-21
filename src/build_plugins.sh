#!/bin/bash
pushd "$(dirname "$0")"

#------ WRAP FILTERS IN XML ------#
for filename in ./filters/filter_*.py; do
    filtername="${filename%.*}"
    python2 python_filter_generator.py $filename "../build/$(basename "$filtername").xml"
done
# filters under development:
for filename in ./filters/dev_*.py; do
    filtername="${filename%.*}"
    python2 python_filter_generator.py $filename "../build/$(basename "$filtername").xml"
done

#------ WRAP SOURCES IN XML ------#
for filename in ./artificial_sources/create_*.py; do
    filtername="${filename%.*}"
    python2 python_filter_generator.py $filename "../build/$(basename "$filtername").xml"
done

#------ WRAP READERS IN XML ------#
for filename in ./readers/read_*.py; do
    filtername="${filename%.*}"
    python2 python_filter_generator.py $filename "../build/$(basename "$filtername").xml"
done

#------ INSTALL ------#
sh ./install_plugins.sh
popd
