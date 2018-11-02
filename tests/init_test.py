import os

import pytest

from webdriver_manager import update, clean, versions, helpers
from webdriver_manager.webdriver.chromedriver import Chromedriver
from webdriver_manager.webdriver.geckodriver import Geckodriver


class Test_update:
    
    @pytest.mark.slow
    def test_update_chrome_to_latest(self, dir_function, caplog):
        os.chdir(dir_function['path'])
        outputdir = helpers.normalize_outputdir()
        platform = helpers.get_platform()
        driver = Chromedriver(outputdir, platform['os_name'], platform['os_bits'])
        latest_version = driver.get_latest_remote_version()
        update('chrome', outputdir)
        files = os.listdir()
        expected_file = 'chromedriver_{}'.format(latest_version)
        if platform['os_name'] == 'windows':
            expected_file += '.exe'
        assert files == [expected_file]
        log_records = caplog.records
        assert log_records[0].levelname == 'INFO'
        assert log_records[0].message == 'updating chromedriver'
        assert log_records[1].levelname == 'INFO'
        assert log_records[1].message == 'got {}'.format(expected_file)

    def test_update_chrome_local_is_up_to_date(self, dir_function, caplog):
        os.chdir(dir_function['path'])
        outputdir = helpers.normalize_outputdir()
        platform = helpers.get_platform()
        driver = Chromedriver(outputdir, platform['os_name'], platform['os_bits'])
        latest_version = driver.get_latest_remote_version()
        dummy_file = 'chromedriver_{}'.format(latest_version)
        if platform['os_name'] == 'windows':
            dummy_file += '.exe'
        open(os.path.join(outputdir, dummy_file), 'w+').close()
        update('chrome', outputdir)
        record = caplog.records[0]
        assert record.levelname == 'INFO'
        assert record.message == 'chromedriver is up to date'

    @pytest.mark.slow
    def test_update_firefox_to_latest(self, dir_function, caplog):
        os.chdir(dir_function['path'])
        outputdir = helpers.normalize_outputdir()
        platform = helpers.get_platform()
        driver = Geckodriver(outputdir, platform['os_name'], platform['os_bits'])
        latest_version = driver.get_latest_remote_version()
        update('firefox', outputdir)
        files = os.listdir()
        expected_file = 'geckodriver_{}'.format(latest_version)
        if platform['os_name'] == 'windows':
            expected_file += '.exe'
        assert files == [expected_file]
        log_records = caplog.records
        assert log_records[0].levelname == 'INFO'
        assert log_records[0].message == 'updating geckodriver'
        assert log_records[1].levelname == 'INFO'
        assert log_records[1].message == 'got {}'.format(expected_file)

    @pytest.mark.slow
    def test_update_firefox_local_is_up_to_date(self, dir_function, caplog):
        os.chdir(dir_function['path'])
        outputdir = helpers.normalize_outputdir()
        platform = helpers.get_platform()
        driver = Geckodriver(outputdir, platform['os_name'], platform['os_bits'])
        latest_version = driver.get_latest_remote_version()
        dummy_file = 'geckodriver_{}'.format(latest_version)
        if platform['os_name'] == 'windows':
            dummy_file += '.exe'
        with open(os.path.join(outputdir, dummy_file), 'w') as f:
            f.write('')
        update('firefox', outputdir)
        record = caplog.records[0]
        assert record.levelname == 'INFO'
        assert record.message == 'geckodriver is up to date'

    def test_update_chrome_version_does_not_exist(self, dir_function, caplog):
        os.chdir(dir_function['path'])
        outputdir = helpers.normalize_outputdir()
        platform = helpers.get_platform()
        driver = Chromedriver(outputdir, platform['os_name'], platform['os_bits'])
        version = '99.99'
        with pytest.raises(SystemExit):
            update('chrome', outputdir, version=version)
        log_records = caplog.records
        assert log_records[0].levelname == 'INFO'
        assert log_records[0].message == 'updating chromedriver'
        assert log_records[1].levelname == 'ERROR'
        url = driver._get_chromedriver_download_url(version)
        msg = ('there was a 404 error trying to reach {} \nThis probably '
               'means the requested version does not exist.'.format(url))
        assert log_records[1].message == msg


