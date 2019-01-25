from django.shortcuts import render, get_object_or_404
# Create your views here.
from django.db import IntegrityError
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response
from .models import Article
from .serializers import ArticleSerializer

class ArticleView(APIView):
    def get(self, request):
        articles = Article.objects.all()
        # the many param informs the serializer that it will be serializing more than a single article.
        serializer = ArticleSerializer(articles, many=True)
        return Response({"articles": serializer.data})


    def post(self, request):
        article = request.data.get('article')
        # Create an article from the above data
        serializer = ArticleSerializer(data=article)
        try:
            if serializer.is_valid(raise_exception=True):
                article_saved = serializer.save()
                return Response({"success": "Article '{}' created successfully".format(article_saved.title)})
        except IntegrityError:
            content = {'error': 'IntegrityError'}
            return Response(content, status=HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        saved_article = get_object_or_404(Article.objects.all(), pk=pk)
        data = request.data.get('article')
        serializer = ArticleSerializer(instance=saved_article, data=data, partial=True)
        try:
            if serializer.is_valid(raise_exception=True):
                article_saved = serializer.save()
            return Response({"success": "Article '{}' updated successfully".format(article_saved.title)})

        except IntegrityError:
            content = {'error': 'IntegrityError'}
            return Response(content, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        # Get object with this pk
        article = get_object_or_404(Article.objects.all(), pk=pk)
        article.delete()
        return Response({"message": "Article with id `{}` has been deleted.".format(pk)}, status=204)



@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                    status=HTTP_200_OK)
