# Rapport de reprise — projet « wsc-pricelist »

Document de passation rédigé à la fin d'une session Cowork, à destination de la session Claude Code qui reprend le projet.
Dernière mise à jour : 22 octobre 2026.

---

## 1. Objet du projet

Transformer les listes de prix de Yannick Montalent (cigares et whiskies) en une page HTML autonome, consultable et filtrable, enrichie d'images produit, d'informations d'origine et de force, et de liens directs vers les fiches de notation.

**Dépôt :** https://github.com/yannickmontalent24/wsc-pricelist
**Page publiée :** https://yannickmontalent24.github.io/wsc-pricelist/ (GitHub Pages, branche `main`, dossier racine)

---

## 2. État actuel

| Élément | État |
|---|---|
| `index.html` | Publié sur `main`, identique au fichier généré localement (81 412 octets) |
| Contenu | 132 références : 83 cigares + 49 whiskies |
| Liste cigares | « CIGARS OCTOBER 2026 » (PDF fourni par le client), stock au 13.10.2026 |
| Liste whiskies | Captures d'écran fournies en début de projet, **non mises à jour depuis** |
| GitHub Pages | Activation à confirmer par le client au moment de la rédaction |

---

## 3. Structure du dépôt

```
index.html            page autonome générée (ne pas éditer à la main)
src/template.html     gabarit : CSS, structure, JavaScript (filtres, vues, rendu)
src/data_cig.py       liste cigares : ref | désignation | prix | PNLMAIN | SHOP | TOTAL
                      + OLD_PRICE / OLD_DESC (liste précédente, pour comparaison)
src/data_wh.py        liste whiskies : lignes complètes (image, note, pays, liens)
src/enrich.py         données par référence cigare : IMG, NOTE, TERM, COUNTRY,
                      SPEC, NEP, LINKS, ACC
src/build.py          assemble template + données → index.html
README.md             présentation, mode d'emploi, réserves
HANDOVER.md           ce document
LICENSE               fourni avec le dépôt d'origine
```

### Régénérer la page

```bash
cd src && python3 build.py     # écrit ../index.html
```

Aucune dépendance externe (Python 3 standard).

---

## 4. Modèle de données

Chaque article est un tableau JavaScript de 12 positions, produit par `build.py` :

| Index | Contenu |
|---|---|
| 0 | Référence (`12BLUERIVIERA…`, `12NICO…`, `4DIAWHI…`) |
| 1 | Désignation, reprise **telle quelle** de la source |
| 2 | Prix (nombre) |
| 3 | URL de l'image (chaîne vide = pas d'image) |
| 4 | Note affichée au survol de la pastille « i » |
| 5 | Nom développé du produit (sert aux recherches et aux titres de liens) |
| 6 | Pays d'origine (`—` pour les accessoires) |
| 7 | Lien Neptune Cigar : `[url, "item"\|"line"]` ou `null` |
| 8 | Specs : `[force, cape, sous-cape, tripe, fabricant, source]` ou `null` |
| 9 | Liens de notation : `[[site, url, exact(1\|0)], …]` ou `null` |
| 10 | Stock : `[PNLMAIN, SHOP, TOTAL]` ou `null` (whiskies) |
| 11 | Booléen « accessoire » |

Codes sites (index 9) : `CA` Cigar Aficionado, `HW` halfwheel, `WB` Whiskybase, `DI` Distiller.
Un lien avec `exact = 0` s'affiche en pointillés suivi de « ≈ » : il pointe vers une autre vitole ou un autre format de la même gamme.

---

## 5. Fonctionnalités de la page

- **Deux vues** : grille (par défaut, image 220 px) et tableau. Le choix est mémorisé via `localStorage` (clé `pricelistView`).
- **Filtres par section** : recherche texte (référence + désignation), menu déroulant Pays, case « Sans image uniquement », case « En stock uniquement » (cigares seulement).
- **Tri** : par en-tête de colonne en vue tableau, par menu déroulant en vue grille (les deux restent synchronisés). Critères : description, prix, stock, référence.
- **Par article** : image, pays, barre de force colorée (5 niveaux : Mild → Full), cape / sous-cape / tripe / fabricant, prix, stock (TOTAL avec détail PNLMAIN+SHOP au survol), liens de notation et lien Neptune Cigar.
- **Badges** : `NOUVEAU` (références apparues en octobre 2026), `ACCESSOIRE`.
- **En-tête** : liens globaux vers Cigar Aficionado, halfwheel, Whiskybase, Whisky Advocate, Distiller, Wine Spectator, Wine Enthusiast, Vivino.
- **Pied de page** : journal de la mise à jour et liste complète des réserves.

---

## 6. Provenance des données

