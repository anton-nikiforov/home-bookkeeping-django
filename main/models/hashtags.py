from django.db import models

class Hashtags(models.Model):
	
	class Meta(object):
		verbose_name="Hashtag"
		verbose_name_plural="Hashtags"
		
	title = models.CharField(
		max_length=100,
		blank=False,
		verbose_name="Title")
		
	def __unicode__(self):
		return self.title

	@classmethod
	def get_list(self, limit=None):
		data = []
		hashtags = self.objects.annotate(
			count=models.Count('elements__id')).order_by('-count')

		if limit is not None:
			hashtags = hashtags[:limit]

		for hashtag in hashtags:
			data.append((
				hashtag.id,
				u'{} ({})'.format(hashtag.title, hashtag.count)
			))
		return data