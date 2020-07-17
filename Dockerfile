# Build from the ParaView base image
# This will have ParaView and conda all set up properly
# See https://github.com/banesullivan/dockerfiles/tree/master/paraview
#     https://hub.docker.com/repository/docker/banesullivan/paraview
FROM banesullivan/paraview

WORKDIR /root
COPY . ./PVGeo-source/
WORKDIR /root/PVGeo-source

# Install PVGeo
RUN conda install --quiet --yes -c conda-forge \
    cython \
    discretize
RUN pip install -r requirements.txt
RUN pip install -e .

ENV PYVISTA_OFF_SCREEN=true
ENV PV_PLUGIN_PATH="/root/PVGeo-source/PVPlugins/"

# Set up for use
WORKDIR /root/

# Make sure to borrow entry point from parent image
ENTRYPOINT ["tini", "-g", "--", "start_xvfb.sh"]
CMD ["/bin/bash"]
# CMD ["jupyter", "notebook", "--port=8877", "--no-browser", "--ip=0.0.0.0", "--allow-root"]
