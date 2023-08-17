from pysnmp.hlapi import *

from Convert import excel_to_csv
from Get import get_state
from Getsub import getsub_state
from Toexcel import excel_export
from Log import get_logger
from Validation import check_ip
from Message import get_message

logger = get_logger('MAIN')

data = excel_to_csv()
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
        if (HOST_list[i] != '') & (check_ip(HOST_list[i]) == True) & (COMMUNITY_list[i] != ''):
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
                get_state(iterator, Message)
        else:
            get_message(HOST_list[i], COMMUNITY_list[i], Message)

    elif TYPE_list[i] == 'GETSUBTREE':
        if (HOST_list[i] != '') & (check_ip(HOST_list[i]) == True) & (COMMUNITY_list[i] != ''):
            Getsub = []
            engine = SnmpEngine()
            host = UdpTransportTarget((HOST_list[i], PORT))
            community = CommunityData(COMMUNITY_list[i], mpModel=1)
            if OID_list[i] == "":
                print('No OID')
                Message.append('OID 없음')
            getsub_state(engine, community, host, OID_list[i], Message, Getsub)
            if len(Message) <= i:
                print('No Information')
                Message.append('정보 없음')
        else:
            get_message(HOST_list[i], COMMUNITY_list[i], Message)
    else:
        if TYPE_list[i] == '':
            print('No SNMP Type')
            Message.append('SNMP 타입 정해지지 않음')
        elif TYPE_list != 'GET' and TYPE_list != 'GETSUBTREE':
            print('Wrong SNMP Type')
            Message.append('잘못된 SNMP Type임')

excel_export(result_data)
