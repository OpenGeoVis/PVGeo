# -*- coding: utf-8 -*-
#
#  docs-include.py
#
#  Copyright 2018 Bane Sullivan <banesullivan@gmail.com>
#  This script generates mkdocs friendly Markdown documentation from a function declaration in a python package.
#  It is based on the the following blog post by Christian Medina
#   https://medium.com/python-pandemonium/python-introspection-with-the-inspect-module-2c85d5aa5a48#.twcmlyack
#
#
from __future__ import print_function
import builtins
import re
import os.path
from codecs import open
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
import os
import sys
from types import ModuleType
import importlib
import inspect

realimport = builtins.__import__

class DummyModule(ModuleType):
    def __getattr__(self, key):
        return None
    __all__ = []   # support wildcard imports

def tryimport(name, globals={}, locals={}, fromlist=[], level=1):
    try:
        return realimport(name, globals, locals, fromlist, level)
    except ImportError:
        return DummyModule(name)


DEF_SYNTAX = re.compile(r'\{def:\s*(.+?)\s*\}')
CLASS_SYNTAX = re.compile(r'\{class:\s*(.+?)\s*\}')

def _cleandocstr(doc, level='####', rmv='\n    '):
    # Decrease indentation from method def
    doc = doc.replace(rmv,'\n')
    # add a newline before list items
    doc = doc.replace('\n- ','\n\n- ')

    # make H3 headers
    lines = doc.split('\n')
    dels = []
    for i in range(len(lines)):
        ln = lines[i]
        if len(ln)>2 and ln[0] == '-' and ln[1] == '-':
            dels.append(i)
            lines[i-1] = '%s '%level + lines[i-1]

    # Delete the underlines
    for i in range(len(dels)):
        del(lines[dels[i]-i])

    # Join the lines
    doc = "\n".join((str(x) for x in lines))
    doc = doc.replace('\n',rmv)
    return doc

################


def _getDefMarkdown(method, module, level='###', rmv='\n    '):
    sig = inspect.signature(method)
    output = ['%s `%s`' % (level, method.__name__)]
    output.append('\n!!! note "Docs"')
    output.append("""
    ```py
    %s.%s%s
    ```""" % (module.__name__, method.__name__, sig))

    if method.__doc__:
        output.append(_cleandocstr(method.__doc__, level='#'+level, rmv=rmv))

    return "\n".join((str(x) for x in output))


####

def _getClassMarkdown(cla, module):
    rmv = '\n        '
    output = ['## Class `%s`' % (cla.__name__)]
    output.append("""
```py
%s.%s
```""" % (module.__name__, cla.__name__))
    if cla.__doc__:
        output.append(_cleandocstr(cla.__doc__))
    members = inspect.getmembers(cla)
    for mem in members:
        if mem[0][0] != '_':
            output.append(_getDefMarkdown(mem[1], cla, level='###', rmv=rmv))
    return "\n".join((str(x) for x in output))


################

def generateDefDocs(modulename):
    sys.path.append(os.getcwd())
    # Attempt import
    p, m = modulename.rsplit('.', 1)
    mod = importlib.import_module(p)
    met = getattr(mod, m)
    if mod is None:
        raise Exception("Module not found")

    # Module imported correctly, let's create the docs
    return _getDefMarkdown(met, mod)

def generateClassDocs(classname):
    sys.path.append(os.getcwd())
    # Attempt import
    p, c = classname.rsplit('.', 1)
    mod = importlib.import_module(p)
    cla = getattr(mod, c)
    if cla is None:
        raise Exception("Class not found")
    if not inspect.isclass(cla):
        raise Exception("Not a class: %s" % cla.__name__)

    # Module imported correctly, let's create the docs
    return _getClassMarkdown(cla, mod)

##############

class MethodInclude(Extension):
    def __init__(self, configs={}):
        self.config = {
            'base_path': ['.', 'Default location from which to evaluate ' \
                'relative paths for the include statement.'],
            'encoding': ['utf-8', 'Encoding of the files used by the include ' \
                'statement.']
        }
        for key, value in configs.items():
            self.setConfig(key, value)

    def extendMarkdown(self, md, md_globals):
        md.preprocessors.add(
            'docs-include', MethodIncludePreprocessor(md,self.getConfigs()),'_begin'
        )


class MethodIncludePreprocessor(Preprocessor):
    '''
    This provides an "include" function for pyhton module definitions for Markdown. The syntax is {def:module.method}, which will be replaced by the contents of doc string for that method. This replacement is done prior to any other Markdown processing. A safe import is used so that the module can be inported into any python environment.
    '''
    def __init__(self, md, config):
        super(MethodIncludePreprocessor, self).__init__(md)
        self.base_path = config['base_path']
        self.encoding = config['encoding']

    def run(self, lines):
        done = False
        builtins.__import__ = tryimport
        while not done:
            for line in lines:
                loc = lines.index(line)
                m = DEF_SYNTAX.search(line)
                c = CLASS_SYNTAX.search(line)
                if m:
                    modname = m.group(1)
                    text = generateDefDocs(modname).split('\n')
                    line_split = DEF_SYNTAX.split(line,maxsplit=0)
                    if len(text) == 0:
                        text.append('')
                    text[0] = line_split[0] + text[0]
                    text[-1] = text[-1] + line_split[2]
                    lines = lines[:loc] + text + lines[loc+1:]
                    break
                elif c:
                    classname = c.group(1)
                    text = generateClassDocs(classname).split('\n')
                    line_split = CLASS_SYNTAX.split(line,maxsplit=0)
                    if len(text) == 0:
                        text.append('')
                    text[0] = line_split[0] + text[0]
                    text[-1] = text[-1] + line_split[2]
                    lines = lines[:loc] + text + lines[loc+1:]
                    break
            else:
                done = True
        builtins.__import__ = realimport
        return lines


def makeExtension(*args,**kwargs):
    return MethodInclude(kwargs)
