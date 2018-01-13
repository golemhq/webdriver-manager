import os

import requests

from .. import config, logger


class Basedriver:
    
    def get_webdriver_full_filename(self, version, os_name):
        exe_suffix = '.exe' if os_name == 'windows' else ''
        base_filename = self.base_filename
        filename = '{}_{}{}'.format(base_filename, version, exe_suffix)
        return filename


    def get_latest_local_version(self, driver_name, outputdir):
        latest_version = None

        webdriver_base_filename = self.base_filename

        # check if it already exists and the version
        path = os.path.join(outputdir, webdriver_base_filename)
        files = os.listdir(outputdir)

        # get files that starts with webdriver_filename

        webdriver_files = [x for x in files if x.startswith(webdriver_base_filename)]
        if webdriver_files:
            sorted_files = sorted(webdriver_files, reverse=True)
            latest_version_filename = sorted_files[0].replace('.exe', '')
            latest_version = latest_version_filename.split('_')[1]
        return latest_version


    def update_driver(self, driver_name, remote_version, platform):
        remote_file_bytes = self.get_remote_file(remote_version, platform['os_name'],
                                                 platform['os_bits'])
        webdriver_filename = self.get_webdriver_full_filename(remote_version,
                                                              platform['os_name'])
        with open(webdriver_filename, 'wb') as webdriver_file:
            webdriver_file.write(remote_file_bytes)
        logger.logger.info('got {}'.format(webdriver_filename))
    
