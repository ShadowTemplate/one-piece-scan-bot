import logging as log


def get_application_logger():
    log.basicConfig(level=log.DEBUG, format="%(asctime)s [%(levelname)s] %(message)s")
    return log
