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
		try:
			data = []
			hashtags = self.objects.all() \
						.annotate(count=Count('elements__id')) \
						.order_by('-count')
			if limit is not None:
				hashtags = hashtags[:limit]
			for hashtag in hashtags:
				data.append((
					hashtag.id,
					u'{} ({})'.format(hashtag.title, hashtag.count)))
		except:
			data = []
		return data