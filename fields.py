from django.db.models.fields.files import ImageField
from django.db.models.fields.files import ImageFieldFile
from PIL import Image
import os


def _add_thumb(s):
	parts = s.split('.')
	parts.insert(-1, 'thumb')
	if parts[-1].lower() not in ['jpeg', 'jpg', 'png', 'gif']:
		parts[-1] = 'jpg'
	return '.'.join(parts)


def _thumb_by_size(url, width, height):
	parts = url.split('.')
	parts.insert(-1, '%sx%s' % (width, height))
	if parts[-1].lower() not in ['jpeg', 'jpg', 'png', 'gif']:
		parts[-1] = 'jpg'
	return '.'.join(parts)


class ThumbImageFieldFile(ImageFieldFile):
	def _get_thumb_path(self):
		return _add_thumb(self.path)
	thumb_path = property(_get_thumb_path)

	def _get_thumb_url(self):
		return _add_thumb(self.url)
	thumb_url = property(_get_thumb_url)

	def thumb(self, width, height):
		thumb_path = _thumb_by_size(self.path, width, height)
		if not os.path.exists(thumb_path):
			img = Image.open(self.path)
			png_info = img.info
			img.thumbnail((width, height), Image.ANTIALIAS)
			img.save(thumb_path, 'PNG', **png_info)
		thumb_url = _thumb_by_size(self.url, width, height)
		return thumb_url

	def save(self, name, content, save=True):
		super(ThumbImageFieldFile, self).save(name, content, save)
		img = Image.open(self.path)
		png_info = img.info

		img.thumbnail(
			(self.field.w, self.field.h),
			Image.ANTIALIAS
		)
		img.save(self.thumb_path, 'PNG', **png_info)

	def delete(self, save=True):
		if os.path.exists(self.thumb_path):
			os.remove(self.thumb_path)
		super(ThumbImageFieldFile, self).delete(save)


class ThumbImageField(ImageField):
	attr_class = ThumbImageFieldFile

	def __init__(self, w=100, h=100, *args, **kwargs):
		self.w = w
		self.h = h
		super(ThumbImageField, self).__init__(*args, **kwargs)
