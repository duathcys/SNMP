from pysnmp.hlapi import *

from Log import get_logger

logger = get_logger('GETSUB')


def GetSubState(engine, community, host, oid, Col, Col2):
    try:
        for (errorIndication,
             errorStatus,
             errorIndex,
             varBinds) in nextCmd(engine,
                                  community,
                                  host,
                                  ContextData(),
                                  ObjectType(ObjectIdentity(oid)),
                                  lexicographicMode=False):
            if errorIndication:
                print(errorIndication)
                Col.append(errorIndication)
                break
            elif errorStatus:
                print('%s at %s' % (errorStatus.prettyPrint(),
                                    errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
                Col.append('%s at %s' % (errorStatus.prettyPrint(),
                                         errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
                break
            elif errorIndex:
                print(errorIndex)
                Col.append(errorIndex)
                break
            else:
                for varBind in varBinds:
                    Col2.append('='.join([x.prettyPrint() for x in varBind]))
                    break
        if len(Col2) != 0:
            result = '\n'.join(Col2)
            print('\n' + result + '\n')
            Col.append(result)


    except Exception as msg:
        logger.error(msg)
        logger.error('GETSUB')
