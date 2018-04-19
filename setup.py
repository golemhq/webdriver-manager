import os
from setuptools import setup, find_packages

import webdriver_manager


here = os.path.abspath(os.path.dirname(__file__))


setup(
    name='webdriver-manager',
    version=webdriver_manager.__version__,
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
    install_requires=['requests', 'tqdm'],
    tests_require=['pytest'],
    include_package_data=True,
    entry_points={  # Optional
        'console_scripts': [
            'webdriver-manager=webdriver_manager.main:main',
        ],
    },
)