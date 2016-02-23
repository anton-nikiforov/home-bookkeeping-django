from django.db import models

class Category(models.Model):
	
	class Meta(object):
		verbose_name="Category"
		verbose_name_plural="Categories"
		
	OPERATION_CHOICES = (
		('+', 'Plus'),
		('-', 'Minus')
	)

	title = models.CharField(max_length=100, blank=False, verbose_name="Title")
	operation = models.CharField(max_length=1, choices=OPERATION_CHOICES, blank=False, verbose_name="Operation")	
		
	def __unicode__(self):
		return self.title