#!/usr/bin/python3
"""
Python "unittest" test module for photo collector library/program
"""
from copy import deepcopy
import os
import re
import shutil
from singleton_decorator import singleton
import subprocess
import sys
import unittest

sys.path.append('')
from tools import (chdir, make_folder, replicate, SingletonPattern, rewire_unittest,
                   File,
                   C_ROOT, PROGRAM_ABS_DIR, PROGRAM_NAME, IS_WINDOWS)

from collect import Collect

IMAGE_TYPES = ('.jpg', '.png', '.bmp', '.tif', '.jpeg')

# The photo files are in the TestData folder under the program path
TEST_SRC = os.path.join(PROGRAM_ABS_DIR, 'TestData')

# Test directory to which test files are copied
TEST_DIR = os.path.join(C_ROOT, 'Photos', 'Test')

UNITTEST_VERBOSITY = 2


class TestFile(File):
    """Test data file

    The source folder contains three sets of image files and some non-image files,
    where images are represented by all image types.
          graphics.*      - small paint-generated files without EXIF info
          photo.*         - small image files with EXIF info
          test_*.*        - Same image of various resolutions and various types
    """
    def __init__(self, file_path, dir_path=None):
        super().__init__(file_path, dir_path)
        self.is_image = self.ext in IMAGE_TYPES
        self.is_graphic = self.name.startswith('graphic')
        self.is_photo = self.name.startswith('photo')
        self.is_test_image = self.name.lower().startswith('test')


class TestData:
    _test_folder_number: int = None
    _test_folders: list = []
    _empty_folder: str = None
    _nonphoto_folder: str = None
    _photo_folder: str = None
    _many_photo_folder: str = None
    _deep_photo_folder: str = None
    _subfolder: str = None

    _src_files: {str:str} = {}
    _src_images: [str] = []
    _src_nonimages: [str] = []
    _src_graphics: [str] = []
    _src_photos: [str] = []
    _src_test_images: [str] = []


@singleton
class Common(TestData):

    def __init__(self):

        # Desination test folders are simply named using a root name
        self._test_folder_number = 0
        self._test_folders = []
    
        # Discover all files under the SRC directory
        # The source folder contains three sets of image files and some non-image files,
        # where images are represented by all image types.
        #       graphics.*      - small paint-generated files without EXIF info
        #       photo.*         - small image files with EXIF info
        #       test_*.*        - Same image of various resolutions and various types
        for file_path in os.listdir(TEST_SRC):
            file = TestFile(file_path, TEST_SRC)
            if file.is_file:
                self._src_files[file.file_name] = file
                if file.is_image:
                    self._src_images.append(file)
                    if file.is_photo:
                        self._src_photos.append(file)
                    elif file.is_graphic:
                        self._src_graphics.append(file)
                    elif file.is_test_image:
                        self._src_test_images.append(file)
                else:
                    self._src_nonimages.append(file)

        # Create 5 test folders
        for _ in range(5):
            dir_path = os.path.join(TEST_DIR, self.next_folder_name())
            self._test_folders.append(dir_path)
            make_folder(dir_path, clean=True)
        self._empty_folder = self._test_folders[0]
        self._nonphoto_folder = self._test_folders[1]
        self._photo_folder = self._test_folders[2]
        self._many_photo_folder = self._test_folders[3]
        self._deep_photo_folder = self._test_folders[4]

        # Create subfolder under last test path
        dir_path = os.path.join(self._test_folders[-1], self.next_folder_name())
        self._test_folders.append(dir_path)
        make_folder(dir_path, clean=True)
        self._subfolder = self._test_folders[5]

        # Folder 0: empty

        # Folder 1: one non-photo file
        for file in self._src_nonimages:
            if file.ext == '.txt':
                file.copy_to(self._nonphoto_folder)
                break

        # Folder 2: one photo file
        for file in self._src_photos:
            if file.ext == '.bmp':
                file.copy_to(self._photo_folder)
                break

        # Folder 3: all supported photo files
        for file in self._src_images:
            file.copy_to(self._many_photo_folder)

        # Folder 4: all supported photo files with some non-photo files
        for file in self._src_files.values():
            file.copy_to(self._deep_photo_folder)

        # Folder 4/subfolder: all supported photo files with some non-photo files
        for file in self._src_files.values():
            file.copy_to(self._subfolder)

    def next_folder_name(self):
        self._test_folder_number += 1
        return f'test_folder{self._test_folder_number}'

    def copy_common(self, other):
        """Copy my non-callable attributes to another object"""
        for key in dir(self):
            if key.startswith('__'):
                continue
            value = getattr(self, key)
            if isinstance(value, (str, int, float, tuple)):
                setattr(other, key, value)
            elif isinstance(value, (list, dict, set)):
                setattr(other, key, deepcopy(value))


