import argparse


def get_parser():
    parser = argparse.ArgumentParser(description='Process some integers.')


    subparsers = parser.add_subparsers(help='sub-command help')

    parser_update = subparsers.add_parser('update', help='update help')
    
    parser_update.set_defaults(action='update')
    # optional, default is 'all', can select from list
    # list = ['all', 'chrome', 'firefox', 'ie', 'edge', 'phantomjs', 'opera', 'safari']
    parser_update.add_argument('-d', '--drivers', action='store',
                               nargs='*', type=str, metavar='drivers',
                               default=[],
                               help='list of drivers to download. By default, download all')
    parser_update.add_argument('-o', '--outputdir', nargs='?', type=str,
                               default=None, help='bar help')
    parser_update.add_argument('-k', '--keep-older', action='store_true', default=False,
                               help="Interactive mode")


    return parser
