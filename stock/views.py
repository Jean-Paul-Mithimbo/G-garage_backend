from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from .models import Stock, Fournisseur, Article
from .serializers import (
    StockSerializer, FournisseurSerializer, ArticleSerializer
)

class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

class FournisseurViewSet(viewsets.ModelViewSet):
    queryset = Fournisseur.objects.all()
    serializer_class = FournisseurSerializer

class ListeStock(generics.ListAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer

class DetailStock(generics.RetrieveAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer

class ListeFournisseurs(generics.ListAPIView):
    queryset = Fournisseur.objects.all()
    serializer_class = FournisseurSerializer
