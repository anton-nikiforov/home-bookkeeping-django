from datetime import datetime    
from django.db import models
from django.conf import settings
from django.core.cache import cache

from .category import Category
from .currency import Currency
from .hashtags import Hashtags
from .models import CustomCacheManager

class ElementsCustomCacheManager(CustomCacheManager):

	def get_queryset(self):
		return super(ElementsCustomCacheManager, self).get_queryset() \
					.select_related('currency', 'category') \
					.prefetch_related('hashtags')

class Elements(models.Model):

	class Meta(object):
		verbose_name="Element"
		verbose_name_plural="Elements"
				
	objects = ElementsCustomCacheManager()

	category = models.ForeignKey(Category, on_delete=models.CASCADE,
				**{'default': settings.DEFAULT_CATEGORY_ID})

	currency = models.ForeignKey(Currency, on_delete=models.CASCADE,
				**{'default': settings.DEFAULT_CURRENCY_ID})

	total = models.DecimalField(max_digits=8, decimal_places=2, blank=False)
	created = models.DateField(default=datetime.now, blank=False)
	hashtags = models.ManyToManyField(Hashtags)

	def __unicode__(self):
		return ' '.join([self.created.strftime('%d.%m.%Y'), \
			str(self.total), str(self.currency)])