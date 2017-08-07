#!/bin/bash

#------ FILTERS ------#
for filename in ./filters_source_code/filter_*.py; do
    filtername="${filename%.*}"
    python python_filter_generator.py $filename "./xml_plugins/$(basename "$filtername").xml"
done


#------ READERS ------#
for filename in ./readers_source_code/read_*.py; do
    filtername="${filename%.*}"
    python python_filter_generator.py $filename "./xml_plugins/$(basename "$filtername").xml"
done

#------ INSTALL ------#
sh ./install_plugins.sh
