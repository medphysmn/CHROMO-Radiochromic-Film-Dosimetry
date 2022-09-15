
#!/usr/bin/env python3
"""TODO: Put module docstring HERE.
"""

# =============================================================================
# Copyright (C) 2020 Ljubomir Kurij <kurijlj@gmail.com>
#
# This file is part of Radiochromic Denoiser.
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option)
# any later version.
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.
#
# =============================================================================


# =============================================================================
#
# 2020-10-25 Ljubomir Kurij <kurijlj@gmail.com>
#
# * data_dir_tsests.py: created.
#
# =============================================================================


# ============================================================================
#
# TODO:
#
#
# ============================================================================


# ============================================================================
#
# References (this section should be deleted in the release version)
#
#
# ============================================================================

# =============================================================================
# Modules import section
# =============================================================================

import unittest
from os.path import basename
from pathlib import Path
from algorithms import DataDir


# =============================================================================
# Test cases
# =============================================================================

TEST_CASES = [
    # Empty dataset (uninitialized).
    DataDir(),
    DataDir(''),  # Path class handles this as current dir.
    DataDir('.'),
    DataDir('./data'),
    DataDir('./actions.py'),
    DataDir('.', 'py'),
    DataDir('./data', 'tif'),
    ]


# =============================================================================
# Unit testing classes
# =============================================================================

class TestEmptyDatadir(unittest.TestCase):
    """TODO: Put class docstring HERE.
    """

    def setUp(self):
        """TODO: Put method docstring HERE.
        """

        self._dataset = TEST_CASES[0]

    def testForNone(self):
        """TODO: Put method docstring HERE.
        """

        self.assertEqual(self._dataset.isNone, True)

    def testExitence(self):
        """TODO: Put method docstring HERE.
        """

        self.assertEqual(self._dataset.exists, False)

    def testIfDir(self):
        """TODO: Put method docstring HERE.
        """

        self.assertEqual(self._dataset.isDir, False)

    def testIfFile(self):
        """TODO: Put method docstring HERE.
        """

        self.assertEqual(self._dataset.isFile, False)

    def testDataFileType(self):
        """TODO: Put method docstring HERE.
        """

        self.assertEqual(self._dataset.dataFileType, 'Any')

    def testFileList(self):
        """TODO: Put method docstring HERE.
        """

        self.assertEqual(self._dataset.listDataFiles(), None)

    def testAbsolutePath(self):
        """TODO: Put method docstring HERE.
        """

        self.assertEqual(self._dataset.absolutePath, None)

    def testName(self):
        """TODO: Put method docstring HERE.
        """

        self.assertEqual(self._dataset.name, None)

    def testIfEmpty(self):
        """TODO: Put method docstring HERE.
        """

        self.assertEqual(self._dataset.isEmpty, True)


class TestEmptyString(unittest.TestCase):
    """TODO: Put class docstring HERE.
    """

    def setUp(self):
        """TODO: Put method docstring HERE.
        """

        self._dataset = TEST_CASES[1]

    def testForNone(self):
        """TODO: Put method docstring HERE.
        """

        self.assertEqual(self._dataset.isNone, False)

    def testExitence(self):
        """TODO: Put method docstring HERE.
        """

        self.assertEqual(self._dataset.exists, True)

    def testIfDir(self):
        """TODO: Put method docstring HERE.
        """

        self.assertEqual(self._dataset.isDir, True)

    def testIfFile(self):
        """TODO: Put method docstring HERE.
        """

        self.assertEqual(self._dataset.isFile, False)

    def testDataFileType(self):
        """TODO: Put method docstring HERE.
        """

        self.assertEqual(self._dataset.dataFileType, 'Any')

    def testAbsolutePath(self):
        """TODO: Put method docstring HERE.
        """

        self.assertEqual(self._dataset.absolutePath, Path('').resolve())

    def testName(self):
        """TODO: Put method docstring HERE.
        """

        self.assertEqual(self._dataset.name, Path('').name)

    def testIfEmpty(self):
        """TODO: Put method docstring HERE.
        """

        self.assertEqual(self._dataset.isEmpty, False)


