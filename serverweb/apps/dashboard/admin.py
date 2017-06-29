from django.contrib import admin
from serverweb.apps.dashboard.models import ServerFunCateg, ServerAppCateg, ServerList, ModuleList


class ServerFunCategAdmin(admin.ModelAdmin):
    list_display = ('id', 'server_categ_name')


class ServerAppCategAdmin(admin.ModelAdmin):
    list_display = ('id', 'server_categ_id', 'app_categ_name')


class ServerListAdmin(admin.ModelAdmin):
    list_display = ('server_app_id', 'server_name', 'server_wip', 'server_lip', 'server_op')


class ModuleListAdmin(admin.ModelAdmin):
    list_display = ('id', 'module_name', 'module_caption', 'module_extend')


admin.site.register(ServerFunCateg, ServerFunCategAdmin)
admin.site.register(ServerAppCateg, ServerAppCategAdmin)
admin.site.register(ServerList, ServerListAdmin)
admin.site.register(ModuleList, ModuleListAdmin)
