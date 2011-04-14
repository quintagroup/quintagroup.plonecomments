import logging

LOGGER = 'quintagroup.plonecomments'
PRODUCTS = []


def warning(msg):
    logging.getLogger(LOGGER).warning(msg)
