import logging


def init_logger():
    logger = logging.getLogger('webdriver_manager')
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(levelname)s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger


logger = init_logger()