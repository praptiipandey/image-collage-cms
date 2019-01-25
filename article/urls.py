from django.conf.urls import url
from django.urls import path
from .views import ArticleView, login
urlpatterns = [
    url(r'articles/$', ArticleView.as_view()),
    path('articles/<int:pk>', ArticleView.as_view()),
    url(r'login/$', login),
    ]