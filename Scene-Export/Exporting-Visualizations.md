# Motivation
In order to effectively communicate our geoscientific findings, we often need to share our 3D visualizations with interested stakeholders. These interested parties are likely not going to have ParaView or other visualization software at hand. Thus we desire to have a means to export our complex visualizations in ParaView to a simple, shareable format that anyone can view. To accomplish this, we will take advantage of vtk.js and its standalone web view for vtk.js formats.

# VTK.js
[vtk.js](https://kitware.github.io/vtk-js/) is a rendering library made for scientific visualization on the web. This code base brings high performance rendering into anyone's web browser. This library allows us to export complex scene's from ParaView and share them with anyone that has a web browser like Safari or Google Chrome.

The vtk.js library has an open-source [standalone scene viewer](https://kitware.github.io/vtk-js/examples/StandaloneSceneLoader.html) that we will recommend using. They also have a scene export macro for ParaView that compresses your data scene in ParaView to a single shareable file for viewing on the web. The macro from the vtk.js library can be found [here](https://raw.githubusercontent.com/Kitware/vtk-js/master/Utilities/ParaView/export-scene-macro.py) but we also deploy this macro in our repository under `macros/scene-export-macro.py`. The standalone scene viewer for your web browser can be found [here](https://kitware.github.io/vtk-js/examples/StandaloneSceneLoader/StandaloneSceneLoader.html). You can choose to either download that file to run locally or simple use the file off of the vtk.js repo by clicking that link.

# How To
First, make a complex scene in ParaView that you might like to share with someone. For a simple example, download [this] folder and load the state file *(be sure to use relative file paths)*. Now that you have your scene loaded, run the `export-scene-macro.py` macro delivered in this repo or download it from the link above if you do not have our repo cloned. To run this macro, select Tools->Python Shell then select Run Script. Choose the macro and it should execute without issue *(if you have trouble post on our issues page or read the vtk.js documentation [here](https://kitware.github.io/vtk-js/examples/StandaloneSceneLoader.html))*

Now open the standalone web viewer by opening the `StandaloneSceneLoader.html` file delivered at the top level of the repo or by opening [this link](https://kitware.github.io/vtk-js/examples/StandaloneSceneLoader/StandaloneSceneLoader.html).

Select the exported scene as the input file for the web viewer from wherever you saved it. The macro should have printed out the location of the saved scene in the Python Shell (also if you did not modify the macro it should save out under a folder called `vtkJsExport` in your home, `~`, directory).

## How to Share
To share these exported scenes with non-technical stakeholders, we recommend the following process:

- Create your scene and export to the vtk.js format
- Quality control your visualization by viewing in web browser yourself (follow process above)
- Send an email with your visualization (`.vtkjs` file) and something along the lines of:


> Check out the data scene/model by downloading the attached file. Then go to the link below and open that downloaded file.
> https://kitware.github.io/vtk-js/examples/StandaloneSceneLoader/StandaloneSceneLoader.html

Another method to share this scenes that might make the end user have a slightly easier process of viewing the file and will handle the case for mobile platforms is to host your file on a web service like GitHub or Google Drive. Then get a link to the `.vtkjs` file on that web service and append it to the web viewer URL in the following manner:

- Copy the url to the web browser: https://kitware.github.io/vtk-js/examples/StandaloneSceneLoader/StandaloneSceneLoader.html
- Append that url with `?fileURL=`
- Then append that with the shareable link to your visualization file from your web file service:
    - For Google drive, we will follow [this guide](https://www.labnol.org/internet/direct-links-for-google-drive/28356/) for direct file links
    - Shared links for Google drive files will have this format:

        > https://drive.google.com/file/d/FILE_ID/edit?usp=sharing

    - Take note of that FILE_ID and replace it in this link to have a direct download link:

        > https://drive.google.com/uc?export=download&id=FILE_ID

    - For example here are the two links to one of our files:

        > https://drive.google.com/a/mymail.mines.edu/file/d/0B6v2US3m042-cW80NGR1RVhsM3M/view?usp=sharing

        > https://drive.google.com/uc?export=download&id=0B6v2US3m042-cW80NGR1RVhsM3M

    - Now here is the appended link for the web viewer:

        > https://kitware.github.io/vtk-js/examples/StandaloneSceneLoader/StandaloneSceneLoader.html?fileUrl=https://drive.google.com/uc?export=download&id=0B6v2US3m042-cW80NGR1RVhsM3M


- This link can then be shared with anyone (on a computer, phone, or tablet)
- Be sure to check the link yourself before sending to make sure the file link is correct (Google Drive can be tricky to figure out)

This is an example of how to fill out your URL

> https://kitware.github.io/vtk-js/examples/StandaloneSceneLoader/StandaloneSceneLoader.html?fileUrl=https://theDirectDownloadURLtoYourFile.vtkjs

Here is a sample URL to one of our files for you to demo the web viewer:

>https://kitware.github.io/vtk-js/examples/StandaloneSceneLoader/StandaloneSceneLoader.html?fileUrl=https://drive.google.com/uc?export=download&id=0B6v2US3m042-cW80NGR1RVhsM3M
