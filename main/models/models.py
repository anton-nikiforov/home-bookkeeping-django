from django.db.models.query import QuerySet
from django.db.models import Manager
from django.db.models.sql.datastructures import EmptyResultSet
from django.core.cache import cache
from django.utils.encoding import smart_str

from funcy import walk

from main.helpers import md5, stamp_fields

class CustomCacheManager(Manager):
	
	def get_queryset(self):
		return CustomQuerySet(model=self.model, using=self._db, hints=self._hints)

class CustomQuerySet(QuerySet):

	def count(self):
		cache_key = self._cache_key()
		data_count = cache.get(cache_key)
		if data_count is None:
			data_count = super(CustomQuerySet, self).count()
			cache.set(cache_key, data_count)
		return data_count

	def iterator(self):
		cache_key = self._cache_key()
		data = cache.get(cache_key)	
		if data is not None:
			return iter(data)

		def iterate():
			self._result_cache = []
			for obj in super(CustomQuerySet, self).iterator():
				self._result_cache.append(obj)
				yield obj
			cache.set(cache_key, self._result_cache)

		return iterate()	

	''' Uses iterator to fetch data
	def get(self, *args, **kwargs):
		if not args \
				and not self.query.select_related \
				and not self.query.where.children:
			cache_key = (self.__class__, self.model) + tuple(sorted(kwargs.items()))
			data = cache.get(cache_key)
			if data is None:
				data = super(CustomQuerySet, self).get(*args, **kwargs)
				cache.set(cache_key, data)
		else:
			return super(CustomQuerySet, self).get(*args, **kwargs)

		return data
	'''
	
	def _cache_key(self):
		"""
		Compute a cache key for this queryset
		"""
		md = md5()
		md.update('%s.%s' % (self.__class__.__module__, self.__class__.__name__))
		# Vary cache key for proxy models
		md.update('%s.%s' % (self.model.__module__, self.model.__name__))
		# Protect from field list changes in model
		md.update(stamp_fields(self.model))
		# Use query SQL as part of a key
		try:
			sql, params = self.query.get_compiler(self.db).as_sql()
			try:
				sql_str = sql % params
			except UnicodeDecodeError:
				sql_str = sql % walk(force_text, params)
			md.update(smart_str(sql_str))
		except EmptyResultSet:
			pass
		# Thing only appeared in Django 1.9
		it_class = getattr(self, '_iterable_class', None)
		if it_class:
			md.update('%s.%s' % (it_class.__module__, it_class.__name__))
		# 'flat' attribute changes results formatting for values_list() in Django 1.8 and earlier
		if hasattr(self, 'flat'):
			md.update(str(self.flat))

		return 'q:%s' % md.hexdigest()
