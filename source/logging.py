import logging

logging.basicConfig(
    format="[%(levelname)s] %(message)s"
)

log = logging.getLogger("engine")
log.level = logging.DEBUG

def log_exception(e : Exception):
    log.error(e)

def log_test(*msg):
    log.debug(*msg)

def log_info(*msg):
    log.debug(*msg)
