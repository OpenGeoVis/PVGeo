import inspect
import re
import numpy as np
import os
import sys
import shutil

# Mock the paraview module to build pvmacros docs
import mock

MOCK_MODULES = ['paraview', 'paraview.simple']
for mod_name in MOCK_MODULES:
    sys.modules[mod_name] = mock.Mock()

path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, path)

import PVGeo

if os.path.exists('./suites'):
    shutil.rmtree('./suites')
os.makedirs('./suites')
if os.path.exists('./pvmacros'):
    shutil.rmtree('./pvmacros')
os.makedirs('./pvmacros')


##########
global moddoccer
moddoccer = r'''

%s
%s

.. automodule:: %s

'''
global classdoccer
classdoccer = r'''

%s
%s

.. auto%s:: %s
    :show-inheritance:
    :members:
    :undoc-members:
    :private-members:

'''
global defdoccer
defdoccer = r'''

%s
%s

.. auto%s:: %s

'''

with open('../index_base.rst', 'r') as fid:
    index = fid.read()
    fid.close()





appIndex = '''

.. toctree::
   :maxdepth: 3
   :caption: PVGeo:
'''


############
global choices
choices = ['base', 'reader', 'filter', 'writer', 'source', 'macro', 'script']
global counts
counts = [0]*len(choices)

table = r'''

Current Statistics
------------------

.. csv-table::
   :header: "Bases", "Readers", "Filters", "Writers", "Sources", "Macros"

   %d, %d, %d, %d, %d, %d

'''

# Write out all of the pages
def MakeFiles(mods, path, modname):
    appIndex = '''

.. toctree::
   :maxdepth: 3
   :caption: %s:
    ''' % modname
    for mod in mods:
        if mod[0][0:2] == '__':
            continue
        try:
            name = mod[1].__displayname__
        except AttributeError:
            name = mod[1].__name__
        feats = inspect.getmembers(mod[1])
        fname = name.replace(' ', '-')+'.rst'
        appIndex += '\n   %s/%s' % (path, fname)

        with open('./%s/%s' % (path, fname), 'w') as fid:
            fid.write(moddoccer % (name, '-'*len(name), mod[1].__name__)) # Page header is module name
            for f in feats:
                # Check for a __displayname__
                if inspect.isclass(f[1]) or inspect.isfunction(f[1]):
                    try:
                        featname = f[1].__displayname__
                    except AttributeError:
                        featname = f[1].__name__
                    # Make the auto doc rst
                    if inspect.isclass(f[1]):
                        fid.write(classdoccer % (featname, '^'*len(featname), 'class', '%s.%s' % (mod[1].__name__, f[1].__name__) ))
                    elif inspect.isfunction(f[1]):
                         fid.write(defdoccer % (featname, '^'*len(featname), 'function', '%s.%s' % (mod[1].__name__, f[1].__name__) ))
                    # Check for stats report
                    try:
                        featType = f[1].__type__
                    except AttributeError:
                        featType = None
                    if featType is not None:
                        # Count the featers
                        for i in range(len(choices)):
                            if featType in choices[i]:
                                counts[i] += 1
            fid.close()
    return appIndex

mods = inspect.getmembers(PVGeo, inspect.ismodule)
appIndex = MakeFiles(mods, 'suites', 'PVGeo')


import pvmacros
mods = inspect.getmembers(pvmacros, inspect.ismodule)
appIndex += MakeFiles(mods, 'pvmacros', 'pvmacros')

# Make the stats report table:

index += table % (counts[0], counts[1], counts[2], counts[3], counts[4], counts[5])

with open('./index.rst', 'w') as fid:
    fid.write(index + appIndex)
