import os
import sys
import shutil
import random
import string

import pytest


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
def dir_fixture():    
    full_path, dir_name = _directory_fixture()
    os.chdir(full_path)
    yield {
            'path': full_path,
            'base_path': BASE_DIR,
            'name': dir_name}
    os.chdir(BASE_DIR)
    shutil.rmtree(dir_name, ignore_errors=True)


@pytest.fixture(scope="function")
def func_dir_fixture():    
    full_path, dir_name = _directory_fixture()
    os.chdir(full_path)
    yield {
            'path': full_path,
            'base_path': BASE_DIR,
            'name': dir_name}
    os.chdir(BASE_DIR)
    shutil.rmtree(dir_name, ignore_errors=True)