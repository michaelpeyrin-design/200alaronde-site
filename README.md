# 200 à la ronde — v5.0.5

Site de l’association : https://200alaronde.fr/  
Version du 16 octobre 2026.

## Nouveautés v5.0.5

- Remplacement de l’iframe Strava directe par le script officiel `https://strava-embeds.com/embed.js`.
- Le script crée le cadre de l’activité, ajoute ses paramètres de communication et ajuste sa hauteur.
- Réutilisation du champ `strava_url` existant, sans changer les liens saisis.
- Suppression de la hauteur CSS fixe de Strava ; Instagram reste à 2 200 px et Deezer est conservé.
- Vérification du générateur, du balisage attendu par le script officiel, du CMS, du SEO et de l’intégrité du ZIP. L’affichage distant de l’activité ne peut pas être confirmé dans cette vérification locale.

## Historique v5.0.4

- Champ facultatif **Lien de la sortie Strava** dans tous les articles, nouveaux ou existants (`strava_url`).
- Activité intégrée juste sous Deezer, avant l’image principale et le récit ; visible même si le champ Deezer est vide.
- Coller le lien complet `https://www.strava.com/activities/NUMERO`, puis enregistrer et attendre le déploiement. Les liens courts `strava.app.link` ne sont pas acceptés.
- Le profil Strava et l’activité doivent être visibles par **Tout le monde** pour être intégrés (documentation Strava consultée le 16 octobre 2026 : https://support.strava.com/fr/articles/15402053-partager-vos-activites-et-itineraires-avec-une-integration-strava).
- Utilisation du format actuel `https://strava-embeds.com/activity/NUMERO` ; champ vide = aucune intégration.
- Deezer et cadre Instagram de 2 200 px conservés ; README et versions actualisés.
- Vérification du champ CMS, des formats acceptés/refusés et du positionnement dans la génération ; construction, SEO et intégrité ZIP contrôlés. Le chargement du contenu distant dépend de Strava et de la visibilité de la sortie.

## Historique v5.0.3

- Cadre Instagram étiré à **2 200 pixels** de haut, à la demande de l’utilisateur, sur ordinateur et mobile.
- Retour à l’iframe Instagram et retrait du script qui imposait son propre redimensionnement.
- Largeur adaptée à l’écran, lecteur Deezer conservé et version affichée actualisée.
- Vérification de la hauteur dans le HTML et le CSS, génération et contrôle SEO réussis. Une publication courte peut laisser de l’espace blanc dans ce cadre volontairement haut.

## Historique v5.0.2

- Publication Instagram intégrée via le script officiel `https://www.instagram.com/embed.js`.
- Suppression du cadre à hauteur fixe de 720 px : Instagram calcule la hauteur de la publication.
- Largeur adaptée aux écrans mobiles ; lecteur Deezer conservé.
- Vérification du HTML généré et de la génération du site ; rendu final de la publication dépend du chargement du service Instagram.

## Historique v5.0.1

- Remplacement des boutons v5.0.0 par un lecteur Deezer sous le titre et une publication Instagram intégrée après le texte et les galeries.
- Les deux champs déjà enregistrés sont réutilisés ; aucun contenu JSON à remplacer.
- Liens Deezer complets vers titre, album, playlist, artiste, podcast ou épisode ; liens Instagram vers publication, carrousel ou Reel public.
- Formulaire précisé et validation des formats ; version du CMS actualisée.

## Fonctionnalités conservées

- Deux liens facultatifs par article : musique Deezer et photos sur Instagram.
- Lecteur Deezer sous le titre ; publication Instagram tout en bas de l’article.
- Les champs vides n’affichent aucun lecteur ni publication. Les anciens articles restent compatibles.
- Conservation du correctif Gravel : toutes les sorties ayant un lien d’inscription sont affichées, y compris mars 2027. Les mois sans lien restent masqués sur Gravel.
- Menu Brevets vers https://brevets.200alaronde.fr/.
- Version affichée portée à v5.0.1 et documentation actualisée.

## Ajouter la musique et les photos d’une sortie

1. Ouvrir `/admin/`, puis **Articles** et l’article à modifier ou à créer.
2. Dans **Musique Deezer**, coller le lien complet du titre, de l’album ou de la playlist.
3. Dans **Photos de la sortie sur Instagram**, coller le lien complet d’une publication, d’un carrousel ou d’un Reel public (pas du profil).
4. Enregistrer/publier l’article et attendre le déploiement Netlify.

Ces deux champs sont facultatifs. Vider un champ supprime l’intégration correspondante. Les lecteurs utilisent les services Deezer et Instagram. Une publication Instagram privée ou dont l’intégration est désactivée peut ne pas être affichée. La disponibilité et la lecture dépendent des services et du navigateur. Utiliser des liens Deezer complets, pas des liens courts deezer.page.link.

Les valeurs sont enregistrées dans `content/articles/*.json` sous les clés `deezer_url` et `instagram_url`. Ne pas remplacer les contenus des articles pour installer cette mise à jour.

## Calendriers

- À venir : `content/pages/nos-sorties.json`.
- Gravel : `content/pages/gravel.json` ; renseigner le nom (par exemple « Mars 2027 ») et le lien d’inscription.
- Sur Gravel, retirer le lien d’une sortie terminée pour la masquer. Le calendrier conserve son classement par numéro de mois ; il ne déduit pas une date du libellé.

## Organisation du dépôt

| Chemin | Rôle |
| --- | --- |
| `build.py` | Génération des articles, pages, archives et sitemap |
| `admin/config.yml` | Champs du CMS |
| `content/articles/` | Sources JSON des articles |
| `content/pages/` | Sources JSON des pages et calendriers |
| `assets/css/site.css` | Styles |
| `articles/`, `pages/`, `index.html`, `sorties.html` | Pages HTML publiées |
| `netlify.toml` | Construction, publication et redirections Netlify |

## Installation dans GitHub

Extraire le ZIP puis déposer les fichiers à la racine du dépôt en conservant leurs dossiers et en remplaçant les versions existantes. Le ZIP est un correctif : il ne contient pas les médias ni les sources JSON des contenus.

Netlify exécute la commande configurée :

```sh
python build.py && python verify_seo.py
```

Pour une vérification locale :

```sh
python build.py
python verify_seo.py
python -m http.server 8000
```

Ouvrir ensuite http://localhost:8000/.

## Suivi des mises à jour

À chaque prochaine livraison, actualiser ce README avec la version, la date, les changements, les consignes utiles et les vérifications effectuées. Mettre également à jour la version affichée dans le générateur et les pages livrées.

### Vérifications de cette version

- Génération du site et vérification SEO.
- Liens absents : aucun bloc vide ; titre/album Deezer et publication/Reel Instagram : URL intégrée correcte. Positionnement du lecteur en haut et d’Instagram après les galeries vérifié dans le HTML généré.
- Échappement HTML des liens et rejet des protocoles autres que HTTP/HTTPS.
- Test du calendrier Gravel en octobre/décembre 2026 et janvier 2027.
- Vérification de l’intégrité du ZIP et de l’absence de médias.

## Références des intégrations

- Deezer, générateur officiel de widget : https://widget.deezer.com/ (consulté le 16 octobre 2026).
- Instagram, aide sur l’intégration des publications : https://help.instagram.com/ (consultée le 16 octobre 2026).
