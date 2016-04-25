from django.db import models
from .models import CustomCacheManager

class Currency(models.Model):
	
	class Meta(object):
		verbose_name="Currencies"
		verbose_name_plural="Currencies"
		
	objects = CustomCacheManager()

	title = models.CharField(max_length=100, blank=False, verbose_name="Title")
	symbol = models.CharField(max_length=3, blank=False, verbose_name="Symbol")
	
	sale = models.DecimalField(max_digits=5, decimal_places=2, blank=False)	
	buy = models.DecimalField(max_digits=5, decimal_places=2, blank=False)	
		
	base = models.BooleanField(verbose_name='Base', blank=True, default=False)		
		
	def __unicode__(self):
		return self.symbol