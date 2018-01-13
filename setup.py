from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))


setup(
    name='webdriver-manager',
    version='1.2.0',
    description='A sample Python project',  # Required
    # long_description=long_description,  # Optional
    # url='https://github.com/pypa/sampleproject',  # Optional
    # author='The Python Packaging Authority',  # Optional
    # author_email='pypa-dev@googlegroups.com',  # Optional
    # classifiers=[  # Optional
    #     # How mature is this project? Common values are
    #     #   3 - Alpha
    #     #   4 - Beta
    #     #   5 - Production/Stable
    #     'Development Status :: 3 - Alpha',

    #     # Indicate who your project is intended for
    #     'Intended Audience :: Developers',
    #     'Topic :: Software Development :: Build Tools',

    #     # Pick your license as you wish (should match "license" above)
    #     'License :: OSI Approved :: MIT License',

    #     # Specify the Python versions you support here. In particular, ensure
    #     # that you indicate whether you support Python 2, Python 3 or both.
    #     'Programming Language :: Python :: 2',
    #     'Programming Language :: Python :: 2.7',
    #     'Programming Language :: Python :: 3',
    #     'Programming Language :: Python :: 3.4',
    #     'Programming Language :: Python :: 3.5',
    #     'Programming Language :: Python :: 3.6',
    # ],
    # keywords='sample setuptools development',  # Optional
    packages=find_packages(),  # Required
    install_requires=['requests',
                      'pytest'],
    # package_data={  # Optional
    #     'sample': ['package_data.dat'],
    # },
    # data_files=[('my_data', ['data/data_file'])],  # Optional
    entry_points={  # Optional
        'console_scripts': [
            'webdriver-manager=webdriver_manager.main:main',
        ],
    },
)