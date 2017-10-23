#!/bin/bash
# This script will build up all of the XML server manager plugins from the .py
#   files that describe the plugins. There are 4 stages to this script. It will
#   build the filters, then the sources, then the readers, and then it will call
#   the install_plugins script to install the built plugins.
#   NOTE: this will only build plugins with specific prefixes to control the
#       the development/deployment process.
#       The prefixes are as follows:
#           Filters     ->      './filters/filter_*.py'
#           Sources     ->      './artificial_sources/create_*.py'
#           Readers     ->      './readers/read_*.py'

pushd "$(dirname "$0")"

#------ WRAP FILTERS IN XML ------#
for filename in ./filters/filter_*.py; do
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
