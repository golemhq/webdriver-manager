import os

from . import helpers, config, logger


__version__ = '0.0.1'


def update(driver_name, outputdir, version=None):
    """Update local driver executable to the latest version or
    a specific version.
    driver : a driver name. Options:
     - chrome
     - firefox
    """
    platform = helpers.get_platform()
    driver_class = helpers.get_driver_class(driver_name)
    driver = driver_class(outputdir, platform['os_name'], platform['os_bits'])
    if version:
        logger.logger.info('updating {}'.format(driver_name))
        driver.download_driver_executable(version=version)
    elif driver.is_remote_higher_than_local():
            logger.logger.info('updating {}'.format(driver_name))
            latest_remote_version = driver.get_latest_remote_version()
            driver.download_driver_executable(version=latest_remote_version)
    else:
        logger.logger.info('{} is up to date'.format(driver_name))


def clean(outputdir, drivers=None):
    """Remove driver executables from the specified outputdir.
    
    drivers can be a list of drivers to filter which executables
    to remove. Use browser names instead i.e.: 'firefox', 'chrome'.
    Specify a version using an equal sign i.e.: 'chrome=2.2'
    """
    if drivers:
        # Generate a list of tuples: [(driver_name, requested_version)]
        # If driver string does not contain a version, the second element
        # of the tuple is None.
        # Example:
        # [('driver_a', '2.2'), ('driver_b', None)]
        drivers_split = [helpers.split_driver_name_and_version(driver) for driver in drivers] 
        file_data = [(helpers.driver_to_executable_filename(x[0]), x[1]) for x in drivers_split]
    else:
        file_data = [(x, None) for x in config.BASE_DRIVER_FILENAMES]

    files = [file for file in os.listdir(outputdir)
             if os.path.isfile(os.path.join(outputdir, file))]
    for file in files:
        for data in file_data:
            prefix, version = data
            starts_with = file.startswith(prefix)
            version_match = 'N/A'
            if version is not None:
                file_version = helpers.extract_version_from_filename(file)
                if file_version == version:
                    version_match = True
                else:
                    version_match = False
            if starts_with and version_match in [True, 'N/A']:
                filepath = os.path.join(outputdir, file)
                try:
                    os.remove(filepath)
                except OSError:
                    pass
                finally:
                    logger.logger.info('removed {}'.format(file))
                    break


def versions(outputdir, drivers=None):
    found_versions = {}
    files = os.listdir(outputdir)
    for file in files:
        for base_filename in config.BASE_DRIVER_FILENAMES:
            if file.startswith(base_filename):
                if not base_filename in found_versions:
                    found_versions[base_filename] = []
                item = (helpers.extract_version_from_filename(file), file)
                found_versions[base_filename].append(item)

    if drivers:
        # filter found_versions to only the required drivers
        driver_filenames = [helpers.driver_to_executable_filename(x) for x in drivers]
        filtered = {}
        for key, value in found_versions.items():
            if key in driver_filenames:
                filtered[key] = value
        found_versions = filtered

    for base_driver_filename, files in found_versions.items():
        # versions = [helpers.extract_version_from_filename(file) for file in files]
        versions = [item[0] for item in files]
        version_string = ', '.join(versions)
        plural = 's' if len(versions) > 1 else ''
        msg = '{} version{} found: {}'.format(base_driver_filename, plural, version_string)
        logger.logger.info(msg)

    return found_versions