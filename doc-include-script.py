#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  include.py
#
#  Copyright 2015 Christopher MacMackin <cmacmackin@gmail.com>
#   Heavily Edited by Bane Sullivan <banesullivan@gmail.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

from __future__ import print_function
import re
import os.path
from codecs import open
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor

INC_SYNTAX = re.compile(r'\{py:\s*(.+?)\s*\}')

def _parseArg(arg):
    args = arg.split('?')
    filename = args[0]
    hl = ''
    if len(args) > 1:
        hl = 'hl_lines="%s"' % args[1]
    return filename, hl


class ScriptInclude(Extension):
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
            'include', ScriptIncludePreprocessor(md,self.getConfigs()),'_begin'
        )


class ScriptIncludePreprocessor(Preprocessor):
    '''
    This provides an "include" function for Python Scripts in mkdocs, similar to that found in LaTeX (also the C pre-processor and Fortran). The syntax is {py:filename}, which will be replaced by the contents of filename. Through in an argument after the filename to highlight specified lines {py:filename?6 9 3}. Any such statements in filename will also be replaced. This replacement is done prior to any other Markdown processing. All file-names are evaluated relative to the location from which mkdocs is being built (path of mkdocs.yml).
    '''
    def __init__(self, md, config):
        super(ScriptIncludePreprocessor, self).__init__(md)
        self.base_path = config['base_path']
        self.encoding = config['encoding']

    def run(self, lines):
        done = False
        while not done:
            for line in lines:
                loc = lines.index(line)
                m = INC_SYNTAX.search(line)

                if m:
                    filename, hl = _parseArg(m.group(1))
                    filename = '%s/%s' % (os.getcwd(), filename)
                    try:
                        with open(filename, 'r', encoding=self.encoding) as r:
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
                    text = ['```py %s ' % hl] + text
                    text[-1] = '```'
                    text[0] = line_split[0] + text[0]
                    text[-1] = text[-1] + line_split[2]
                    lines = lines[:loc] + text + lines[loc+1:]
                    break
            else:
                done = True
        return lines


def makeExtension(*args,**kwargs):
    return ScriptInclude(kwargs)
