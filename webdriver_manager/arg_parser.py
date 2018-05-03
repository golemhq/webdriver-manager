import argparse


USAGE = """
Usage webdriver-manager:

  webdriver-manager update [-d|--drivers] [-o|--outputdir]
  webdriver-manager versions [-d|--drivers] [-o|--outputdir]
  webdriver-manager clean [-d|--drivers] [-o|--outputdir]
  webdriver-manager [-h|--help <command>]
"""

UPDATE_USAGE = """
Usage: webdriver-manager update [-d|--drivers] [-o|--outputdir]

  Downloads a remote webdriver executable if it's version is
  greater than the local version.
  Without any extra arguments this will download the
  default drivers into the current directory or into the ./drivers
  directory if this already exists.

  update optional arguments:
  -d | --drivers     define a list of drivers to download.
                     Specify a version with `-d chrome=2.2`
  -o | --outputdir   define the output directory. Default is current
                     directory or ./drivers if it exists.
"""

VERSIONS_USAGE = """
Usage: webdriver-manager versions [-d|--drivers] [-o|--outputdir]

  List the versions of all the local webdriver executables. 

  versions optional arguments
  -d | --drivers     select which drivers to list
  -o | --outputdir   define the directory to look for webdriver executables.
                     Default is current directory or ./drivers if it exists.
"""

CLEAN_USAGE = """
Usage: webdriver-manager clean [-d|--drivers] [-o|--outputdir]
  
  Clean all the webdriver executables in the outputdir

  clean optional arguments
  -d | --drivers     select which drivers to clean. Specify a version with 
                     `-d chrome=2.2`
  -o | --outputdir   define the directory to look for webdriver executables.
                     Default is current directory or ./drivers if it exists.
"""


def get_parser():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-h', '--help', nargs='?', const=True, default=False)
    subparsers = parser.add_subparsers(dest='action')
    # update
    parser_update = subparsers.add_parser('update', add_help=False)
    parser_update.add_argument('-d', '--drivers', action='store', nargs='*',
                               default=[], type=str,)
    parser_update.add_argument('-o', '--outputdir', nargs='?', default=None, type=str)
    parser_update.add_argument('-h', '--help', action='store_true')
    # clean
    parser_clean = subparsers.add_parser('clean', add_help=False)
    parser_clean.add_argument('-d', '--drivers', action='store', nargs='*',
                              default=[], type=str)
    parser_clean.add_argument('-o', '--outputdir', nargs='?', default=None, type=str)
    parser_clean.add_argument('-h', '--help', action='store_true')
    # versions
    parser_versions = subparsers.add_parser('versions', add_help=False)
    parser_versions.add_argument('-d', '--drivers', action='store', nargs='*',
                              type=str, default=[])
    parser_versions.add_argument('-o', '--outputdir', nargs='?', default=None, type=str)
    parser_versions.add_argument('-h', '--help', action='store_true')

    return parser
