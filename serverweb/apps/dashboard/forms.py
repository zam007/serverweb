#!_*_coding:utf-8_*_
# __author__:"zam"
from django import forms
from serverweb.apps.dashboard.models import ModuleList


class ModuleCreateForm(forms.ModelForm):
    """
    使用 ModelForm 从 ModuleList 创建表单
    """

    class Meta:
        model = ModuleList
        fields = ('module_name', 'module_caption', 'module_extend')
