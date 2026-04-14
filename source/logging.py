import logging

logging.basicConfig(
    format="[%(levelname)s] [%(name)s] %(message)s"
)

log = logging.getLogger("engine")
log.setLevel(logging.DEBUG)

def log_exception(e : Exception):
    log.exception(e)
    exit(1)
    
def log_test(*msg):
    log.debug(*msg)

def log_info(*msg):
    log.debug(*msg)
