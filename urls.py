# -*- coding: utf-8 -*
from django.conf.urls import patterns
from django.conf.urls import url

urlpatterns = patterns('catalog.views',
	# Canalog
	url(r'^$', 'category_list', name='category_list'),
	# Basket
	url(r'^basket/$', 'basket', name='basket'),
	# Order
	url(r'^order/$', 'order', name='order'),
	# Product
	url(r'^(?P<url>[-\w/\_]+)/(?P<article>[-\w\d_]+)/$', 'product_detail', name='product_detail'),
	# Category
	url(r'^(?P<url>[-\w/\_]+)/$', 'category_detail', name='catalog_category'),
)
