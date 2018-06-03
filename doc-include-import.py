# -*- coding: utf-8 -*-
#
#  doc-include-import.py
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

################

def getSections(doc):
    """Possible sections: @desc, @param, @return, @notes, @example"""
    keys = re.findall('@\S+:', doc)
    vals = re.split('@\S+:', doc)
    del(vals[0])
    secs = {}
    for i in range(len(keys)):
        secs[keys[i]] = vals[i].lstrip()
    return secs

def _beautifyDesc(val):
    val = '**Description:**\n\n%s' % val
    return val

def _beautifyParams(val):
    """param1 : str : req : A string variable about foo"""
    lines = [v.lstrip() for v in val.splitlines()]
    params = {}
    for ln in lines:
        ln = [l.lstrip().rstrip() for l in ln.split(':')]
        if len(ln[0]) < 1:
            continue
        elif len(ln) == 3:
            # Assume it is a required parameter
            ln.insert(2, 'required')
        elif len(ln) != 4:
            raise Exception('Parmater `%s` improperly formatted.' % ln[0])
        info = {}
        info['type'] = ln[1]
        info['req'] = ln[2] in ['req', 'required']
        info['desc'] = ln[3]
        params[ln[0]] = info
    # Now format in markdown
    for par in params.keys():
        info = params[par]
        form = '*'
        if info['req']: form = '**'
        ln = '- %s`%s` (%s):%s %s' % (form,par,info['type'],form,info['desc'])
        params[par] = ln

    return '**Parameters:**\n\n%s\n' % ('\n'.join((params[key] for key in params.keys())))

def _beautifyNotes(val):
    val = [v.lstrip() for v in val.splitlines()]
    for i in range(len(val)):
        if len(val[i]) > 0 and val[i][0] is not '-':
            val[i] = '- %s' % val[i]
    return '**Notes:**\n\n%s\n' % ('\n'.join((v for v in val)))

def _beautifyReturn(val):
    val = [v.rstrip().lstrip() for v in val.split(':')]
    val[0] = '`%s`' % val[0]
    return '**Return:**\n\n%s\n' % (': '.join((v for v in val)))

def _beautifyExample(val):
    lines = [v.lstrip() for v in val.splitlines()]
    lines.insert(0, '```py\n')
    lines.append('\n```')
    return '**Example:**\n\n%s\n' % ('\n'.join((ln for ln in lines)).format(val))

def beautifySections(secs):
    for key in secs.keys():
        if key[1:-1].lower() in ['notes', 'note']:
            secs[key] = _beautifyNotes(secs[key])
        elif key[1:-1].lower() in ['desc', 'description']:
            secs[key] = _beautifyDesc(secs[key])
        elif key[1:-1].lower() in ['param','params','parameters','parameter']:
            secs[key] = _beautifyParams(secs[key])
        elif key[1:-1].lower() in ['ret', 'return', 'returns']:
            secs[key] = _beautifyReturn(secs[key])
        elif key[1:-1].lower() in ['ex', 'example']:
            secs[key] = _beautifyExample(secs[key])
    return secs

def _beautifySig(sig):
    return sig

def makeMkDown(doc, title, sig):
    secs = getSections(doc)
    try:
        secs = beautifySections(secs)
    except Exception as er:
        print('While generating docs for %s, Exception caught: %s' % (title, er))

    docs = sig + \
        '\n\n' + \
        '\n'.join(s for s in secs.values())
    # Now indent for admonition widget
    docs = '!!! abstract "%s"\n' % title + re.sub( '^',' '*4, docs ,flags=re.MULTILINE )
    return docs

################


def _getDefMarkdown(method, module):
    sig = inspect.signature(method)

    sig = '<big><big>`#!py %s%s`</big></big>' % ( method.__name__, sig)
    title = '%s.%s' % (module.__name__, method.__name__)

    if method.__doc__:
        return makeMkDown(method.__doc__, title, sig)

    return sig




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
                """elif c:
                    raise Exception('Classes not implemented yet')
                    classname = c.group(1)
                    text = generateClassDocs(classname).split('\n')
                    line_split = CLASS_SYNTAX.split(line,maxsplit=0)
                    if len(text) == 0:
                        text.append('')
                    text[0] = line_split[0] + text[0]
                    text[-1] = text[-1] + line_split[2]
                    lines = lines[:loc] + text + lines[loc+1:]
                    break"""
            else:
                done = True
        builtins.__import__ = realimport
        return lines


def makeExtension(*args,**kwargs):
    return MethodInclude(kwargs)
