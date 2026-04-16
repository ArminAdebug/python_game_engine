"""Module with logging functions
"""

import logging

# setup basic configs for logging
logging.basicConfig(
    format="[%(levelname)s] [%(name)s] %(message)s"
)

log = logging.getLogger("engine")
log.setLevel(logging.DEBUG)


class Logger:
    """logging methods
    """
    @staticmethod
    def log_exception(e: Exception):
        """logs exception with last Traceback and exit with 1 code

        Args:
            e (Exception): Error that will logged.
        """

        log.exception(e)
        exit(1)

    @staticmethod
    def log_error(*msg):
        """log error in output
        """
        log.error(*msg)

    @staticmethod
    def log_test(*msg):
        """log something for debuging
        """
        log.debug(*msg)

    @staticmethod
    def log_info(*msg):
        """log something for giving info
        """
        log.debug(*msg)
