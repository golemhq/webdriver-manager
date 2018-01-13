import zipfile
import io

import requests

from .. import config
from .basedriver import Basedriver


class Chromedriver(Basedriver):
    
    base_filename = 'chromedriver'

    def _get_chromedriver_download_url(self, version, os_name):
        os_suffix = ''
        if os_name == 'windows':
            os_suffix = 'win32'
        elif os_name == 'mac':
            os_suffix = 'mac64'
        elif os_name == 'linux':
            os_suffix = 'linux64'
        else:
            raise Exception(('Could not generate filename for '
                             'geckodrive in {}'.format(os_name)))
        filename = 'chromedriver_{}.zip'.format(os_suffix)
        url = '{}/{}/{}'.format(config.CHROMEDRIVER_STORAGE_URL,
                                version, filename)
        return url

    def get_latest_remote_version(self):
        latest_version = None
        try:
            response = requests.get(config.CHROMEDRIVER_LATEST_FILE)
            latest_version = response.text.strip()
        except:
            raise Exception('Could not get latest remote version for chromedriver')
        return latest_version

    def get_remote_file(self, remote_version, os_name, os_bits=None):
        url = self._get_chromedriver_download_url(remote_version, os_name)
        response = requests.get(url, stream=True)
        zipf = zipfile.ZipFile(io.BytesIO(response.content))
        file_list = zipf.namelist()
        expected_file = 'chromedriver'
        if os_name == 'windows':
            expected_file = 'chromedriver.exe'
        chromedriver_file = zipf.read(expected_file)
        return chromedriver_file
