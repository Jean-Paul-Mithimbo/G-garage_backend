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
    EntreeSerializer, SortieSerializer,FournisseursSerializer
)

# repport lab

import io
from datetime import datetime
from django.shortcuts        import get_object_or_404
from django.http             import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.lib           import colors
from reportlab.lib.units     import mm
from reportlab.platypus      import (
    SimpleDocTemplate, Paragraph,
    Spacer, Table, TableStyle
)
from reportlab.lib.styles    import getSampleStyleSheet, ParagraphStyle
from django.utils.timezone   import localtime


class FournisseursViewSet(viewsets.ModelViewSet):
    """
    CRUD Article.
    À la création d’un article, on crée aussi son stock initial à 0.
    """
    queryset = Fournisseurs.objects.all()
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




# # fiche de stock
# def fiche_stock_article_pdf(request, article_id):
#     """
#     Génère un PDF « FICHE DE STOCK » identique au modèle envoyé,
#     avec en-tête Université, N°, Nom, Code, Unité, et tableau complet FIFO.
#     """
#     # 1️⃣ Charger l’article
#     article = get_object_or_404(Article, pk=article_id)

#     # 2️⃣ Préparer le buffer et le document
#     buffer   = io.BytesIO()
#     document = SimpleDocTemplate(
#         buffer,
#         pagesize=A4,
#         leftMargin=15*mm, rightMargin=15*mm,
#         topMargin=20*mm, bottomMargin=20*mm,
#     )

#     # 3️⃣ Styles
#     styles      = getSampleStyleSheet()
#     title_style = ParagraphStyle(
#         'Title', parent=styles['Heading2'],
#         alignment=1, fontSize=14, spaceAfter=4*mm
#     )
#     normal      = styles['Normal']

#     elements = []

#     # 4️⃣ En-tête fixe
#     elements.append(Paragraph("UNIVERSITÉ ADVENTISTE DE LUKANGA", normal))
#     elements.append(Paragraph("B.P 180 BUTEMBO", normal))
#     elements.append(Spacer(1, 3*mm))
#     elements.append(Paragraph("<b>FICHE DE STOCK</b>", title_style))
#     elements.append(Spacer(1, 2*mm))

#     # Zone d’identification
#     #    Nom de l’Article, Code, Unité, N°
#     #    (on suppose que Article a les attributs code et unite)
#     header_data = [
#         ["Nom de l’Article :", article.nom, "N° :", str(article.pk)],
#         ["Code :", getattr(article, 'code', '—'), "Unité :", getattr(article, 'unite', 'pcs')],
#     ]
#     header_table = Table(header_data, colWidths=[30*mm, 70*mm, 15*mm, 30*mm])
#     header_table.setStyle(TableStyle([
#         ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
#         ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
#         ('FONTSIZE', (0,0), (-1,-1), 10),
#         ('BOTTOMPADDING', (0,0), (-1,-1), 4),
#     ]))
#     elements.append(header_table)
#     elements.append(Spacer(1, 4*mm))

#     # 6️⃣ Préparer le tableau des mouvements
#     columns = [
#         "Date", "Désignation",
#         "Entrées Qté", "Entrées PU", "Entrées PT",
#         "Sorties Qté","Sorties PU","Sorties PT",
#         "Stocks Qté","Stocks PU","Stocks PT",
#         "Observations"
#     ]
#     table_data = [columns]

#     # Charger et fusionner mouvements
#     ents = LigneEntree.objects.filter(article=article).values(
#         'date_entree','quantite','prix_unitaire','entree__libele'
#     )
#     sors = LigneSortie.objects.filter(article=article).values(
#         'date_sortie','quantite','sortie__motif'
#     )
#     mouvements = []
#     for e in ents:
#         mouvements.append({
#             'date'         : e['date_entree'].date(),
#             'designation'  : e['entree__libele'] or "Entrée",
#             'q_in'         : e['quantite'],
#             'pu_in'        : float(e['prix_unitaire']),
#             'q_out'        : 0,
#             'obs'          : ""
#         })
#     for s in sors:
#         mouvements.append({
#             'date'         : s['date_sortie'].date(),
#             'designation'  : s['sortie__motif'] or "Sortie",
#             'q_in'         : 0,
#             'pu_in'        : 0,
#             'q_out'        : s['quantite'],
#             'obs'          : ""
#         })
#     mouvements.sort(key=lambda m: m['date'])

#     # FIFO et calculs
#     fifo_layers = []   # [ [qty, pu], ... ]
#     stock_qty    = 0
#     stock_val    = 0

#     for mv in mouvements:
#         # renseigner variables ligne
#         date_str = mv['date'].strftime('%d/%m/%Y')
#         desig    = mv['designation']
#         q_in     = mv['q_in']
#         pu_in    = mv['pu_in']
#         pt_in    = q_in * pu_in if q_in else 0

#         q_out     = mv['q_out']
#         # détail FIFO pour sorties
#         pt_out = 0
#         pu_out = 0
#         detail  = ""
#         if q_in:
#             # entrée : on empile
#             fifo_layers.append([q_in, pu_in])
#             stock_qty += q_in
#             stock_val += pt_in
#         else:
#             # sortie : on prélève en FIFO
#             reste = q_out
#             parts = []
#             for layer in fifo_layers:
#                 if reste == 0:
#                     break
#                 take = min(layer[0], reste)
#                 pt_out += take * layer[1]
#                 parts.append(f"{take}@{layer[1]:.2f}")
#                 layer[0] -= take
#                 reste -= take
#             fifo_layers = [l for l in fifo_layers if l[0]>0]
#             stock_qty -= q_out
#             stock_val -= pt_out
#             pu_out = 0  # on n’affiche pas un PU unique
#             detail = " + ".join(parts)

#         # remplir la ligne du tableau
#         row = [
#             date_str,
#             desig[:20],                   # tronquer si trop long
#             str(q_in) if q_in else "",    # Entrées Qté
#             f"{pu_in:.2f}" if q_in else "",
#             f"{pt_in:.2f}" if q_in else "",
#             str(q_out) if q_out else "",
#             "" if q_out==0 else "FIFO",
#             f"{pt_out:.2f}" if q_out else "",
#             str(stock_qty),
#             f"{(stock_val/stock_qty):.2f}" if stock_qty else "",
#             f"{stock_val:.2f}",
#             detail
#         ]
#         table_data.append(row)

#     # ajouter la ligne de solde mensuel (optionnel)
#     table_data.append([
#         "", "SOLDE MENSUEL",
#         "", "", "",
#         "", "", "",
#         str(stock_qty), "", f"{stock_val:.2f}", ""
#     ])

#     # 7️⃣ Style et insertion du tableau
#     col_widths = [20*mm, 30*mm] + [15*mm]*8 + [40*mm]
#     table = Table(table_data, colWidths=col_widths, repeatRows=1)
#     table.setStyle(TableStyle([
#         ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
#         ('GRID',       (0,0), (-1,-1), 0.5, colors.grey),
#         ('VALIGN',     (0,0), (-1,-1), 'MIDDLE'),
#         ('ALIGN',      (2,1), (-3,-1), 'RIGHT'),
#         ('FONTNAME',   (0,0), (-1,0), 'Helvetica-Bold'),
#     ]))
#     elements.append(table)

#     # 8️⃣ Pied de page
#     elements.append(Spacer(1,4*mm))
#     elements.append(Paragraph("© UNIVERSITÉ ADVENTISTE DE LUKANGA", normal))

#     # 9️⃣ Générer le PDF
#     document.build(elements)
#     buffer.seek(0)
#     return HttpResponse(
#         buffer,
#         content_type='application/pdf',
#         headers={
#             # 'Content-Disposition':
#             # f'attachment; filename="FICHE_DE_STOCK_{article.nom}.pdf"'
#             'Content-Disposition': f'inline; filename="fiche_stock_article_{article_id}.pdf"'

#         }
#     )




