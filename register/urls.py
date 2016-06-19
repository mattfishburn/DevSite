from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.Index, name='index'),
    url(r'^new/$', views.NewEmail, name='index'),
    url(r'^new/submit$', views.NewEmailRequestDone, name='index'),
    url(r'^new/confirm/(?P<code>[a-zA-Z0-9\-]+)$', views.ConfirmEmail, name='index'),
]
