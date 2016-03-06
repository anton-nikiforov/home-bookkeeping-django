from django.shortcuts import render
from django.conf import settings

from import_app.models import Elements as ElementsImport
from import_app.models import Categories as CategoriesImport
from import_app.models import Hashtags as HashtagsImport
from import_app.models import ElementsHashtags as ElementsHashtagsImport

from main.models.elements import Elements
from main.models.category import Category
from main.models.hashtags import Hashtags
from main.models.currency import Currency

def import_view(request):

	message = ''

	if request.POST.get('action') == 'import/category':
		categories = CategoriesImport.objects.using('import_db').all()

		if categories:
			for category in categories:
				category_new = Category(id=category.id, title=category.title)
				category_new.save()

		message = 'Categories were imported.'

	elif request.POST.get('action') == 'import/hashtags':
		hashtags = HashtagsImport.objects.using('import_db').all()

		if hashtags:
			for hashtag in hashtags:
				hashtag_new = Hashtags(id=hashtag.id, title=hashtag.title)
				hashtag_new.save()

		message = 'Hashtags were imported.'

	elif request.POST.get('action') == 'import/elements':
		elements = ElementsImport.objects.using('import_db').all()
		currency = Currency.objects.get(id=settings.DEFAULT_CURRENCY_ID)

		if elements:
			for element in elements:
				category_instance = Category.objects.get(id=element.categoryid)

				element_new = Elements(id=element.id, category=category_instance, created=element.created, 
					total=element.sum, currency=currency)
				element_new.save()

		message = 'Elements were imported.'

	elif request.POST.get('action') == 'import/elements_hashtags':
		elements = Elements.objects.all()

		for element in elements:
			elements_hashtags = ElementsHashtagsImport.objects.using('import_db').filter(elements_id=element.id)

			if elements_hashtags:
				for element_hashtags in elements_hashtags:
					hashtag = Hashtags.objects.get(id=element_hashtags.hashtags_id)
					if hashtag:
						element.hashtags.add(hashtag)

		message = 'Connections between elements and hashtags were imported.'
			

	return render(request, "import_app/import_view.html", {'title' : 'Import from old database', 'message' : message})