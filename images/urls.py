from django.conf.urls import url
from . import images
urlpatterns = [
    url(r'^all/', images.Images.as_view(), name='images'),
    # url(r'^<id>$', images.Selected.as_view(), name='selected'),
    url(r'^(?P<user_id>[0-9]+)/$',images.Selected.as_view(), name='selected'),
    url(r'^$(?P<user_date>\d{4}-\d{2}-\d{2})/$',images.Selected.as_view(), name='list'),
    # url('2/',images.Selected.as_view(), name='selected'),
]