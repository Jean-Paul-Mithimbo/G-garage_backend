from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from .models import Stock, Fournisseur, Commande, DétailCommande, Livraison, Retour

def liste_stock(request):
    stocks = Stock.objects.all()
    return render(request, 'stock/liste_stock.html', {'stocks': stocks})

def detail_stock(request, stock_id):
    stock = get_object_or_404(Stock, id=stock_id)
    return render(request, 'stock/detail_stock.html', {'stock': stock})

def liste_fournisseurs(request):
    fournisseurs = Fournisseur.objects.all()
    return render(request, 'fournisseurs/liste_fournisseurs.html', {'fournisseurs': fournisseurs})

def creer_commande(request, fournisseur_id):
    fournisseur = get_object_or_404(Fournisseur, id=fournisseur_id)
    commande = Commande.objects.create(fournisseur=fournisseur)
    return JsonResponse({'message': f'Commande {commande.id} créée pour {fournisseur.nom}.'})

def ajouter_produit_commande(request, commande_id, stock_id, quantite):
    commande = get_object_or_404(Commande, id=commande_id)
    stock = get_object_or_404(Stock, id=stock_id)
    
    if stock.quantite < quantite:
        return JsonResponse({'error': 'Stock insuffisant.'})

    DétailCommande.objects.create(commande=commande, stock=stock, quantite=quantite)
    return JsonResponse({'message': f'{quantite} x {stock.nom} ajouté à la commande {commande.id}.'})

def marquer_commande_livree(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id)
    
    if commande.statut == 'expediee':
        livraison, created = Livraison.objects.get_or_create(commande=commande)
        livraison.date_livraison = timezone.now()
        livraison.statut = 'livree'
        livraison.save()
        
        # Mise à jour des stocks
        for detail in commande.details.all():
            detail.stock.quantite += detail

