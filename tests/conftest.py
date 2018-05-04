import os
import sys
import shutil
import random
import string
import subprocess

import pytest


sys.path.append(os.path.join(os.path.dirname(__file__), 'helpers'))


def pytest_addoption(parser):
    parser.addoption("--runslow", action="store_true",
                     default=False, help="run slow tests")


def pytest_collection_modifyitems(config, items):
    if config.getoption("--runslow"):
        # --runslow given in cli: do not skip slow tests
        return
    skip_slow = pytest.mark.skip(reason="need --runslow option to run")
    for item in items:
        if "slow" in item.keywords:
            item.add_marker(skip_slow)


# FIXTURES

BASE_DIR = None


def random_string(length):
    st = ''.join(random.choice(string.ascii_lowercase) for _ in range(length))
    return st


def _directory_fixture():
    global BASE_DIR
    if not BASE_DIR:
        BASE_DIR = os.getcwd()
    os.chdir(BASE_DIR)
    dir_name = 'test_' + random_string(5)
    full_path = os.path.join(BASE_DIR, dir_name)
    if not os.path.exists(full_path):
        os.makedirs(full_path)
    os.chdir(full_path)
    sys.path.append(full_path)
    return full_path, dir_name


@pytest.fixture(scope="session")
def dir_session():    
    full_path, dir_name = _directory_fixture()
    os.chdir(full_path)
    yield {
            'path': full_path,
            'base_path': BASE_DIR,
            'name': dir_name}
    os.chdir(BASE_DIR)
    shutil.rmtree(full_path, ignore_errors=True)


@pytest.fixture(scope="function")
def dir_function():    
    full_path, dir_name = _directory_fixture()
    os.chdir(full_path)
    yield {
            'path': full_path,
            'base_path': BASE_DIR,
            'name': dir_name}
    os.chdir(BASE_DIR)
    shutil.rmtree(full_path, ignore_errors=True)


@pytest.fixture(scope="function")
def test_utils():    
    """A fixture that returns an instance of Test_utils"""
    yield Test_utils


# TEST UTILS   

class Test_utils:

    @staticmethod
    def create_test_files(path):
        open(os.path.join(path, 'chromedriver_2.2'), 'a').close()
        open(os.path.join(path, 'chromedriver_2.3'), 'a').close()
        open(os.path.join(path, 'geckodriver_2.5'), 'a').close()
        open(os.path.join(path, 'geckodriver_2.6'), 'a').close()

    @staticmethod
    def create_test_files_windows(path):
        open(os.path.join(path, 'chromedriver_2.2.exe'), 'a').close()
        open(os.path.join(path, 'chromedriver_2.3.exe'), 'a').close()
        open(os.path.join(path, 'geckodriver_2.5.exe'), 'a').close()
        open(os.path.join(path, 'geckodriver_2.6.exe'), 'a').close()

    @staticmethod
    def run_command(cmd):
        output = ''
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT, shell=True)
        for line in iter(p.stdout.readline, b''):
            line_parsed = line.decode('ascii').replace('\r', '')
            output += line_parsed

        if len(output) > 1 and output[-1] == '\n':
            output = output[:-1]
        return output