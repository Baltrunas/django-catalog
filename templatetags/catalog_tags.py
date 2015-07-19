from django import template
register = template.Library()

from ..models import Category


@register.simple_tag
def catalog(parent=None):
	tpl = template.loader.get_template('catalog/category_tree.html')

	context = {}

	if parent:
		context['level'] = parent.get_level() + 2
	else:
		context['level'] = 1

	context['parent'] = parent
	context['categories'] = Category.objects.filter(public=True, parent=parent).order_by('order')


	return tpl.render(template.Context(context))
