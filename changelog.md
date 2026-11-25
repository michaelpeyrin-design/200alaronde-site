# Historique des modifications

## v5.1.7 — 25 novembre 2026

- Les copains : uniquement les catégories Magasin et Artisan.
- Sous-titre : « les rencontres de 200àlaronde ».
- Onglet Applications : bleu clair et texte foncé, sur ordinateur et mobile.

## v5.1.6 — 25 novembre 2026

- Navigation sur une ligne avec un onglet Applications bleu foncé.
- Page Applications présentant Cols & Dodecaudax, Brevets, Bon braquet et Roadbook avec descriptions et liens.
- Les copains : cartes par ordre alphabétique, sans dates ni regroupement par année ou mois, avec le lien « En savoir plus ».
- Calendrier gravel renommé Gravel.
- Bouton d’accueil : Application Cols & Dodecaudax.

## v5.1.5 — 25 novembre 2026

- Accueil : le bouton Classement Dodecaudax devient Application Cols et challenges Dodecaudax.

- Ajout du lien Bon braquet vers lebonbraquet.200alaronde.fr dans les menus ordinateur et mobile.
- Nouvelle page Les copains, au format Archives, filtrée sur Magazine article (ou Article magazine), Magasin et Artisan, indépendamment de la sélection Archives.
- Mise en valeur des applications Bon braquet, Brevets et Dodecaudax en bleu foncé avec texte blanc, y compris dans le menu mobile et la section gravel.

## v5.1.4 — 23 novembre 2026

- Mosaïques adaptées aux photographies portrait : affichage à la hauteur naturelle sans recadrage, y compris pour les photos paysage.
- Responsive : 2 colonnes sur iPhone et petits écrans, 3 sur tablette et 4 sur ordinateur ; espacement ajusté.
- Images chargées progressivement avec décodage asynchrone et débordements limités sur mobile.
- Conservation des marqueurs de placement `[[galerie:N]]` dans le texte des articles.

## v5.1.3 — 23 novembre 2026

- Correction du placement des galeries dans les articles contenant du HTML mélangé au Markdown, notamment les blocs « Photo réglable » : les marqueurs `[[galerie:N]]` sont désormais interprétés dans les deux cas.
- Les galeries explicitement placées ne sont plus ajoutées en bas de l'article ; les anciens articles sans marqueurs restent compatibles.

## v5.1.2 — 23 novembre 2026

- Correction du doublonnage des mosaïques et carrousels en fin d'article : lorsqu'au moins un emplacement `[[galerie:N]]` est utilisé dans le contenu, seules les galeries explicitement positionnées sont affichées.
- Les anciens articles sans emplacement explicite conservent le comportement historique : galeries affichées en fin d'article.

## v5.1.1 — 23 novembre 2026

- Nouvelle rubrique « Catégories » dans l'administration : création et modification des catégories d'articles sans intervenir dans le code.
- Le champ Catégorie des articles propose désormais les catégories enregistrées, avec recherche.
- Reprise des catégories existantes, y compris les anciennes valeurs « Article » et « Groupe What's App », pour conserver la compatibilité avec les articles publiés.

## v5.1.0 — 23 novembre 2026

- Nouveau bloc « Photo réglable » dans l'éditeur d'articles : choix de largeur 600, 800, 1200, 1600 px ou 100 %, y compris pour une photo déjà enregistrée.
- Nouveau bloc « Galerie à cet endroit » : permet de placer chaque mosaïque ou carrousel n'importe où dans le contenu de l'article en utilisant son numéro.
- Compatibilité avec les articles existants : les galeries non placées explicitement restent à la fin de l'article.
- Le réglage de largeur concerne l'affichage ; seule la compression à l'envoi réduit le poids réel du fichier.

## v5.0.9 — 23 novembre 2026

- Compression automatique des nouvelles images JPEG, PNG et WebP chargées dans l'administration : largeur de 1600 px, qualité 80 %, conversion WebP et suppression des métadonnées, sans recadrage.
- Mise à jour de Decap CMS vers la version 3.18.0 pour utiliser le traitement des médias documenté.
- Correction de l'affichage des images insérées dans les articles Markdown avec un crédit photo entre guillemets après le chemin de l'image (notamment Gravel Matheysine).
- Aucun fichier d'image existant modifié : les anciennes photos doivent être optimisées et remplacées séparément si nécessaire.

## v5.0.8 — 19 octobre 2026

- Ajout du champ facultatif « Informations sur la sortie » pour chaque mois des calendriers route et gravel dans l’administration. Le texte apparaît avant le bouton Inscription ; un champ vide reste masqué.
- Affichage des 12 mois dans les deux calendriers, sans filtre fondé sur le mois courant : janvier 2027 et novembre 2026 restent visibles.
- Bouton Inscription uniquement lorsqu’un lien HTTP ou HTTPS est renseigné ; retirer le lien retire le bouton.
- Les calendriers chargent leur JSON depuis le site déployé, avec conservation du HTML généré si le chargement échoue.
- Onglets renommés « Calendrier route » et « Calendrier gravel » sur ordinateur et mobile.
- Version du site et de l’administration actualisée ; historique consultable en bas des pages.

## Versions précédentes

L’historique détaillé des versions v5.0.1 à v5.0.7 est conservé dans le [README du dépôt](https://github.com/michaelpeyrin-design/200alaronde-site/blob/main/README.md).
