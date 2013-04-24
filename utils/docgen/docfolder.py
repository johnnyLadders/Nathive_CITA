#!/usr/bin/env python
#coding=utf-8

# Nathive (and this file) is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or newer.
#
# You should have received a copy of the GNU General Public License along with
# this file. If not, see <http://www.gnu.org/licenses/>.


import os
import docgen


class DocFolder(object):

    def __init__(self, infolder, outfolder):

        self.infolder = infolder
        self.outfolder = outfolder
        self.filenames = self.find_files()
        self.initpath = os.path.join(outfolder, '__init__.rst')


    def find_files(self):

        filenames = os.listdir(self.infolder)
        filenames.sort()
        filenames.remove('__init__.py')
        filenames = [x for x in filenames if '.py' in x]
        return filenames


    def clear_toc(self):

        data = open(self.initpath).read()
        content, toc = data.split('.. toctree::')
        toc = toc.split('\n')
        toc = [x for x in toc if x.startswith('   :')]
        toc = '\n'.join(toc)
        data = content + '.. toctree::\n' + toc + '\n\n'
        open(self.initpath, 'w').write(data)


    def generate(self):

        print 'generating documentation for %s' % self.infolder
        self.clear_toc()
        for filename in self.filenames:
            name, ext = os.path.splitext(filename)
            docspath = os.path.join(self.outfolder, '%s.rst' % name)
            codepath = os.path.join(self.infolder, filename)
            docfile = docgen.DocFile(codepath)
            rst = docfile.dump()
            open(docspath, 'w').write(rst)
            open(self.initpath, 'a').write('   %s\n' % name)
