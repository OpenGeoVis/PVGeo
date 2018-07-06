#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  doc-download-button.py
#

from __future__ import print_function
import re
from codecs import open
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor

DLBTN_SYNTAX = re.compile(r'\{btn:\s*(.+?)\s*\}')

class DownloadButton(Extension):
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
            'include', DownloadButtonPreprocessor(md,self.getConfigs()),'_begin'
        )


class DownloadButtonPreprocessor(Preprocessor):
    '''This includes an ability to make a download button'''
    def __init__(self, md, config):
        super(DownloadButtonPreprocessor, self).__init__(md)
        self.base_path = config['base_path']
        self.encoding = config['encoding']

    def _genButton(self, link, width=r'width:100%'):
        return ['''<a href="%s"><button class="btn" style="%s"><i class="fa fa-download"></i> Download</button></a>''' % (link, width)]

    def run(self, lines):
        done = False
        while not done:
            for line in lines:
                loc = lines.index(line)
                m = DLBTN_SYNTAX.search(line)
                if m:
                    text = self._genButton(m.group(1))
                    line_split = DLBTN_SYNTAX.split(line,maxsplit=0)
                    if len(text) == 0: text.append('')
                    #text = ['File Included From: %s' % filename] + text
                    text[0] = line_split[0] + text[0]
                    text[-1] = text[-1] + line_split[2]
                    lines = lines[:loc] + text + lines[loc+1:]
                    break
            else:
                done = True
        return lines


def makeExtension(*args,**kwargs):
    return DownloadButton(kwargs)