| Donnée | Source | Méthode |
|---|---|---|
| Références, désignations, prix, stocks | Documents du client (captures puis PDF) | Transcription manuelle, aucune valeur inventée |
| Images cigares | atlanticcigar.com, cigarterminal.com, cigar.com, cigarworld.de, tabacos.cz | URL extraite de la fiche produit, appelée en lien externe |
| Images whiskies | thewhiskyexchange.com, masterofmalt.com, thewhiskyworld.com, nicolas.com, manila-wine.com | idem |
| Pays d'origine | Fiches produit (ligne « Country of Origin ») + Distiller | **Au niveau de la gamme** : une vitole vérifiée, valeur appliquée à toute la gamme |
| Force et composition | Atlantic Cigar principalement ; Cigar Country (Fifty-Five), Cigar Smoker Club (Blend 15), CigarTerminal (cubains) | idem, au niveau de la gamme |
| Liens de notation | Résultats de recherche web restreints par domaine | **Aucune URL construite ou devinée** : seules des URL apparues telles quelles dans les résultats |

### Règle appliquée tout au long du projet

Aucune donnée inventée. Toute absence est signalée dans la page (`IMAGE MANQUANTE`, « pas de fiche trouvée », `[DONNÉE MANQUANTE : …]`) plutôt que comblée par une approximation silencieuse. Toute substitution (autre vitole, autre format, autre cape) est signalée par la pastille « i » ou par le suffixe « ≈ ».

---

## 7. Reste à faire

### 7.1 Images manquantes — 14 cigares

- **Nouvelles références d'octobre 2026 non identifiées avec certitude :** `62` (AJF Cigars Sampler Toro), `66` (AJF Premium Sampler), `121` (New World Sampler), `84` (Quorum Shade Tres Petit — vitole absente de la gamme Quorum Shade chez Atlantic Cigar).
- **Vitoles non référencées chez les marchands consultés :** `71` (B.House Connec Short Torp), `94` (Diamond Crown JC 95 Perf), `112` (R.Patel Number 6 Corona).
- **Accessoires, non recherchés :** `28`, `32`, `35`, `37`, `39`, `40`, `41`.

### 7.2 Liens de notation manquants — 35 cigares

`05`, `28`, `32`, `35`, `37`, `39`, `40`, `41`, `50`, `57`, `58`, `59`, `60`, `61`, `62`, `63`, `64`, `65`, `66`, `67`, `76`, `79`, `80`, `81`, `82`, `84`, `85`, `90`, `94`, `102`, `103`, `104`, `105`, `116`, `121`

Dont deux cas distincts :

- **Jamais cherchés** (quota de recherches web épuisé en fin de session) : `57`, `59`, `60`, `61`, `63`, `64`, `65`, plus toutes les nouvelles références d'octobre 2026.
- **Cherchés sans résultat** : la gamme Quorum Shade (`79` à `85`) n'a ni fiche Cigar Aficionado ni review halfwheel ; idem pour `90`, `94`, `102`, `104`, `105`, `116`.

### 7.3 Liens Neptune Cigar manquants — 28 cigares

Les 8 cubains (Neptune ne vend pas de havanes) et les nouvelles références d'octobre 2026, plus `63`, `64`, `65` (Blend 15, absent de Neptune).

### 7.4 Whiskies

- `4DIAWHICOF20` et `4DIAWHICOF21` (coffrets twin pack) : pas d'image trouvée.
- 6 whiskies sans lien Distiller : `12NICO0811`, `12NICO1175`, `12NICO1323`, `4DIAWHI0002`, `4DIAWHI0009`, `4DIAWHI0062`.
- Aucun lien Whisky Advocate par article (structure de recherche du site non confirmée) ; le site reste en lien global d'en-tête.
- Liste whiskies jamais mise à jour depuis les captures initiales.

### 7.5 Demandes évoquées, non réalisées

- **Spécifications Neptune Cigar** (longueur, diamètre, forme, couleur de cape, UPC) : le client les souhaitait à l'origine. Les fiches Neptune reviennent systématiquement tronquées avant le bloc « Specifications » lors d'une récupération web classique. Le client a accepté qu'on prenne les données Atlantic Cigar à la place. Piste restante : lire les pages via le navigateur du client (extension Chrome ou navigateur intégré).
- **Longueur et diamètre** des cigares : non repris, quelle que soit la source.

---

## 8. Contraintes rencontrées

1. **Fiches Neptune Cigar illisibles.** Les pages produit reviennent tronquées avant le bloc « Specifications ». Une seule page est passée (Brick House Corona Larga). Les URL Neptune utilisées dans la page proviennent de résultats de recherche, pas d'une lecture de page.
2. **Quota de recherches web.** La session plafonne à 200 recherches ; le plafond a été atteint deux fois, ce qui explique les lacunes du § 7.2. Les sous-agents partagent ce même quota.
3. **Sites bloquant la lecture.** Cigar Aficionado, halfwheel, Whiskybase et Whisky Advocate refusent la récupération automatique (robots.txt ou erreur HTTP) : les liens n'ont pas pu être ouverts pour vérification.
4. **Images non vérifiables depuis l'environnement d'exécution.** Le proxy sortant bloque les CDN des marchands ; les images ne s'affichent jamais dans les captures de contrôle. Elles se chargent normalement chez le client.
5. **Push GitHub refusé.** Le proxy git de la session n'autorise que les dépôts déclarés à son démarrage. Le client a poussé lui-même depuis sa machine (Windows / PowerShell — attention, `&&` n'y est pas accepté).
6. **Environnement réinitialisé en cours de projet.** Le fichier HTML a été perdu une fois et reconstruit depuis l'historique de conversation. D'où la mise en place de `src/` : **toute évolution doit passer par les fichiers de données et le gabarit**, jamais par une retouche directe de `index.html`.

