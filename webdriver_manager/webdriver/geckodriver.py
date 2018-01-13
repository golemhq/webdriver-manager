import zipfile
import io
import json

import requests

from .. import config
from .basedriver import Basedriver


class Geckodriver(Basedriver):
    
    base_filename = 'geckodriver'

    def _get_geckodriver_download_url(self, version, os_name, os_bits):

        os_suffix = ''
        if os_name == 'windows':
            if os_bits == 32:
                os_suffix = 'win32.zip'
            else:
                os_suffix = 'win64.zip'
        elif os_name == 'mac':
            os_suffix = 'macos.tar.gz'
        elif os_name == 'linux':
            if os_bits == 32:
                os_suffix = 'linux32.tar.gz'
            else:
                os_suffix = 'linux64.tar.gz'
        else:
            raise Exception(('Could not generate filename for '
                             'geckodrive in {}'.format(os_name)))
        filename = 'geckodriver-v{}-{}'.format(version, os_suffix)
        url = '{}/v{}/{}'.format(config.GECKODRIVER_URL_BASE,
                                version, filename)
        return url

    def get_latest_remote_version(self):
        latest_version = None
        try:
            response = requests.get(config.GECKODRIVER_LASTEST_URL)
            latest_version = response.json().get('tag_name')
            latest_version = latest_version.replace('v', '')
        except:
            raise Exception('Could not get latest remote version for geckodriver')
        return latest_version

    def get_remote_file(self, remote_version, os_name, os_bits):
        url = self._get_geckodriver_download_url(remote_version, os_name, os_bits)
        response = requests.get(url, stream=True)
        zipf = zipfile.ZipFile(io.BytesIO(response.content))
        file_list = zipf.namelist()
        expected_file = 'geckodriver'
        if os_name == 'windows':
            expected_file = 'geckodriver.exe'
        geckodriver_file = zipf.read(expected_file)
        return geckodriver_file