class TestCurrentDir(unittest.TestCase):
    """TODO: Put class docstring HERE.
    """

    def setUp(self):
        """TODO: Put method docstring HERE.
        """

        self._dataset = TEST_CASES[2]

    def testForNone(self):
        """TODO: Put method docstring HERE.
        """

        self.assertEqual(self._dataset.isNone, False)

    def testExitence(self):
        """TODO: Put method docstring HERE.
        """

        self.assertEqual(self._dataset.exists, True)

    def testIfDir(self):
        """TODO: Put method docstring HERE.
        """

        self.assertEqual(self._dataset.isDir, True)

    def testIfFile(self):
        """TODO: Put method docstring HERE.
        """

        self.assertEqual(self._dataset.isFile, False)

    def testDataFileType(self):
        """TODO: Put method docstring HERE.
        """

        self.assertEqual(self._dataset.dataFileType, 'Any')

    def testAbsolutePath(self):
        """TODO: Put method docstring HERE.
        """

        self.assertEqual(self._dataset.absolutePath, Path('.').resolve())

    def testName(self):
        """TODO: Put method docstring HERE.
        """

        self.assertEqual(self._dataset.name, Path('.').name)

    def testIfEmpty(self):
        """TODO: Put method docstring HERE.
        """

        self.assertEqual(self._dataset.isEmpty, False)


class TestRealDir(unittest.TestCase):
    """TODO: Put class docstring HERE.
    """

    def setUp(self):
        """TODO: Put method docstring HERE.
        """

        self._dataset = TEST_CASES[3]

    def testForNone(self):
        """TODO: Put method docstring HERE.
        """

        self.assertEqual(self._dataset.isNone, False)

    def testExitence(self):
        """TODO: Put method docstring HERE.
        """

        self.assertEqual(self._dataset.exists, True)

    def testIfDir(self):
        """TODO: Put method docstring HERE.
        """

        self.assertEqual(self._dataset.isDir, True)

    def testIfFile(self):
        """TODO: Put method docstring HERE.
        """

        self.assertEqual(self._dataset.isFile, False)

    def testDataFileType(self):
        """TODO: Put method docstring HERE.
        """

        self.assertEqual(self._dataset.dataFileType, 'Any')

    def testFileList(self):
        """TODO: Put method docstring HERE.
        """

        fl = (
            'img20191023_12463056.tif',
            'img20191101_13592687.png',
            'QA20200727016.tif',
            'QA20200727017.tif',
            'QA20200727018.tif',
            'QA20200727019.tif',
            'QA20200727020.tif',
            'test_dummy.py',
            'test_dummy.tif',
            'test_dummy.txt'
            )

        result = list()
        for path in self._dataset.listDataFiles():
            result.append(basename(path))

        self.assertEqual(tuple(result), fl)

    def testAbsolutePath(self):
        """TODO: Put method docstring HERE.
        """

        self.assertEqual(self._dataset.absolutePath, Path('./data').resolve())

    def testName(self):
        """TODO: Put method docstring HERE.
        """

        self.assertEqual(self._dataset.name, Path('./data').name)

    def testIfEmpty(self):
        """TODO: Put method docstring HERE.
        """

        self.assertEqual(self._dataset.isEmpty, False)


class TestRealFile(unittest.TestCase):
    """TODO: Put class docstring HERE.
    """

    def setUp(self):
        """TODO: Put method docstring HERE.
        """

        self._dataset = TEST_CASES[4]

    def testForNone(self):
        """TODO: Put method docstring HERE.
        """

        self.assertEqual(self._dataset.isNone, False)

    def testExitence(self):
        """TODO: Put method docstring HERE.
        """

        self.assertEqual(self._dataset.exists, True)

    def testIfDir(self):
        """TODO: Put method docstring HERE.
        """

        self.assertEqual(self._dataset.isDir, False)

    def testIfFile(self):
        """TODO: Put method docstring HERE.
        """

        self.assertEqual(self._dataset.isFile, True)

    def testDataFileType(self):
        """TODO: Put method docstring HERE.
        """

        self.assertEqual(self._dataset.dataFileType, 'Any')

    def testFileList(self):
        """TODO: Put method docstring HERE.
        """

        self.assertEqual(self._dataset.listDataFiles(), None)

    def testAbsolutePath(self):
        """TODO: Put method docstring HERE.
        """

        self.assertEqual(
            self._dataset.absolutePath,
            Path('./actions.py').resolve()
            )

    def testName(self):
        """TODO: Put method docstring HERE.
        """

        self.assertEqual(self._dataset.name, Path('./actions.py').name)

    def testIfEmpty(self):
        """TODO: Put method docstring HERE.
        """

        self.assertEqual(self._dataset.isEmpty, True)