class CommonTest(unittest.TestCase, TestData):

    @classmethod
    def setUpClass(cls):
        cls.common = Common()
        replicate(cls.common, cls)


class Test1_CollectStructure(CommonTest):
    """
    Test the "collect.py" library and program
    """

    def test_collector_library(self):
        try:
            import collect
        except (ImportError, ModuleNotFoundError):
            self.fail("Unable to import collect.py library")
        col = collect.Collect()

    def test_collector_import_class(self):
        try:
            from collect import Collect
        except ModuleNotFoundError:
            self.fail("Unable to import collect.py library")
        except ImportError:
            self.fail("Unable to import 'Collect' class from collect.py library")
        col = Collect()

    def test_collector_program(self):
        try:
            if IS_WINDOWS:
                subprocess.call(['py', 'collect.py'])
            else:
                subprocess.call(['/usr/bin/python3', 'collect.py'])
        except subprocess.CalledProcessError:
            self.fail("Unable to invoke collect.py program")


class Test2_CommonSetup(CommonTest):

    def test_all_folders(self):
        # Assure all folders exist
        self.assertEqual(len(self._test_folders), 6)
        for n in range(5):
            folder_path = self._test_folders[n]
            expected_file_name = f'test_folder{n+1}'
            dir_part, name_part = os.path.split(folder_path)
            self.assertEqual(dir_part, TEST_DIR)
            self.assertEqual(name_part, expected_file_name)
            self.assertTrue(os.path.isdir(folder_path), f"Folder path '{folder_path}' not found")

        folder_path = self._subfolder
        expected_file_name = f'test_folder6'
        name_part = os.path.split(folder_path)[1]
        self.assertEqual(name_part, expected_file_name)
        self.assertTrue(os.path.isdir(folder_path), f"Folder path '{folder_path}' not found")

    def _get_folder_content(self, dir_path):
        return list(os.listdir(dir_path))

    def test_folder1(self):
        # Validate folder 1 is empty
        content = self._get_folder_content(self._empty_folder)
        self.assertEqual(len(content), 0)

    def test_folder2(self):
        # Validate folder 2 has one non-photo file
        content = self._get_folder_content(self._nonphoto_folder)
        self.assertEqual(len(content), 1, "Too many files in non-photo folder")
        self.assertTrue(content[0].endswith('.txt'), f"Content unexpected: {str(content)}")

    def test_folder3(self):
        # Validate folder 3 has a photo file
        content = self._get_folder_content(self._photo_folder)
        self.assertEqual(len(content), 1)
        self.assertTrue(content[0].endswith(IMAGE_TYPES), f"Content unexpected: {str(content)}")

    def test_folder4(self):
        # Validate folder 4 has all photo types
        counters = {}
        content = self._get_folder_content(self._many_photo_folder)
        for file in content:
            ext = os.path.splitext(file)[1]
            if ext not in counters:
                counters[ext] = 0
            counters[ext] += 1
        for ext in IMAGE_TYPES:
            self.assertTrue(ext in counters, f"File type {ext} not found in "
                                              f"{self._many_photo_folder}")

    def test_folder5(self):
        # Validate folder 5 has all photo types
        counters = {}
        content = self._get_folder_content(self._deep_photo_folder)
        for file in content:
            ext = os.path.splitext(file)[1]
            if ext not in counters:
                counters[ext] = 0
            counters[ext] += 1
        for ext in IMAGE_TYPES:
            self.assertTrue(ext in counters, f"File type {ext} not found in "
                                              f"{self._deep_photo_folder}")

    def test_folder6(self):
        # Validate folder 5 has all photo types
        counters = {}
        content = self._get_folder_content(self._subfolder)
        for file in content:
            ext = os.path.splitext(file)[1]
            if ext not in counters:
                counters[ext] = 0
            counters[ext] += 1
        for ext in IMAGE_TYPES:
            self.assertTrue(ext in counters, f"File type {ext} not found in "
                                              f"{self._subfolder}")


