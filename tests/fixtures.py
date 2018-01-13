import os
import sys
import shutil

import pytest


BASE_DIR = None


@pytest.fixture(scope="session")
def testdir_fixture():    
    global BASE_DIR
    if not BASE_DIR:
        BASE_DIR = os.getcwd()
    os.chdir(BASE_DIR)
    testdir_name = 'temp_directory'
    full_path = os.path.join(BASE_DIR, testdir_name)
    if not os.path.exists(full_path):
    	os.makedirs(full_path)
    os.chdir(full_path)
    sys.path.append(full_path)
    yield {
            'path': full_path,
            'base_path': BASE_DIR,
            'name': testdir_name}
    os.chdir(BASE_DIR)
    #shutil.rmtree(testdir_name, ignore_errors=True)

