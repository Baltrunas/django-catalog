from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^brand/(?P<slug>[-\w\d]+)/$', views.brand, name='catalog_brand'),
	url(r'^(?P<url>[-//\w\d]+)/(?P<id>\d+)/$', views.product, name='catalog_product'),
	url(r'^(?P<url>[-//\w\d]+)/$', views.category, name='catalog_category'),
]
