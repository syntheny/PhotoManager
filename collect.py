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
import os
import re
import sys


class Collect:
    pass

if __name__ == '__main__':
    collect = Collect()
