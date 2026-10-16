# 200 à la ronde — v5.0.0

Site de l’association : https://200alaronde.fr/  
Version du 16 octobre 2026.

## Nouveautés v5.0.0

- Deux liens facultatifs par article : musique Deezer et photos sur Instagram.
- Boutons affichés sous le titre, avant l’image principale et le texte, avec ouverture dans un nouvel onglet.
- Les champs vides n’affichent aucun bouton. Les anciens articles restent compatibles.
- Conservation du correctif Gravel : toutes les sorties ayant un lien d’inscription sont affichées, y compris mars 2027. Les mois sans lien restent masqués sur Gravel.
- Menu Brevets vers https://brevets.200alaronde.fr/.
- Version affichée portée à v5.0.0 et documentation actualisée.

## Ajouter la musique et les photos d’une sortie

1. Ouvrir `/admin/`, puis **Articles** et l’article à modifier ou à créer.
2. Dans **Musique Deezer**, coller le lien complet du titre, de l’album ou de la playlist.
3. Dans **Photos de la sortie sur Instagram**, coller le lien complet de la publication, du carrousel ou du profil.
4. Enregistrer/publier l’article et attendre le déploiement Netlify.

Ces deux champs sont facultatifs. Vider un champ supprime le bouton correspondant. Il s’agit de liens externes : aucun lecteur musical ni galerie Instagram ne sont intégrés au site.

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
- Liens absents : aucun bloc vide ; liens présents : deux boutons en tête d’article.
- Échappement HTML des liens et rejet des protocoles autres que HTTP/HTTPS.
- Test du calendrier Gravel en octobre/décembre 2026 et janvier 2027.
- Vérification de l’intégrité du ZIP et de l’absence de médias.
