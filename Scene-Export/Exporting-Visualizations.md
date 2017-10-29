# Motivation
In order to effectively communicate our geoscientific findings, we often need to share our 3D visualizations with interested stakeholders. These interested parties are likely not going to have ParaView or other visualization software at hand. Thus we desire to have a means to export our complex visualizations in ParaView to a simple, shareable format that anyone can view. To accomplish this, we will take advantage of vtk.js and its standalone web viewer for vtk.js formats.

# VTK.js
[vtk.js](https://kitware.github.io/vtk-js/) is a rendering library made for scientific visualization on the web. This code base brings high performance rendering into anyone's web browser. This library allows us to export complex scene's from ParaView and share them with anyone that has a web browser like Safari or Google Chrome.

The vtk.js library has an open-source [standalone scene viewer](https://kitware.github.io/vtk-js/examples/StandaloneSceneLoader.html) that we will recommend using. They also have a scene export macro for ParaView that compresses your data scene in ParaView to a single shareable file for viewing on the web. The macro from the vtk.js library can be found [here](https://raw.githubusercontent.com/Kitware/vtk-js/master/Utilities/ParaView/export-scene-macro.py) but we also deploy this macro in our repository under `macros/scene-export-macro.py`. The standalone scene viewer for your web browser can be found [here](https://kitware.github.io/vtk-js/examples/StandaloneSceneLoader/StandaloneSceneLoader.html). You can choose to either download that file to run locally or simple use the file off of the vtk.js repo by clicking that link.

# How To
First, make a complex scene in ParaView that you might like to share with someone. For a simple example, download [this] folder and load the state file *(be sure to use relative file paths)*. Now that you have your scene loaded, run the `export-scene-macro.py` macro delivered in this repo or download it from the link above if you do not have our repo cloned. To run this macro, select Tools->Python Shell then select Run Script. Choose the macro and it should execute without issue *(if you have trouble post on our issues page or read the vtk.js documentation [here](https://kitware.github.io/vtk-js/examples/StandaloneSceneLoader.html))*

Now open the standalone web viewer by opening the `StandaloneSceneLoader.html` file delivered at the top level of the repo or by opening [this link](https://kitware.github.io/vtk-js/examples/StandaloneSceneLoader/StandaloneSceneLoader.html).

Select the exported scene as the input file for the web viewer from wherever you saved it. The macro should have printed out the location of the saved scene in the Python Shell (also if you did not modify the macro it should save out under a folder called `vtkJsExport` in your home, `~`, directory).

## How to Share

### Quick and Easy
To share these exported scenes with non-technical stakeholders, we recommend the following process:

- Create your scene and export to the vtk.js format
- Quality control your visualization by viewing in web browser yourself (follow process above)
- Send an email with your visualization (`.vtkjs` file) and something along the lines of:


> Check out the data scene/model by downloading the attached file. Then go to the link below and open that downloaded file.

> https://kitware.github.io/vtk-js/examples/StandaloneSceneLoader/StandaloneSceneLoader.html


### A Bit More Robust
Another method to share scenes that might make the end user have a slightly easier process of viewing the file and will handle the case for mobile platforms is to host your file on a web service like GitHub or Dropbox *(we have been unsuccessful in getting Google Drive to work)*. Then get a public link to the `.vtkjs` file on that web service and append it to the web viewer URL in the following manner:

- Copy the url to the web browser which we host on the repo: `https://rawgit.com/banesullivan/ParaViewGeophysics/master/StandaloneSceneLoader.html?fileURL=`
- Note the appended `?fileURL=`
- Then append that with the shareable link to your visualization file from your web file service:
    - For Dropbox, we will follow this method to get direct download file links
    - Shared links for Dropbox files will have this format:

        > `https://www.dropbox.com/s/84ytq8t5mfa4ons/SampleVis.vtkjs?dl=0`

    - Change the 'www' to 'dl' in the link such that it looks like:

        > `https://dl.dropbox.com/s/84ytq8t5mfa4ons/SampleVis.vtkjs?dl=0`

    - Now append the link for the web viewer hosted on our GitHub repo with the direct download link in the following manner:

        > `https://rawgit.com/banesullivan/ParaViewGeophysics/master/StandaloneSceneLoader.html?fileURL=https://dl.dropbox.com/s/84ytq8t5mfa4ons/SampleVis.vtkjs?dl=0`


- This link can then be shared with anyone (on a computer, phone, or tablet)
- Be sure to check the link yourself before sending to make sure everything worked


Here is a sample URL to one of vtk.js' [sample scenes](https://rawgit.com/banesullivan/ParaViewGeophysics/master/StandaloneSceneLoader.html?fileURL=https://data.kitware.com/api/v1/file/587003d08d777f05f44a5c99/download) and one of [our scenes](https://rawgit.com/banesullivan/ParaViewGeophysics/master/StandaloneSceneLoader.html?fileURL=https://dl.dropbox.com/s/84ytq8t5mfa4ons/SampleVis.vtkjs?dl=0) for you to demo the web viewer:
