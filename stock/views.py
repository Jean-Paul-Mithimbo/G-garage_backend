from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db import transaction
from django.db.models import F
from django.utils import timezone

from .models import (
    Fournisseurs,
    Article, Stock,
    Entree, LigneEntree,
    Sortie, LigneSortie
)
from .serializers import (
    ArticleSerializer, StockSerializer,
    EntreeSerializer, SortieSerializer,FournisseurSerializer
)

class FournisseursViewSet(viewsets.ModelViewSet):
    """
    CRUD Article.
    À la création d’un article, on crée aussi son stock initial à 0.
    """
    queryset = Fournisseursobjects.all()
    serializer_class = FournisseursSerializer

class ArticleViewSet(viewsets.ModelViewSet):
    """
    CRUD Article.
    À la création d’un article, on crée aussi son stock initial à 0.
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def perform_create(self, serializer):
        article = serializer.save()
        # Création automatique du Stock lié à l'article
        Stock.objects.create(article=article, quantite=0)


class StockViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Lecture seule de l’état du stock.
    """
    queryset = Stock.objects.select_related('article')
    serializer_class = StockSerializer


# class EntreeViewSet(viewsets.ModelViewSet):
#     """
#     CRUD Entrée (Entree + LigneEntree) :
#     - create: crée l'entrée et ses lignes, puis augmente le stock.
#     - update: annule l’ancienne entrée, puis applique la nouvelle.
#     - destroy: retire les quantités de l'entrée puis supprime l’entrée.
#     """
#     queryset = Entree.objects.prefetch_related('lignes')
#     serializer_class = EntreeSerializer

#     def create(self, request, *args, **kwargs):
#         """
#         POST /api/entrees/
#         """
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         with transaction.atomic():
#             # 1. Création de l'Entree
#             fournisseur = serializer.validated_data.get('fournisseur', '')
#             nouvelle_entree = Entree.objects.create(fournisseur=fournisseur)

#             # 2. Pour chaque ligne d'entrée, on crée la ligne et on met à jour le stock
#             for ligne_data in serializer.validated_data['lignes']:
#                 article_obj = ligne_data['article']
#                 quantite_entree = ligne_data['quantite']
#                 prix_unitaire = ligne_data['prix_unitaire']
#                 date_exp = ligne_data['date_expiration']

#                 # On enregistre la ligne d'entrée
#                 LigneEntree.objects.create(
#                     entree=nouvelle_entree,
#                     article=article_obj,
#                     quantite=quantite_entree,
#                     prix_unitaire=prix_unitaire,
#                     date_expiration=date_exp
#                 )

#                 # On augmente le stock
#                 Stock.objects.filter(article=article_obj).update(
#                     quantite=F('quantite') + quantite_entree
#                 )

#         return Response(EntreeSerializer(nouvelle_entree).data,
#                         status=status.HTTP_201_CREATED)

#     def update(self, request, *args, **kwargs):
#         """
#         PUT /api/entrees/{id}/
#         """
#         entree_instance = self.get_object()
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         with transaction.atomic():
#             # 1. Rollback des anciennes lignes : on retire leur quantité du stock
#             for ancienne_ligne in entree_instance.lignes.all():
#                 Stock.objects.filter(article=ancienne_ligne.article).update(
#                     quantite=F('quantite') - ancienne_ligne.quantite
#                 )
#             # on supprime ces anciennes lignes
#             entree_instance.lignes.all().delete()

#             # 2. Mise à jour du fournisseur
#             entree_instance.fournisseur = serializer.validated_data.get('fournisseur', '')
#             entree_instance.save(update_fields=['fournisseur'])

#             # 3. Création des nouvelles lignes et mise à jour du stock
#             for ligne_data in serializer.validated_data['lignes']:
#                 article_obj = ligne_data['article']
#                 quantite_entree = ligne_data['quantite']
#                 prix_unitaire = ligne_data['prix_unitaire']
#                 date_exp = ligne_data['date_expiration']

#                 LigneEntree.objects.create(
#                     entree=entree_instance,
#                     article=article_obj,
#                     quantite=quantite_entree,
#                     prix_unitaire=prix_unitaire,
#                     date_expiration=date_exp
#                 )
#                 Stock.objects.filter(article=article_obj).update(
#                     quantite=F('quantite') + quantite_entree
#                 )

