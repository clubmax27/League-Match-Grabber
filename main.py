"""
TODO

- DONE/ Faire une config file avec le token API à ajouter dans le .gitignore
- Créer le modèle de la base de donnée


- Pour chaque tier et division :
	- tant que GET_getLeagueEntries ne renvoie pas [] :
		- trouver le puuid des joueurs
		- remplir la base de donnée avec les données de GET_getByPUUID (puuid, rank, winrate)


- Pour chaque joueur, trouver l'historique de ses matchs avec , et les ajouter à la bdd


- Pour chaque match, tirer les données du match avec GET_getMatch, les données des mastery
  avec GET_getChampionMastery et les ajouter dans la bdd
"""


import cassiopeia as cass

import config


def main():
    """Entry point of the function"""

    API_TOKEN = config.API_TOKEN
    cass.set_riot_api_key(API_TOKEN)

    REGION = "EUW"

    unit_test_summoner_info()

    bronze_2_league = cass.LeagueEntries(
        region=REGION,
        queue=cass.Queue.ranked_solo_fives,
        tier=cass.Tier.bronze,
        division=cass.Division.one,
    )

    print(bronze_2_league[0].summonerName)


def unit_test_summoner_info():
    """Unit test that displays summoner info"""

    summoner = cass.get_summoner(name="Bartemul1us", region="EUW")
    print(
        f"{summoner.name} is level {summoner.level} and their current elo \
in ranked solo/duo is {summoner.ranks[cass.data.Queue.ranked_solo_fives]}"
    )


main()
