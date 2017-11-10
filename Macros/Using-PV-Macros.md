More to come!

<!--- TODO --->

# What are Macros?
Macros are scripts that complete tedious or recurring tasks either in ParaViews gui or in ParaView's batch processing environment. We will commonly use macros for the loading of scenes and for the exporting of scenes. It is often helpful to set up a macro for a project so that you can easily run all the visualization processing at once each time you update your model files or create new versions of your data. We will also use macros to complete common tasks like saving screenshots of isometric views of a data seen or tedious tasks like making numerous slices of a single data set along a line.

The macros that we publish will be defined in the PVGPpy module for easy use and we will provide some templates in the `macros/` directory for building your own macros. More details to come!

# How to Run Macros
Use the python shell from 'Tools->Python Shell' in the ParaView GUI. DO NOT IMPORT THE macros as they become static in the ParaView GUI and make managing/changing quite difficult. To use macros in the batch processing environment, use the `pvpython` program delivered in ParaView. On my OS X operating system it is under the `Applications/ParaView/Contents/bin/pvpython`. More info on all of this to come!

To simply run the macros in this repo, edit the macro files under the `macros/` directory for your use, then run them in ParaView by selecting Tools->Python Shell then click 'Run Script'. Navigate to the macros folder in this repo and select the macro you desire to use.
