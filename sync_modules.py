import os
import shutil
import sys


class _Module:
    def __init__(self, dir_path, rel_file_path):
        self.rel_file_path = rel_file_path.replace('\\', os.sep).replace('/', os.sep)
        self.dir_path = os.path.abspath(dir_path)
        self.file_path = os.path.join(self.dir_path, self.rel_file_path)
        self.name = os.path.splitext(os.path.split(self.rel_file_path)[1])[0]
        self.exists = os.path.isfile(self.file_path)
        if self.exists:
            self.mod_time = os.stat(self.file_path).st_mtime
        else:
            self.mod_time = 0

    def sync(self, other):
        if self.mod_time == other.mod_time:
            return False
        if self.mod_time < other.mod_time:
            shutil.copy2(other.file_path, self.file_path)
        elif self.exists:
            shutil.copy2(self.file_path, other.file_path)
        else:
            raise ImportError(f"Unable to synchronize module {self.rel_file_path}"
                              "--missing source"
                              )
        del sys.modules[self.name]
        __import__(self.name, [], ())
        return True


class _Sync:

    def __init__(self):
        _tools_repo = r'C:\Tools' if 'win' in sys.platform else '/mnt/c/Tools'
        _curdir = os.getcwd()

        _other = _Module(_tools_repo, 'tools.py')
        _mine = _Module(_curdir, 'tools.py')
        _mine.sync(_other)
        
        _other = _Module(_tools_repo, 'sync_modules.py')
        _mine = _Module(_curdir, 'sync_modules.py')
        _mine.sync(_other)


_sync = _Sync()

