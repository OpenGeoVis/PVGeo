import PVGeo
import inspect
import re
import numpy as np
import sys

path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print(path)
sys.path.insert(0, path)


##########

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
    name = mod[1].__displayname__
    #print('On: ', name)
    feats = inspect.getmembers(mod[1])
    fname = name.replace(' ', '-')+'.rst'
    index += '\n   suites/%s' % fname

    with open('./suites/%s' % fname, 'w') as fid:
        fid.write('%s\n%s' % (name, '='*len(name))) # Page header is mosule name
        for f in feats:
            if inspect.isclass(f[1]):
                #print('\t' + f[1].__name__)
                fid.write(classdoccer % (f[1].__name__, '-'*len(f[1].__name__), 'class', '%s.%s' % (mod[1].__name__, f[1].__name__) ))
            elif inspect.isfunction(f[1]):
                 fid.write(defdoccer % (f[1].__name__, '-'*len(f[1].__name__), 'function', '%s.%s' % (mod[1].__name__, f[1].__name__) ))


        fid.close()


with open('./index.rst', 'w') as fid:
    fid.write(index)
