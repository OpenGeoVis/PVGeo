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


INC_SYNTAX = re.compile(r'\{def:\s*(.+?)\s*\}')

def _cleandocstr(doc):
    # Decrease indentation from method def
    doc = doc.replace('\n    ','\n')
    # add a newline before list items
    doc = doc.replace('\n- ','\n\n- ')

    # make H3 headers
    lines = doc.split('\n')
    dels = []
    for i in range(len(lines)):
        ln = lines[i]
        if len(ln)>2 and ln[0] == '-' and ln[1] == '-':
            dels.append(i)
            lines[i-1] = '#### ' + lines[i-1]

    # Delete the underlines
    for i in range(len(dels)):
        del(lines[dels[i]-i])

    # Join the lines
    doc = "\n".join((str(x) for x in lines))
    return doc

def _getmarkdown(method, module):
    sig = inspect.signature(method)
    output = ['### `%s`' % (method.__name__)]
    output.append("""
```py
%s.%s%s
```""" % (module.__name__, method.__name__, sig))

    if method.__doc__:
        output.append(_cleandocstr(method.__doc__))

    return "\n".join((str(x) for x in output))


def generatedocs(modulename):
    sys.path.append(os.getcwd())
    # Attempt import
    p, m = modulename.rsplit('.', 1)
    mod = importlib.import_module(p)
    met = getattr(mod, m)
    if mod is None:
        raise Exception("Module not found")

    # Module imported correctly, let's create the docs
    return _getmarkdown(met, mod)


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
                m = INC_SYNTAX.search(line)

                if m:
                    modname = m.group(1)
                    text = generatedocs(modname).split('\n')
                    line_split = INC_SYNTAX.split(line,maxsplit=0)
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
