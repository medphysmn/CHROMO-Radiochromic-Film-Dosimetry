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
# * denoise.py: created.
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

import argparse
import actions


# =============================================================================
# Global constants
# =============================================================================


# =============================================================================
# Utility classes and functions
# =============================================================================

def _format_epilog(epilog_addition, bug_mail):
    """Formatter for generating help epilogue text. Help epilogue text is an
    additional description of the program that is displayed after the
    description of the arguments. Usually it consists only of line informing
    to which email address to report bugs to, or it can be completely
    omitted.

    Depending on provided parameters function will properly format epilogue
    text and return string containing formatted text. If none of the
    parameters are supplied the function will return None which is default
    value for epilog parameter when constructing parser object.
    """

    fmt_mail = None
    fmt_eplg = None

    if epilog_addition is None and bug_mail is None:
        return None

    if bug_mail is not None:
        fmt_mail = 'Report bugs to <{0}>.'.format(bug_mail)
    else:
        fmt_mail = None

    if epilog_addition is None:
        fmt_eplg = fmt_mail

    elif fmt_mail is None:
        fmt_eplg = epilog_addition

    else:
        fmt_eplg = '{0}\n\n{1}'.format(epilog_addition, fmt_mail)

    return fmt_eplg


def _formulate_action(action, **kwargs):
    """Factory method to create and return proper action object.
    """

    return action(**kwargs)


# =============================================================================
# Command line app class
# =============================================================================

class CommandLineApp():
    """Actual command line app object containing all relevant application
    information (NAME, VERSION, DESCRIPTION, ...) and which instantiates
    action that will be executed depending on the user input from
    command line.
    """

    def __init__(
            self,
            program_name=None,
            program_description=None,
            program_license=None,
            version_string=None,
            year_string=None,
            author_name=None,
            author_mail=None,
            epilog=None
            ):

        self.program_license = program_license
        self.version_string = version_string
        self.year_string = year_string
        self.author_name = author_name
        self.author_mail = author_mail

        fmt_eplg = _format_epilog(epilog, author_mail)

        self._parser = argparse.ArgumentParser(
            prog=program_name,
            description=program_description,
            epilog=fmt_eplg,
            formatter_class=argparse.RawDescriptionHelpFormatter
            )

        # Since we add argument options to groups by calling group
        # method add_argument, we have to sore all that group objects
        # somewhere before adding arguments. Since we want to store all
        # application relevant data in our application object we use
        # this list for that purpose.
        self._arg_groups = []

        self._action = None

    @property
    def program_name(self):
        """Utility function that makes accessing program name attribute
        neat and hides implementation details.
        """
        return self._parser.prog

    @property
    def program_description(self):
        """Utility function that makes accessing program description
        attribute neat and hides implementation details.
        """
        return self._parser.description

    def add_argument_group(self, title=None, description=None):
        """Adds an argument group to application object.
        At least group title must be provided or method will rise
        NameError exception. This is to prevent creation of titleless
        and descriptionless argument groups. Although this is allowed bu
        argparse module I don't see any use of a such utility."""

        if title is None:
            raise NameError('Missing arguments group title.')

        group = self._parser.add_argument_group(title, description)
        self._arg_groups.append(group)

        return group

    def _group_by_title(self, title):
        group = None

        for item in self._arg_groups:
            if title == item.title:
                group = item
                break

        return group

    def add_argument(self, *args, **kwargs):
        """Wrapper for add_argument methods of argparse module. If
        parameter group is supplied with valid group name, argument will
        be added to that group. If group parameter is omitted argument
        will be added to parser object. In a case of invalid group name
        it rises ValueError exception.
        """

        if 'group' not in kwargs or kwargs['group'] is None:
            self._parser.add_argument(*args, **kwargs)

        else:
            group = self._group_by_title(kwargs['group'])

            if group is None:
                raise ValueError(
                    'Trying to reference nonexisten argument group.'
                    )

            kwargsr = {k: kwargs[k] for k in kwargs if k != 'group'}
            group.add_argument(*args, **kwargsr)

    def parse_args(self, args=None, namespace=None):
        """Wrapper for parse_args method of a parser object. It also
        instantiates action object that will be executed based on a
        input from command line.
        """

        arguments = self._parser.parse_args(args, namespace)

        if arguments.usage:
            self._action = _formulate_action(
                actions.ProgramUsageAction,
                parser=self._parser,
                exitf=self._parser.exit
                )

        elif arguments.version:
            self._action = _formulate_action(
                actions.ShowVersionAction,
                prog=self._parser.prog,
                ver=self.version_string,
                year=self.year_string,
                author=self.author_name,
                license=self.program_license,
                exitf=self._parser.exit
                )

        else:
            self._action = _formulate_action(
                actions.DefaultAction,
                prog=self._parser.prog,
                exitf=self._parser.exit,
                )

            self._action.scans_path = arguments.scans_dir
            self._action.color_channel = arguments.color_channel
            self._action.newImageValidator(
                None,
                arguments.resolution_units,
                arguments.resolution
                )
            self._action.newFilterValidator(
                arguments.filter,
                arguments.kernel_size
                )

    def run(self):
        """This method executes action code.
        """

        self._action.execute()


