import urllib
import urllib2
import json

from django.core.management.base import BaseCommand
from django.core.management.base import CommandError

from django.utils.text import slugify

from django.conf import settings

from ...models import Category
from ...models import Brand


def urlencode(string):
	string = urllib.unquote(string)
	string = u'' + urllib.quote(string.encode('utf-8'))
	return string


class Command(BaseCommand):
	help = 'Create slug for categories and brands. Resort categories and create absolute url for them.'

	def handle(self, *args, **options):
		for category in Category.objects.all():
			# Update categories without slug, resort all
			if not category.slug:
				urlencode_name = urlencode(category.name)
				url = 'https://translate.yandex.net/api/v1.5/tr.json/translate?key=%s&lang=ru-en&text=%s' % (settings.YANDEX_TRANSLATE_KEY, urlencode_name)
				try:
					req = urllib2.Request(url)
					response = urllib2.urlopen(req)
					to_slug = json.loads(response.read())['text'][0]
				except:
					raise CommandError('Cannot get translate')
				category.slug = slugify(to_slug)
			category.save()
			self.stdout.write('Category updated: ' + category.name)

		self.stdout.write('')
		self.stdout.write('Slugs and URLs for categories created and resort complite!')

		for brand in Brand.objects.all():
			# Update brands without slug
			if not brand.slug:
				urlencode_name = urlencode(brand.name)
				url = 'https://translate.yandex.net/api/v1.5/tr.json/translate?key=%s&lang=ru-en&text=%s' % (settings.YANDEX_TRANSLATE_KEY, urlencode_name)
				try:
					req = urllib2.Request(url)
					response = urllib2.urlopen(req)
					to_slug = json.loads(response.read())['text'][0]
				except:
					raise CommandError('Cannot get translate')

				brand.slug = slugify(to_slug)
				brand.save()
				self.stdout.write('Brand updated: ' + brand.name)

		self.stdout.write('')
		self.stdout.write('Slugs brands created!')
		self.stdout.write('Update complite!')
