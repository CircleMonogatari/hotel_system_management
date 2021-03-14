# -- coding: utf-8 --
from django import forms


class id_list_from(forms.Form):
    data_list = forms.CharField(label='ID List 用, 隔开',
                                help_text='用,隔开',
                                )
