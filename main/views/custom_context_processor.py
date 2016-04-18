from django.conf import settings

def custom_context_processor(request):
	context = {
		'CACHE_TIMEOUT': settings.CACHE_TIMEOUT,
	}

	return context