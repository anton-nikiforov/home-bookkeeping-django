from django.db.models import (
	Model, CharField, Count, Sum
)
from django.core.cache import cache

from .models import CustomCacheManager

class Hashtags(Model):
	
	class Meta(object):
		verbose_name="Hashtag"
		verbose_name_plural="Hashtags"
		
	objects = CustomCacheManager()

	title = CharField(max_length=100, blank=False, verbose_name="Title")
		
	def __unicode__(self):
		return self.title

	@classmethod
	def get_list(self, limit=None):
		key = 'hashtags_get_list_{}'.format(limit)
		data = cache.get(key)
		if data is None:
			data = []
			try:
				hashtags = self.objects.annotate(count=Count('elements__id')) \
								.order_by('-count')
				if limit is not None:
					hashtags = hashtags[:limit]
				for hashtag in hashtags:
					data.append((
						hashtag.id,
						u'{} ({})'.format(hashtag.title, hashtag.count)))
				cache.set(key, data)
			except:
				pass
		return data

	@classmethod
	def get_summary_by_hashtags(self, limit=None):
		key = 'get_summary_by_hashtags_{}'.format(limit)
		summary = cache.get(key)		
		if summary is None:
			try:
				summary = Hashtags.objects.all() \
					.values('title', 'elements__currency__symbol') \
					.annotate(count=Count('elements__id')) \
					.annotate(sum=Sum('elements__total')) \
					.order_by('-count')
				if limit is not None:
					summary = summary[:limit]					
				cache.set(key, summary)
			except:
				pass
		return summary	