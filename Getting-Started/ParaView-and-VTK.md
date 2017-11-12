# A Brief Introduction to ParaView

ParaView is an open-source platform that can visualize 2D, 3D, and 4D (time varying) datasets. ParaView can process multiple very large data sets in parallel then later collect the results to yield a responsive graphics environment with which a user can interact. The better the processor and graphics hardware the machine or machines hosting the software, the faster and better ParaView will run, however it can run quite well on a laptop with a standard graphics card such as a MacBook Pro.

Since ParaView is an open source application, anyone can download the program and its source code for modifications. The easiest way to get started with ParaView is to download the compiled binary installers for your operating system from [here](https://www.paraview.org/download/).

For further help, check out the [documentation](https://www.paraview.org/documentation/) provided by Kitware. In particular, the two worth looking through for a quick tour of ParaView are the 'The ParaView Guide' and 'The ParaView Tutorial.' One is a tutorial of the ParaView software and shows the user how to create sources, apply filters, and more. The other is a guide on how to do scripting, macros, and more intense use of the application.

# Installation
Open the downloaded binary installer and follow the prompts then drag the application into your applications folder.

Tour around software:
Take a look at Section 2.1 of 'The ParaView Tutorial' for details of the application’s GUI environment. Chapter 2 of the tutorial as a whole does an excellent job touring the software and its workflow for those unfamiliar with the software and its general capabilities.

# Notes
* Enable Auto Apply in the preferences for interactive slicers and so you don't always have to click apply. (*Note:* sometimes you may want this off when working with large datasets)
* One convenient feature is to save the state of the ParaView environment. This saves all the options you selected on all the filters you applied to visualize some data. Select File->Save State… (*Note:* this saves the absolute path of the files loaded into ParaView, so be sure to select 'Search for Files Under Directory...' when opening these state files)
