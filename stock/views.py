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







def fiche_stock_article_pdf(request, article_id):
    """
    Génère un PDF « FICHE DE STOCK » avec :
      - 2 lignes d’en-tête (Entrées/Sorties/Stock)
      - colonnes à largeur variable selon contenu
      - texte qui se wrappe automatiquement
      - tableau centré et marge standard A4
    """

    # Charger l’article ou 404
    article = get_object_or_404(Article, pk=article_id)

    #  Préparer buffer et document (A4 avec marges de 15mm)
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=10*mm,
        rightMargin=10*mm,
        topMargin=20*mm,
        bottomMargin=20*mm,
    )

    #  Récupérer les styles et définir un style wrap-capable
    styles      = getSampleStyleSheet()
    normal      = styles['Normal']
    normal.wordWrap = 'CJK'  # active le retour à la ligne automatique
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading2'],
        alignment=1,
        fontSize=14,
        spaceAfter=4*mm
    )

    elements = []

    #  En-tête du document centré
    elements.append(Paragraph("UNIVERSITÉ ADVENTISTE DE LUKANGA", styles['Title']))
    elements.append(Paragraph("B.P 180 BUTEMBO", styles['Title']))
    elements.append(Spacer(1, 3*mm))
    elements.append(Paragraph("<b>FICHE DE STOCK</b>", title_style))
    elements.append(Spacer(1, 2*mm))

    #  Infos article
    info_data = [
        ["Nom de l’Article :", article.nom, "N° :", str(article.pk)],
        ["Code :", getattr(article, 'code', '—'), "Unité :", getattr(article, 'unite', 'pcs')]
    ]
    info_table = Table(info_data, colWidths=[None, None, None, None])
    info_table.setStyle(TableStyle([
        ('VALIGN',       (0,0), (-1,-1), 'MIDDLE'),
        ('FONTNAME',     (0,0), (-1,-1), 'Helvetica'),
        ('FONTSIZE',     (0,0), (-1,-1), 10),
        ('BOTTOMPADDING',(0,0), (-1,-1), 4),
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 5*mm))

    # 6️⃣ Charger et fusionner mouvements
    entrees = LigneEntree.objects.filter(article=article).values(
        'date_entree','quantite','prix_unitaire','entree__libele'
    )
    sorties = LigneSortie.objects.filter(article=article).values(
        'date_sortie','quantite','sortie__motif'
    )

    mouvements = []
    for e in entrees:
        mouvements.append({
            'datetime': e['date_entree'],
            'designation': e['entree__libele'] or "Entrée",
            'q_in': e['quantite'],
            'pu_in': float(e['prix_unitaire']),
            'q_out': 0
        })
    for s in sorties:
        mouvements.append({
            'datetime': s['date_sortie'],
            'designation': s['sortie__motif'] or "Sortie",
            'q_in': 0,
            'pu_in': 0.0,
            'q_out': s['quantite']
        })
    # Tri précis : date+heure, puis entrées avant sorties si même timestamp
    mouvements.sort(key=lambda m: (m['datetime'], 0 if m['q_in']>0 else 1))

    #  Préparer les deux lignes d’en-tête
    header1 = [
        "Date", "Désignation",
        "Entrées", "", "",
        "Sorties", "",
        "Stock", "", "",
        "Observations"
    ]
    header2 = [
        "",  "",
        "Qté", "PU", "PT",
        "Qté", "PT",
        "Qté", "PU", "PT",
        ""
    ]
    table_data = [
        [Paragraph(h, normal) for h in header1],
        [Paragraph(h, normal) for h in header2]
    ]

    #  Construire les lignes de données avec FIFO
    fifo_layers = []
    stock_qty    = 0
    stock_val    = 0

    for mv in mouvements:
        date_str = mv['datetime'].strftime('%d/%m/%Y %H:%M')
        desig    = Paragraph(mv['designation'], normal)
        q_in     = mv['q_in']
        pu_in    = mv['pu_in']
        pt_in    = q_in * pu_in
        q_out    = mv['q_out']
        pt_out   = 0.0
        detail   = ""

        if q_in:
            # empile le lot
            fifo_layers.append([q_in, pu_in])
            stock_qty += q_in
            stock_val += pt_in
        else:
            # prélève selon FIFO
            reste = q_out
            parts = []
            for layer in fifo_layers:
                if reste==0: break
                take = min(layer[0], reste)
                pt_out += take * layer[1]
                parts.append(f"{take}@{layer[1]:.2f}")
                layer[0] -= take; reste -= take
            fifo_layers = [l for l in fifo_layers if l[0]>0]
            stock_qty -= q_out
            stock_val -= pt_out
            detail = ", ".join(parts)

        # crée la ligne de tableau, wrap possible sur chaque
        row = [
            Paragraph(date_str, normal),
            desig,
            Paragraph(str(q_in) if q_in else "", normal),
            Paragraph(f"{pu_in:.2f}" if q_in else "", normal),
            Paragraph(f"{pt_in:.2f}" if q_in else "", normal),
            Paragraph(str(q_out) if q_out else "", normal),
            Paragraph(f"{pt_out:.2f}" if q_out else "", normal),
            Paragraph(str(stock_qty), normal),
            Paragraph(f"{(stock_val/stock_qty):.2f}" if stock_qty else "", normal),
            Paragraph(f"{stock_val:.2f}", normal),
            Paragraph(detail, normal),
        ]
        table_data.append(row)

    #  Ligne de solde final
    final_row = [
        "", Paragraph("<b>SOLDE FINAL</b>", normal),
        "", "", "",
        "", "",
        Paragraph(f"<b>{stock_qty}</b>", normal),
        Paragraph("", normal),
        Paragraph(f"<b>{stock_val:.2f}</b>", normal),
        ""
    ]
    table_data.append(final_row)

    #  Construire et styler le tableau
    table = Table(
        table_data,
        repeatRows=2,      # fige les header1 et header2
        hAlign='CENTER'    # centre sur la page
        # colWidths absents → auto-adaptation
    )
    table.setStyle(TableStyle([
        # fusion en-tête 1
        ('SPAN', (2,0), (4,0)),  # Entrées
        ('SPAN', (5,0), (6,0)),  # Sorties
        ('SPAN', (7,0), (9,0)),  # Stock
        # style en-têtes
        ('BACKGROUND', (0,0), (-1,1), colors.lightgrey),
        ('FONTNAME',   (0,0), (-1,1), 'Helvetica-Bold'),
        ('ALIGN',      (0,0), (-1,1), 'CENTER'),
        # grille
        ('GRID',       (0,0), (-1,-1), 0.5, colors.grey),
        ('VALIGN',     (0,0), (-1,-1), 'MIDDLE'),
        # align chiffres à droite
        ('ALIGN',      (2,2), (-1,-1), 'RIGHT'),
        # alternance de fonds
        ('ROWBACKGROUNDS', (2,2), (-1,-1), [colors.whitesmoke, None]),
        # padding sur en-tête
        ('TOPPADDING',    (0,0), (-1,1), 6),
        ('BOTTOMPADDING', (0,0), (-1,1), 6),
    ]))

    elements.append(table)
    elements.append(Spacer(1,4*mm))
    elements.append(Paragraph("© UNIVERSITÉ ADVENTISTE DE LUKANGA", normal))

    #  Générer et retourner le PDF
    doc.build(elements)
    buffer.seek(0)
    return HttpResponse(
        buffer,
        content_type='application/pdf',
        headers={'Content-Disposition': f'inline; filename="FICHE_DE_STOCK_{article.pk}.pdf"'}
    )