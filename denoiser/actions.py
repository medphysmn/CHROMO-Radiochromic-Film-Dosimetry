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
# 2020-10-25 Ljubomir Kurij <ljubomir_kurij@protonmail.com>
#
# * actions.py: created.
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

from sys import (
    stderr,
    stdout
    )
from os.path import basename
from enum import Enum
from scipy import ndimage
from tifffile import (
    imwrite,
    TiffFile
    )
import numpy as np
from algorithms import (
    ColorChannelOption,
    FilterSelectionValidate,
    gaussian_kernel,
    ImageDir,
    Path,
    res_unit_value,
    TiffConformityMatch,
    wiener_filter
    )


# =============================================================================
# Module level constants
# =============================================================================


# =============================================================================
# Module utility classes and functions
# =============================================================================

class AppError(Enum):
    """TODO: Put class docstring here.
    """

    noerror = 0
    wrongunits = 1
    nonexistentpath = 2
    notdir = 3
    emptydir = 4
    novalidimages = 5
    invalidcolorchannel = 6
    invalidfilter = 7
    invalidkernelsize = 8


# =============================================================================
# App action classes
# =============================================================================

class ProgramAction():
    """Abstract base class for all program actions, that provides execute.

    The execute method contains code that will actually be executed after
    arguments parsing is finished. The method is called from within method
    run of the CommandLineApp instance.
    """

    def __init__(self, exitf):
        self._exit_app = exitf

    def execute(self):
        """Put method docstring HERE.
        """


class ProgramUsageAction(ProgramAction):
    """Program action that formats and displays usage message to the stdout.
    """

    def __init__(self, parser, exitf):
        super().__init__(exitf)
        self._usg_msg = \
            '{usage}Try \'{prog} --help\' for more information.'\
            .format(usage=parser.format_usage(), prog=parser.prog)

    def execute(self):
        """Put method docstring HERE.
        """

        print(self._usg_msg)
        self._exit_app()


class ShowVersionAction(ProgramAction):
    """Program action that formats and displays program version information
    to the stdout.
    """

    def __init__(self, prog, ver, year, author, license, exitf):
        super().__init__(exitf)
        self._ver_msg = \
            '{0} {1} Copyright (C) {2} {3}\n{4}'\
            .format(prog, ver, year, author, license)

    def execute(self):
        """Put method docstring HERE.
        """

        print(self._ver_msg)
        self._exit_app()


