from django.contrib import admin

from .models import Brand
from .models import Category
from .models import Product
from .models import Image
from .models import GroupsFeature
from .models import FeatureKey
from .models import FeatureValue


class BrandAdmin(admin.ModelAdmin):
	list_display = ['name']
	search_fields = ['name']
	save_as = True

admin.site.register(Brand, BrandAdmin)



class ImageInline(admin.TabularInline):
	model = Image
	extra = 0

class ProductAdmin(admin.ModelAdmin):
	list_display = ['name', 'sync_id', 'articul', 'retail_price', 'retail_price_with_discount', 'sort', 'public', 'main']
	list_filter = ['public', 'main', 'category']
	list_editable = ['sort', 'public', 'main']
	search_fields = ['name', 'articul']
	inlines = [ImageInline]
	save_as = True

admin.site.register(Product, ProductAdmin)


class CategoryAdmin(admin.ModelAdmin):
	list_display = ['__unicode__', 'slug', 'url', 'real_order']
	list_filter = ['level']
	search_fields = ['name', 'slug']
	save_as = True

admin.site.register(Category, CategoryAdmin)


class ImageAdmin(admin.ModelAdmin):
	list_display = ['__unicode__']
	list_filter = ['created_at', 'updated_at']
	search_fields = ['name']

admin.site.register(Image, ImageAdmin)


admin.site.register(GroupsFeature)
admin.site.register(FeatureKey)
admin.site.register(FeatureValue)