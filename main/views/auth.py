from django.contrib.auth import (
    REDIRECT_FIELD_NAME, get_user_model, views
)
from django.contrib.auth.forms import (
    AuthenticationForm,
)

from meta.views import Meta

def login(request, template_name='registration/login.html',
          redirect_field_name=REDIRECT_FIELD_NAME,
          authentication_form=AuthenticationForm,
          extra_context=None):
    """
    Displays the login form and handles the login action.
    """
    return views.login(request, template_name, redirect_field_name,
    	authentication_form, extra_context={'meta': Meta(**{
		'title': 'Sign in'})})