import os
import sys

from . import helpers, config, arg_parser, update, clean, versions
from .webdriver import chromedriver


def main():
    args = arg_parser.get_parser().parse_args()
    action = args.action
    helpv = args.help
    if helpv:
        if helpv == 'update' or action == 'update':
            sys.exit(arg_parser.UPDATE_USAGE)
        elif helpv == 'clean' or action == 'clean':
            sys.exit(arg_parser.CLEAN_USAGE)
        elif helpv == 'versions' or action == 'versions':
            sys.exit(arg_parser.VERSIONS_USAGE)
        else:
            sys.exit(arg_parser.USAGE)
    elif action:
        outputdir = helpers.normalize_outputdir(args.outputdir)
        if action == 'update':
            drivers = args.drivers
            if not drivers:
                drivers = config.DEFAULT_DRIVERS
            elif drivers == 'all':
                drivers = config.ALL_DRIVERS
            for driver in drivers:
                # The user can request a specific driver version with:
                # webdriver-manager update -d chrome=3.5
                driver_name, requested_version = helpers.split_driver_name_and_version(driver)
                update(driver_name, outputdir, version=requested_version)
        elif action == 'versions':
            versions(outputdir, drivers=args.drivers)
        elif action == 'clean':
            clean(outputdir, drivers=args.drivers)
        else:
            sys.exit(arg_parser.USAGE)
    else:
        sys.exit(arg_parser.USAGE)


if __name__ == '__main__':
    main()