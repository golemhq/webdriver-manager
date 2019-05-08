import os

from .. import helpers
from ..logger import logger


class Basedriver:
    """Base driver class. Contains common methods.
    It should be used through it's subclasses
    """
    latest_remote_version = None

    def __init__(self, outputdir, os_name, os_bits):
        """Instantiate a new webdriver class
        Args:
          outputdir:    The path to the directory to use.
          os_name:      Valid options: ['windows', 'linux', 'mac']
          os_bits:      Valid options: ['32', '64']
        """
        if type(self) == Basedriver:
            raise Exception('Basedriver cannot be instantiated')
        self.outputdir = outputdir
        self.os_name = os_name
        self.os_bits = os_bits

    def get_driver_full_filename(self, version):
        full_filename = '{}_{}'.format(self.base_filename, version)
        if self.os_name == 'windows':
            full_filename = full_filename + '.exe'
        return full_filename

    def get_latest_local_version(self, strict=False, loose=False):
        """Get the latest local version in the outputdir.
        If no version is found, returns '0.0'
        """
        latest_version = '0.0'
        # check if it already exists and its version
        files = os.listdir(self.outputdir) if os.path.isdir(self.outputdir) else []
        webdriver_files = [x for x in files if x.startswith(self.base_filename)]
        if webdriver_files:
            sorted_files = sorted(webdriver_files, reverse=True)
            latest_version_filename = sorted_files[0]
            extracted_version = helpers.extract_version_from_filename(latest_version_filename)
            if extracted_version:
                latest_version = extracted_version
        if strict:
            latest_version = helpers.strict_version(latest_version)
        elif loose:
            latest_version = helpers.loose_version(latest_version)
        return latest_version

    def is_remote_higher_than_local(self):
        latest_local = self.get_latest_local_version(loose=True)
        latest_remote = self.get_latest_remote_version(loose=True)
        return latest_remote > latest_local

    def download_driver_executable(self, version):
        webdriver_filename = self.get_driver_full_filename(version)
        webdriver_path = os.path.join(self.outputdir, webdriver_filename)
        if os.path.isfile(webdriver_path):
            logger.warning(('file {} already exists, skipping'
                            .format(webdriver_filename)))
        else:
            logger.info('updating {}'.format(self.base_filename))
            os.makedirs(os.path.dirname(webdriver_path), exist_ok=True)
            remote_file_bytes = self.get_remote_file(version)
            with open(webdriver_path, 'wb') as webdriver_file:
                webdriver_file.write(remote_file_bytes)
                try:
                    os.chmod(webdriver_path, 0o777)
                except:
                    pass
            logger.info('got {}'.format(webdriver_filename))
    
