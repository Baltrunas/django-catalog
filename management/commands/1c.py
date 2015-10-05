import os
import re
import unicodecsv

from django.conf import settings

from django.core.management.base import BaseCommand
from django.core.management.base import CommandError

from ...models import Brand
from ...models import Product
from ...models import Category
from ...models import Image


import xmltodict

class Command(BaseCommand):
	help = 'Synchronize catalog with 1c'

	def handle(self, *args, **options):
		file_puth = os.path.abspath(settings.MEDIA_ROOT + '/1c/Menu.xml')
		images_puth = os.path.abspath(settings.MEDIA_ROOT + '/1c/upload/')


		try:
			xml_file = open(file_puth, 'rb').read()
		except:
			raise CommandError('Cannot open file /1c/Menu.xml')


		doc = xmltodict.parse(xml_file)

		for category in doc['XML']['category']:
			new_category, created = Category.objects.get_or_create(
				id=category['id'],
				name=category['name']
			)
			if category['myPlace'] and int(category['myPlace']):
				new_category.parent=Category.objects.get(id=category['myPlace'])
			new_category.save(sort=False)

		defaults = {'description': ''}

		for product in doc['XML']['item']:
			new_product, created = Product.objects.get_or_create(sync_id=product['id'], defaults=defaults)
			if product['status'] == 'yes':
				new_product.public = True
			else:
				new_product.public = False

			new_product.guid = product['guid']

			if created:
				new_product.name = product['nameInMenu']

				if int(product['myCategory']):
					new_product.category=Category.objects.get(id=product['myCategory'])

			# For all
			if product['price']:
				price = product['price']
			else:
				price = '0'
			new_product.retail_price = price
			new_product.wholesale_price = price
			new_product.retail_price_with_discount = price

			product_images = []
			for image_file in os.listdir(images_puth):
				img_re = '^0*' + product['id'] + '-(.*)\.jpg'
				compiled_img_re = re.compile(img_re)
				image_r = compiled_img_re.findall(image_file)

				if image_r:
					product_images.append({'file': image_file, 'name': image_r[0]})

			# Update images
			if product_images:
				new_product.cover = '1c/upload/' + product_images[0]['file']
				for pimg in product_images[1:]:
					new_image, created = Image.objects.get_or_create(product=new_product, name=pimg['name'])
					new_image.image = '1c/upload/' + pimg['file']
					new_image.save()


			new_product.save()
			self.stdout.write('Sync: ' + new_product.name)
