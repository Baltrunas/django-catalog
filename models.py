# -*- coding: utf-8 -*
from django.db import models
from datetime import datetime
from hashlib import md5
# Fields
from catalog.fields import ThumbImageField
# Translation
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import SafeUnicode


class Category(models.Model):
	name = models.CharField(verbose_name=_('Name'), max_length=256)
	slug = models.SlugField(verbose_name=_('Slug'), max_length=128, unique=True)
	url = models.SlugField(verbose_name=_('Full URL'), max_length=512, editable=False)
	parent = models.ForeignKey('self', verbose_name=_('Parent'), null=True, blank=True, related_name='childs')
	order = models.PositiveSmallIntegerField(verbose_name=_('Order'), default=500)
	description = models.TextField(verbose_name=_('Description'), null=True, blank=True)

	def upload_path(instance, filename):
		filename = filename.split('.')
		filetype = filename[len(filename) - 1].lower()
		return 'catalog/category/%s.%s' % (instance.url, filetype)

	img = ThumbImageField(
		w=185,
		h=185,
		verbose_name=_('Image'),
		upload_to=upload_path,
		blank=True
	)

	main = models.BooleanField(verbose_name=_('Main'))
	public = models.BooleanField(verbose_name=_('Public'), default=True)
	created_at = models.DateTimeField(verbose_name=_('Created At'), auto_now_add=True)
	updated_at = models.DateTimeField(verbose_name=_('Updated At'), auto_now=True)

	def image_preview(self):
		if self.img:
			return '<img src="%s" width="100">' % self.img.thumb_url
		else:
			return '(none)'
	image_preview.short_description = _('Image')
	image_preview.allow_tags = True

	def url_puth(self, this):
		if this.parent:
			return self.url_puth(this.parent) + '/' + this.slug
		else:
			return this.slug

	def display(self):
		return '&nbsp;' * (len(self.url.split('/')) - 1) * 6 + self.name
	display.short_description = _('Category')
	display.allow_tags = True

	def save(self, *args, **kwargs):
		self.url = self.url_puth(self)
		super(Category, self).save(*args, **kwargs)
		for child in self.childs.all():
			child.save()

	@models.permalink
	def get_absolute_url(self):
		return ('catalog_category', (), {'url': self.url})

	def __unicode__(self):
		return SafeUnicode('&nbsp;' * (len(self.url.split('/')) - 1) * 6 + self.name)

	class Meta:
		ordering = ['url', 'order']
		verbose_name = _('Category')
		verbose_name_plural = _('Categories')


class Brand(models.Model):
	name = models.CharField(verbose_name=_('Name'), max_length=255)
	slug = models.SlugField(verbose_name=_('Slug'), max_length=128, unique=True)
	description = models.TextField(verbose_name=_('Description'), null=True, blank=True)

	img = ThumbImageField(
		w=132,
		h=132,
		verbose_name=_('Image'),
		upload_to=lambda instance, filename: 'catalog/brand/%s.%s' % (instance.slug, filename.split('.')[len(filename.split('.')) - 1].lower()),
		blank=True
	)

	def image_preview(self):
		if self.img:
			return '<img src="%s" width="100">' % self.img.thumb_url
		else:
			return '(none)'
	image_preview.short_description = _('Image')
	image_preview.allow_tags = True

	order = models.PositiveSmallIntegerField(verbose_name=_('Order'), default=500)
	public = models.BooleanField(verbose_name=_('Public'), default=True)
	created_at = models.DateTimeField(verbose_name=_('Created At'), auto_now_add=True)
	updated_at = models.DateTimeField(verbose_name=_('Updated At'), auto_now=True)

	def __unicode__(self):
		return self.name

	class Meta:
		ordering = ['order', 'name']
		verbose_name = _('Brand')
		verbose_name_plural = _('Brands')


