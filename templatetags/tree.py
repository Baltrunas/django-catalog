# -*- coding: utf-8 -*
from django import template
# from django.template .loader
from magazine.models import *
register = template.Library()

@register.simple_tag
def tree(parent, tpl):
	t = template.loader.get_template(tpl)
	child_set = parent.child_set.all()
	return t.render(template.Context({'child_set': child_set}))