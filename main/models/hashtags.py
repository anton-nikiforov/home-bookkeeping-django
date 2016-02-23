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