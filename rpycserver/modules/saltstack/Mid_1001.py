# -*- coding: utf-8 -*-
from Public_lib import *

#查看系统日志模块#

class Modulehandle():
    def __init__(self,moduleid,hosts,sys_param_row):
        self.hosts = ""
        self.Runresult = ""
        self.moduleid = moduleid
        self.sys_param_array= sys_param_row
        self.hosts=target_host(hosts,"HN").split(";")

    def __str__(self):
        return "HOST:" + ','.join(self.hosts) + " Action:" + str(self.moduleid)

    def run(self):
        try:
            client = salt.client.LocalClient()
            self.Runresult  = client.cmd(self.hosts,'cmd.run',["/usr/bin/tail -"+str(self.sys_param_array[0])+" /var/log/messages"],expr_form='list')
            if len(self.Runresult) == 0:
                return "No hosts found,请确认主机已经添加saltstack环境！"
        except Exception as e:
            return str(e)
        return self.Runresult
