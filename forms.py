# -*- coding: utf-8 -*-
from django.forms import ModelForm
from .models import Category, Product, Image


class CategoryForm(ModelForm):
	class Meta:
		model = Category
		fields = ['name', 'slug', 'parent', 'order']


class ProductForm(ModelForm):
	class Meta:
		model = Product
		fields = ['name' ,'barcode', 'category', 'cover', 'description', 'articul', 'retail_price', 'wholesale_price', 'retail_price_with_discount']


class ImageForm(ModelForm):

	class Meta:
		model = Image
		exclude = ['product']