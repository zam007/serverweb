from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import json
# common
from serverweb.common.decorators import ajax_required
# Form
from serverweb.apps.dashboard.forms import ModuleCreateForm
# model
from serverweb.apps.dashboard.models import ServerFunCateg, ServerAppCateg, ServerList, ModuleList


def index(request):
    """
    =dashboard 主页
    """
    res_template_dist = {'system_name': settings.SYSTEM_NAME}
    return render(request,
                  "dashboard/main.html",
                  res_template_dist)


@ajax_required
def server_fun_categ(request):
    """
    =Return server function categ
    """
    categ_id = "-1"
    categ_name = "<-请选择功能类别->"

    # ServerFunCateg表对象，实现读取所有功能列表，以 'id' 排序
    ServerFunObj = ServerFunCateg.objects.order_by('id')
    for e in ServerFunObj:
        categ_id += "," + str(e.id)
        categ_name += "," + e.server_categ_name
    fun_categ_string = categ_name + "|" + categ_id
    return HttpResponse(fun_categ_string)


@ajax_required
def server_app_categ(request):
    """
    =Return server app categ
    """
    categ_id = "-1"
    categ_name = "<-请选择应用类别->"

    if not 'fun_categId' in request.GET:
        fun_categId = ""
    else:
        # 获取用户选择的 功能 分类ID
        fun_categId = request.GET['fun_categId']

    ServerAppObj = ServerAppCateg.objects.filter(server_categ_id=fun_categId)
    for e in ServerAppObj:
        categ_id += "," + str(e.id)
        categ_name += "," + e.app_categ_name
    app_categ_string = categ_name + "|" + categ_id
    return HttpResponse(app_categ_string)


@ajax_required
def server_list(request):
    """
    =Return server IP list
    """
    ip = ""
    ip_hostname = ""

    if not 'app_categId' in request.GET:
        app_categId = ""
    else:
        # 获取用户选择的 应用 分类ID
        app_categId = request.GET['app_categId']

    ServerListObj = ServerList.objects.filter(server_app_id=app_categId)
    for e in ServerListObj:
        ip += "," + e.server_lip
        ip_hostname += "," + e.server_lip + "*" + e.server_name

    # 输出格式：192.168.1.10,192.168.1.20|192.168.1.10*servername1,192.168.1.20*servername2
    # 分隔符 "|" 前部分为 IP 地址，作为 HTML <option> 下拉框显示项目，后部为 <option> 的value,以 "*" 分隔
    server_list_string = ip[1:] + "|" + ip_hostname[1:]
    return HttpResponse(server_list_string)


@ajax_required
def module_list(request):
    """
    =Return module list
    """
    module_id = "-1"
    module_name = "请选择功能模块..."

    ModuleObj = ModuleList.objects.order_by('id')
    for e in ModuleObj:
        module_id += "," + str(e.id)
        module_name += "," + e.module_name
    module_list_string = module_name + "|" + module_id
    return HttpResponse(module_list_string)


def module_add(request):
    """
    =模块添加方法
    """
    if request.method == 'POST':

        form = ModuleCreateForm(data=request.POST)
        if form.is_valid():
            # 还未分配模块ID暂时不存储到数据库
            new_module_obj = form.save(commit=False)
            # 检查数据库中是否已经有模块，如果没有，设置最新的模块ID为1000，如果有，则在最后一个id+1为新模块ID
            try:
                lastId = ModuleList.objects.latest('id').id
            except:
                lastId = 1000
            new_module_obj.id = lastId + 1
            new_module_id = form.save().id
            return HttpResponse('祝贺你，模块前端添加成功，模块 ID 为：{},' \
                                '下一步请在服务器端编写模块逻辑！'.format(new_module_id))
    else:
        return render(request,
                      "dashboard/module_add.html")


@ajax_required
def module_info(request):
    """
    =Return module info
    """
    Module_Id = request.POST.get('currvalue')
    ModuleObj = ModuleList.objects.get(id=Module_Id)
    # 以json格式返回modul信息
    module_json_obj = json.dumps({
        'module_id': ModuleObj.id,
        'module_name': ModuleObj.module_name,
        'module_caption': ModuleObj.module_caption,
        'module_extend': ModuleObj.module_extend
    })

    return HttpResponse(module_json_obj)


def module_run(request):
    """
    =Run module
    =向 rpyc 服务器端发起任何请求
    """
    from serverweb.common.librc4 import tdecode, tencode
    import rpyc
    import urllib.parse, logging
    put_string = ""

    # 获取前端json对象
    module_json_obj = json.loads(urllib.parse.unquote(request.body.decode()))

    if not 'ModuleID' in module_json_obj:
        Module_Id = ""
    else:
        Module_Id = module_json_obj['ModuleID']
    put_string += Module_Id + "@@"

    if not 'hosts' in module_json_obj:
        Hosts = ""
    else:
        Hosts = ','.join(module_json_obj['hosts'])
        put_string += Hosts + "@@"

    if not 'sys_param_1' in module_json_obj:
        Sys_param_1 = ""
    else:
        Sys_param_1 = module_json_obj['sys_param_1']
    put_string += Sys_param_1 + "@@"

    if not 'sys_param_2' in module_json_obj:
        Sys_param_2 = ""
    else:
        Sys_param_2 = module_json_obj['sys_param_2']
    put_string += Sys_param_2 + "@@"
    try:
        # conn = rpyc.connect('192.168.0.205', 11511)
        conn = rpyc.connect('118.190.68.4', 11511)
        conn.root.login('OMuser', 'KJS23o4ij09gHF734iuhsdfhkGYSihoiwhj38u4h')
    except Exception as e:
        logging.error('connect rpyc server error:' + str(e))
        return HttpResponse('connect rpyc server error:' + str(e))

    # 生成要由rpyc传输的byte对象
    put_string = tencode(put_string, settings.SECRET_KEY)

    # 获取rpyc返回的信息，并用SECRET_KEY解密
    OPresult = tdecode(conn.root.Runcommands(put_string), settings.SECRET_KEY)
    return HttpResponse(OPresult)
