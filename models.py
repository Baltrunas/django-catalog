from decimal import Decimal

from django.db import models
from django.contrib.contenttypes.models import ContentType

from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import SafeUnicode


class BaseModel(models.Model):
	public = models.BooleanField(verbose_name=_('Public'), default=True)
	created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
	updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

	class Meta:
		abstract = True


def file_type(filename):
	filename = filename.split('.')
	filetype = filename[len(filename) - 1].lower()
	return filetype

def brand_upload(instance, filename):
	return 'catalog/_brands/%s.%s' % (instance.slug, file_type(filename))

def image_upload(instance, filename):
	return 'catalog/%s/%s.%s' % (instance.product.id, instance.id, file_type(filename))

def category_cover_upload(instance, filename):
	return 'catalog/_categories/%s_cover.%s' % (instance.slug, file_type(filename))

def category_icon_upload(instance, filename):
	return 'catalog/_categories/%s_icon.%s' % (instance.slug, file_type(filename))

def product_upload(instance, filename):
	return 'catalog/%s/_cover.%s' % (instance.id, file_type(filename))


class Brand(BaseModel):
	name = models.CharField(verbose_name=_('Name'), max_length=128)
	slug = models.SlugField(verbose_name=_('Slug'), max_length=128, help_text=_('A slug is the part of a URL which identifies a page using human-readable keywords'))
	logo = models.FileField(verbose_name=_('Logo'), upload_to=brand_upload, null=True, blank=True)


	@models.permalink
	def get_absolute_url(self):
		return ('catalog_brand', (), {'slug': self.slug})

	def __unicode__(self):
		return self.name

	class Meta:
		ordering = ['name']
		verbose_name = _('Brand')
		verbose_name_plural = _('Brands')


class Category(BaseModel):
	name = models.CharField(_('Name'), max_length=128)
	slug = models.SlugField(_('Slug'), max_length=128, help_text=_('A slug is the part of a URL which identifies a page using human-readable keywords'))
	cover = models.FileField(_('Cover'), upload_to=category_cover_upload, null=True, blank=True)
	icon = models.FileField(_('Icon'), upload_to=category_icon_upload, null=True, blank=True)

	parent = models.ForeignKey('self', verbose_name=_('Parent'), related_name='childs', null=True, blank=True)

	level = models.IntegerField(default=0, editable=False)
	order = models.IntegerField(default=500, null=True, blank=True)
	real_order = models.IntegerField(default=500, null=True, blank=True, editable=False)

	childs_count = models.IntegerField(default=0, null=True, blank=True, editable=False)
	products_count = models.IntegerField(default=0, null=True, blank=True, editable=False)
	products_total_count = models.IntegerField(default=0, null=True, blank=True, editable=False)

	url = models.CharField(verbose_name=_('URL'), max_length=1024, null=True, blank=True, editable=False)
	features = models.ManyToManyField('FeatureKey', verbose_name=_('Feature Key'), blank=True)

	def __init__(self, *args, **kwargs):
		super(Category, self).__init__(*args, **kwargs)
		self._prev_parent = self.parent
		self._prev_level = self.level
		self._prev_order = self.order

	@models.permalink
	def get_absolute_url(self):
		return ('catalog_category', (), {'url': self.url})

	def get_childs(self):
		return self.childs.filter(public=True)

	def get_products(self):
		return self.products.filter(deleted=False, public=True)

	def get_childs_count(self):
		return self.childs.filter(public=True).count()

	def get_products_count(self):
		return self.products.filter(deleted=False, public=True).count()

	def get_products_total_count(self):
		count = self.get_products_count()
		for child in self.childs.filter(public=True):
			count += child.get_products_total_count()
		return count

	def get_level(self):
		level = self.url.count('/')
		return level

	def resort(self, parent, i):
		if parent:
			categories = Category.objects.filter(parent=parent).order_by('order')
		else:
			categories = Category.objects.filter(parent__isnull=True).order_by('order')

		for category in categories:
			i += 1
			category.real_order = i
			category.save(sort=False)
			i = self.resort(category.id, i)
		return i

	def is_current(self, url):
		if self.url == url:
			return True
		else:
			return False

	def is_parent(self, url):
		childs = self.childs.filter(public=True)
		if childs:
			for item in childs:
				if item.url == url:
					return True
				else:
					return item.is_parent(url)
		else:
			return False

	def save(self, sort=True, *args, **kwargs):
		if self.parent:
			self.url = self.parent.url + '/' + self.slug 
		else:
			self.url = self.slug

		self.level = self.get_level()
		self.childs_count = self.get_childs_count()
		self.products_count = self.get_products_count()
		self.products_total_count = self.get_products_total_count()

		super(Category, self).save(*args, **kwargs)

		if sort:
			if self._prev_parent != self.parent or self._prev_order != self.order or self._prev_level != self.level:
				self.resort(0, 0)

	def __unicode__(self):
		padding = self.level * 4
		display = '&nbsp;' * padding + self.name
		return SafeUnicode(display)


	class Meta:
		ordering = ['real_order', 'name']
		verbose_name = _('Category')
		verbose_name_plural = _('Categories')


