import contextlib
from copy import deepcopy
from datetime import datetime
from glob import glob
import hashlib
import os
import re
import shutil
import sys
import subprocess
import traceback
import unittest

import py7zr

# The "tools.py" library module is maintained under a Tools repository. However, it also needs to
# be copied into this project repository so that its current state can be committed to the
# project repository. The same is true for "sync_modules.py" which is a small module unlikely to
# change frequently.
import sync_modules


PROGRAM_DIR, PROGRAM_FILE_NAME = os.path.split(sys.argv[0])
PROGRAM_ABS_DIR = os.path.abspath(PROGRAM_DIR)
PROGRAM_NAME = os.path.splitext(PROGRAM_FILE_NAME)[0]

C_ROOT = list(filter(lambda x: os.path.isdir(x + os.sep + 'Windows'), ['/mnt/c', '/c', 'C:']))[0]
C_ROOT += os.sep
IS_WINDOWS = 'win' in sys.platform


class Error:
    def __init__(self, msg, exit=True, trace=False):
        if exit:
            msg += ' -- program terminated'
        print(f"ERROR: {msg}")
        if trace:
            traceback.print_stack()
        if exit:
            sys.exit(2)


@contextlib.contextmanager
def chdir(new_dir=None):
    curdir = os.getcwd()
    if new_dir is None:
        new_dir = curdir
    elif not os.path.isdir(new_dir):
        raise OSError("No directory '%s'" % new_dir)
    os.chdir(new_dir)
    try:
        yield new_dir
    finally:
        os.chdir(curdir)


def clean_folder(dir_path):
    """Clean files and subfolders from directory"""
    shutil.rmtree(dir_path, ignore_errors=True)


def make_folder(dir_path, clean=True):
    """Make folder path; optionally clean of files and subfolders if it already exists"""
    if os.path.isdir(dir_path):
        if clean:
            clean_folder(dir_path)
    os.makedirs(dir_path, exist_ok=True)


def replicate(src, dst):
    """Copy my non-callable attributes to another object"""
    for key in dir(src):
        if key.startswith('__'):
            continue
        value = getattr(src, key)
        if isinstance(value, (str, int, float, tuple)):
            setattr(dst, key, value)
        elif isinstance(value, (list, dict, set)):
            setattr(dst, key, deepcopy(value))


def _getTestCaseNames(self, test_class):
    """Return a sorted sequence of method names found within test_class

    self is an unittest.TestLoader instance
    """
    from fnmatch import fnmatchcase

    def is_test_method(attrname):
        if not attrname.startswith(self.testMethodPrefix):
            return False
        testFunc = getattr(test_class, attrname)
        if not callable(testFunc):
            return False
        fullName = f'%s.%s.%s' % (
            test_class.__module__, test_class.__qualname__, attrname
            )
        return self.testNamePatterns is None or \
               any(fnmatchcase(fullName, pattern) for pattern in self.testNamePatterns)

    lineno_names: [(int,str)] = []

    for name in filter(is_test_method, dir(test_class)):
        lineno = getattr(test_class, name).__code__.co_firstlineno
        lineno_names.append((lineno, name))

    lineno_names.sort()
    names = [name for line, name in lineno_names]
    return names


def rewire_unittest():
    setattr(unittest.TestLoader, 'getTestCaseNames', _getTestCaseNames)


def unpack_archive(src_archive_file:str, dst_dir:str):
    """Unpack an archive file into the destination directory--may be 7z, 7zip, zip, or other 
    format"""
    shutil.register_unpack_format('7zip', ['.7z'], py7zr.unpack_7zarchive)
    shutil.unpack_archive(src_archive_file, dst_dir)

def pack_archive(dst_archive_file:str, files:[]):
    """Create an archive file--the extent indicates the format"""
    shutil.register_archive_format('7zip', ['7z'], py7zr.pack_7zarchive())
    dir_path, file_name = os.path.split(dst_archive_file)
    base_name, format = os.path.splitext(file_name)
    if format and format[0] == '.':
        format = format[1:]
    shutil.make_archive(base_name, format)

class SingletonPattern:
    """Singleton Pattern decorator"""
    _instance = None
    _cls = None

    def __init__(self, cls):
        self._cls = cls

    def __call__(self, *arg, **kwargs):
        if self._instance is None:
            self._instance = self._cls(*arg, **kwargs)
        return self._instance


class File:
    """Generic file handler"""
    def __init__(self, file_path, dir_path=None):
        """file_path is just the file name if dir_path is specified"""
        if dir_path:
            self.file_path = os.path.abspath(os.path.join(dir_path, file_path))
            self.dir_path = dir_path
            self.file_name = file_path
        else:
            self.file_path = os.path.abspath(file_path)
            self.dir_path, self.file_name = os.path.split(self.file_path)
        self.name, self.ext = os.path.splitext(self.file_name)
        self._exists = None
        self._is_dir = None
        self._is_file = None
        self._hash = None
        self._stats = None

    def __str__(self):
        return f"{self.file_name} -- {self.file_path}"
        
    @property
    def is_dir(self):
        if self._is_dir is None:
            self._is_dir = os.path.isdir(self.file_path)
            if self._is_dir:
                self._exists = True
        return self._is_dir

    @property
    def is_file(self):
        if self._is_file is None:
            self._is_file = os.path.isfile(self.file_path)
            if self._is_file:
                self._exists = True
        return self._is_file

    @property
    def exists(self):
        if self._exists is None:
            self._is_dir = os.path.isdir(self.file_path)
            self._is_file = os.path.isfile(self.file_path)
            self._exists = self._is_dir or self._is_file
        return self._exists

    @property
    def hash(self):
        if self._hash is None:
            with open(self.file_path, 'rb') as f:
                self._hash = hashlib.file_digest(f, 'sha1').hexdigest()
        return self._hash

    @property
    def stats(self):
        if self._stats is None:
            self._stats = os.stats(self.file_path)
        return self._stats

    def copy_to(self, dst_path):
        """Copy file to destination path"""
        try:
            shutil.copy(self.file_path, dst_path)
        except PermissionError:
            Error(f"Copy {self.file_name} to {dst_path} -- no permission")
        except KeyboardInterrupt:
            Error(f"Copy {self.file_name} to {dst_path} -- Keyboard interrupt")
        except Exception as exc:
            Error(f"Copy {self.file_name} to {dst_path} -- {exc}")
