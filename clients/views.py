from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Client, Devis, Facture, Paiement, Abonnement, Fidélité

def liste_clients(request):
    clients = Client.objects.all()
    return render(request, 'clients/liste_clients.html', {'clients': clients})

def detail_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    return render(request, 'clients/detail_client.html', {'client': client})

def liste_devis(request):
    devis = Devis.objects.all()
    return render(request, 'devis/liste_devis.html', {'devis': devis})

def liste_factures(request):
    factures = Facture.objects.all()
    return render(request, 'factures/liste_factures.html', {'factures': factures})

def liste_paiements(request):
    paiements = Paiement.objects.all()
    return render(request, 'paiements/liste_paiements.html', {'paiements': paiements})

def liste_abonnements(request):
    abonnements = Abonnement.objects.all()
    return render(request, 'abonnements/liste_abonnements.html', {'abonnements': abonnements})

def liste_fidelites(request):
    fidelites = Fidélité.objects.all()
    return render(request, 'fidelites/liste_fidelites.html', {'fidelites': fidelites})

def verifier_statut_facture(request, facture_id):
    facture = get_object_or_404(Facture, id=facture_id)
    return JsonResponse({'facture_id': facture.id, 'statut': facture.statut})