class Test3_Collection(CommonTest):
    
    unexpected = "Unexpected collection from nonphoto folder"

    def test_empty(self):
        collection = Collect(self._empty_folder, IMAGE_TYPES)
        self.assertEqual(len(collection.files), 0, "Empty folder is not empty")

    def test_folder1(self):
        collection = Collect(self._empty_folder, IMAGE_TYPES)
        self.assertEqual(len(collection.files), 0, "Collected something from empty folder")

    def test_folder2_any_file(self):
        collection = Collect(self._nonphoto_folder)
        self.assertEqual(len(collection.files), 1, self.unexpected)

    def test_folder2_photo(self):
        collection = Collect(self._nonphoto_folder, IMAGE_TYPES)
        self.assertEqual(len(collection.files), 0, self.unexpected)

    def test_folder2_text_file(self):
        collection = Collect(self._nonphoto_folder, 'txt')
        self.assertEqual(len(collection.files), 1, self.unexpected)

    def test_folder3_any_file(self):
        collection = Collect(self._photo_folder)
        self.assertEqual(len(collection.files), 1, self.unexpected)

    def test_folder3_photo(self):
        collection = Collect(self._photo_folder, IMAGE_TYPES)
        self.assertEqual(len(collection.files), 1, self.unexpected)

    def test_folder3_text_file(self):
        collection = Collect(self._photo_folder, 'txt')
        self.assertEqual(len(collection.files), 0, self.unexpected)

    def test_folder4_no_image(self):
        # _many_photo_folder is expeced to contain only image files
        collection = Collect(self._many_photo_folder, not_exts=IMAGE_TYPES)
        self.assertEqual(len(collection.files), 0, self.unexpected)

    def test_folder4_any_file(self):
        # _many_photo_folder is expected to contain only image files
        collection = Collect(self._many_photo_folder)
        self.assertEqual(len(collection.files), len(self._src_images), self.unexpected)

    def test_folder4_photo(self):
        collection = Collect(self._many_photo_folder, IMAGE_TYPES)
        self.assertEqual(len(collection.files), len(self._src_images), self.unexpected)

    def test_folder4_text_file(self):
        collection = Collect(self._many_photo_folder, 'txt')
        self.assertEqual(len(collection.files), 0, self.unexpected)

    def test_folder5rec_no_image(self):
        collection = Collect(self._deep_photo_folder, not_exts=IMAGE_TYPES, recursive=True)
        self.assertEqual(len(collection.files), 2*len(self._src_nonimages), self.unexpected)

    def test_folder5rec_any_file(self):
        # _deep_photo_folder is expeced to contain only image files
        collection = Collect(self._deep_photo_folder, recursive=True)
        self.assertEqual(len(collection.files), 2*len(self._src_files), self.unexpected)

    def test_folder5rec_photo(self):
        collection = Collect(self._deep_photo_folder, IMAGE_TYPES, recursive=True)
        self.assertEqual(len(collection.files), 2*len(self._src_images), self.unexpected)

    def test_folder5rec_text_file(self):
        collection = Collect(self._deep_photo_folder, 'txt', recursive=True)
        self.assertEqual(len(collection.files), 2, self.unexpected)


class Test4_CommandLine(CommonTest):
    """
    Test command line options

    The collect.py is expected to have an "Options" class that parses the command line. The
    Options init method may take command line from system, or as passed to the init method.

    Each test case method will invoke the instantiation separately, both through a library import
    and through program call.
    """
    import collect

    def setUp(self):
        pass

    def empty_command_line(self):
        pass


if __name__ == '__main__':
    rewire_unittest()
    unittest.main(module=PROGRAM_NAME, verbosity=UNITTEST_VERBOSITY)
