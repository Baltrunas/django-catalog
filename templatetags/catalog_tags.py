from django import template
register = template.Library()

from ..models import Category, Product


@register.simple_tag
def catalog(parent=None):
	context = {}

	tpl = template.loader.get_template('catalog/category_tree.html')

	if parent:
		context['level'] = parent.get_level() + 2
	else:
		context['level'] = 1

	context['parent'] = parent
	context['categories'] = Category.objects.filter(public=True, parent=parent).order_by('order')


	return tpl.render(template.Context(context))


@register.simple_tag(takes_context=True)
def products(context, category_slug):
	tpl = template.loader.get_template('catalog/products.html')
	context['products'] = Product.objects.filter(public=True, category__slug=category_slug).order_by('sort')

	return tpl.render(template.Context(context))
