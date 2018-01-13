import os

import requests

from .. import config
from ..logger import logger


class Basedriver:
    
    def get_webdriver_full_filename(self, version, os_name):
        exe_suffix = '.exe' if os_name == 'windows' else ''
        base_filename = self.base_filename
        filename = '{}_{}{}'.format(base_filename, version, exe_suffix)
        return filename

    def get_latest_local_version(self, driver_name, outputdir):
        latest_version = None
        webdriver_base_filename = self.base_filename
        # check if it already exists and it's version
        path = os.path.join(outputdir, webdriver_base_filename)
        files = os.listdir(outputdir)
        # get the files that starts with webdriver_base_filename
        webdriver_files = [x for x in files if x.startswith(webdriver_base_filename)]
        if webdriver_files:
            sorted_files = sorted(webdriver_files, reverse=True)
            latest_version_filename = sorted_files[0].replace('.exe', '')
            latest_version = latest_version_filename.split('_')[1]
        return latest_version

    def download_driver_executable(self, version, platform):
        webdriver_filename = self.get_driver_full_filename(version,
                                                           platform['os_name'])
        if os.path.isfile(webdriver_filename):
            logger.warning(('file {} already exists, skipping'
                            .format(webdriver_filename)))
        else:
            remote_file_bytes = self.get_remote_file(version,
                                                     platform['os_name'],
                                                     platform['os_bits'])
            with open(webdriver_filename, 'wb') as webdriver_file:
                webdriver_file.write(remote_file_bytes)
            logger.info('got {}'.format(webdriver_filename))
    
