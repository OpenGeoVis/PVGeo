"""
These are helpers specifically for the file readers for private use only.
@author: Bane Sullivan
"""

__all__ = [
    'cleanDataNm',
    'createModifiedCallback',
]

import os

def cleanDataNm(data_name, filename):
    """A helper to clean a filename to make a useful data array name"""
    if data_name is None or data_name == '':
        data_name = os.path.splitext(os.path.basename(filename))[0]
    return data_name


def createModifiedCallback(anobject):
    import weakref
    weakref_obj = weakref.ref(anobject)
    anobject = None
    def _markmodified(*args, **kwars):
        o = weakref_obj()
        if o is not None:
            o.Modified()
    return _markmodified
