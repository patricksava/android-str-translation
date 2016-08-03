from django.conf.urls import url

from . import views

urlpatterns = [

    url(r'^index/$', views.index, name='index'),
    url(r'^write/$', views.write, name='write'),
    url(r'^make/$', views.make, name='make'),

]