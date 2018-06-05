# Animate Tunnel Boring Machine

!!! failure "Description to come!"
    There are a lot of pages in the documentation and we are trying to fill all content as soon as possible. Stay tuned for updates to this page

This filter analyzes a vtkTable containing position information about a Tunnel Boring Machine (TBM). This Filter iterates over each row of the table as a timestep and uses the XYZ coordinates of a single parts of the TBM to generate a tube that represents taht part of the TBM. To create a directional vector for the length of the cylider that represents the TBM component, this filter searches for the next different point and gets a unit vector bewtween the two. Then two points are constructed in the positive and negative directions of that vector for the ends of the cylinder. This only uses rows that have a Status of 2.
