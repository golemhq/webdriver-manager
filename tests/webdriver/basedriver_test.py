import os

from webdriver_manager import helpers
from webdriver_manager.webdriver.basedriver import Basedriver
from webdriver_manager.webdriver.chromedriver import Chromedriver
from webdriver_manager.webdriver.geckodriver import Geckodriver

from tests.fixtures import dir_function
from tests import test_utils


class Test_get_driver_full_filename:

    def test_get_driver_full_filename_chrome(self):
        # outputdir = helpers.normalize_outputdir()
        platform = helpers.get_platform()
        driver = Chromedriver('', 'linux', platform['os_bits'])
        full_name = driver.get_driver_full_filename('2.2')
        assert full_name == 'chromedriver_2.2'

    def test_get_driver_full_filename_chrome_windows(self):
        # outputdir = helpers.normalize_outputdir()
        platform = helpers.get_platform()
        driver = Chromedriver('', 'windows', platform['os_bits'])
        full_name = driver.get_driver_full_filename('2.2')
        assert full_name == 'chromedriver_2.2.exe'

    def test_get_driver_full_filename_firefox(self):
        # outputdir = helpers.normalize_outputdir()
        platform = helpers.get_platform()
        driver = Geckodriver('', 'linux', platform['os_bits'])
        full_name = driver.get_driver_full_filename('2.2')
        assert full_name == 'geckodriver_2.2'

    def test_get_driver_full_filename_firefox_windows(self):
        # outputdir = helpers.normalize_outputdir()
        platform = helpers.get_platform()
        driver = Geckodriver('', 'windows', platform['os_bits'])
        full_name = driver.get_driver_full_filename('2.2')
        assert full_name == 'geckodriver_2.2.exe'


class Test_get_latest_local_version:

    def test_get_latest_local_version_chrome(self, dir_function):
        os.chdir(dir_function['path'])
        outputdir = helpers.normalize_outputdir()
        platform = helpers.get_platform()
        test_utils.create_test_files(outputdir)
        driver = Chromedriver(outputdir, 'linux', platform['os_bits'])
        latest_version = driver.get_latest_local_version()
        assert latest_version == '2.3'

    def test_get_latest_local_version_chrome_windows(self, dir_function):
        os.chdir(dir_function['path'])
        outputdir = helpers.normalize_outputdir()
        platform = helpers.get_platform()
        test_utils.create_test_files_windows(outputdir)
        driver = Chromedriver(outputdir, 'windows', platform['os_bits'])
        latest_version = driver.get_latest_local_version()
        assert latest_version == '2.3'

    def test_get_latest_local_version_firefox(self, dir_function):
        os.chdir(dir_function['path'])
        outputdir = helpers.normalize_outputdir()
        platform = helpers.get_platform()
        test_utils.create_test_files(outputdir)
        driver = Geckodriver(outputdir, 'linux', platform['os_bits'])
        latest_version = driver.get_latest_local_version()
        assert latest_version == '2.6'

    def test_get_latest_local_version_firefox_windows(self, dir_function):
        os.chdir(dir_function['path'])
        outputdir = helpers.normalize_outputdir()
        platform = helpers.get_platform()
        test_utils.create_test_files_windows(outputdir)
        driver = Geckodriver(outputdir, 'windows', platform['os_bits'])
        latest_version = driver.get_latest_local_version()
        assert latest_version == '2.6'

    def test_get_latest_local_no_files_exist(self, dir_function):
        os.chdir(dir_function['path'])
        outputdir = helpers.normalize_outputdir()
        platform = helpers.get_platform()
        driver = Chromedriver(outputdir, 'linux', platform['os_bits'])
        latest_version = driver.get_latest_local_version()
        assert latest_version == '0.0'