class Product(models.Model):
	name = models.CharField(verbose_name=_('Name'), max_length=255)
	article = models.SlugField(verbose_name=_('Article'), max_length=128, unique=True, help_text=_('Latin simbols'))
	category = models.ForeignKey(Category, verbose_name=_('Category'), related_name='products')
	brand = models.ForeignKey(Brand, verbose_name=_('Brand'), related_name='products')
	short_description = models.TextField(verbose_name=_('Short Description'), null=True, blank=True)
	description = models.TextField(verbose_name=_('Description'), null=True, blank=True)
	price = models.DecimalField(verbose_name=_('Price'), max_digits=10, decimal_places=2)
	main = models.BooleanField(verbose_name=_('Main'))
	public = models.BooleanField(verbose_name=_('Public'), default=True)
	created_at = models.DateTimeField(verbose_name=_('Created At'), auto_now_add=True)
	updated_at = models.DateTimeField(verbose_name=_('Updated At'), auto_now=True)

	img = ThumbImageField(
		w=229,
		h=229,
		verbose_name=_('Image'),
		upload_to=lambda instance, filename: 'catalog/price/%s.%s' % (instance.article, filename.split('.')[len(filename.split('.')) - 1].lower()),
		blank=True
	)

	def image_preview(self):
		if self.img:
			return '<img src="%s" width="100">' % self.img.thumb_url
		else:
			return '(none)'
	image_preview.short_description = _('Image')
	image_preview.allow_tags = True

	@models.permalink
	def get_absolute_url(self):
		return ('product_detail', (), {'url': self.category.url, 'article': self.article})

	def __unicode__(self):
		return self.name + '(' + str(self.price) + ')'

	class Meta:
		ordering = ['name']
		verbose_name = _('Product')
		verbose_name_plural = _('Products')


class Images(models.Model):
	name = models.CharField(verbose_name=_('Name'), max_length=255)
	img = ThumbImageField(
		w=200,
		h=200,
		verbose_name=_('Image'),
		upload_to=lambda instance, filename: 'catalog/price/%s/%s' % (instance.product.article, filename),
	)
	product = models.ForeignKey(Product, verbose_name=_('Product'), related_name='images')

	def __unicode__(self):
		return self.name


class Files(models.Model):
	name = models.CharField(verbose_name=_('Name'), max_length=255)
	description = models.TextField(verbose_name=_('Description'), blank=True)
	FILE_TYPE_CHOICES = (
		('video', _('Video')),
		('other', _('Other')),
	)
	file_type = models.CharField(max_length=10, choices=FILE_TYPE_CHOICES, verbose_name=_('File Type'))
	product = models.ForeignKey(Product, verbose_name=_('Product'))
	file_data = models.FileField(
		verbose_name=_('File'),
		upload_to=lambda instance, filename: 'catalog/price/%s/%s.%s' % (instance.file_type, md5(str(datetime.now()) + filename).hexdigest(), filename.split('.')[len(filename.split('.')) - 1].lower()),
	)

	def __unicode__(self):
		return '[%s] - %s' % (self.name, self.file_type)

	class Meta:
		ordering = ['name']
		verbose_name = _('File')
		verbose_name_plural = _('Files')


class Order(models.Model):
	name = models.CharField(verbose_name=_('Name'), max_length=256)
	email = models.EmailField(verbose_name=_('E-Mail'))
	phone = models.CharField(verbose_name=_('Phone'), max_length=32)
	comment = models.TextField(verbose_name=_('Comment'), null=True, blank=True)
	created_at = models.DateTimeField(verbose_name=_('Created At'), auto_now_add=True)
	total_price = models.DecimalField(verbose_name=_('Total Price'), max_digits=10, decimal_places=2)
	delivery_status = models.BooleanField(verbose_name=_('Delivery Status'), default=False)

	def __unicode__(self):
		return '%s (%s)' % (self.email, self.total_price)

	class Meta:
		verbose_name = _('Order')
		verbose_name_plural = _('Orders')


class Basket(models.Model):
	visitor = models.CharField(max_length=32, verbose_name=_('Visitor'), editable=False, default='')
	product = models.ForeignKey(Product, verbose_name=_('Price'))
	count = models.PositiveIntegerField(verbose_name=_('Count'), default=0)
	total_price = models.DecimalField(verbose_name=_('Total Price'), max_digits=10, decimal_places=2)
	order = models.ForeignKey(Order, verbose_name=_('Order'), blank=True, null=True)
	created_at = models.DateTimeField(verbose_name=_('Created At'), auto_now_add=True)
	updated_at = models.DateTimeField(verbose_name=_('Updated At'), auto_now=True)
	send_order = models.BooleanField(verbose_name=_('Order Send'), default=False)

	def __unicode__(self):
		return '%s x %s = %s' % (self.product.name, self.count, self.total_price)

	class Meta:
		verbose_name = _('Basket')
		verbose_name_plural = _('Basket')