# =============================================================================
# Script main body
# =============================================================================

if __name__ == '__main__':
    PROGRAM_DESCRIPTION = '\
CLI application development for Python implementing argp option parsing \
engine.\n\
Mandatory arguments to long options are mandatory for short options too.'
    PROGRAM_LICENSE = '\
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>\
\n\
This is free software: you are free to change and redistribute it.\n\
There is NO WARRANTY, to the extent permitted by law.'

    program = CommandLineApp(
        program_description=PROGRAM_DESCRIPTION.replace('\t', ''),
        program_license=PROGRAM_LICENSE.replace('\t', ''),
        version_string='0.1',
        year_string='2020',
        author_name='Ljubomir Kurij',
        author_mail='ljubomir_kurij@protonmail.com',
        epilog=None
        )

    program.add_argument_group('general options')
    program.add_argument(
        '-V', '--version',
        action='store_true',
        help='print program version',
        group='general options'
        )
    program.add_argument(
        '--usage',
        action='store_true',
        help='give a short usage message'
        )
    program.add_argument(
            '-d', '--scans-dir',
            metavar='DIR_PATH',
            type=str,
            nargs='?',
            default='.',
            help='directory holding scans to be averaged and denoised. \
Current directory is searched by default.')
    program.add_argument(
            '-u', '--resolution-units',
            metavar='UNIT_STRING',
            type=str,
            nargs='?',
            help='a convinience option for passing scans resolution units. \
Option accepts two values: dpi (dots per inch) and dpm (dots per milimeter). \
If this option is not supplied processing is carried out without taking \
resolution into account. Default value is \'dpi\'')
    program.add_argument(
            '-r', '--resolution',
            metavar='RESOLUTION',
            type=int,
            nargs='?',
            default=400,
            help='a convinience option for passing reference scans resolution. \
If resolution units are not supplied this option is ignored. Default value is \
400.')
    program.add_argument(
            '-f', '--filter',
            metavar='FILTER',
            type=str,
            nargs='?',
            default='no',
            help='a convinience option for selecting denoising filter. \
It can be one of the three values: no (do not apply filter), median (apply \
median filter, wiener (apply zero phase wiener filter). If one of the filters \
is selected, one must specify size of the deconvolution kernel using option \
-k / --kernel-size.')
    program.add_argument(
            '-k', '--kernel-size',
            metavar='KERNEL_SIZE',
            type=int,
            nargs='?',
            default=3,
            help='a convinience option for passing size of the deconvolution \
kernel for the image smoothing algorithms. Argument accepts odd numbers > 3. \
If no denoising filter is selected this option is ignored. Default value \
is 3.')
    program.add_argument(
            '-c', '--color-channel',
            metavar='COLOR',
            type=str,
            nargs='?',
            help='a convinience option for selecting image color channel to \
process. Supported values are \'red\', \'green\' and \'blue\'.')

    program.parse_args()
    program.run()
