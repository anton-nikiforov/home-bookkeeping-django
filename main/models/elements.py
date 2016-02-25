from datetime import datetime    
from django.db import models

from category import Category
from hashtags import Hashtags

# TODO: add field default to Category model
DEFAULT_CATEGORY_ID = 3;

class Elements(models.Model):

	class Meta(object):
		verbose_name="Element"
		verbose_name_plural="Elements"
				
	category = models.ForeignKey(Category, on_delete=models.CASCADE, **{'default': DEFAULT_CATEGORY_ID})
	total = models.DecimalField(max_digits=8, decimal_places=2, blank=False)
	created = models.DateTimeField(default=datetime.now, blank=True)
	hashtags = models.ManyToManyField(Hashtags)

	def __unicode__(self):
		return self.created + ' ' + self.total