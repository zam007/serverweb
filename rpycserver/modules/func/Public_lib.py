import sys
import xmlrpclib
import xmlrpc.client
import func.overlord.client as fc


def target_host(hosts, target_type='HN'):
    """
    =处理传入的hosts字符串，根据需求以';'分割返回hostname或者IP地址
    例子：
    传入：'192.168.1.1*4号服务器,118.190.68.4*func-master,202.77.130.94*hk-test'
    返回：'4号服务器;func-master;hk-test'或者'192.168.1.1;118.190.68.4;202.77.130.94'
    """
    target_string = ""
    hosts_string = ""
    for hrow in hosts.split(','):
        if target_type == "HN":
            hosts_string += hrow.split('*')[1] + ";"
        elif target_type == "IP":
            hosts_string += hrow.split('*')[0] + ";"
    target_string = hosts_string[0:len(hosts_string) - 1]
    return target_string
