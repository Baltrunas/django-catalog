# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.shortcuts import get_object_or_404

from .models import Product
from .models import Category


def category(request, url):
	context = {}
	context['category'] = get_object_or_404(Category, public=True, url=url)
	context['title'] = context['category'].name

	context['categories'] = Category.objects.filter(public=True, parent=context['category'].id)
	context['products'] = Product.objects.filter(public=True, category=context['category'].id)
	context['products_brands'] = Product.objects.filter(public=True, category=context['category'].id).order_by('brand')

	return render(request, 'catalog/category.html', context)


def product(request, url, id):
	context = {}
	context['product'] = get_object_or_404(Product, public=True, category__url=url, id=id)
	context['title'] = context['product'].name
	return render(request, 'catalog/product.html', context)
