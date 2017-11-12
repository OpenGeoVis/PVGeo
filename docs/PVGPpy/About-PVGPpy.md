# PVGPpy
PVGPpy is a python module we are developing for direct use of our macros in the ParaView shell. This module will contain the bulk of our macros for your use. We are publishing our macros in this manner to:

1. Streamline their use by allowing users to call the macros like python functions directly from the ParaView shell.
2. Easily update/change the macros without constant merge conflictions as users will need to input certain parameters for their use. This is much easily done through function calls than overwriting the macro files.


-------


# Macros vs. Scripts
<!--- TODO: we need more info here --->
We will from now on refer to macros as a set of common codes that can be used regardless of data sets or scenes in ParaView. ParaView's sense of macro is not robust enough for us, so we will be referring to traditional macros in ParaView as 'scripts' from here on. Scripts will be used on specific sets of data where as macros can be used on any set of data.

## Macros
Macros are Python codes that complete tedious or recurring tasks either in ParaView's gui or in ParaView's batch processing environment. We will use macros to complete common tasks like saving screenshots of isometric views of a data scene or tedious tasks like making numerous slices of a single data set along a line.

## Scripts
Scripts are Python codes we will use for tasks like loading scenes and for applying several macros at once. It is often helpful to set up a script for a project so that you can easily run all the visualization processing at once each time you update your model files or create new versions of your data.


-------


# How to Run Scripts
Use the Python Shell from 'Tools->Python Shell' in the ParaView GUI. Do not import scripts as macros in ParaView as they become static in the ParaView GUI and make managing/changing quite difficult. To use scripts in the batch processing environment, use the `pvpython` program delivered in ParaView. On my OS X operating system it is under the `Applications/ParaView/Contents/bin/pvpython`. More info on all of this to come! <!-- TODO -->

To simply run the scripts in this repo, edit the script files under the `scripts/` directory for your use, then run them in ParaView by selecting 'Tools->Python Shell' then click 'Run Script'. Navigate to the `scripts/` directory in this repo and select the script you desire to use.


-------


# Make Your Own Scripts
Description to come! There are a lot of pages in the documentation and we are trying to fill all content as soon as possible. Stay tuned for updates to this page
<!--- TODO --->

## Using the Trace Tool
<!--- TODO: how to make meaning of the trace output --->
Description to come!

## Using PVPython
<!--- TODO: Batch processing --->
Description to come!
