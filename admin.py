# -*- coding: utf-8 -*
from django.contrib import admin
from catalog.models import Category
from catalog.models import Brand
from catalog.models import Product
from catalog.models import Images
from catalog.models import Files
from catalog.models import Basket
from catalog.models import Order


class CategoryAdmin(admin.ModelAdmin):
	list_display = ('name', 'slug', 'url', 'public', 'main', 'order', 'image_preview')
	search_fields = ('img', 'name', 'slug', 'url', 'public', 'main')
	list_editable = ('public', 'main', 'order')
	list_filter = ['public', 'main']

admin.site.register(Category, CategoryAdmin)


class BrandAdmin(admin.ModelAdmin):
	list_display = ('name', 'slug', 'order', 'public', 'image_preview')
	search_fields = ('name', 'slug', 'order', 'public')
	list_editable = ('public', 'order')
	list_filter = ['public']


admin.site.register(Brand, BrandAdmin)


class ImagesInline(admin.TabularInline):
	model = Images
	extra = 0


class FilesInline(admin.TabularInline):
	model = Files
	extra = 0


class ProductAdmin(admin.ModelAdmin):
	list_display = ('name', 'price', 'public', 'main', 'created_at', 'image_preview')
	search_fields = ('name', 'price', 'public', 'main')
	list_editable = ('public', 'main')
	list_filter = ['public', 'main', 'brand', 'category']
	inlines = [ImagesInline, FilesInline]

admin.site.register(Product, ProductAdmin)


class BasketAdmin(admin.ModelAdmin):
	list_display = ('visitor', 'product', 'count', 'total_price', 'created_at', 'updated_at', 'send_order')
	search_fields = ('visitor', 'product', 'count', 'total_price', 'created_at', 'updated_at', 'send_order')
	list_filter = ['visitor', 'send_order']

admin.site.register(Basket, BasketAdmin)


class BasketInline(admin.StackedInline):
	model = Basket


class OrderAdmin(admin.ModelAdmin):
	list_display = ('name', 'email', 'phone', 'comment', 'created_at', 'total_price', 'delivery_status')
	search_fields = ('name', 'email', 'phone', 'comment', 'created_at', 'total_price', 'delivery_status')
	list_filter = ['name', 'email', 'phone', 'delivery_status']

admin.site.register(Order, OrderAdmin)
