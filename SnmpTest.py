from pysnmp.hlapi import *

from Convert import ExcelToCSV
from GET import GetState
from GETSUB import GetSubState
from Toexcel import ExcelOut
from log import get_logger
from validation import checkIP

logger = get_logger('MAIN')

data = ExcelToCSV()
data = data.fillna('')
NAME = data['장비명']
HOST = data['IP주소']
PORT = 161
COMMUNITY = data['커뮤니티명']
OID = data['OID']
TYPE  = data['SNMP 타입']
HOST_list = HOST.values.tolist()
COMMUNITY_list = COMMUNITY.values.tolist()
NAME_list = NAME.values.tolist()
OID_list = OID.values.tolist()
TYPE_list = TYPE.values.tolist()

Message=[]
Getsub=[]

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
    if TYPE_list[i]=='GET':
        if (HOST_list[i] != '') & (checkIP(HOST_list[i]) == True) & (COMMUNITY_list[i] != ''):
            engine = SnmpEngine()
            host = UdpTransportTarget((HOST_list[i], PORT))
            community = CommunityData(COMMUNITY_list[i], mpModel=1)
            identity_obj_list = [
                ObjectType(ObjectIdentity(OID_list[i]))
            ]
            for identity_obj in identity_obj_list:
                iterator = getCmd(engine, community, host, ContextData(), identity_obj)
                GetState(iterator, Message)
        else:
            if HOST_list[i] == '' or COMMUNITY_list[i] == '':
                if HOST_list[i] == '' and COMMUNITY_list[i] != '':
                    print('No IP')
                    Message.append('IP 주소 없음')
                elif HOST_list[i] != '' and COMMUNITY_list[i] == '':
                    print('No Community')
                    Message.append('커뮤니티명 없음')
                else:
                    print('No IP & Community')
                    Message.append('IP 주소와 커뮤니티명 모두 없음')
            elif checkIP(HOST_list[i]) == False:
                print('Not available IP')
                Message.append('IP 주소 올바르지 않음')

    elif TYPE_list[i]=='GETSUBTREE':
        if (HOST_list[i] != '') & (checkIP(HOST_list[i]) == True) & (COMMUNITY_list[i] != ''):
            Getsub = []
            engine = SnmpEngine()
            host = UdpTransportTarget((HOST_list[i], PORT))
            community = CommunityData(COMMUNITY_list[i], mpModel=1)
            GetSubState(engine, community, host, OID_list[i], Message, Getsub)
            if len(Message) <= i:
                print('No Information')
                Message.append('정보 없음')

        else:
            if HOST_list[i] == '' or COMMUNITY_list[i] == '':
                if HOST_list[i] == '' and COMMUNITY_list[i] != '':
                    print('No IP')
                    Message.append('IP 주소 없음')
                elif HOST_list[i] != '' and COMMUNITY_list[i] == '':
                    print('No Community')
                    Message.append('커뮤니티명 없음')
                else:
                    print('No IP & Community')
                    Message.append('IP 주소와 커뮤니티명 모두 없음')
            elif checkIP(HOST_list[i]) == False:
                print('Not available IP')
                Message.append('IP 주소 올바르지 않음')
    else:
        if TYPE_list[i] == '':
            print('No SNMP Type')
            Message.append('SNMP 타입 정해지지 않음')
        elif TYPE_list != 'GET' and TYPE_list != 'GETSUBTREE':
            print('Wrong SNMP Type')
            Message.append('잘못된 SNMP Type임')

ExcelOut(result_data)
