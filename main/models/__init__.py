from .hashtags import Hashtags
from .category import Category
from .elements import Elements
from .currency import Currency

from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Elements, dispatch_uid="remove_cache_elements")
@receiver(post_save, sender=Hashtags, dispatch_uid="remove_cache_hashtags")
def remove_cache(sender, instance, **kwargs):
	cache.delete_pattern('%s:q:*' % sender.__name__)