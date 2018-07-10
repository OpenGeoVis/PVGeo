import PVGeo
import inspect
import re
import numpy as np
# iterate recursively through the project to find classes
# in the class doc string look for an @type: qualifier
# types can be: base, reader, filter, writer, source, macro, script


choices = ['base', 'reader', 'filter', 'writer', 'source', 'macro', 'script']
counts = [0]*len(choices)
names = [ [] for c in choices]

tofix = []


def _getSections(doc):
    """Possible sections: @type, @desc, @param, @return, @notes, @example"""
    keys = re.findall('@\S+:', doc)
    vals = re.split('@\S+:', doc)
    del(vals[0])
    secs = {}
    for i in range(len(keys)):
        secs[keys[i]] = vals[i].lstrip()
    return secs

def CountFeatures(mod):
    feats = inspect.getmembers(mod)
    for f in feats:
        if inspect.isclass(f[1]) and f[1].__doc__ and '@type:' in f[1].__doc__:
            c = f[1]
            secs = _getSections(c.__doc__)
            typ = secs['@type:'].strip()
            for i in range(len(choices)):
                if typ in choices[i]:
                    counts[i] += 1
                    names[i].append(c.__name__)
        elif inspect.isclass(f[1]) and f[1].__doc__ and '@desc:' in f[1].__doc__:
            tofix.append(f[1].__name__)



mods = inspect.getmembers(PVGeo, inspect.ismodule)
for mod in mods:
    CountFeatures(mod[1])



for i in range(len(choices)):
    print(choices[i] + ': %d' % counts[i] )
    print('\t' + '\n\t'.join(names[i]))

print('To Fix: ')
print('\t' + '\n\t'.join(tofix))
