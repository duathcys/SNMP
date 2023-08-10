from pysnmp.hlapi import *

from Convert import ExcelToCSV
from Get import GetState
from Getsub import GetSubState
from Toexcel import ExcelOut
from Log import get_logger
from Validation import checkIP
from Message import getMessage

logger = get_logger('MAIN')

data = ExcelToCSV()
data = data.fillna('')
NAME = data['장비명']
HOST = data['IP주소']
PORT = 161
COMMUNITY = data['커뮤니티명']
OID = data['OID']
TYPE = data['SNMP 타입']
HOST_list = HOST.values.tolist()
COMMUNITY_list = COMMUNITY.values.tolist()
NAME_list = NAME.values.tolist()
OID_list = OID.values.tolist()
TYPE_list = TYPE.values.tolist()

Message = []
Getsub = []

SIZE = len(HOST_list)
print(SIZE)

result_data = {
    '장비명': NAME_list,
    'IP주소': HOST_list,
    '커뮤니티명': COMMUNITY_list,
    'SNMP 타입': TYPE_list,
    'OID': OID_list,
    '결과메세지': Message
}

for i in range(SIZE):
    if TYPE_list[i] == 'GET':
        if (HOST_list[i] != '') & (checkIP(HOST_list[i]) == True) & (COMMUNITY_list[i] != ''):
            engine = SnmpEngine()
            host = UdpTransportTarget((HOST_list[i], PORT))
            community = CommunityData(COMMUNITY_list[i], mpModel=1)
            if OID_list[i] == "":
                print('No OID')
                Message.append('OID 없음')
            identity_obj_list = [
                ObjectType(ObjectIdentity(OID_list[i]))
            ]
            for identity_obj in identity_obj_list:
                iterator = getCmd(engine, community, host, ContextData(), identity_obj)
                GetState(iterator, Message)
        else:
            getMessage(HOST_list[i], COMMUNITY_list[i], Message)

    elif TYPE_list[i] == 'GETSUBTREE':
        if (HOST_list[i] != '') & (checkIP(HOST_list[i]) == True) & (COMMUNITY_list[i] != ''):
            Getsub = []
            engine = SnmpEngine()
            host = UdpTransportTarget((HOST_list[i], PORT))
            community = CommunityData(COMMUNITY_list[i], mpModel=1)
            if OID_list[i] == "":
                print('No OID')
                Message.append('OID 없음')
            GetSubState(engine, community, host, OID_list[i], Message, Getsub)
            if len(Message) <= i:
                print('No Information')
                Message.append('정보 없음')
        else:
            getMessage(HOST_list[i], COMMUNITY_list[i], Message)
    else:
        if TYPE_list[i] == '':
            print('No SNMP Type')
            Message.append('SNMP 타입 정해지지 않음')
        elif TYPE_list != 'GET' and TYPE_list != 'GETSUBTREE':
            print('Wrong SNMP Type')
            Message.append('잘못된 SNMP Type임')

ExcelOut(result_data)