class DefaultAction(ProgramAction):
    """Program action that wraps some specific code to be executed based on
    command line input. In this particular case it prints simple message
    to the stdout.
    """

    def __init__(self, prog, exitf):
        super().__init__(exitf)
        self._program_name = prog
        # Set default path for seraching for film scans.
        self._scans_path = ImageDir('.', 'tiff')
        self._filter_validator = FilterSelectionValidate()
        self._img_validator = TiffConformityMatch()
        self._selchnl = ColorChannelOption()

    @property
    def color_channel(self):
        """Put method docstring HERE.
        """

        return self._selchnl.value

    @color_channel.setter
    def color_channel(self, chnl):
        """Put method docstring HERE.
        """

        if chnl is not None:
            self._selchnl = ColorChannelOption(chnl)

    @property
    def image_validator(self):
        """Put method docstring HERE.
        """

        return (
            self._img_validator.target_size,
            self._img_validator.target_units,
            self._img_validator.target_resolution
            )

    @property
    def scans_path(self):
        """Put method docstring HERE.
        """

        return self._scans_path.absolutePath

    @scans_path.setter
    def scans_path(self, scans_path):
        """Put method docstring HERE.
        """

        if scans_path is not None:
            self._scans_path = ImageDir(scans_path, 'tiff')

    def execute(self):
        """Put method docstring HERE.
        """

        # Do some sanity checks first. First we chack if all options arguments
        # passed are valid. So verify if correct resolution units are passed
        # as option.
        if not self._img_validator.validUnits():
            # Invalid units string passed as option argument.
            print(
                '{0}: Supplied resolution units \'{1}\' are not supported.'\
                        .format(
                    self._program_name,
                    self._img_validator.target_units
                    ),
                file=stderr
                )
            self._exit_app(AppError.wrongunits)

        # Then we check if supplied path to scans exists at all, is directory
        # and is not empty.
        if not self._scans_path.exists:
            print(
                '{0}: Supplied path \'{1}\' does not exist.'.format(
                    self._program_name,
                    self._scans_path.absolutePath
                    ),
                file=stderr
                )
            self._exit_app(AppError.nonexistentpath)

        # Check if provided path is directory at all.
        if not self._scans_path.isDir:
            print(
                '{0}: Supplied path \'{1}\' is not a dir.'.format(
                    self._program_name,
                    self._scans_path.absolutePath
                    ),
                file=stderr
                )
            self._exit_app(AppError.notdir)

        # Check if provided path is empty (contain no files).
        if self._scans_path.isEmpty:
            # Supplied path contains no files.
            print(
                '{0}: Supplied path \'{1}\' contains no image files.'.format(
                    self._program_name,
                    self._scans_path.absolutePath
                    ),
                file=stderr
                )
            self._exit_app(AppError.emptydir)

        # Check if selected image denoising filter is valid (if one selected at
        # all).
        if self._filter_validator.FilterIsSelected():
            if not self._filter_validator.FilterIsValid():
                # Invalid filter selected.
                print(
                    '{0}: Selected image filter ({1}) is not supported.'\
                            .format(
                        self._program_name,
                        self._filter_validator.filter
                        ),
                    file=stderr
                    )
                self._exit_app(AppError.invalidfilter)

            if not self._filter_validator.KernelSizeIsValid():
                # Invalid filter selected.
                print(
                    '{0}: Selected kernel size ({1}x{1}) is not supported.'\
                            .format(
                        self._program_name,
                        self._filter_validator.size
                        ),
                    file=stderr
                    )
                self._exit_app(AppError.invalidkernelsize)

        # Check if selected color channel value is valid..
        if not self._selchnl.isValid():
            # Color channel option value is not valid.
            print(
                '{0}: Supplied color channel value ({1}) is not supported.'\
                        .format(
                    self._program_name,
                    self._scans_path.absolutePath
                    ),
                file=stderr
                )
            self._exit_app(AppError.invalidcolorchannel)

        tifs = self._scans_path.listDataFiles()
        valid_tifs = list()

        # Check if contents of the user supplied directory confrom to the
        # specified conditions.
        namesAddedMB = []
        for iMB, tif in enumerate(tifs):
            print('Loading image for denoising: \'{0}\' ...'.format(Path(tif).name))
            stdout.flush()
            tif_obj = TiffFile(tif)
            self._img_validator.tiff_object = tif_obj

            if not self._img_validator.unitsMatch():
                print(
                    '{0}: Image \'{1}\' does not conform to the required'
                    .format(self._program_name, basename(tif))
                    + ' resolution units: {0}.'
                    .format(self._img_validator.target_units),
                    file=stderr
                    )
                stdout.flush()

                # Image resolution units don't conform to a user set
                # resolution units so go to the next image in the list.
                continue

            if not self._img_validator.resolutionMatch():
                print(
                    '{0}: Image \'{1}\' does not conform to the required'
                    .format(self._program_name, basename(tif))
                    + ' resolution: {0}.'.format(
                        self._img_validator.target_resolution
                        ),
                    file=stderr
                    )
                stdout.flush()

                # Image resolution doesn't conform to a user set resolution
                # units so go to the next image in the list.
                continue

            # Check if reference image size have been set. If not set reference
            # size from the first image on the stack that confroms with target
            # resolution and units.
            height = tif_obj.pages[0].shape[0]
            width = tif_obj.pages[0].shape[1]
            nameAddedMB = Path(tif).name
            namesAddedMB.append(nameAddedMB.replace(".tif", ''))
            if self._img_validator.target_size is None:
                self.newImageValidator(
                    (height, width),
                    self.image_validator[1],
                    self.image_validator[2]
                    )
                self._img_validator.tiff_object = tif_obj

            # if not self._img_validator.sizeMatch():
            #     print(
            #         '{0}: Image \'{1}\' size is not equal to the size of'
            #         .format(self._program_name, basename(tif))
            #         + ' first image in the list (HxW: {0}x{1}).'\
            #         .format(
            #             self._img_validator.target_size[0],
            #             self._img_validator.target_size[1]
            #             ),
            #         file=stderr
            #         )
            #     stdout.flush()

            #     # Image size is not equal to the image size of the first image
            #     # in the list so we skip this image and go to the next image
            #     # in the list.
            #     continue

            # Image conforms to all requirements so add its data to the stack.
            valid_tifs.append(tif_obj)


        if not valid_tifs:
            # Supplied path contains no valid image files.
            print(
                '{0}: Supplied path \'{1}\' contains no valid image files.'\
                        .format(
                    self._program_name,
                    self._scans_path.absolutePath
                    ),
                file=stderr
                )

            self._exit_app(AppError.novalidimages)

        print('Averaging images ...')
        stdout.flush()

        result = None
        if self._selchnl.isNone():
            height, width = self._img_validator.target_size
            result = np.zeros((height, width, 3), dtype=np.float)
        else:
            result = np.zeros(self._img_validator.target_size, dtype=np.float)

        weight = len(valid_tifs)

        # for tif in valid_tifs:
        #     data = tif.asarray().astype(np.float)

        #     if self._selchnl.isNone():
        #         result[:, :, 0] += (data[:, :, 0] / weight)
        #         result[:, :, 1] += (data[:, :, 1] / weight)
        #         result[:, :, 2] += (data[:, :, 2] / weight)

        #     else:
        #         result += (data[:, :, self._selchnl.int] / weight)
        
        results = []
        for tif in valid_tifs:
            data = tif.asarray().astype(np.float)
            # print(data)
            results.append(data)
        
        print('Applying filter ...')
        stdout.flush()
        
        for jMB, result in enumerate(results):
            if self._filter_validator.FilterIsSelected():
                # Denoise image using selected filter.


                if self._filter_validator.isMedian():
                    # Median filter is selected.
                    results[jMB] = ndimage.median_filter(
                        result,
                        self._filter_validator.size
                        )

                else:
                    # Wiener filter is selected. First we have to calculate signal
                    # to noise ratio of the averaged image.
                    snr = None
                    if self._selchnl.isNone():
                        snr = (
                            results[jMB][:, :, 0].mean() / result[:, :, 0].std(),
                            results[jMB][:, :, 1].mean() / result[:, :, 1].std(),
                            results[jMB][:, :, 2].mean() / result[:, :, 2].std(),
                        )
                    else:
                        snr = result.mean() / result.std()

                    kernel = gaussian_kernel(self._filter_validator.size)
                    if self._selchnl.isNone():
                        results[jMB][:, :, 0] = wiener_filter(result[:, :, 0], kernel, snr[0])
                        results[jMB][:, :, 1] = wiener_filter(result[:, :, 1], kernel, snr[1])
                        results[jMB][:, :, 2] = wiener_filter(result[:, :, 2], kernel, snr[2])
                    else:
                        results[jMB] = wiener_filter(img, kernel, snr)

        print('Saving result ...')
        stdout.flush()
    

        for kMB, result in enumerate(results):
            res = self._img_validator.target_resolution
            uni = self._img_validator.target_units
            output_name = namesAddedMB[kMB]

            # if self._filter_validator.FilterIsSelected():
            #     output_name += '_{0}_{1}x{1}'.format(
            #         self._filter_validator.filter,
            #         self._filter_validator.size
            #         )

            output_name += '.tif'

            if self._img_validator.target_units:
                #print(output_name)
                imwrite(
                    output_name,
                    result.astype(np.uint16),
                    resolution=(
                        self._img_validator.target_resolution,
                        self._img_validator.target_resolution
                        ),
                    metadata={'ResolutionUnit':
                              res_unit_value(self._img_validator.target_units)}
                        )

            else:
                #print(output_name)
                imwrite(
                    output_name,
                    result.astype(np.uint16),
                    )

        self._exit_app(0)

    def newFilterValidator(self, filter_name, kernel_size):
        """Put method docstring HERE.
        """

        if filter_name != FilterSelectionValidate.filters[0]:
            self._filter_validator = FilterSelectionValidate(
                filter_name,
                kernel_size
                )

    def newImageValidator(self, size=None, units=None, resolution=None, name = None):
        """Put method docstring HERE.
        """
        
        if size is not None or units is not None:
            self._img_validator = TiffConformityMatch(size, units, resolution, name)
        # if name is not None:
        #     print(name)
