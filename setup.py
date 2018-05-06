import os
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


here = os.path.abspath(os.path.dirname(__file__))


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['tests']
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)


setup(
    name='py-webdriver-manager',
    version='0.0.1',
    description='Webdriver executable manager utility',
    url='https://github.com/lucianopuccio/webdriver-manager',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Natural Language :: English',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: Software Development :: Testing',
        ],
    keywords='test selenium webdriver webdriver-manager',
    packages=find_packages(),
    install_requires=['requests', 'tqdm==4.23.1'],
    tests_require=['pytest'],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'webdriver-manager=webdriver_manager.main:main',
        ],
    },
    cmdclass={'test': PyTest}
)