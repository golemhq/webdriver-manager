import sys
import os
import platform
from distutils.version import StrictVersion
import io

import requests
from tqdm import tqdm

from .logger import logger
from .webdriver import chromedriver, geckodriver


EXPECTED_MAXSIZE_32 = 2**31 - 1
EXPECTED_MAXSIZE_64 = 2**63 - 1


def normalize_outputdir(outputdir=None):
    """ if output dir is None try using the ./drivers directory
    if it already exists, otherwise use the current working directory
    """
    normalized = ''
    cwd = os.getcwd()
    if not outputdir:
        outputdir_drivers = os.path.join(cwd, 'drivers')
        if os.path.isdir(outputdir_drivers):
            normalized = outputdir_drivers
        else:
            normalized = cwd
    else:
        normalized = os.path.join(cwd, os.path.normpath(outputdir))
    return normalized


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


def get_driver_class(driver_name):
    driver_class = None
    if driver_name == 'chrome':
        driver_class = chromedriver.Chromedriver
    elif driver_name == 'firefox':
        driver_class = geckodriver.Geckodriver
    else:
        raise Exception('driver {} is not implemented'.format(driver_name))
    return driver_class


def strict_version(version):
    return StrictVersion(version)


def split_driver_name_and_version(driver_name):
    split = driver_name.split('=')
    if len(split) == 1:
        return driver_name, None
    elif len(split) == 2:
        return split[0], split[1]
    else:
        raise Exception('{} is an invalid driver value'.format(driver_name))


def download_file_with_progress_bar(url):
    """Downloads a file from the given url, displays 
    a progress bar.
    Returns a io.BytesIO object
    """
    request = requests.get(url, stream=True)
    if request.status_code == 404:
        msg = ('there was a 404 error trying to reach {} \nThis probably '
               'means the requested version does not exist.'.format(url))
        # raise Exception(msg)
        logger.error(msg)
        import sys
        sys.exit()
    total_size = int(request.headers["Content-Length"])
    chunk_size = 1024
    bars = int(total_size / chunk_size)
    bytes_io = io.BytesIO()
    pbar = tqdm(request.iter_content(chunk_size=chunk_size), total=bars,
                unit="kb", leave=False)
    for chunk in pbar:
        bytes_io.write(chunk)
    return bytes_io


def driver_to_executable_filename(browser):
    driver_name = ''
    if browser == 'chrome':
        driver_name = 'chromedriver'
    elif browser == 'firefox':
        driver_name = 'geckodriver'
    else:
        raise Exception('driver {} is not implemented'.format(browser))
    return driver_name


def extract_version_from_filename(filename):
    components = filename.replace('.exe', '').split('_')
    if len(components) == 2:
        return components[1]
    else:
        return None