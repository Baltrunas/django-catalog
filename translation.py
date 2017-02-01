from modeltranslation.translator import translator
from modeltranslation.translator import TranslationOptions


from .models import Category
from .models import Product
from .models import Image


class CategoryTranslationOptions(TranslationOptions):
	fields = ['name']

translator.register(Category, CategoryTranslationOptions)


class ProductTranslationOptions(TranslationOptions):
	fields = ['name', 'description']

translator.register(Product, ProductTranslationOptions)


class ImageTranslationOptions(TranslationOptions):
	fields = ['name']

translator.register(Image, ImageTranslationOptions)
