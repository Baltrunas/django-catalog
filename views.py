# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.shortcuts import get_object_or_404

from .models import Product
from .models import Category
from .models import Brand


def category(request, url):
	context = {}
	context['category'] = get_object_or_404(Category, public=True, url=url)
	context['childs'] = Category.objects.filter(public=True, parent=context['category']).order_by('name')
	context['title'] = context['category'].name

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
