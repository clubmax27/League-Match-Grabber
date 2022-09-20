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


import sqlite3
import os

from riotwatcher import LolWatcher, ApiError

import config


def main():
    """Entry point of the function"""

    API_TOKEN = config.API_TOKEN
    DATABASE_NAME = config.DATABASE_NAME
    DATABASE_PATH = config.DATABASE_PATH

    if DATABASE_PATH == "/":
        current_directory = os.path.dirname(os.path.abspath(__file__))
        DATABASE_PATH = current_directory

    lol_watcher_handle = LolWatcher(API_TOKEN)

    unit_test_summoner_info(lol_watcher_handle)

    complete_path = f"{DATABASE_PATH}\\{DATABASE_NAME}.sql"

    # If the database doesn't exist or isn't valid
    if not is_database_valid(complete_path):
        create_database(complete_path)

    database_handle = sqlite3.connect(complete_path)

    try:
        # Get all entries for the tier BRONZE I
        entries = lol_watcher_handle.league.entries(
            region="EUW1", queue="RANKED_SOLO_5x5", tier="BRONZE", division="I", page=1
        )

        # For every summoner found

        players_data = []

        for (count, entry) in enumerate(entries):
            if count > 30:
                continue
            print(f"summoner n°{count} is named {entry['summonerName']}")

            summonerId = entry["summonerId"]
            summoner_ranked_info = lol_watcher_handle.league.by_summoner(
                region="EUW1", encrypted_summoner_id=summonerId
            )

            for league_type in summoner_ranked_info:
                # We only want ranked solo/duo data
                if not league_type["queueType"] == "RANKED_SOLO_5x5":
                    continue

                rank = league_type["tier"]
                rank = convert_rank_string_to_int(rank)
                division = league_type["rank"]
                division = convert_division_to_int(division)

                wins = league_type["wins"]
                losses = league_type["losses"]
                winrate = round(100 * wins / (losses + wins), 1)

                players_data.append(
                    (
                        summonerId,
                        rank,
                        division,
                        winrate,
                        rank,
                        division,
                        winrate,
                    )
                )

        add_many_player_to_database(database_handle, players_data)

    except ApiError as err:
        handle_api_error(err)


def add_many_player_to_database(
    database_handle: sqlite3.Connection, players_data: tuple
) -> None:
    """Add the player data list to the database

    Args:
        database_handle (sqlite3.Connection): The database handle
        players_data (tuple): A tuple that contains the players data.
                It must be (summonerId, rank, division, winrate, rank, division, winrate,)
    """

    cursor = database_handle.cursor()

    for player_data in players_data:
        cursor.execute(
            """
            INSERT INTO Players (summonerId, rank, division, winrate)
            VALUES (?, ?, ?, ?)
                ON CONFLICT(summonerId) DO UPDATE SET rank = (?), division = (?), winrate = (?)
            """,
            player_data,
        )

    database_handle.commit()


def create_database(path: str) -> None:
    """Creates the database tables and file in the path given as a parameter

    Args:
        path (string): The path to which the file will be created

    Returns:
        str: The location of the database file
    """

    database_handle = sqlite3.connect(path)

    cursor = database_handle.cursor()

    # We delete the Ranks table
    cursor.execute(
        """
        DROP TABLE IF EXISTS Ranks;
        """
    )
    database_handle.commit()

    # We recreate the Ranks table
    cursor.execute(
        """
        CREATE TABLE Ranks(
            rank_int INTERGER PRIMARY KEY UNIQUE,
            rank_text TEXT
        )
        """
    )
    database_handle.commit()

    # The different constants for the Ranks
    values = [
        ("BRONZE", 1),
        ("SILVER", 2),
        ("GOLD", 3),
        ("PLATINIUM", 4),
        ("DIAMOND", 5),
        ("MASTER", 6),
        ("GRANDMASTER", 7),
        ("CHALLENGER", 8),
    ]

    # We insert those values into the Ranks table
    cursor.executemany(
        """
        INSERT INTO Ranks(rank_text, rank_int) VALUES(?, ?)
        """,
        values,
    )
    database_handle.commit()

    # We create the Player table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Players(
            summonerId TEXT PRIMARY KEY UNIQUE,
            rank INTEGER,
            division INTERGER,
            winrate FLOAT
        )
        """
    )
    database_handle.commit()

    print("Database successfuly created")


def is_database_valid(path: str) -> bool:
    """A function that check if the path is a database file and has the correct schema

    Args:
        path (str): The path of the database file

    Returns:
        bool: True if the database file exists and has the correct schema, False if not
    """

    # If the file doesn't exist
    if not os.path.isfile(path):
        return False

    database_handle = sqlite3.connect(path)
    cursor = database_handle.cursor()

    # Check if the "Players" table exists
    cursor.execute(
        """
        SELECT name FROM sqlite_master WHERE type='table' AND name='Players';
        """
    )

    table_existance_bool = cursor.fetchone()

    if not bool(table_existance_bool):
        return False

    return True


def handle_api_error(err: ApiError) -> None:
    """Function that goes through the diffrent error codes that the Riot API can return

    Args:
        err (ApiError): The error handle
    """

    if err.response.status_code == 429:
        print(f"We should retry in {err.response.headers['Retry-After']} seconds.")
        print("this retry-after is handled by default by the RiotWatcher library")
        print("future requests wait until the retry-after time passes")
    elif err.response.status_code == 404:
        print("Error 404 : The parameters were probably incorrect")
    else:
        # Should never happen
        print(err)
        print("Error not handled, exiting program ...")
        exit(-1)


def convert_rank_string_to_int(rank_string: str) -> int:
    """A function to convert a rank name into it's corresponding database value

    Args:
        rank_string (str): The rank's name

    Returns:
        int: The rank's corresponding integer
    """

    rank_dict = {
        "BRONZE": 1,
        "SILVER": 2,
        "GOLD": 3,
        "PLATINIUM": 4,
        "DIAMOND": 5,
        "MASTER": 6,
        "GRANDMASTER": 7,
        "CHALLENGER": 8,
    }

    try:
        return_value = rank_dict[rank_string]

    # If the string is not in the dictionary
    except KeyError:
        return_value = -1

    return return_value


def convert_division_to_int(division_string: str) -> int:
    """A function to convert a division name into it's corresponding database value

    Args:
        rank_string (str): The division's name

    Returns:
        int: The division's corresponding integer
    """

    rank_dict = {
        "I": 1,
        "II": 2,
        "III": 3,
        "IV": 4,
    }

    try:
        return_value = rank_dict[division_string]

    # If the string is not in the dictionary
    except KeyError:
        return_value = -1

    return return_value


def unit_test_summoner_info(lol_watcher_handle: LolWatcher) -> None:
    """Unit test that displays summoner info

    Args:
        lol_watcher_handle (LolWatcher): The LolWatcher handle
    """

    try:
        summoner = lol_watcher_handle.summoner.by_name("EUW1", "Bartemul1us")
        summoner_ranked_stats = lol_watcher_handle.league.by_summoner(
            "EUW1", summoner["id"]
        )
    except ApiError as err:
        handle_api_error(err)

    print(
        f"{summoner['name']} is level {summoner['summonerLevel']} and their current elo \
in ranked solo/duo is {summoner_ranked_stats[0]['tier']} {summoner_ranked_stats[0]['rank']}"
    )


if __name__ == "__main__":
    main()
