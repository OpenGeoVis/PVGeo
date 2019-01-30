"""
These are helpers specifically for the file readers for private use only.
@author: Bane Sullivan
"""

__all__ = [
    'clean_data_name',
    'create_modified_callback',
]

import os

def clean_data_name(data_name, filename):
    """A helper to clean a filename to make a useful data array name"""
    if data_name is None or data_name == '':
        data_name = os.path.splitext(os.path.basename(filename))[0]
    return data_name


def create_modified_callback(anobject):
    import weakref
    weakref_obj = weakref.ref(anobject)
    anobject = None
    def _mark_modified(*args, **kwars):
        o = weakref_obj()
        if o is not None:
            o.Modified()
    return _mark_modified
