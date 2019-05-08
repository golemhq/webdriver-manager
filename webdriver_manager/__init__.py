from .commands import update as update_command
from .commands import clean as clean_command
from .commands import versions as versions_command


__version__ = '0.0.3'


def update(driver_name, outputdir, version=None):
    update_command(driver_name, outputdir, version)


def clean(outputdir, drivers=None):
    clean_command(outputdir, drivers)


def versions(outputdir, drivers=None):
    versions_command(outputdir, drivers)
