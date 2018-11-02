import requests

from .. import config, helpers
from .basedriver import Basedriver


class Chromedriver(Basedriver):
    
    base_filename = 'chromedriver'

    def _get_chromedriver_download_url(self, version):
        os_suffix = ''
        if self.os_name == 'windows':
            os_suffix = 'win32'
        elif self.os_name == 'mac':
            os_suffix = 'mac64'
        elif self.os_name == 'linux':
            os_suffix = 'linux64'
        else:
            raise Exception(('Could not generate filename for '
                             'chromedriver in {}'.format(self.os_name)))
        filename = 'chromedriver_{}.zip'.format(os_suffix)
        url = '{}/{}/{}'.format(config.CHROMEDRIVER_STORAGE_URL,
                                version, filename)
        return url

    def get_latest_remote_version(self, strict=False):
        if self.latest_remote_version:
            latest_version = self.latest_remote_version
        else:
            try:
                response = requests.get(config.CHROMEDRIVER_LATEST_FILE)
                latest_version = response.text.strip()
                self.latest_remote_version = latest_version
            except:
                raise Exception('Could not get latest remote version for chromedriver')
        if strict:
            latest_version = helpers.strict_version(latest_version)
        return latest_version

    def get_remote_file(self, remote_version):
        url = self._get_chromedriver_download_url(remote_version)
        bytes_io = helpers.download_file_with_progress_bar(url)
        expected_file = 'chromedriver.exe' if self.os_name == 'windows' else 'chromedriver'
        return helpers.extract_file_from_zip(bytes_io, expected_file)
