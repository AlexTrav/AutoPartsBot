# Модуль логирования

import logging
import logging.handlers


def init_logger(name):
    logger = logging.getLogger(name)
    FORMAT = '%(asctime)s :: %(name)s:%(lineno)s :: %(levelname)s :: %(message)s'
    logger.setLevel(logging.DEBUG)

    sh = logging.StreamHandler()
    sh.setFormatter(logging.Formatter(FORMAT))
    sh.setLevel(logging.DEBUG)
    logger.addHandler(sh)

    fh = logging.handlers.RotatingFileHandler(filename='logs/logs.log', maxBytes=100000)
    fh.setFormatter(logging.Formatter(FORMAT))
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)

    logger.debug('The logger was initialized')


init_logger('app')
