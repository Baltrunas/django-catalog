# -*- coding: utf-8 -*-
import json
from django.http import HttpResponse
from django.core import serializers
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

from django.conf import settings

# from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Product
from .models import Category
from .models import Brand
from .models import Image

from .forms import ProductForm, ImageForm


def category(request, url):
	context = {}
	context['category'] = get_object_or_404(Category, public=True, url=url)
	context['childs'] = Category.objects.filter(public=True, parent=context['category']).order_by('name')
	context['title'] = context['category'].name

	# # Pagination
	pages_list = context['category'].get_products()
	page_number = request.GET.get('page', None)

	paginator = Paginator(pages_list, settings.CATALOG_PER_PAGE)
	try:
		pages_list = paginator.page(page_number)
	except PageNotAnInteger:
		pages_list = paginator.page(1)
	except EmptyPage:
		pages_list = paginator.page(paginator.num_pages)

	context['pages_list'] = pages_list


	# context['products_brands'] = Product.objects.filter(public=True, category=context['category'].id).order_by('brand')

	return render(request, 'catalog/category.html', context)


def brand(request, slug):
	context = {}
	context['brand'] = get_object_or_404(Brand, public=True, slug=slug)
	context['childs'] = Product.objects.filter(public=True, brand=context['brand']).order_by('name')
	context['title'] = context['brand'].name

	return render(request, 'catalog/brand.html', context)


def product(request, url, id):
	context = {}
	context['product'] = get_object_or_404(Product, public=True, category__url=url, id=id)
	context['similar'] = Product.objects.filter(public=True, category=context['product'].category).order_by('?')[:5]
	context['title'] = context['product'].name
	return render(request, 'catalog/product.html', context)



def auth_check(view):
	def wrapped(request, *args, **kwargs):
		username = request.POST.get('username', None)
		password = request.POST.get('password', None)
		try:
			user = User.objects.get(username=username)
			status = user.check_password(password)
		except:
			return HttpResponse(json.dumps({'auth': False}), content_type='application/json')
		return view(request, *args, **kwargs)
	return wrapped


@csrf_exempt
@auth_check
def json_category_list(request):
	context = {}
	context['auth'] = True
	categories = []
	for category in Category.objects.all():
		category_dict = {
			"id": category.id,
			"name": category.name,
			"parent": category.parent,
		}
		categories.append(category_dict)
		context['categories'] = categories
	return HttpResponse(json.dumps(context, ensure_ascii=False, indent=4), content_type="application/json; charset=utf-8")


def list_to_json(raw_products):
	products = []
	for product in raw_products:
		product.retail_price = str(product.retail_price)
		product.wholesale_price = str(product.wholesale_price)
		product.retail_price_with_discount = str(product.retail_price_with_discount)
		images = []
		for image in product.images.all():
			image_dict = {
				"id": image.id,
				"product_id": image.product.id,
				"name": image.name,
				"image": image.image.url,
			}
			images.append(image_dict)
		product_dict = {
			"id": product.id,
			"barcode": product.barcode,
			"name": product.name,
			"cover": product.cover.url,
			"description": product.description,
			"retail_price": product.retail_price,
			"wholesale_price": product.wholesale_price,
			"retail_price_with_discount": product.retail_price_with_discount,
			"images": images,
		}
		products.append(product_dict)
	return products


@csrf_exempt
@auth_check
def json_product_list(request):
	context = {}
	context['auth'] = True
	context['products'] = list_to_json(Product.objects.all())
	return HttpResponse(json.dumps(context, ensure_ascii=False, indent=4), content_type="application/json; charset=utf-8")


@csrf_exempt
# @auth_check
def search(request):
	if 'q' in request.GET and request.GET['q']:
		q = request.GET['q']
		product = list_to_json(Product.objects.filter(Q(name__icontains=q) | Q(barcode__icontains=q), public=True, deleted=False)[:100])
		return HttpResponse(json.dumps(product, ensure_ascii=False, indent=4), content_type="application/json; charset=utf-8")


@csrf_exempt
def ajax_search(request):
	products = []
	if 'q' in request.GET and request.GET['q']:
		q = request.GET['q']
	for product in Product.objects.filter(Q(name__icontains=q) | Q(barcode__icontains=q), public=True, deleted=False)[:100]:
		products.append(product.name)
	return HttpResponse(json.dumps(products, ensure_ascii=False, indent=4), content_type="application/json; charset=utf-8")


@csrf_exempt
@auth_check
def json_product_update(request, product_id):
	context = {}
	context['auth'] = True
	product_instance = Product.objects.get(id=product_id)
	form = ProductForm(request.POST or None, request.FILES or None, instance=product_instance)
	if form.is_valid():
		form.save()
		context['status'] = True
	else:
		context['status'] = False
		context['errors'] = form.errors
	return HttpResponse(json.dumps(context, ensure_ascii=False), content_type="application/json; charset=utf-8")


@csrf_exempt
@auth_check
def json_product_delete(request, product_id):
	context = {}
	context['auth'] = True
	try:
		del_product = Product.objects.get(id=product_id)
		del_product.delete()
		context['status'] = True
	except:
		context['status'] = False
	return HttpResponse(json.dumps(context))


@csrf_exempt
@auth_check
def json_image_add(request, product_id):
	context = {}
	context['auth'] = True
	image_form = ImageForm(request.POST, request.FILES)
	if request.method == 'POST' and image_form.is_valid():
		new_file = image_form.save(commit=False)
		new_file.product = Product.objects.get(id=product_id)
		new_file.save()
		context['status'] = True
	else:
		context['status'] = False
	return HttpResponse(json.dumps(context), content_type='application/json')


@csrf_exempt
@auth_check
def json_image_delete(request, image_id):
	context = {}
	context['auth'] = True
	try:
		del_image = Image.objects.get(id=image_id)
		del_image.delete()
		context['status'] = True
	except:
		context['status'] = False
	return HttpResponse(json.dumps(context))
