import os

import requests

from . import helpers, config, arg_parser, update, clean, versions
from .webdriver import chromedriver


def main():

    args = arg_parser.get_parser().parse_args()
    if 'action' in args:
        outputdir = helpers.normalize_outputdir(args.outputdir)

        if args.action == 'update':
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
        
        if args.action == 'versions':
            versions(outputdir, drivers=args.drivers)

        if args.action == 'clean':
            clean(outputdir, drivers=args.drivers)
    else:
        print(arg_parser.USAGE_MSG)


if __name__ == '__main__':
    main()