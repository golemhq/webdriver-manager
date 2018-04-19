import os


def create_test_files(path):
    open(os.path.join(path, 'chromedriver_2.2'), 'a').close()
    open(os.path.join(path, 'chromedriver_2.3'), 'a').close()
    open(os.path.join(path, 'geckodriver_2.5'), 'a').close()
    open(os.path.join(path, 'geckodriver_2.6'), 'a').close()


def create_test_files_windows(path):
    open(os.path.join(path, 'chromedriver_2.2.exe'), 'a').close()
    open(os.path.join(path, 'chromedriver_2.3.exe'), 'a').close()
    open(os.path.join(path, 'geckodriver_2.5.exe'), 'a').close()
    open(os.path.join(path, 'geckodriver_2.6.exe'), 'a').close()   