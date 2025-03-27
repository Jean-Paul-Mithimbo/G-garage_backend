from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from rest_framework import viewsets
from .models import Client, Vehicule, Panne, EquipeReparation, Intervention, HistoriqueReparation

def liste_clients(request):
    clients = Client.objects.all()
    return render(request, 'clients/liste_clients.html', {'clients': clients})

def detail_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    return render(request, 'clients/detail_client.html', {'client': client})

def liste_vehicules(request):
    vehicules = Vehicule.objects.all()
    return render(request, 'vehicules/liste_vehicules.html', {'vehicules': vehicules})

def liste_pannes(request):
    pannes = Panne.objects.all()
    return render(request, 'pannes/liste_pannes.html', {'pannes': pannes})

def liste_equipes(request):
    equipes = EquipeReparation.objects.all()
    return render(request, 'equipes/liste_equipes.html', {'equipes': equipes})

def liste_interventions(request):
    interventions = Intervention.objects.all()
    return render(request, 'interventions/liste_interventions.html', {'interventions': interventions})

def liste_historiques(request):
    historiques = HistoriqueReparation.objects.all()
    return render(request, 'historiques/liste_historiques.html', {'historiques': historiques})

def affecter_equipe(request, intervention_id, equipe_id):
    intervention = get_object_or_404(Intervention, id=intervention_id)
    equipe = get_object_or_404(EquipeReparation, id=equipe_id)
    intervention.equipe = equipe
    intervention.save()
    return JsonResponse({'message': f'Équipe {equipe.nom} affectée à l\'intervention {intervention.id}.'})

def cloturer_intervention(request, intervention_id):
    intervention = get_object_or_404(Intervention, id=intervention_id)
    if intervention.statut == 'en_cours':
        intervention.statut = 'terminee'
        intervention.date_fin_reelle = timezone.now()
        intervention.save()
        HistoriqueReparation.objects.create(intervention=intervention, details="Intervention terminée et archivée.")
        return JsonResponse({'message': f'Intervention {intervention.id} clôturée et archivée.'})
    return JsonResponse({'error': 'Intervention déjà clôturée ou annulée.'})
