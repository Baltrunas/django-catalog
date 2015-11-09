from django.conf.urls import url

from . import views

urlpatterns = [
	#Api json
	url(r'^api/json/category/list/$', views.json_category_list, name='json_category_list'),
	url(r'^api/json/product/list/$', views.json_product_list, name='json_product_list'),
	url(r'^api/json/product/search/$', views.search, name='search'),
	url(r'^api/json/product/ajax-search/$', views.ajax_search, name='ajax_search'),
	url(r'^api/json/product/update/(?P<product_id>\d+)/$', views.json_product_update, name='json_product_update'),
	url(r'^api/json/product/delete/(?P<product_id>\d+)/$', views.json_product_delete, name='json_product_delete'),
	url(r'^api/json/image/add/(?P<product_id>\d+)/$', views.json_image_add, name='json_image_add'),
	url(r'^api/json/image/delete/(?P<image_id>\d+)/$', views.json_image_delete, name='json_image_delete'),

	# Base
	url(r'^brand/(?P<slug>[-\w\d]+)/$', views.brand, name='catalog_brand'),
	url(r'^(?P<url>[-//\w\d]+)/(?P<id>\d+)/$', views.product, name='catalog_product'),
	url(r'^(?P<url>[-//\w\d]+)/$', views.category, name='catalog_category'),
]
