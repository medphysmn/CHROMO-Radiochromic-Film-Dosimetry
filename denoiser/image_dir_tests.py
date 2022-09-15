
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
# 2020-11-01 Ljubomir Kurij <kurijlj@gmail.com>
#
# * image_dir_tsests.py: created.
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
from algorithms import ImageDir


# =============================================================================
# Test cases
# =============================================================================

TEST_CASES = [
    ImageDir('./data', 'tiff'),
    ImageDir('./data/test_empty', 'tiff'),
    ]


# =============================================================================
# Unit testing classes
# =============================================================================

class TestDirWithTifImages(unittest.TestCase):
    """TODO: Put class docstring HERE.
    """

    def setUp(self):
        """TODO: Put method docstring HERE.
        """

        self._dataset = TEST_CASES[0]

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

        self.assertEqual(self._dataset.dataFileType, 'tiff')

    def testFileList(self):
        """TODO: Put method docstring HERE.
        """

        fl = (
            'img20191023_12463056.tif',
            'QA20200727016.tif',
            'QA20200727017.tif',
            'QA20200727018.tif',
            'QA20200727019.tif',
            'QA20200727020.tif'
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


class TestEmptyDir(unittest.TestCase):
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

        self.assertEqual(self._dataset.dataFileType, 'tiff')

    def testFileList(self):
        """TODO: Put method docstring HERE.
        """

        self.assertEqual(self._dataset.listDataFiles(), None)

    def testAbsolutePath(self):
        """TODO: Put method docstring HERE.
        """

        self.assertEqual(self._dataset.absolutePath, Path('./data/test_empty').resolve())

    def testName(self):
        """TODO: Put method docstring HERE.
        """

        self.assertEqual(self._dataset.name, Path('./data/test_empty').name)

    def testIfEmpty(self):
        """TODO: Put method docstring HERE.
        """

        self.assertEqual(self._dataset.isEmpty, True)


# =============================================================================
# Script main body
# =============================================================================

if __name__ == '__main__':
    unittest.main()