class Test_clean:

    def test_clean(self, dir_function, test_utils, caplog):
        os.chdir(dir_function['path'])
        outputdir = helpers.normalize_outputdir()
        test_utils.create_test_files(outputdir)
        clean(outputdir)
        assert len(os.listdir(outputdir)) == 0

    def test_clean_only_chrome(self, dir_function, test_utils):
        os.chdir(dir_function['path'])
        outputdir = helpers.normalize_outputdir()
        test_utils.create_test_files(outputdir)
        clean(outputdir, drivers=['chrome'])
        files = os.listdir(outputdir)
        assert len(files) == 2
        assert 'geckodriver_2.5' in files
        assert 'geckodriver_2.6' in files

    def test_clean_only_firefox(self, dir_function, test_utils):
        os.chdir(dir_function['path'])
        outputdir = helpers.normalize_outputdir()
        test_utils.create_test_files(outputdir)
        clean(outputdir, drivers=['firefox'])
        files = os.listdir(outputdir)
        assert len(files) == 2
        assert 'chromedriver_2.2' in files
        assert 'chromedriver_2.3' in files

    def test_clean_chrome_specific_version(self, dir_function, test_utils):
        os.chdir(dir_function['path'])
        outputdir = helpers.normalize_outputdir()
        test_utils.create_test_files(outputdir)
        clean(outputdir, drivers=['chrome=2.2'])
        files = os.listdir(outputdir)
        assert len(files) == 3
        assert 'geckodriver_2.5' in files
        assert 'geckodriver_2.6' in files
        assert 'chromedriver_2.3' in files

    def test_clean_only_chrome_windows(self, dir_function, test_utils):
        os.chdir(dir_function['path'])
        outputdir = helpers.normalize_outputdir()
        test_utils.create_test_files_windows(outputdir)
        clean(outputdir, drivers=['chrome'])
        files = os.listdir(outputdir)
        assert len(files) == 2
        assert 'geckodriver_2.5.exe' in files
        assert 'geckodriver_2.6.exe' in files

    def test_clean_only_chrome_windows_specific_version(self, dir_function, test_utils):
        os.chdir(dir_function['path'])
        outputdir = helpers.normalize_outputdir()
        test_utils.create_test_files_windows(outputdir)
        clean(outputdir, drivers=['chrome=2.2'])
        files = os.listdir(outputdir)
        assert len(files) == 3
        assert 'geckodriver_2.5.exe' in files
        assert 'geckodriver_2.6.exe' in files
        assert 'chromedriver_2.3.exe' in files

    def test_clean_multiple_drivers(self, dir_function, test_utils):
        os.chdir(dir_function['path'])
        outputdir = helpers.normalize_outputdir()
        test_utils.create_test_files(outputdir)
        clean(outputdir, drivers=['chrome=2.2', 'firefox=2.5'])
        files = os.listdir(outputdir)
        assert len(files) == 2
        assert 'geckodriver_2.6' in files
        assert 'chromedriver_2.3' in files

    def test_clean_console_output(self, dir_function, test_utils, caplog):
        os.chdir(dir_function['path'])
        outputdir = helpers.normalize_outputdir()
        test_utils.create_test_files(outputdir)
        clean(outputdir, drivers=['firefox=2.5', 'chrome=2.3'])
        log_record_list = ['{} {}'.format(x.levelname, x.message) for x in caplog.records]
        assert 'INFO removed chromedriver_2.3' in log_record_list
        assert 'INFO removed geckodriver_2.5' in log_record_list


class Test_versions:

    def test_versions_no_drivers_specified(self, dir_function, test_utils, caplog):
        os.chdir(dir_function['path'])
        outputdir = helpers.normalize_outputdir()
        test_utils.create_test_files(outputdir)
        result = versions(outputdir)
        log_record_list = ['{} {}'.format(x.levelname, x.message) for x in caplog.records]
        assert 'INFO chromedriver versions found: 2.2, 2.3' in log_record_list
        assert 'INFO geckodriver versions found: 2.5, 2.6' in log_record_list
        expected = {
            'chromedriver': [('2.2', 'chromedriver_2.2'), ('2.3', 'chromedriver_2.3')],
            'geckodriver': [('2.5', 'geckodriver_2.5'), ('2.6', 'geckodriver_2.6')]
        }
        assert result == expected

    def test_versions_driver_specified(self, dir_function, test_utils, caplog):
        os.chdir(dir_function['path'])
        outputdir = helpers.normalize_outputdir()
        test_utils.create_test_files(outputdir)
        result = versions(outputdir, drivers=['chrome'])
        log_records = caplog.records
        assert log_records[0].levelname == 'INFO'
        assert log_records[0].message == 'chromedriver versions found: 2.2, 2.3'
        assert len(log_records) == 1
        expected = {
            'chromedriver': [('2.2', 'chromedriver_2.2'), ('2.3', 'chromedriver_2.3')]
        }
        assert result == expected

    def test_versions_windows(self, dir_function, test_utils, caplog):
        os.chdir(dir_function['path'])
        outputdir = helpers.normalize_outputdir()
        test_utils.create_test_files_windows(outputdir)
        result = versions(outputdir)
        log_record_list = ['{} {}'.format(x.levelname, x.message) for x in caplog.records]
        assert 'INFO chromedriver versions found: 2.2, 2.3' in log_record_list
        assert 'INFO geckodriver versions found: 2.5, 2.6' in log_record_list
        expected = {
            'chromedriver': [('2.2', 'chromedriver_2.2.exe'), ('2.3', 'chromedriver_2.3.exe')],
            'geckodriver': [('2.5', 'geckodriver_2.5.exe'), ('2.6', 'geckodriver_2.6.exe')]
        }
        assert result == expected