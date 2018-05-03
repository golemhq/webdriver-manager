Webdriver Manager
==================================================
[![Build Status](https://travis-ci.org/lucianopuccio/webdriver-manager.svg?branch=master)](https://travis-ci.org/lucianopuccio/webdriver-manager)


A Selenium Webdriver executable manager utility written in Python.

# Installation

Requires Python 3.4+ and PIP.
```
pip install ?
```

# Download webdriver executables

```
webdriver-manager update
```

Downloads the executables into the current directory or into the ./drivers directory if it already exists.

**Specify a diferent output directory**

```
webdriver-manager update -o /some/other/directory
```

**Specify which drivers to update**

```
webdriver-manager update -d chrome firefox
```

**Specify which versions to download**

```
webdriver-manager update -d chrome=2.38
```

# Clean local webdriver files

```
webdriver-manager clean
```

Use the -o flag to specify an output directory and the -d flag to specify a webdriver.

# List local versions

```
webdriver-manager versions [-d | -o] 
```

# Using webdriver manager from code

**Functions:**

*webdriver_manager.update(driver_name, outputdir, version=None)*

*webdriver_manager.clean(outputdir, drivers=None)*

*webdriver_manager.versions(outputdir, drivers=None)*


**Example usage**

```
from webdriver_manager as wm

wm.update('chrome', './executables', version='2.38')
wm.update('firefox', './executables')

versions = wm.versions('./executables', ['chrome', 'firefox'])
# {
#   'chromedriver': [('2.38', 'chromedriver_2.38')],
#   'geckodriver': [('0.20.1', 'geckodriver_0.20.1')]
# }

wm.clean('./executables', ['chrome', 'firefox=0.20.1'])
```

