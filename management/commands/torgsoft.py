import os
import unicodecsv

from django.conf import settings

from django.core.management.base import BaseCommand
from django.core.management.base import CommandError

from ...models import Brand
from ...models import Product
from ...models import Category


class Command(BaseCommand):
	help = 'Synchronize catalog with TorgSoft'

	def handle(self, *args, **options):
		file_puth = os.path.abspath(settings.MEDIA_ROOT + '/export/TSGoods.trs')

		try:
			csv_file = open(file_puth, 'rb').read().decode('cp1251').encode('utf8')[:-1]
		except:
			raise CommandError('Cannot open file export/TSGoods.trs')

		try:
			product_string = unicodecsv.reader(csv_file.split('\n'), delimiter=';', quotechar='"')
		except:
			raise CommandError('Cannot parse export/TSGoods.trs, make sure that the file format is correct')

		next(product_string)
		for row in product_string:
			defaults = {'description': ''}
			product, created = Product.objects.get_or_create(sync_id=row[0], defaults=defaults)
			if created:
				product.name=row[1]
				product.description=row[2]
				product.articul=row[4]

				product.height=row[9]
				product.width=row[10]

				product.warehouse_quantity=row[12]

				product.public=row[13]
				product.size=row[14]
				product.color=row[15]
				product.material=row[16]

				product.sex=row[18]
				product.season=row[22]
				product.barcode=row[23]
				product.age=row[28]

				# Update images
				image_puth = '%s/export/%s.jpg' % (settings.MEDIA_ROOT, row[0])
				image_cover = 'export/%s.jpg' % (row[0])
				if os.path.isfile(image_puth):
					product.cover = image_cover

			# # For all
			product.retail_price=row[5]
			product.wholesale_price=row[6]
			product.retail_price_with_discount=row[7]
			product.min_quantity_for_order=row[8]

			# Update category
			category = None
			for category_name in row[20].split(','):
				category, created = Category.objects.get_or_create(name=category_name, parent=category)
				category.save(sort=False)
			product.category = category

			# Update brand
			brand = row[21].split(',')[-1]
			brand, created = Brand.objects.get_or_create(name=brand)
			brand.save()
			product.brand = brand

			product.save()
			self.stdout.write('Sync: ' + product.name)
