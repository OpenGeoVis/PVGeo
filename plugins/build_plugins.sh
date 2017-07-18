#!/bin/bash

#------ FILTERS ------#
# Table To ImageData Filter
python python_filter_generator.py filters_source_code/filter_table_to_image_data.py xml_plugins/table_to_image_data.xml

# Flip ImageData Axis Filter
python python_filter_generator.py filters_source_code/filter_flip_image_data_axis.py xml_plugins/flip_image_data_axis.xml


#------ READERS ------#
# Read Binary File To Table
python python_filter_generator.py readers_source_code/read_binary_file_to_table.py xml_plugins/read_binary_file_to_table.xml

# Read Delimited Files To Table
python python_filter_generator.py readers_source_code/read_delimited_file_to_table.py xml_plugins/read_delimited_file_to_table.xml

# Read GEO EAS Files To Table
python python_filter_generator.py readers_source_code/read_geoeas_file_to_table.py xml_plugins/read_geoeas_file_to_table.xml
