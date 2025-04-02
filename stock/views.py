from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from .models import Stock, Fournisseur, Commande, DétailCommande, Livraison
from .serializers import (
    StockSerializer, FournisseurSerializer, CommandeSerializer, DétailCommandeSerializer, LivraisonSerializer
)

class ListeStock(generics.ListAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer

class DetailStock(generics.RetrieveAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer

class ListeFournisseurs(generics.ListAPIView):
    queryset = Fournisseur.objects.all()
    serializer_class = FournisseurSerializer

class ListeCommandes(generics.ListAPIView):
    queryset = Commande.objects.all()
    serializer_class = CommandeSerializer

class CreerCommande(APIView):
    def post(self, request, fournisseur_id, format=None):
        try:
            fournisseur = Fournisseur.objects.get(id=fournisseur_id)
            commande = Commande.objects.create(fournisseur=fournisseur)
            return Response({'message': f'Commande {commande.id} créée pour {fournisseur.nom}.'})
        except Fournisseur.DoesNotExist:
            return Response({'error': 'Fournisseur introuvable.'}, status=404)

class AjouterProduitCommande(APIView):
    def post(self, request, commande_id, stock_id, quantite, format=None):
        try:
            commande = Commande.objects.get(id=commande_id)
            stock = Stock.objects.get(id=stock_id)

            if stock.quantite < quantite:
                return Response({'error': 'Stock insuffisant.'}, status=400)

            DétailCommande.objects.create(commande=commande, stock=stock, quantite=quantite)
            return Response({'message': f'{quantite} x {stock.nom} ajouté à la commande {commande.id}.'})
        except (Commande.DoesNotExist, Stock.DoesNotExist):
            return Response({'error': 'Commande ou produit introuvable.'}, status=404)

class MarquerCommandeLivree(APIView):
    def post(self, request, commande_id, format=None):
        try:
            commande = Commande.objects.get(id=commande_id)

            if commande.statut == 'expediee':
                livraison, created = Livraison.objects.get_or_create(commande=commande)
                livraison.date_livraison = timezone.now()
                livraison.statut = 'livree'
                livraison.save()

                # Mise à jour des stocks
                for detail in commande.details.all():
                    detail.stock.quantite += detail.quantite
                    detail.stock.save()

                return Response({'message': f'Commande {commande.id} livrée et stock mis à jour.'})
            
            return Response({'error': 'Commande non expédiée ou déjà livrée.'}, status=400)
        except Commande.DoesNotExist:
            return Response({'error': 'Commande introuvable.'}, status=404)
