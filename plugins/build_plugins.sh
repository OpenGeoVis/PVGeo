#!/bin/bash

#------ FILTERS ------#
# Table To ImageData Filter
python python_filter_generator.py filters_source_code/filter_table_to_image_data.py xml_plugins/table_to_image_data.xml

# Flip ImageData Axis Filter
python python_filter_generator.py filters_source_code/filter_flip_image_data_axii.py xml_plugins/filter_flip_image_data_axii.xml

# filter_unstructured_points_to_image_data
python python_filter_generator.py filters_source_code/filter_unstructured_grid_maker.py xml_plugins/filter_unstructured_grid_maker.xml

# Time to Space stuff
python python_filter_generator.py filters_source_code/filter_time_to_space.py xml_plugins/filter_time_to_space.xml

# Reshape Table
python python_filter_generator.py filters_source_code/filter_reshape_table.py xml_plugins/filter_reshape_table.xml



#------ READERS ------#
# Read Binary File To Table
python python_filter_generator.py readers_source_code/read_binary_file_to_table.py xml_plugins/read_binary_file_to_table.xml

# Read Delimited Files To Table
python python_filter_generator.py readers_source_code/read_delimited_file_to_table.py xml_plugins/read_delimited_file_to_table.xml

# Read GEO EAS Files To Table
python python_filter_generator.py readers_source_code/read_geoeas_file_to_table.py xml_plugins/read_geoeas_file_to_table.xml

sh ./install_plugins.sh
