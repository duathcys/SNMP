from pysnmp.hlapi import *

from log import get_logger

logger = get_logger('GET')


def GetState(iterator, Col):
    try:
        errorIndication, errorStatus, errorIndex, varBinds = next(iterator)
        if errorIndication:  # SNMP engine errors
            print(errorIndication)
            Col.append(errorIndication)
        else:
            if errorStatus:  # SNMP agent errors
                print('%s at %s' % (errorStatus.prettyPrint(),
                                varBinds[int(errorIndex) - 1] if errorIndex else '?'))
                Col.append('%s at %s' % (errorStatus.prettyPrint(),
                                varBinds[int(errorIndex) - 1] if errorIndex else '?'))
            else:
                for varBind in varBinds:  # SNMP response contents
                    print('='.join([x.prettyPrint() for x in varBind]))
                    Col.append(' = '.join([x.prettyPrint() for x in varBind]))
    except Exception as msg:
        logger.error(msg)
        logger.error('GET')