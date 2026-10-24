# wsc-pricelist

Pricelist cigares, whiskies, vins et spiritueux — petit site statique, une page par catégorie, avec un panier qui prépare le message de commande.

**Site en ligne :** https://yannickmontalent24.github.io/wsc-pricelist/
(à activer une fois : *Settings → Pages → Source : Deploy from a branch → main / root*)

## Pages

| Page | Contenu |
|---|---|
| `index.html` | Cigares (liste « CIGARS OCTOBER 2026 », stock au 13.10.2026) |
| `whiskies.html` | Whiskies (liste précédente, prix du catalogue festif 2026/2027 pour les références qui y figurent) |
| `vins.html` | Vins — filtre Blanc / Rosé / Rouge, liens Vivino |
| `bulles.html` | Champagnes et autres bulles — filtre Prosecco / Vin effervescent / Champagne / Apéritif, liens Vivino |
| `gins.html`, `sans-alcool.html`, `rhums.html`, `liqueurs.html` | Catalogue festif 2026/2027 |

Toutes les pages partagent la barre de navigation et le **panier** (bouton en haut à droite). Le panier est conservé dans le navigateur ; il produit le message « Je voudrais passer la commande suivante: » avec quantité, type (Cigare / bouteille) et désignation, modifiable puis copiable.

## Sources

| Fichier | Rôle |
|---|---|
| `src/template.html` | Gabarit commun : mise en forme, navigation, filtres, vues tableau/grille, panier |
| `src/data_cig.py` | Liste cigares (référence, désignation, prix, stocks PNLMAIN/SHOP/TOTAL) |
| `src/data_wh.py` | Liste whiskies (référence, désignation, prix, image, pays, liens) |
| `src/enrich.py` | Données cigares par référence : images, pays, force, composition, longueur, liens Neptune et de notation |
| `src/data_cat.py` | Catalogue « Le Bottle Shop — Sélection festive 2026 / 2027 » : transcription, cadres d'images, rapprochements whiskies |
| `src/vivino.py` | Liens Vivino des vins et bulles du catalogue |
| `src/crop_catalogue.py` | Outil ponctuel (PyMuPDF) : découpe les bouteilles du PDF du catalogue vers `img/cat/` |
| `img/cat/` | Images des bouteilles découpées dans le catalogue |
| `src/build.py` | Assemble le gabarit et les données pour produire les pages |

## Régénérer le site

```bash
cd src && python3 build.py
```

Le script écrit les huit pages HTML à la racine du dépôt.
