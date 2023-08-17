from Validation import check_ip


def get_message(host, community, message):
    if host == '' or community == '':
        if host == '' and community != '':
            print('No IP')
            message.append('IP 주소 없음')
        elif host != '' and community == '':
            print('No Community')
            message.append('커뮤니티명 없음')
        else:
            print('No IP & Community')
            message.append('IP 주소와 커뮤니티명 모두 없음')
    elif not check_ip(host):
        print('Not available IP')
        message.append('IP 주소 올바르지 않음')
