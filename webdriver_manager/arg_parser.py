import argparse


USAGE_MSG = """
Usage:
  webdriver-manager update [-d|--drivers -o|--outputdir]
  webdriver-manager versions [-d|--drivers -o|--outputdir]
  webdriver-manager clean [-d|--drivers -o|--outputdir]
  webdriver-manager -h | --help
"""

HELP_MSG = """
webdriver-manager update

  Downloads a remote webdriver executable if it's version is greater than the 
  local version.
  Without any extra arguments this will download the default drivers into the current
  directory or into the ./drivers directory if this already exists.

  update optional arguments:
  -d | --drivers :   define a list of drivers to download
  -o | --outputdir : define the output directory

webdriver-manager versions

  List the versions of all the local webdriver executables. 

  versions optional arguments
  -d | --drivers :   select which drivers to list
  -o | --outputdir : define the directory to look for webdriver executables
"""


def get_parser():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(dest='action')

    parser_update = subparsers.add_parser('update')
    parser_update.add_argument('-d', '--drivers', action='store',
                               nargs='*', type=str,
                               default=[],
                               help='list of drivers to download. By default, download all')
    parser_update.add_argument('-o', '--outputdir', nargs='?', type=str,
                               metavar='', default=None, help='directory to use. By default use current or /drivers if it exists')

    parser_clean = subparsers.add_parser('clean')
    parser_clean.add_argument('-d', '--drivers', action='store',
                               nargs='*', type=str,
                               default=[],
                               help='')
    parser_clean.add_argument('-o', '--outputdir', nargs='?', type=str,
                              default=None)

    parser_clean = subparsers.add_parser('versions')
    parser_clean.add_argument('-d', '--drivers', action='store',
                               nargs='*', type=str,
                               default=[])
    parser_clean.add_argument('-o', '--outputdir', nargs='?', type=str,
                               default=None)

    return parser
