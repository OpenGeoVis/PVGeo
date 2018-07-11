import inspect
import re
import numpy as np
import sys
import os

path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, path)

import PVGeo


##########

moddoccer = r'''

%s
%s

.. automodule:: %s

'''

classdoccer = r'''

%s
%s

.. auto%s:: %s
    :show-inheritance:
    :members:
    :undoc-members:

'''

defdoccer = r'''

%s
%s

.. auto%s:: %s

'''

with open('../index_base.rst', 'r') as fid:
    index = fid.read()
    fid.close()


############
mods = inspect.getmembers(PVGeo, inspect.ismodule)

modnames = []

# Write out all of the pages
for mod in mods:
    if mod[0][0:2] == '__':
        continue
    try:
        name = mod[1].__displayname__
    except AttributeError:
        name = mod[1].__name__
    feats = inspect.getmembers(mod[1])
    fname = name.replace(' ', '-')+'.rst'
    index += '\n   suites/%s' % fname

    with open('./suites/%s' % fname, 'w') as fid:
        fid.write(moddoccer % (name, '='*len(name), mod[1].__name__)) # Page header is module name
        for f in feats:
            if inspect.isclass(f[1]):
                fid.write(classdoccer % (f[1].__name__, '-'*len(f[1].__name__), 'class', '%s.%s' % (mod[1].__name__, f[1].__name__) ))
            elif inspect.isfunction(f[1]):
                 fid.write(defdoccer % (f[1].__name__, '-'*len(f[1].__name__), 'function', '%s.%s' % (mod[1].__name__, f[1].__name__) ))
            # TODO: now check for stats report


        fid.close()


with open('./index.rst', 'w') as fid:
    fid.write(index)
