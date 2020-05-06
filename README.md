Projet 7 - GrandpyBot

# Présentation

Ce projet est un exercice de formation Python.

GranpyBot est un papy-robot qui répond à vos demandes géographiques en ajoutant un récit sur le lieu recherché.
Vous devez lui poser une question, par exemple : "Coucou grandpy ! La forme ? Connais-tu l'emplacement de la tour de pise par hasard ?"
Et il vous répondra où elle se trouve, avec un carte google maps indiquant l'endroit précis, et un texte sur un des lieux alentours.
Vous ne pouvez pas lui demander d'itinéraire, il répond seulement à des emplacements "simples".

# Fonctionnement

Le programme parse votre question pour en retirer les mots clés, recherche ce que vous demandez sur google maps via l'API Google Places, pour en récupérer les coordonnées ainsi que l'adresse.
Les coordonnées sont envoyées à l'API de Wikipédia pour effectuer une GeoSearch, qui renvoie une liste de 10 pages wikipédia aux alentours de cette position (dans un rayon de 10km).
Le programme choisit une page au hasard, et requête encore une fois l'API de Wikipédia cette fois avec l'id de la page, pour en extraire le titre, les quatre premières lignes de texte et l'url.
Une fois toutes ces infos récupérées, il reste à construire la réponse de Grandpy, avant de l'afficher dans la zone centrale de l'écran sans recharger la page. Si vous rechargez la page, vous perdez tout l'historique de questions / réponses.
Amusez-vous bien :)

# Utilisation

Le projet est déployé sur heroku à l'adresse suivante : https://grandpy-bot-project.herokuapp.com/

Sinon, forkez ce dépot puis clonez le dans votre répertoire local.
Installez les requirements pour pouvoir utiliser les paquets installés.
Enfin; pour lancer le projet, utilisez la commande 
```
python main.py
```
