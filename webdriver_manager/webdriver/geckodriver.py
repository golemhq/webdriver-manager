import requests

from .. import config, helpers
from .basedriver import Basedriver


class Geckodriver(Basedriver):
    
    base_filename = 'geckodriver'

    def _get_geckodriver_download_url(self, version):
        os_suffix = ''
        if self.os_name == 'windows':
            if self.os_bits == 32:
                os_suffix = 'win32.zip'
            else:
                os_suffix = 'win64.zip'
        elif self.os_name == 'mac':
            os_suffix = 'macos.tar.gz'
        elif self.os_name == 'linux':
            if self.os_bits == 32:
                os_suffix = 'linux32.tar.gz'
            else:
                os_suffix = 'linux64.tar.gz'
        else:
            raise Exception(('Could not generate filename for '
                             'geckodriver in {}'.format(self.os_name)))
        filename = 'geckodriver-v{}-{}'.format(version, os_suffix)
        url = '{}/v{}/{}'.format(config.GECKODRIVER_URL_BASE,
                                version, filename)
        return url

    def get_latest_remote_version(self, strict=False):
        if self.latest_remote_version:
            latest_version = self.latest_remote_version
        else:
            try:
                response = requests.get(config.GECKODRIVER_LASTEST_URL)
                latest_version = response.json().get('tag_name')
                latest_version = latest_version.replace('v', '')
                self.latest_remote_version = latest_version
            except:
                raise Exception('Could not get latest remote version for geckodriver')
        if strict:
            latest_version = helpers.strict_version(latest_version)
        return latest_version

    def get_remote_file(self, remote_version):
        url = self._get_geckodriver_download_url(remote_version)
        bytes_io = helpers.download_file_with_progress_bar(url)
        expected_file = 'geckodriver.exe'if self.os_name == 'windows' else 'geckodriver'
        if url.endswith('tar.gz'):
            return helpers.extract_file_from_tar(bytes_io, expected_file)
        else:
            return helpers.extract_file_from_zip(bytes_io, expected_file)
