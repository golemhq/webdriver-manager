import os

import pytest

from webdriver_manager import arg_parser, helpers
from webdriver_manager.webdriver.chromedriver import Chromedriver
from webdriver_manager.webdriver.geckodriver import Geckodriver

from fixtures import dir_session, dir_function
from test_utils import run_command


class Test_webdriver_manager:

    def test_wm_without_args(self):
        result = run_command('webdriver-manager')
        assert result == arg_parser.USAGE


class Test_help:

    commands = [
        ('webdriver-manager -h', arg_parser.USAGE),
        ('webdriver-manager --help', arg_parser.USAGE),
        ('webdriver-manager -h update', arg_parser.UPDATE_USAGE),
        ('webdriver-manager -h clean', arg_parser.CLEAN_USAGE),
        ('webdriver-manager -h versions', arg_parser.VERSIONS_USAGE),
        ('webdriver-manager update -h', arg_parser.UPDATE_USAGE),
        ('webdriver-manager clean -h', arg_parser.CLEAN_USAGE),
        ('webdriver-manager versions -h', arg_parser.VERSIONS_USAGE)
    ]

    @pytest.mark.parametrize('command, expected', commands)
    def test_help(self, command, expected, dir_session):
        os.chdir(dir_session['path'])
        result = run_command(command)
        assert result == expected


class Test_udpate:

    @pytest.mark.slow
    def test_update_no_args(self, dir_function):
        """Latest version of config.DEFAULT_DRIVERS are downloaded
        to current dir
        """
        tempdir = dir_function['path']
        os.chdir(tempdir)
        result = run_command('webdriver-manager update')
        platform = helpers.get_platform()
        chromedriver = Chromedriver(tempdir, platform['os_name'], platform['os_bits'])
        latest_version_chrome = chromedriver.get_latest_remote_version()
        geckodriver = Geckodriver(tempdir, platform['os_name'], platform['os_bits'])
        latest_version_gecko = geckodriver.get_latest_remote_version()
        files = os.listdir()
        expected_file_chrome = 'chromedriver_{}'.format(latest_version_chrome)
        if platform['os_name'] == 'windows':
            expected_file_chrome += '.exe'
        expected_file_gecko = 'geckodriver_{}'.format(latest_version_gecko)
        if platform['os_name'] == 'windows':
            expected_file_gecko += '.exe'
        assert len(files) == 2
        assert expected_file_chrome in files
        assert expected_file_gecko in files
        assert 'INFO updating chromedriver' in result
        assert 'INFO got {}'.format(expected_file_chrome) in result
        assert 'INFO updating geckodriver' in result
        assert 'INFO got {}'.format(expected_file_gecko) in result

    @pytest.mark.slow
    def test_update_drivers_dir_exists(self, dir_function):
        """Verify when ./drivers exists it is used as output dir"""
        tempdir = dir_function['path']
        os.chdir(tempdir)
        os.mkdir('./drivers')
        result = run_command('webdriver-manager update -d chrome')
        platform = helpers.get_platform()
        chromedriver = Chromedriver(tempdir, platform['os_name'], platform['os_bits'])
        latest_version_chrome = chromedriver.get_latest_remote_version()
        files = os.listdir('./drivers')
        expected_file_chrome = 'chromedriver_{}'.format(latest_version_chrome)
        if platform['os_name'] == 'windows':
            expected_file_chrome += '.exe'
        assert files == [expected_file_chrome]

    @pytest.mark.slow
    def test_update_drivers_dir_exists(self, dir_function):
        """Verify when ./drivers exists it is used as output dir"""
        tempdir = dir_function['path']
        os.chdir(tempdir)
        os.mkdir('./drivers')
        result = run_command('webdriver-manager update -d chrome')
        platform = helpers.get_platform()
        chromedriver = Chromedriver(tempdir, platform['os_name'], platform['os_bits'])
        latest_version_chrome = chromedriver.get_latest_remote_version()
        files = os.listdir('./drivers')
        expected_file_chrome = 'chromedriver_{}'.format(latest_version_chrome)
        if platform['os_name'] == 'windows':
            expected_file_chrome += '.exe'
        assert files == [expected_file_chrome]

    @pytest.mark.slow
    def test_update_outputdir_does_not_exist(self, dir_function):
        """Verify outputdir is created if it does not exist"""
        tempdir = dir_function['path']
        os.chdir(tempdir)
        result = run_command('webdriver-manager update -d chrome -o my_outputdir')
        assert os.path.isdir(os.path.join(tempdir, 'my_outputdir'))
        files = os.listdir('./my_outputdir')
        assert len(files) == 1

    @pytest.mark.slow
    def test_update_local_version_higher_than_remote(self, dir_function):
        tempdir = dir_function['path']
        os.chdir(tempdir)
        filename = 'chromedriver_99.99'
        if helpers.get_platform()['os_name'] == 'windows':
            filename += '.exe'
        open(filename, 'w+').close()
        result = run_command('webdriver-manager update -d chrome')
        assert result == 'INFO chromedriver is up to date'

    @pytest.mark.slow
    def test_update_local_version_lower_than_remote(self, dir_function):
        tempdir = dir_function['path']
        os.chdir(tempdir)
        filename = 'chromedriver_1.1'
        if helpers.get_platform()['os_name'] == 'windows':
            filename += '.exe'
        open(filename, 'w+').close()
        result = run_command('webdriver-manager update -d chrome')
        assert 'INFO updating chromedriver' in result
        assert 'INFO got chromedriver_' in result
        files = os.listdir()
        assert len(files) == 2

    @pytest.mark.slow
    def test_update_specify_driver_version(self, dir_function):
        tempdir = dir_function['path']
        os.chdir(tempdir)
        filename = 'chromedriver_2.38'
        if helpers.get_platform()['os_name'] == 'windows':
            filename += '.exe'
        result = run_command('webdriver-manager update -d chrome=2.38')
        assert 'INFO updating chromedriver' in result
        assert 'INFO got {}'.format(filename) in result
        files = os.listdir()
        assert files == [filename]

    @pytest.mark.slow
    def test_update_version_specified_does_not_exist(self, dir_function):
        tempdir = dir_function['path']
        os.chdir(tempdir)
        result = run_command('webdriver-manager update -d chrome=99.99')
        assert 'ERROR there was a 404 error trying to reach' in result
        assert 'This probably means the requested version does not exist.' in result
        files = os.listdir()
        assert files == []        

    @pytest.mark.slow
    def test_update_version_specified_already_exists(self, dir_function):
        tempdir = dir_function['path']
        os.chdir(tempdir)
        filename = 'chromedriver_2.38'
        if helpers.get_platform()['os_name'] == 'windows':
            filename += '.exe'
        open(filename, 'w+').close()
        result = run_command('webdriver-manager update -d chrome=2.38')
        expected = ('WARNING file chromedriver_2.38.exe already exists, skipping')
        assert result == expected

    def test_update_specified_driver_is_incorrect(self, dir_function):
        tempdir = dir_function['path']
        os.chdir(tempdir)
        result = run_command('webdriver-manager update -d invalid_driver')
        assert 'Exception: driver invalid_driver is not implemented' in result