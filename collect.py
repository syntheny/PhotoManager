#!/usr/bin/python3
"""
"collect.py" Photo Collector library and program

The Photo Collector is an application program that searches for photo and video files under
specific paths, collects image files, and stores the unique files in a "collections" folder. The
Collector function is a part of a "Photo Manager" utility that further processes the collected
files. As development of other parts of the PhotoManager evolve, those parts may be incorporated
into a single application, but that is yet to be determined.

In my environment, I have photo and video files scattered in various systems and media. Often,
that scattering is more of a redistribution of files from one form to another, without deletion
of the source files. For example, Files are uploaded from a camera SD card to a PC storage,
some files may be duplicated for whatever reason without change and placed in other folders,
then folders of files are automatically uploaded to the cloud (Google photo storage or Apple
cloud)--later, those cloud files are brought back to earth in another PC folder. Thus, a file can
be found on many folders on several PCs.

Another wrinkle in the scattering of photos is that many have been placed into folders named for
a date and/or a activity.

"""
from glob import glob
import os
import re
import sys

from tools import File


class List(list):
    def __init__(self, obj=None):
        if obj is None:
            super().__init__()
            return
        if not isinstance(obj, (list, tuple)):
            obj = [obj]
        super().__init__(obj)


class Collect:
    def __init__(self, paths:[str] = None, exts:[str] = None, *,
                 not_exts: [str] = None,
                 patterns:[str] = None,
                 recursive=False):
        self.paths: [str] = List(paths)

        self.recursive = recursive
        if not patterns:
            patterns = ['*']
        self.patterns = patterns

        if exts:
            self.exts = tuple([x if x[0]=='.' else f'.{x}' for x in List(exts)])
        else:
            self.exts = None

        if not_exts:
            self.not_exts = tuple([x if x[0]=='.' else f'.{x}' for x in List(not_exts)])
        else:
            self.not_exts = None

        self.exts_not_used = not self.exts and not self.not_exts

        self.files: [File] = []

        for dir_path in self.paths:
            self.collect(dir_path)

    def collect(self, dir_path):
        globs = []
        # glob collect everything, including direcroties which need to be filtered.
        for patt in self.patterns:
            if self.recursive:
                globs += glob(f'{dir_path}{os.sep}**{os.sep}{patt}', recursive=True)
            else:
                globs += glob(f'{dir_path}{os.sep}{patt}', recursive=False)

        # For each globbed item, a File object is created, then checked for "is_file", discarding
        # anything that is not.
        files = []
        for item in globs:
            file = File(item)
            if file.is_file:
                files.append(file)

        if self.exts_not_used:
            self.files += files
        else:
            if self.exts:
                for file in files:
                    if file.ext in self.exts:
                        self.files.append(file)
            if self.not_exts:
                for file in files:
                    if file.ext not in self.not_exts:
                        self.files.append(file)