class Product(BaseModel):
	sync_id = models.IntegerField(_('Sync ID'), null=True, blank=True, editable=False)
	guid = models.CharField(_('GUID'), max_length=37, null=True, blank=True)
	barcode = models.CharField(_('Barcode'), max_length=40, null=True, blank=True)

	name = models.CharField(_('Name'), max_length=500)
	brand = models.ForeignKey(Brand, verbose_name=_('Brand'), null=True, blank=True)
	category = models.ForeignKey(Category, verbose_name=_('Category'), related_name='products')
	cover = models.FileField(verbose_name=_('Image'), upload_to=product_upload, null=True, blank=True)
	description = models.TextField(_('Description'), null=True, blank=True)

	articul = models.CharField(_('Articul'), max_length=30, null=True, blank=True)

	similar_product = models.ManyToManyField('self', verbose_name=_('Similar products'), related_name='similar_products', blank=True)

	retail_price = models.DecimalField(_('Retail Price'), max_digits=16, decimal_places=4, default=Decimal('0.0000'))
	wholesale_price = models.DecimalField(_('Wholesale Price'), max_digits=16, decimal_places=4, null=True, blank=True, default=Decimal('0.0000'))
	retail_price_with_discount = models.DecimalField(_('Retail Price With Discount'), max_digits=16, decimal_places=4, null=True, blank=True, default=Decimal('0.0000'))
	min_quantity_for_order = models.IntegerField(_('Min Quantity For Order'), default=0)
	warehouse_quantity = models.IntegerField(_('Warehouse Quantity'), default=0)

	height = models.IntegerField(_('Height'), null=True, blank=True)
	width = models.IntegerField(_('Width'), null=True, blank=True)
	size = models.CharField(_('The Size'), max_length=20, null=True, blank=True)
	color = models.CharField(_('Color'), max_length=50, null=True, blank=True)
	material = models.CharField(_('Material'), max_length=200, null=True, blank=True)

	SEX_CHOICES = (
		(0, _('Undefined')),
		(1, _('Man')),
		(2, _('Women')),
		(3, _('Boy')),
		(4, _('Girl')),
		(5, _('Unisex')),
	)
	sex = models.SmallIntegerField(_('Sex'), choices=SEX_CHOICES, default=0)

	season = models.CharField(_('Season'), max_length=100, null=True, blank=True)
	age = models.CharField(_('Age'), max_length=256, null=True, blank=True)

	sort = models.IntegerField(verbose_name=_('Sort'), default=500, blank=True, null=True)

	PRICE_FOR = (
		('one', _('For one')),
		('kg', _('Kilogram')),
		('day', _('Day')),
	)

	price_for = models.CharField(_('Price for'), max_length=50, choices=PRICE_FOR, default='one')

	main = models.BooleanField(verbose_name=_('Main'), default=False)
	deleted = models.BooleanField(_('Deleted'), default=False)

	class Meta:
		ordering = ['sort', 'name']
		verbose_name = _('Product')
		verbose_name_plural = _('Products')

	@models.permalink
	def get_absolute_url(self):
		return ('catalog_product', (), {'url': self.category.url, 'id': self.id})

	def get_content_type(self):
		return ContentType.objects.get_for_model(self)

	def __unicode__(self):
		return self.name


class Image(BaseModel):
	product = models.ForeignKey(Product, verbose_name=_('Product'), related_name='images')
	name = models.CharField(_('Name'), max_length=128, null=True, blank=True)
	image = models.FileField(_('Image'), upload_to=image_upload)

	def __unicode__(self):
		name = '%s -> %s' % (self.product.name, self.name or self.id)
		return name

	class Meta:
		ordering = ['name']
		verbose_name = _('Image')
		verbose_name_plural = _('Images')

# FeatureGroup
class GroupsFeature(BaseModel):
	name = models.CharField(_('Name'), max_length=256)

	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name=_('Groups Feature')
		verbose_name_plural=_('Groups Features')


class FeatureKey(BaseModel):
	group = models.ForeignKey(GroupsFeature, verbose_name=_('Group'), related_name='group_features', null=True)
	name = models.CharField(_('Name'), max_length=350)
	key = models.SlugField(_('Key'), unique=True)
	KIND = (
		('choice', _('Choice')),
		('range', _('Range')),
		('bool', _('Bool')),
	)
	kind = models.CharField(verbose_name=_('Kind'), max_length=10, choices=KIND)

	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name=_('Feature')
		verbose_name_plural=_('Features')


class FeatureValue(BaseModel):
	product = models.ForeignKey(Product, verbose_name=_('Product'), related_name='product_features', db_index=True)
	features = models.ForeignKey(FeatureKey, verbose_name=_('Feature Key'), db_index=True)
	value = models.CharField(_('Value'), max_length=4096)

	def __unicode__(self):
		return self.features.name + ': ' + self.value

	class Meta:
		# unique_together product features
		verbose_name=_('Feature Product')
		verbose_name_plural=_('Feature Products')


class Rent (models.Model):
	product = models.ForeignKey(Product, verbose_name=_('Product'))

	retail_price = models.DecimalField(_('Retail price'), max_digits=16, decimal_places=4, default=Decimal('0.0000'))
	retail_price_with_discount = models.DecimalField(_('Discount price'), max_digits=16, decimal_places=4, null=True, blank=True, default=Decimal('0.0000'))

	rent_from = models.DateTimeField(_('Rent from'))
	rent_to = models.DateTimeField(_('Rent to'))
	rent_count = models.PositiveIntegerField(_('Rent count'))

	def name(self):
		return '%s [%s - %s]' % (self.product.name, self.rent_from.date(), self.rent_to.date())

	def cover(self):
		return self.product.cover

	def save(self, sort=True, *args, **kwargs):
		if self.product.price_for == 'day':
			self.rent_count = (self.rent_to - self.rent_from).days

			self.retail_price = self.rent_count * self.product.retail_price
			self.retail_price_with_discount = self.rent_count * self.product.retail_price_with_discount

		rent = super(Rent, self).save(*args, **kwargs)
		return rent

	def get_content_type(self):
		return ContentType.objects.get_for_model(self)
