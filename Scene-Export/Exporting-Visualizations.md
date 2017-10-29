# Motivation
In order to effectively communicate our geoscientific findings, we often need to share our 3D visualizations with interested stakeholders. These interested parties are likely not going to have ParaView or other visualization software at hand. Thus we desire to have a means to export our complex visualizations in ParaView to a simple, shareable format that anyone can view. To accomplish this, we will take advantage of vtk.js and its standalone web view for vtk.js formats.

# VTK.js
[vtk.js](https://kitware.github.io/vtk-js/) is a rendering library made for scientific visualization on the web. This code base brings high performance rendering into anyone's web browser. This library allows us to export complex scene's from ParaView and share them with anyone that has a web browser like Safari or Google Chrome.

The vtk.js library has an open-source [standalone scene viewer](https://kitware.github.io/vtk-js/examples/StandaloneSceneLoader.html) that we will recommend using. They also have a scene export macro for ParaView that compresses your data scene in ParaView to a single shareable file for viewing on the web. The macro from the vtk.js library can be found [here](https://raw.githubusercontent.com/Kitware/vtk-js/master/Utilities/ParaView/export-scene-macro.py) but we also deploy this macro in our repository under `macros/scene-export-macro.py`. The standalone scene viewer for your web browser can be found [here](https://kitware.github.io/vtk-js/examples/StandaloneSceneLoader/StandaloneSceneLoader.html). You can choose to either download that file to run locally or simple use the file off of the vtk.js repo by clicking that link.

# How To

![Scene-Viewer](https://kitware.github.io/vtk-js/examples/StandaloneSceneLoader/StandaloneSceneLoader.html)
