from django.shortcuts import render

def import_view(request):
	
	
	return render(request, "import_app/import_view.html", {'title' : 'Import from old database'})