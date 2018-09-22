"""
These are helpers specifically for the file readers for private use only.
@author: Bane Sullivan
"""
__all__ = [
    'cleanDataNm',
    'createModifiedCallback',
]


import os
from . import errors as _helpers



def cleanDataNm(dataNm, FileName):
    """A helper to clean a FileName to make a useful data array name"""
    if dataNm is None or dataNm == '':
        dataNm = os.path.splitext(os.path.basename(FileName))[0]
    return dataNm


def createModifiedCallback(anobject):
    import weakref
    weakref_obj = weakref.ref(anobject)
    anobject = None
    def _markmodified(*args, **kwars):
        o = weakref_obj()
        if o is not None:
            o.Modified()
    return _markmodified
