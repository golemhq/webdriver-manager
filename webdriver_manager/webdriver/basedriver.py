import os

import requests

from .. import config, helpers
from ..logger import logger


class Basedriver:
    
    latest_remote_version = None

    def __init__(self, outputdir, os_name, os_bits):
        self.outputdir = outputdir
        self.os_name = os_name
        self.os_bits = os_bits

    def get_driver_full_filename(self, version):
        full_filename = '{}_{}'.format(self.base_filename, version)
        if self.os_name == 'windows':
            full_filename = full_filename + '.exe'
        return full_filename

    def get_latest_local_version(self, strict=True):
        """Get the latest local version in the outputdir.
        If no version is found, returns '0.0'
        """
        latest_version = '0.0'
        webdriver_base_filename = self.base_filename
        # check if it already exists and it's version
        files = os.listdir(self.outputdir) if os.path.isdir(self.outputdir) else []
        webdriver_files = [x for x in files if x.startswith(webdriver_base_filename)]
        if webdriver_files:
            sorted_files = sorted(webdriver_files, reverse=True)
            latest_version_filename = sorted_files[0]
            extracted_version = helpers.extract_version_from_filename(latest_version_filename)
            if extracted_version:
                latest_version = extracted_version
        if strict:
            latest_version = helpers.strict_version(latest_version)
        return latest_version

    def is_remote_higher_than_local(self):
        latest_local = self.get_latest_local_version(strict=True)
        latest_remote = self.get_latest_remote_version(strict=True)
        return latest_remote > latest_local

    def download_driver_executable(self, version):
        webdriver_filename = self.get_driver_full_filename(version)
        webdriver_path = os.path.join(self.outputdir, webdriver_filename)
        if os.path.isfile(webdriver_path):
            logger.warning(('file {} already exists, skipping'
                            .format(webdriver_filename)))
        else:
            os.makedirs(os.path.dirname(webdriver_path), exist_ok=True)
            remote_file_bytes = self.get_remote_file(version)
            with open(webdriver_path, 'wb') as webdriver_file:
                webdriver_file.write(remote_file_bytes)
            logger.info('got {}'.format(webdriver_filename))
    
