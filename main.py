"""
TODO

- Faire une config file avec le token API à ajouter dans le .gitignore
- Créer le modèle de la base de donnée


- Pour chaque tier et division :
	- tant que GET_getLeagueEntries ne renvoie pas [] :
		- trouver le puuid des joueurs
		- remplir la base de donnée avec les données de GET_getByPUUID (puuid, rank, winrate)


- Pour chaque joueur, trouver l'historique de ses matchs avec , et les ajouter à la bdd

 
- Pour chaque match, tirer les données du match avec GET_getMatch, les données des mastery avec GET_getChampionMastery et les ajouter dans la bdd
"""