---

## 9. Préférences du client à respecter

Règles explicitement posées par Yannick Montalent :

1. **Sourçage et factualité absolue.** Aucune invention, estimation ni extrapolation de chiffre, prix ou donnée. Donnée manquante → marqueur `[DONNÉE MANQUANTE : description]`, jamais une valeur devinée. Sur une tâche longue, ne pas interrompre l'ensemble pour un seul manque : poser le marqueur à l'endroit concerné et récapituler tous les manques en fin de réponse.
2. **Vérification préalable.** Lecture intégrale des instructions et documents avant toute production. Point bloquant ambigu → poser la question avant de commencer. Ambiguïté secondaire → signaler, appliquer l'hypothèse la plus littérale, ne pas bloquer. Contradiction interne dans un document → la signaler, ne pas trancher silencieusement.
3. **Exécution littérale et directe.** Aucun embellissement ni ajout non demandé. Résultat en premier, sans préambule ni formule de politesse.
4. **Interdiction d'anticipation.** Aucune initiative ni étape suivante sans accord explicite. Seule exception : le signalement des manques et ambiguïtés, qui reste obligatoire.

Le client écrit en français et attend des réponses en français.

---

## 10. Points de vigilance sur les données

- **Prix :** l'intitulé de la colonne et la devise ne figurent sur aucun document source. Marqué `[DONNÉE MANQUANTE]` dans l'en-tête de la page.
- **Doublons signalés dans les sources :**
  - `4DIAWHI0081` et `4DIAZZZ0034` portent la même désignation « HAIG CLUB CLUBMAN 70CL », au même prix.
  - `12BLUERIVIERA52` et `12BLUERIVIERA122` désignent la même vitole (San Lotano Req Conn Toro) à deux prix différents : 810,00 et 765,00.
- **Cape non précisée** pour les Enclave et les Perla del Mar : hypothèses retenues (Enclave Habano ; Perla del Mar Shade pour le Short Robusto, Corojo pour Double Toro et Corona Gorda), signalées dans la page.
- **Bellas Artes « Hybrid » :** aucune fiche dédiée trouvée ; images, pays et composition proviennent de la gamme Bellas Artes standard.
- **`12BLUERIVIERA67`** « NEW WORLD DORADO GOLD STAN/5/ » : image du New World Dorado Sampler, correspondance avec « Gold Standard » non confirmée.
- **`12BLUERIVIERA98`** (retiré depuis) utilisait une URL sur le sous-domaine `origin.cigaraficionado.com`, seule forme apparue dans les résultats.

---

## 11. Historique des modifications de la liste cigares

Passage de la liste initiale (78 références, captures d'écran) à « CIGARS OCTOBER 2026 » (83 références) :

- **Aucun changement de prix** entre les deux listes.
- **12 références retirées :** `43`, `44` (Enclave Toro et Figurado), `55` (Dias de Gloria Gordo), `70` (B.House Dbl Conne Mighty), `83`, `86` (Quorum Shade Churchill et Double Gordo), `95` à `98` (El Baton, 4 vitoles), `115` (R.Patel Grand Res Rob), `118` (R.Patel Disciple Toro).
- **17 références ajoutées :** 10 cigares (`05`, `50`, `58`, `62`, `66`, `67`, `76`, `84`, `103`, `121`) et 7 accessoires (`28`, `32`, `35`, `37`, `39`, `40`, `41`).
- **Ajout des colonnes de stock** PNLMAIN / SHOP / TOTAL, du tri par stock et du filtre « En stock uniquement ».

Les anciens prix et désignations retirées restent dans `src/data_cig.py` (`OLD_PRICE`, `OLD_DESC`) pour permettre la comparaison lors de la prochaine mise à jour.

---

## 12. Procédure recommandée pour la prochaine mise à jour de liste

1. Transcrire la nouvelle liste dans `src/data_cig.py` (bloc `NEW`), en conservant les désignations telles quelles.
2. Déplacer les prix de la liste précédente dans `OLD_PRICE` et les désignations retirées dans `OLD_DESC`.
3. Lancer `python3 src/build.py`, puis comparer : références retirées, références ajoutées, prix modifiés.
4. Pour chaque nouvelle référence : chercher image, pays, force et composition **au niveau de la gamme**, puis les liens de notation. Ne rien inventer ; marquer les manques.
5. Mettre à jour le bloc « Mise à jour cigares » du pied de page dans `src/template.html`.
6. Vérifier le rendu (nombre de fiches, filtres, tri) avant de pousser.