#         return Response(EntreeSerializer(entree_instance).data,
#                         status=status.HTTP_200_OK)

#     def destroy(self, request, *args, **kwargs):
#         """
#         DELETE /api/entrees/{id}/
#         """
#         entree_instance = self.get_object()
#         with transaction.atomic():
#             # Rollback : on retire chaque quantité d'entrée du stock
#             for ligne in entree_instance.lignes.all():
#                 Stock.objects.filter(article=ligne.article).update(
#                     quantite=F('quantite') - ligne.quantite
#                 )
#             # Suppression de l'entrée
#             entree_instance.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


class EntreeViewSet(viewsets.ModelViewSet):
    """
    CRUD pour Entree + LigneEntree, avec mise à jour du Stock.
    - create: création de l'Entree (libele, date_op) + lignes, puis augmentation du stock.
    - update: annulation des anciennes lignes, mise à jour de date_op/libele, création des nouvelles lignes + ajustement du stock.
    - destroy: retrait des quantités de chaque ligne puis suppression de l'Entree.
    """
    queryset         = Entree.objects.prefetch_related('lignes')
    serializer_class = EntreeSerializer

    def create(self, request, *args, **kwargs):
        """
        POST /api/entrees/
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            # 1. Création de l'Entree avec libele et date_op
            titre_entree = serializer.validated_data.get('libele', '')
            date_operation = serializer.validated_data['date_op']
            nouvelle_entree = Entree.objects.create(
                libele = titre_entree,
                date_op = date_operation
            )

            # 2. Création des lignes et mise à jour du Stock
            for ligne_data in serializer.validated_data['lignes']:
                article_obj     = ligne_data['article']
                qte_entree      = ligne_data['quantite']
                prix_unitaire   = ligne_data['prix_unitaire']
                date_expiration = ligne_data['date_expiration']

                # on crée la ligne d'entrée
                LigneEntree.objects.create(
                    entree          = nouvelle_entree,
                    article         = article_obj,
                    quantite        = qte_entree,
                    prix_unitaire   = prix_unitaire,
                    date_expiration = date_expiration
                )

                # on augmente le stock lié à l'article
                Stock.objects.filter(article=article_obj).update(
                    quantite = F('quantite') + qte_entree
                )

        return Response(EntreeSerializer(nouvelle_entree).data,
                        status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """
        PUT /api/entrees/{id}/
        """
        entree_instance = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            # 1. Rollback des anciennes lignes : on retire leurs quantités du stock
            for ancienne_ligne in entree_instance.lignes.all():
                Stock.objects.filter(article=ancienne_ligne.article).update(
                    quantite = F('quantite') - ancienne_ligne.quantite
                )
            # suppression des anciennes lignes
            entree_instance.lignes.all().delete()

            # 2. Mise à jour de libele et date_op
            entree_instance.libele   = serializer.validated_data.get('libele', '')
            entree_instance.date_op  = serializer.validated_data['date_op']
            entree_instance.save(update_fields=['libele', 'date_op'])

            # 3. Re-création des nouvelles lignes + mise à jour du stock
            for ligne_data in serializer.validated_data['lignes']:
                article_obj     = ligne_data['article']
                qte_entree      = ligne_data['quantite']
                prix_unitaire   = ligne_data['prix_unitaire']
                date_expiration = ligne_data['date_expiration']

                LigneEntree.objects.create(
                    entree          = entree_instance,
                    article         = article_obj,
                    quantite        = qte_entree,
                    prix_unitaire   = prix_unitaire,
                    date_expiration = date_expiration
                )
                Stock.objects.filter(article=article_obj).update(
                    quantite = F('quantite') + qte_entree
                )

        return Response(EntreeSerializer(entree_instance).data,
                        status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        """
        DELETE /api/entrees/{id}/
        """
        entree_instance = self.get_object()
        with transaction.atomic():
            # rollback : on retire chaque ligne du stock
            for ligne in entree_instance.lignes.all():
                Stock.objects.filter(article=ligne.article).update(
                    quantite = F('quantite') - ligne.quantite
                )
            # suppression de l'Entree et de ses lignes en cascade
            entree_instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SortieViewSet(viewsets.ModelViewSet):
    """
    CRUD Sortie (Sortie + LigneSortie) :
    - create: prélève en FIFO (expiration > date_entree), diminue le stock.
    - update: annule l’ancienne sortie (remet en stock), puis applique la nouvelle.
    - destroy: remet les quantités en stock puis supprime la sortie.
    """
    queryset = Sortie.objects.prefetch_related('lignes')
    serializer_class = SortieSerializer

    def create(self, request, *args, **kwargs):
        """
        POST /api/sorties/
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            motif_sortie = serializer.validated_data.get('motif', '')
            nouvelle_sortie = Sortie.objects.create(motif=motif_sortie)

            for ligne_data in serializer.validated_data['lignes']:
                article_obj = ligne_data['article']
                quantite_demandee = ligne_data['quantite']

                # 1. Sélection des lots FIFO (non périmés)
                lots_fifo = (
                    LigneEntree.objects
                    .filter(
                        article=article_obj,
                        quantite__gt=0,
                        date_expiration__gte=timezone.now().date()
                    )
                    .order_by('date_expiration', 'date_entree')
                )

                quantite_restante = quantite_demandee
                # 2. Prélèvement dans chaque lot
                for lot in lots_fifo:
                    if quantite_restante == 0:
                        break
                    prise = min(lot.quantite, quantite_restante)
                    # Décrémente le lot
                    lot.quantite = F('quantite') - prise
                    lot.save(update_fields=['quantite'])
                    quantite_restante -= prise

                if quantite_restante > 0:
                    raise ValueError(
                        f"Stock insuffisant pour {article_obj.nom} "
                        f"(manque {quantite_restante})."
                    )

                # 3. Création de la ligne de sortie et mise à jour du stock
                LigneSortie.objects.create(
                    sortie=nouvelle_sortie,
                    article=article_obj,
                    quantite=quantite_demandee
                )
                Stock.objects.filter(article=article_obj).update(
                    quantite=F('quantite') - quantite_demandee
                )

        return Response(SortieSerializer(nouvelle_sortie).data,
                        status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """
        PUT /api/sorties/{id}/
        """
        sortie_instance = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            # 1. Rollback de l’ancienne sortie : remise en stock
            for ancienne_ligne in sortie_instance.lignes.all():
                Stock.objects.filter(article=ancienne_ligne.article).update(
                    quantite=F('quantite') + ancienne_ligne.quantite
                )
            sortie_instance.lignes.all().delete()

            # 2. Mise à jour du motif
            sortie_instance.motif = serializer.validated_data.get('motif', '')
            sortie_instance.save(update_fields=['motif'])

            # 3. Application de la nouvelle sortie (même algorithme que create)
            for ligne_data in serializer.validated_data['lignes']:
                article_obj = ligne_data['article']
                quantite_demandee = ligne_data['quantite']

                lots_fifo = (
                    LigneEntree.objects
                    .filter(
                        article=article_obj,
                        quantite__gt=0,
                        date_expiration__gte=timezone.now().date()
                    )
                    .order_by('date_expiration', 'date_entree')
                )

                quantite_restante = quantite_demandee
                for lot in lots_fifo:
                    if quantite_restante == 0:
                        break
                    prise = min(lot.quantite, quantite_restante)
                    lot.quantite = F('quantite') - prise
                    lot.save(update_fields=['quantite'])
                    quantite_restante -= prise

                if quantite_restante > 0:
                    raise ValueError(
                        f"Stock insuffisant pour {article_obj.nom} "
                        f"(manque {quantite_restante})."
                    )

                LigneSortie.objects.create(
                    sortie=sortie_instance,
                    article=article_obj,
                    quantite=quantite_demandee
                )
                Stock.objects.filter(article=article_obj).update(
                    quantite=F('quantite') - quantite_demandee
                )

        return Response(SortieSerializer(sortie_instance).data,
                        status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        """
        DELETE /api/sorties/{id}/
        """
        sortie_instance = self.get_object()
        with transaction.atomic():
            # Remise en stock de chaque ligne
            for ligne in sortie_instance.lignes.all():
                Stock.objects.filter(article=ligne.article).update(
                    quantite=F('quantite') + ligne.quantite
                )
            # Suppression de la sortie
            sortie_instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
