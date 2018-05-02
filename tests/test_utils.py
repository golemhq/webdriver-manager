import os
import subprocess


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