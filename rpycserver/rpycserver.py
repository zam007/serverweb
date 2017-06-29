#!_*_coding:utf-8_*_
# __author__:"zam"
import time
import os, sys
from pickle import dumps
from rpyc import Service
from rpyc.utils.server import ThreadedServer
import configparser
import logging
from librc4 import *
from config import *

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# 将选用的模块方式加载到环境变量.
sys.path.append(os.sep.join((BASE_DIR, 'modules/' + AUTO_PLATFORM)))
print(sys.path)



class ManagerService(Service):
    def exposed_login(self, user, passwd):
        """
        =rpyc密码验证
        """
        if user == 'OMuser' and passwd == 'KJS23o4ij09gHF734iuhsdfhkGYSihoiwhj38u4h':
            self.Checkout_pass = True
        else:
            self.Checkout_pass = False

    def exposed_Runcommands(self, get_string):
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s [%(levelname)s] %(message)s',
                            filename=sys.path[0] + '/logs/omsys.log',
                            filemode='a')
        try:
            if self.Checkout_pass != True:
                return tencode("User verify failed!", SECRET_KEY)
        except:
            return tencode("Invalid Login!", SECRET_KEY)

        self.get_string_array = []
        # 按照'@@'分隔获取到的字符串
        self.get_string_array = tdecode(get_string, SECRET_KEY).split('@@')

        # 获取要操作的模块ID
        self.ModuleId = self.get_string_array[0]
        # 获取要操作的hosts
        self.Hosts = self.get_string_array[1]

        sys_param_array = []
        for i in range(2, len(self.get_string_array) - 1):
            sys_param_array.append(self.get_string_array[i])

        mid = "Mid_" + self.ModuleId
        importstring = "from " + mid + " import Modulehandle"
        try:
            exec(importstring)
        except:
            return tencode(u"Module \"" + mid + u"\" does not exist, Please add it", SECRET_KEY)

        Runobj = Modulehandle(self.ModuleId, self.Hosts, sys_param_array)
        Runmessages = Runobj.run()

        if AUTO_PLATFORM == "func":
            if type(Runmessages) == dict:
                returnString = func_transform(Runmessages, self.Hosts)
            else:
                returnString = str(Runmessages).strip()

        elif AUTO_PLATFORM == "ansible":
            if type(Runmessages) == dict:
                returnString = ansible_transform(Runmessages, self.Hosts)
            else:
                returnString = str(Runmessages).strip()

        elif AUTO_PLATFORM == "saltstack":
            if type(Runmessages) == dict:
                returnString = saltstack_transform(Runmessages, self.Hosts)
            else:
                returnString = str(Runmessages).strip()

        return tencode(returnString, SECRET_KEY)


s = ThreadedServer(ManagerService, port=11511, auto_register=False)
s.start()
