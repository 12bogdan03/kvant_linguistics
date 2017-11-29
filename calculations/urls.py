from django.conf.urls import url

from . import views

app_name = 'calculations'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
]