def fiche_stock_article_pdf(request, article_id):
    """
    Génère un PDF « FICHE DE STOCK » reprenant exactement
    le design reçu, avec logique FIFO.
    """
    # Récupérer l’article (ou 404)
    article = get_object_or_404(Article, pk=article_id)

    # Préparation du buffer et du document
    buffer   = io.BytesIO()
    doc      = SimpleDocTemplate(
        buffer, pagesize=A4,
        leftMargin=15*mm, rightMargin=15*mm,
        topMargin=20*mm, bottomMargin=20*mm
    )

    # Styles
    styles      = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'Title', parent=styles['Heading2'],
        alignment=1, fontSize=14, spaceAfter=4*mm
    )
    normal      = styles['Normal']

    elements = []

    # En-tête fixe
    elements.append(Paragraph("UNIVERSITÉ ADVENTISTE DE LUKANGA", normal))
    elements.append(Paragraph("B.P 180 BUTEMBO", normal))
    elements.append(Spacer(1, 3*mm))
    elements.append(Paragraph("<b>FICHE DE STOCK</b>", title_style))
    elements.append(Spacer(1, 2*mm))

    # Zone d’identification
    header_data = [
        ["Nom de l’Article :", article.nom, "N° :", str(article.pk)],
        ["Code :", getattr(article, 'code', '—'), "Unité :", getattr(article, 'unite', 'pcs')],
    ]
    header_table = Table(header_data, colWidths=[30*mm, 65*mm, 15*mm, 30*mm])
    header_table.setStyle(TableStyle([
        ('VALIGN',      (0,0), (-1,-1), 'MIDDLE'),
        ('FONTNAME',    (0,0), (-1,-1), 'Helvetica'),
        ('FONTSIZE',    (0,0), (-1,-1), 10),
        ('BOTTOMPADDING',(0,0),(-1,-1),4),
    ]))
    elements.append(header_table)
    elements.append(Spacer(1, 4*mm))

    # Charger mouvements
    entrees = LigneEntree.objects.filter(article=article).values(
        'date_entree','quantite','prix_unitaire','entree__libele'
    )
    sorties = LigneSortie.objects.filter(article=article).values(
        'date_sortie','quantite','sortie__motif'
    )
    mouvements = []
    for e in entrees:
        mouvements.append({
            'date':         e['date_entree'].date(),
            'designation':  e['entree__libele'] or "Entrée",
            'q_in':         e['quantite'],
            'pu_in':        float(e['prix_unitaire']),
            'q_out':        0,
        })
    for s in sorties:
        mouvements.append({
            'date':         s['date_sortie'].date(),
            'designation':  s['sortie__motif'] or "Sortie",
            'q_in':         0,
            'pu_in':        0.0,
            'q_out':        s['quantite'],
        })
    mouvements.sort(key=lambda m: m['date'])

    # Préparer données de tableau
    fifo_layers = []
    stock_qty    = 0
    stock_val    = 0

    table_data = [[
        "Date", "Désignation",
        "Entrées Qté","Entrées PU","Entrées PT",
        "Sorties Qté","Sorties PT",
        "Stock Qté","Stock PU","Stock PT",
        "Observations"
    ]]

    for mv in mouvements:
        date_str = mv['date'].strftime('%d/%m/%Y')
        desig    = mv['designation'][:20]
        q_in     = mv['q_in']
        pu_in    = mv['pu_in']
        pt_in    = q_in * pu_in
        q_out    = mv['q_out']
        detail   = ""
        pt_out   = 0.0

        if q_in:
            # Entrée
            fifo_layers.append([q_in, pu_in])
            stock_qty += q_in
            stock_val += pt_in
            row = [
                date_str, desig,
                str(q_in), f"{pu_in:.2f}", f"{pt_in:.2f}",
                "", "", str(stock_qty),
                f"{(stock_val/stock_qty):.2f}", f"{stock_val:.2f}", ""
            ]
        else:
            # Sortie FIFO
            reste = q_out
            parts = []
            for layer in fifo_layers:
                if reste == 0: break
                take = min(layer[0], reste)
                pt_out += take * layer[1]
                parts.append(f"{take}@{layer[1]:.2f}")
                layer[0] -= take
                reste -= take
            fifo_layers = [l for l in fifo_layers if l[0] > 0]
            stock_qty -= q_out
            stock_val -= pt_out
            detail = " + ".join(parts)
            row = [
                date_str, desig,
                "", "", "",
                str(q_out), f"{pt_out:.2f}",
                str(stock_qty), f"{(stock_val/stock_qty if stock_qty else 0):.2f}",
                f"{stock_val:.2f}", detail
            ]

        table_data.append(row)

    # Ligne de SOLDE
    table_data.append([
        "", "SOLDE FINAL",
        "", "", "",
        "", "",
        str(stock_qty), "", f"{stock_val:.2f}", ""
    ])

    # Colonnes calibrées à la largeur A4 utile (~180mm)
    col_widths = [
        20*mm,  35*mm,
         15*mm, 15*mm, 15*mm,
         15*mm, 15*mm,
         15*mm, 15*mm, 15*mm,
         40*mm
    ]

    # Construction du tableau, aligné à gauche
    table = Table(table_data, colWidths=col_widths, repeatRows=1, hAlign='LEFT')
    table.setStyle(TableStyle([
        ('BACKGROUND',     (0,0), (-1,0),   colors.lightgrey),
        ('FONTNAME',       (0,0), (-1,0),   'Helvetica-Bold'),
        ('ALIGN',          (2,1), (-1,-1),  'RIGHT'),
        ('VALIGN',         (0,0), (-1,-1),  'MIDDLE'),
        ('GRID',           (0,0), (-1,-1),  0.5, colors.grey),
        ('ROWBACKGROUNDS', (0,1), (-1,-1),  [colors.whitesmoke, None]),
        ('BOTTOMPADDING',  (0,0), (-1,0),   6),
        ('TOPPADDING',     (0,0), (-1,0),   6),
    ]))
    elements.append(table)

    # Pied de page
    elements.append(Spacer(1, 4*mm))
    elements.append(Paragraph("© UNIVERSITÉ ADVENTISTE DE LUKANGA", normal))

    # Génération du PDF
    doc.build(elements)
    buffer.seek(0)
    return HttpResponse(
        buffer,
        content_type='application/pdf',
        headers={'Content-Disposition': f'inline; filename="FICHE_DE_STOCK_{article.pk}.pdf"'}
    )