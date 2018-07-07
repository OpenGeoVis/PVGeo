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
import PVGeo
import vtk
import numpy as np

realimport = builtins.__import__


class DummyModule(ModuleType):
    def __getattr__(self, key):
        return None
    __all__ = []   # support wildcard imports

def tryimport(name, globals={}, locals={}, fromlist=[], level=1):
    #globals = dict(globals)
    try:
        return realimport(name, globals, locals, fromlist, level)
    except (ImportError):
        return DummyModule(name)


DEF_SYNTAX = re.compile(r'\{def:\s*(.+?)\s*\}')
CLASS_SYNTAX = re.compile(r'\{class:\s*(.+?)\s*\}')
INC_SYNTAX = re.compile(r'\{py:\s*(.+?)\s*\}')

################

def _getSections(doc):
    """Possible sections: @desc, @param, @return, @notes, @example"""
    keys = re.findall('@\S+:', doc)
    vals = re.split('@\S+:', doc)
    del(vals[0])
    secs = {}
    for i in range(len(keys)):
        secs[keys[i]] = vals[i].lstrip()
    return secs

def _beautifyDesc(val):
    lines = [v.lstrip() for v in val.splitlines()]
    return '**Description:**\n\n%s\n' % ('\n'.join((l for l in lines)))

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
    if '```' not in val:
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


################

def _joinSections(doc):
    if doc is None or len(doc) < 1:
        return ''
    secs = _getSections(doc)
    try:
        secs = beautifySections(secs)
    except Exception as er:
        print('While generating docs for %s, Exception caught: %s' % (title, er))
    return '\n'.join(s for s in secs.values())


def makeMkDown(doc, title, sig, admon='!!!'):
    secs = _joinSections(doc)
    tit = 'abstract "%s"' % title
    if ' _' in title: # it is a private/internal method
        tit = 'quote "%s (private)"' % title

    atype = '%s %s\n' % (admon, tit)
    if len(secs.strip()) < 1:
        admon = '!!!' # overide
        atype = '%s %s\n' % (admon, tit)

    docs = sig + '\n\n' + secs

    # Now indent for admonition widget
    docs = atype + re.sub( '^',' '*4, docs ,flags=re.MULTILINE )
    return docs

################


def _getDefMarkdown(method, module, admon='!!!'):
    sig = str(inspect.signature(method)).replace('(self, ', '(').replace('(self', '(')

    sig = '<big>`#!py %s%s`</big>' % ( method.__name__, sig)
    title = '%s' % (method.__name__)#'%s.%s' % (module.__name__, method.__name__)

    #if method.__doc__:
    return makeMkDown(method.__doc__, sig, '', admon=admon) # TODO: clean up


def _getClassMarkdown(clas, module):
    """This method id for the class docs and __init__ method for a class"""
    HEAD = r'<big><big>%s</big></big>'
    sig = inspect.signature(clas)
    sig = HEAD % '`#!py %s%s`' % ( clas.__name__, sig)
    title = '%s.%s' % (module.__name__, clas.__name__)

    # Get the class doc string and signature to start
    docs = ''
    methods = []
    # get class docs
    bases = ', '.join('`' + c.__name__ + '`' for c in clas.__bases__)
    gram = 'es' if len(clas.__bases__) > 1 else ''
    base = '*Base Class%s:* %s' % (gram, bases)
    csecs = _joinSections(clas.__doc__) if clas.__doc__ else ''
    docs = sig + ('\n\n%s\n\n' % (base)) + csecs
    # TODO: constructor/init def docs
    #docs += '\n\n' + _joinSections(clas.__init__.__doc__)
    # Now indent for admonition widget for whole class (top level)
    docs = '!!! abstract "%s"\n' % title + re.sub( '^',' '*4, docs, flags=re.MULTILINE)

    def _getMems(clas, base, methods, USED, name=''):
        all = inspect.getmembers(clas, predicate=inspect.isfunction)
        basemem = inspect.getmembers(clas.__bases__[0])
        members = [mem for mem in all if mem not in basemem and mem[0] not in USED and mem[0][1] != '_']
        USED += [mem[0] for mem in members]
        if len(members) < 1:
            return USED
        methods.append(name)
        def _isabstract(method):
            sig = '%s' % inspect.signature(method[1])
            return '(self' not in sig
        # First do static methods:
        memstats = [mem for mem in members if _isabstract(mem)]
        if len(memstats) > 0:
            methods.append('<big>Static Methods:</big>')
            for mem in memstats:
                methods.append(_getDefMarkdown(mem[1], clas, admon='???'))
        members = [mem for mem in members if mem not in memstats]
        if len(members) > 0:
            methods.append('<big>Instance Methods:</big>')
            for mem in members:
                methods.append(_getDefMarkdown(mem[1], clas, admon='???'))
        return USED


    USED = []

    # Get this class' explicitly defined functions:
    USED = _getMems(clas, clas.__bases__[0], methods, USED)

    # Iterate over inherreted functionality
    base = clas.__bases__[0] # TODO: assumes class only inhere functionality of a single other class
    while (base is not vtk.util.vtkAlgorithm.VTKPythonAlgorithmBase and base is not object):
        USED = _getMems(base, base.__bases__[0], methods, USED, name=(HEAD % 'Inherreted from: `%s`' % base.__name__))
        base = base.__bases__[0]

    methods = "\n\n".join((met for met in methods))
    # ident one more level to be nested in class admonition
    methods = re.sub( '^',' '*4, methods , flags=re.MULTILINE)
    return docs + '\n\n' + methods




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
    clas = getattr(mod, c)
    if mod is None:
        raise Exception("Module not found")

    # Module imported correctly, let's create the docs
    return _getClassMarkdown(clas, mod)

def _parseArg(arg):
    args = arg.split('?')
    filename = args[0]
    hl = ''
    if len(args) > 1:
        hl = 'hl_lines="%s"' % args[1]
    return filename, hl


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
                s = INC_SYNTAX.search(line)
                if m or c:
                    if m :
                        modname = m.group(1)
                        text = generateDefDocs(modname).split('\n')
                        line_split = DEF_SYNTAX.split(line,maxsplit=0)
                    if c:
                        classname = c.group(1)
                        text = generateClassDocs(classname).split('\n')
                        line_split = CLASS_SYNTAX.split(line,maxsplit=0)
                    if len(text) == 0:
                        text.append('')
                    text[0] = line_split[0] + text[0]
                    text[-1] = text[-1] + line_split[2]
                    lines = lines[:loc] + text + lines[loc+1:]
                    break
                if s:
                    filename, hl = _parseArg(s.group(1))
                    pfilename = '%s/%s' % (os.getcwd(), filename)
                    try:
                        with open(pfilename, 'r', encoding=self.encoding) as r:
                            text = r.readlines()
                    except Exception as e:
                        print('Warning: could not find file {}. Ignoring '
                            'include statement. Error: {}'.format(filename, e))
                        lines[loc] = INC_SYNTAX.sub('',line)
                        break

                    line_split = INC_SYNTAX.split(line,maxsplit=0)
                    if len(text) == 0: text.append('')
                    for i in range(len(text)):
                        text[i] = text[i][0:-1]
                    text[-1] = '```'
                    text = ['```py %s ' % hl] + text
                    #text = ['File Included From: %s' % filename] + text
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
