import argparse


USAGE_MSG = """
Usage:
  webdriver-manager update
  webdriver-manager update [-d|--drivers -o|--outputdir -v|--version]
  webdriver-manager versions [-d | --drivers]
  webdriver-manager versions [-l | --latest]
  webdriver-manager versions [-o | --outputdir]
  webdriver-manager version <driver-name> [-l | --latest]
  webdriver-manager -h | --help

Options:
  -d --drivers  
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
  -v | --version :   specify a version to download

webdriver-manager versions

  List the versions of all the local webdriver executables. 

  versions optional arguments
  -d | --drivers :   select which drivers to list
  -o | --outputdir : define the directory to look for webdriver executables
  -l | --latest : list only the latest versions  
"""


def get_parser():
    parser = argparse.ArgumentParser(description='Process some integers.')


    subparsers = parser.add_subparsers(help='sub-command help')

    parser_update = subparsers.add_parser('update', help='update help')
    
    parser_update.add_argument('-d', '--drivers', action='store',
                               nargs='*', type=str, metavar='',
                               default=[],
                               help='list of drivers to download. By default, download all')
    parser_update.add_argument('-o', '--outputdir', nargs='?', type=str,
                               metavar='', default=None, help='directory to use. By default use current or /drivers if it exists')


    return parser
