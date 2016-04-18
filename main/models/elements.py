from datetime import datetime    
from django.db import models
from django.conf import settings
from django.core.cache import cache

from . import (
	Category, Hashtags, Currency
)
from .models import CustomCacheManager

class Elements(models.Model):

	class Meta(object):
		verbose_name="Element"
		verbose_name_plural="Elements"
				
	objects = CustomCacheManager()

	category = models.ForeignKey(Category, on_delete=models.CASCADE,
				**{'default': settings.DEFAULT_CATEGORY_ID})

	currency = models.ForeignKey(Currency, on_delete=models.CASCADE,
				**{'default': settings.DEFAULT_CURRENCY_ID})

	total = models.DecimalField(max_digits=8, decimal_places=2, blank=False)
	created = models.DateField(default=datetime.now, blank=False)
	hashtags = models.ManyToManyField(Hashtags)

	def __unicode__(self):
		return ' '.join([self.created.strftime('%d.%m.%Y'), \
			str(self.total), self.currency.symbol])

	@classmethod
	def get_summary_by_category(self, queryset=None, cache_key=None):
		cache_key = cache_key if queryset is not None else None		
		key = 'get_summary_by_category_{}'.format(cache_key)
		queryset = queryset if queryset is not None else self.objects.all() 
		summary = cache.get(key)
		if summary is None:
			try:
				summary = queryset \
					.values('category__title', 'currency__symbol') \
					.annotate(sum=models.Sum('total')).order_by('sum')
				cache.set(key, summary)
			except:
				pass
		return summary