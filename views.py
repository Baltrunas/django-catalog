# -*- coding: utf-8 -*
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

from django.template import RequestContext

# Translation
from django.utils.translation import ugettext as _

from datetime import datetime
from catalog.models import *
from catalog.forms import OrderForm

import hashlib


def category_list(request):
	context = {}
	context['title'] = _('Catalog')
	context['categories'] = Category.objects.filter(public=True, parent=None)
	return render_to_response('catalog/category.html', context, context_instance=RequestContext(request))


def category_detail(request, url):
	context = {}
	context['category'] = get_object_or_404(Category, public=True, url=url)
	context['categories'] = Category.objects.filter(public=True, parent=context['category'].id)
	context['products'] = Product.objects.filter(public=True, category=context['category'].id)
	context['products_brands'] = Product.objects.filter(public=True, category=context['category'].id).order_by('brand')
	context['title'] = _('Catalog') + ' &rarr; ' + context['category'].name
	context['header'] = _('Catalog') + ' &rarr; ' + context['category'].name
	return render_to_response('catalog/category.html', context, context_instance=RequestContext(request))


def product_detail(request, url, article):
	context = {}
	context['product'] = get_object_or_404(Product, public=True, category__url=url, article=article)
	context['title'] = _('Catalog') + ' &rarr; ' + context['product'].name
	return render_to_response('catalog/product.html', context, context_instance=RequestContext(request))


def basket(request):
	context = {}
	if 'visitor' in request.COOKIES:
		visitor = request.COOKIES['visitor']
	else:
		visitor = hashlib.md5(str(datetime.now())).hexdigest()

	context['visitor'] = visitor

	if request.method == 'POST':
		if 'product' in request.POST:
			product = int(request.POST['product'])
			if 'count' in request.POST:
				count = abs(int(request.POST['count']))
			else:
				count = 1
			if Product.objects.filter(id=product, public=True).count():
				product = Product.objects.get(id=product)
				total_price = (product.price * count)
				if Basket.objects.filter(visitor=visitor, product=product, send_order=False).count():
					basket = Basket.objects.get(visitor=visitor, product=product, send_order=False)
					basket.count += count
					basket.total_price += total_price
				else:
					basket = Basket(visitor=visitor, product=product, count=count, total_price=total_price)
				basket.save()
			else:
				context['error'] = _('Price what you try to add does not exist!')
		elif 'save' in request.POST:
			if 'basket_id' in request.POST:
				id = int(request.POST['basket_id'])
				if Basket.objects.filter(id=id, visitor=visitor, send_order=False).count():
					basket = Basket.objects.get(id=id, visitor=visitor, send_order=False)
					basket.count = int(request.POST['count'])
					basket.total_price = (basket.product.price * basket.count)
					basket.save()
				else:
					context['error'] = _('Price what you try to save does not exist!')
		elif 'delet' in request.POST:
			if 'basket_id' in request.POST:
				id = int(request.POST['basket_id'])
				if Basket.objects.filter(id=id, visitor=visitor, send_order=False).count():
					Basket.objects.get(id=id, visitor=visitor, send_order=False).delete()
				else:
					context['error'] = _('Price what you try to delete does not exist!')

	context['basket'] = Basket.objects.filter(visitor=visitor, send_order=False)
	total_price = 0
	for i in context['basket']:
		total_price += i.total_price
	context['total_price'] = total_price
	desc = ''
	desc_i = 1
	for item in context['basket']:
		if desc_i != context['basket'].count():
			desc += item.product.name + ' [' + str(item.count) + ': ' + str(item.total_price) + '], '
		else:
			desc += item.product.name + ' [' + str(item.count) + ': ' + str(item.total_price) + ']'
		desc_i += 1
	context['basket_desc'] = desc

	context['form'] = OrderForm()

	context['title'] = _('Basket')
	response = render_to_response('catalog/basket.html', context, context_instance=RequestContext(request))
	response.set_cookie('visitor', visitor)
	return response


def order(request):
	context = {}
	if 'visitor' in request.COOKIES:
		visitor = request.COOKIES['visitor']
	else:
		visitor = hashlib.md5(str(datetime.now())).hexdigest()

	context['visitor'] = visitor

	if Basket.objects.filter(visitor=visitor, send_order=False).count():
		if request.method == 'POST':
			context['form'] = OrderForm(request.POST)
			context['basket'] = Basket.objects.filter(visitor=visitor, send_order=False)
			if context['form'].is_valid():
				context['ok'] = True
				context['formdate'] = context['form'].cleaned_data

				total_price = 0
				for basket_product in context['basket']:
					total_price += basket_product.total_price
				context['total_price'] = total_price

				order = Order(
					name=context['formdate'].get('name', None),
					email=context['formdate'].get('email', None),
					phone=context['formdate'].get('phone', None),
					comment=context['formdate'].get('comment', None),
					total_price=total_price
				)
				order.save()

				for basket_product in context['basket']:
					basket_product.order = order
					basket_product.send_order = True
					basket_product.save()
					total_price += basket_product.total_price

				admin_content = render_to_string('catalog/email.html', context)
				admin_subject = _('New Order')
				sendmsg = EmailMultiAlternatives(admin_subject, admin_content, 'zakaz@winnie-pooh.kg', ['himik89@gmail.com'])
				sendmsg.attach_alternative(admin_content, "text/html")
				sendmsg.send()
	else:
		context['empty'] = True

	context['title'] = _('Checkout')
	response = render_to_response('catalog/order.html', context, context_instance=RequestContext(request))
	response.set_cookie('visitor', visitor)
	return response
