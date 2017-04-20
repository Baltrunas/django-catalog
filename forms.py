# -*- coding: utf-8 -*-
from django.forms import ModelForm, Form
from django import forms
from .models import Category, Product, Image, FeatureValue, Rent
from django.utils.translation import ugettext_lazy as _


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

from django.utils.dateparse import parse_date
from datetime import date, timedelta

class RentForm(ModelForm):
	def clean_rent_from(self):
		if 'rent_from' in self.cleaned_data:
			today = date.today()
			rent_from = self.cleaned_data['rent_from'].date()
			if rent_from < today:
				raise forms.ValidationError(_('Min check in date is Today'))

		return self.cleaned_data['rent_from']


	def clean_rent_to(self):
		if 'rent_to' in self.cleaned_data:
			tomorrow = date.today() + timedelta(days=1)
			rent_to = self.cleaned_data['rent_to'].date()
			if rent_to < tomorrow:
				raise forms.ValidationError(_('Min check out date is Tomorrow'))

		if 'rent_from' in self.cleaned_data and 'rent_to' in self.cleaned_data:
			rent_from = self.cleaned_data['rent_from'].date()
			rent_to = self.cleaned_data['rent_to'].date()

			if rent_from > rent_to:
				raise forms.ValidationError(_('Check in must be after check out'))

		return self.cleaned_data['rent_to']


	class Meta:
		model = Rent
		fields = ['product', 'rent_from', 'rent_to', 'rent_count']
