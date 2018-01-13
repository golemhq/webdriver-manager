import sys
import os
import platform
from distutils.version import StrictVersion

from .logger import logger
from .webdriver import chromedriver, geckodriver


EXPECTED_MAXSIZE_32 = 2**31 - 1
EXPECTED_MAXSIZE_64 = 2**63 - 1


def normalize_outputdir(outputdir_raw=None):
    """ if output dir is None try using the ./drivers directory
    if it already exists, otherwise use the current working directory
    """
    outputdir = ''
    cwd = os.getcwd()
    if not outputdir_raw:
        outputdir_drivers = os.path.join(cwd, 'drivers')
        if os.path.isdir(outputdir_drivers):
            outputdir = outputdir_drivers
        else:
            outputdir = cwd
    else:
        outputdir = os.path.join(cwd, outputdir_raw)
    return outputdir


def get_platform():

    platform_data = {
        'os_name': None,
        'os_bits': None
    }
    os_name = platform.system()
    normalize_os = {
        'Windows': 'windows',
        'Linux': 'linux',
        'Darwin': 'mac'
    }
    if os_name in normalize_os.keys():
        platform_data['os_name'] = normalize_os[os_name]
    else:
        raise Exception('Could not normalize os name {}'.format(os_name))
    # try to get the os bits
    maxsize = sys.maxsize
    if maxsize == EXPECTED_MAXSIZE_32:
        platform_data['os_bits'] = '32'
    elif maxsize == EXPECTED_MAXSIZE_64:
        platform_data['os_bits'] = '64'
    else:
        platform_data['os_bits'] = '64'
        logger.warning('could not determine os bits, setting default to 64')
    return platform_data


def get_driver(driver_name):
    driver = None
    if driver_name == 'chrome':
        driver = chromedriver.Chromedriver()
    elif driver_name == 'firefox':
        driver = geckodriver.Geckodriver()
    else:
        raise Exception('The {} driver is not implemented'.format(driver_name))
    return driver


def remote_higher_than_local(remote_version, local_version):
    remote_strict = StrictVersion(remote_version)
    if local_version:
        local_strict = StrictVersion(local_version)
    else:
        local_strict = StrictVersion('0.0')
    return remote_strict > local_strict