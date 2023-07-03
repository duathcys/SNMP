import ipaddress
from log import get_logger

logger = get_logger('validation')


def checkIP(value):
    try:
        try:
            ip = ipaddress.ip_address(value)
            return True
        except:
            return False
    except Exception as msg:
        logger.error(msg)
        logger.error('validation')
