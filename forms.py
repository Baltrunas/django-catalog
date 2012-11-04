# -*- coding: utf-8 -*-
from django.forms.widgets import Input
from django import forms
from django.utils.translation import ugettext as _


class Html5EmailInput(Input):
	input_type = 'email'
	required = 'required'


class OrderForm(forms.Form):
	name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'required': 'required'}), label=_('Name'))
	phone = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'required': 'required'}), label=_('Phone'))
	email = forms.EmailField(max_length=200, widget=Html5EmailInput(attrs={'required': 'required', 'placeholder': 'email@example.com'}), label=_('E-Mail'))
	comment = forms.CharField(required=False, widget=forms.Textarea(), label=_('Comment'))