class TestDirWithPythonScripts(unittest.TestCase):
    """TODO: Put class docstring HERE.
    """

    def setUp(self):
        """TODO: Put method docstring HERE.
        """

        self._dataset = TEST_CASES[5]

    def testForNone(self):
        """TODO: Put method docstring HERE.
        """

        self.assertEqual(self._dataset.isNone, False)

    def testExitence(self):
        """TODO: Put method docstring HERE.
        """

        self.assertEqual(self._dataset.exists, True)

    def testIfDir(self):
        """TODO: Put method docstring HERE.
        """

        self.assertEqual(self._dataset.isDir, True)

    def testIfFile(self):
        """TODO: Put method docstring HERE.
        """

        self.assertEqual(self._dataset.isFile, False)

    def testDataFileType(self):
        """TODO: Put method docstring HERE.
        """

        self.assertEqual(self._dataset.dataFileType, 'py')

    def testFileList(self):
        """TODO: Put method docstring HERE.
        """

        fl = (
            'actions.py',
            'algorithms.py',
            'data_dir_tests.py',
            'denoise.py'
            )

        result = list()
        for path in self._dataset.listDataFiles():
            result.append(basename(path))

        self.assertEqual(tuple(result), fl)

    def testAbsolutePath(self):
        """TODO: Put method docstring HERE.
        """

        self.assertEqual(self._dataset.absolutePath, Path('.').resolve())

    def testName(self):
        """TODO: Put method docstring HERE.
        """

        self.assertEqual(self._dataset.name, Path('.').name)

    def testIfEmpty(self):
        """TODO: Put method docstring HERE.
        """

        self.assertEqual(self._dataset.isEmpty, False)


class TestDirWithTifImages(unittest.TestCase):
    """TODO: Put class docstring HERE.
    """

    def setUp(self):
        """TODO: Put method docstring HERE.
        """

        self._dataset = TEST_CASES[6]

    def testForNone(self):
        """TODO: Put method docstring HERE.
        """

        self.assertEqual(self._dataset.isNone, False)

    def testExitence(self):
        """TODO: Put method docstring HERE.
        """

        self.assertEqual(self._dataset.exists, True)

    def testIfDir(self):
        """TODO: Put method docstring HERE.
        """

        self.assertEqual(self._dataset.isDir, True)

    def testIfFile(self):
        """TODO: Put method docstring HERE.
        """

        self.assertEqual(self._dataset.isFile, False)

    def testDataFileType(self):
        """TODO: Put method docstring HERE.
        """

        self.assertEqual(self._dataset.dataFileType, 'tif')

    def testFileList(self):
        """TODO: Put method docstring HERE.
        """

        fl = (
            'img20191023_12463056.tif',
            'QA20200727016.tif',
            'QA20200727017.tif',
            'QA20200727018.tif',
            'QA20200727019.tif',
            'QA20200727020.tif',
            'test_dummy.tif'
            )

        result = list()
        for path in self._dataset.listDataFiles():
            result.append(basename(path))

        self.assertEqual(tuple(result), fl)

    def testAbsolutePath(self):
        """TODO: Put method docstring HERE.
        """

        self.assertEqual(self._dataset.absolutePath, Path('./data').resolve())

    def testName(self):
        """TODO: Put method docstring HERE.
        """

        self.assertEqual(self._dataset.name, Path('./data').name)

    def testIfEmpty(self):
        """TODO: Put method docstring HERE.
        """

        self.assertEqual(self._dataset.isEmpty, False)


# =============================================================================
# Script main body
# =============================================================================

if __name__ == '__main__':
    unittest.main()
