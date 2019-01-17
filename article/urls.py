from django.conf.urls import url
from .views import ArticleView, login
urlpatterns = [
    url(r'articles/$', ArticleView.as_view()),
    url(r'login/$', login),
    ]