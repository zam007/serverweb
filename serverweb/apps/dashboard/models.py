from django.db import models


class ServerFunCateg(models.Model):
    """
    ServerFunCateg服务功能分类表
    id : 服务功能分类ID
    server_categ_name : 服务功能分类名称
    """
    # id = models.IntegerField(primary_key=True, db_column='ID')
    server_categ_name = models.CharField(max_length=60)

    class Meta:
        db_table = u'server_fun_categ'

    def __str__(self):
        return self.server_categ_name


class ServerAppCateg(models.Model):
    """
    ServerAppCateg服务应用分类表
    id : 服务应用分类ID
    server_categ_id : 服务功能分类ID
    app_categ_name : 服务应用分类名称
    """
    # id = models.IntegerField(primary_key=True, db_column='ID')
    server_categ_id = models.ForeignKey(ServerFunCateg, related_name='serverappcateg')
    app_categ_name = models.CharField(max_length=90)

    class Meta:
        db_table = u'server_app_categ'

    def __str__(self):
        return self.app_categ_name


class ServerList(models.Model):
    """
    ServerList服务器列表
    server_name : 主机名称
    server_wip : 主机外网IP
    server_lip : 主机内网IP
    server_op : 主机操作系统
    server_app_id : 服务应用分类ID
    """
    server_app_id = models.ForeignKey(ServerAppCateg, related_name="serverlist")
    server_name = models.CharField(max_length=39, primary_key=True)
    server_wip = models.CharField(max_length=45)
    server_lip = models.CharField(max_length=36)
    server_op = models.CharField(max_length=30)

    class Meta:
        db_table = u'server_list'

    def __str__(self):
        return self.server_name


class ModuleList(models.Model):
    """
    ModuleList模块列表
    id : 模块ID号
    module_name : 模块名称
    module_caption : 模块功能描述
    module_extend : 模块前端扩展
    """
    id = models.IntegerField(primary_key=True, db_column='ID')
    module_name = models.CharField(max_length=60)
    module_caption = models.CharField(max_length=765)
    module_extend = models.CharField(max_length=6000)

    class Meta:
        db_table = u'module_list'
