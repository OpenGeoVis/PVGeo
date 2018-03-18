!!! info "Purpose"
    This macro will translate a clip through a data scene at a given time interval.

## pvmacors.vis.clipThrough

```py
pvmacros.vis.clipThrough(clip, ax, bounds, num=10, delay=1.0)
```

### Description
This macro takes a clip source and progresses its location through a set of bounds in the data scene. The macro requires that the clip already exist in the pipeline. This is especially useful if you have many clips linked together as all will move through the seen as a result of this macro.

### Parameters
`clip` : string

- The string name of the clip source to be translated.

`ax` : int

- This is the axis on which to translate (0 for x, 1 for y, 2 for z).
- Think of this as the normal vector for the clip.

`bounds` : 6-element list or tuple

- These are the bounds to constrain the clip translation.

`num` : int, optional

- The number of discritizations in the clip translation.

`delay` : float, optional

- Time delay in seconds before conducting each clip translation.
