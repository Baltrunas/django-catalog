from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^(?P<url>[-//\w\d]+)/(?P<id>\d+)/$', views.product, name='catalog_product'),
	url(r'^(?P<url>[-//\w\d]+)/$', views.category, name='catalog_category'),
]
