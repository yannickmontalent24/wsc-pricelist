# wsc-pricelist

Pricelist cigares &amp; whiskies — page HTML autonome, consultable en tableau ou en grille.

**Page en ligne :** https://yannickmontalent24.github.io/wsc-pricelist/
(à activer une fois : *Settings → Pages → Source : Deploy from a branch → main / root*)

## Contenu

| Fichier | Rôle |
|---|---|
| `index.html` | La pricelist complète (page autonome, aucune dépendance à installer) |
| `src/template.html` | Gabarit de la page : mise en forme, filtres, vues tableau/grille |
| `src/data_cig.py` | Liste cigares (référence, désignation, prix, stocks PNLMAIN/SHOP/TOTAL) |
| `src/data_wh.py` | Liste whiskies (référence, désignation, prix, image, pays, liens) |
| `src/enrich.py` | Données par référence : images, pays, force, composition, liens Neptune et liens de notation |
| `src/data_cat.py` | Catalogue « Le Bottle Shop — Sélection festive 2026 / 2027 » : vins, bulles, gins, sans alcool, rhums, liqueurs, whiskies (transcription, cadres d'images, rapprochements whiskies) |
| `src/crop_catalogue.py` | Outil ponctuel (PyMuPDF) : découpe les bouteilles du PDF du catalogue vers `img/cat/` |
| `img/cat/` | Images des bouteilles découpées dans le catalogue |
| `src/build.py` | Assemble le gabarit et les données pour produire `index.html` |

## Régénérer la page

```bash
cd src && python3 build.py
```

Le script écrit `index.html` à la racine du dépôt.

## Ce que contient la page

- **132 références** : 83 cigares (liste « CIGARS OCTOBER 2026 », stock au 13.10.2026) et 49 whiskies.
- **Deux vues** : grille (par défaut, grande image) et tableau. Le choix est mémorisé par le navigateur.
- **Filtres** : recherche texte, pays, « sans image uniquement », « en stock uniquement » (cigares), tri par description, prix, stock ou référence.
- **Par article** : image, pays d'origine, force (barre colorée), cape / sous-cape / tripe / fabricant, prix, stock, liens directs vers les fiches de notation et vers Neptune Cigar.

## Réserves

- **Prix** : l'intitulé de la colonne et la devise ne figurent pas sur les documents source.
- **Images** : appelées en lien externe depuis les sites marchands ; une connexion internet est nécessaire et les liens peuvent être retirés par ces sites.
- **Pays, force, composition** : relevés au niveau de la gamme (une vitole vérifiée par gamme), pas par vitole ; longueur et diamètre non repris.
- **Liens de notation** : un lien suivi de « ≈ » pointe vers la fiche la plus proche (autre vitole de la même gamme). Les nouvelles références d'octobre 2026 n'ont pas encore de liens.
- Le détail complet des manques figure en bas de la page.
