# -*- coding: utf-8 -*-
from django.forms import ModelForm, Form
from django import forms
from .models import Category, Product, Image, FeatureValue, Rent


class CategoryForm(ModelForm):
	class Meta:
		model = Category
		fields = ['name', 'slug', 'parent', 'order', 'public']


class ProductForm(ModelForm):
	class Meta:
		model = Product
		fields = ['name' ,'barcode', 'category', 'cover', 'description', 'articul', 'retail_price', 'wholesale_price', 'retail_price_with_discount', 'public', 'main', 'deleted']


class ImageForm(ModelForm):

	class Meta:
		model = Image
		exclude = ['product']


class FilterForm(Form):
	# category = forms.ModelMultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple, queryset=Category.objects.filter(public=True))

	def __init__(self, category, *args, **kwargs):
		initial = kwargs.pop('initial', {})

		super(FilterForm, self).__init__(*args, **kwargs)

		for key in category.features.all():
			if key.kind == 'choice':
				queryset = FeatureValue.objects.filter(public=True, features=key)
				self.fields[key.key] = forms.ModelMultipleChoiceField(label=key.name, required=False, widget=forms.CheckboxSelectMultiple, queryset=queryset)
			elif key.kind == 'range':
				min_max = Product.objects.filter(public=True).aggregate(
					Max('retail_price'),
					Min('retail_price'),
				)

class RentForm(ModelForm):
	class Meta:
		model = Rent
		fields = ['product', 'rent_from', 'rent_to', 'rent_count']
