import os

import requests

from . import helpers, arg_parser, config, logger
from .webdriver import chromedriver


"""
Usage:
webdriver-manager update -d all -o /drivers -k
webdriver-manager update -drivers chrome firefox -outputdir /drivers -keep-older

webdriver-manager versions [-l | --latest]

webdriver-manager version chrome [-l | --latest]


"""


def update(drivers, outputdir=None):

    # if output dir is None try using the ./drivers
    # directory if it already exists, otherwise
    # use the current working directory
    cwd = os.getcwd()
    if not outputdir:
        tmp_drivers_dir = os.path.join(cwd, 'drivers')
        if os.path.isdir(tmp_drivers_dir):
            outputdir = tmp_drivers_dir
        else:
            outputdir = cwd

    if not drivers:
        # DEFAULT_DRIVERS are used when no specific
        # drivers were defined, i.e.: just chrome and firefox
        drivers = config.DEFAULT_DRIVERS
    # if drivers = all, assign all drivers
    elif drivers == 'all':
        drivers = config.ALL_DRIVERS

    # get the platform
    platform = helpers.get_platform()

    # for each driver
    for driver_name in drivers:
        driver = helpers.get_driver(driver_name)

        latest_local_version = driver.get_latest_local_version(driver_name, outputdir)
        latest_remote_version = driver.get_latest_remote_version()
        remote_higher_than_local = helpers.remote_higher_than_local(
                                                latest_remote_version,
                                                latest_local_version)
        if remote_higher_than_local:
            # must update local version
            logger.logger.info('Updating {}'.format(driver_name))
            driver.update_driver(driver_name, latest_remote_version, platform)
        else:
            logger.logger.info('{} up to date'.format(driver_name))


def version(driver, outputdir):

    webdriver_filename = _get_webdriver_base_filename(driver)

    # get files from outputdir

    files = []

    # get files that starts with webdriver_filename

    webdriver_files = [x for x in files if x.startswith(webdriver_filename)]





def main():

    args = arg_parser.get_parser().parse_args()
    
    if 'action' in args:
        if args.action == 'update':
            outputdir = args.outputdir
            drivers = args.drivers
            update(drivers, outputdir)
        if args.action == 'versions':
            pass
    else:
        pass

if __name__ == '__main__':
    main()