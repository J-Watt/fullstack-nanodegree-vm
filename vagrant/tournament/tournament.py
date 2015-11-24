# ------------------------------------------------------------------------------
# Name:         tournament
# Purpose:      Read & update a database for managing a swiss style tournament
#
# Author:       Jordan Alexander Watt
#
# Modified:     24-11-2015
# Created:      13-11-2015
# ------------------------------------------------------------------------------

import psycopg2
from math import ceil
from math import log
from random import random
from random import choice


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches(tourney=None):
    """If no torunament specified, remove all the match records from the
       database. Otherwise remove all matches from specific tournament

       Args:
            tourney: unique tournament id to effect. Default None
    """
    tourney_db = connect()
    cursor = tourney_db.cursor()
    if tourney is not None:
        query = "DELETE FROM Matches WHERE tourney_id = %s"
        query_add = tourney
        cursor.execute(query, [query_add])
    else:
        query = "DELETE FROM Matches;"
        cursor.execute(query)
    tourney_db.commit()
    tourney_db.close()


def deletePlayers(player=None):
    """If no player specified, remove all the player records from the
       database. Otherwise remove only specified player. Also can clear
       Players table to prevent ghost players not associated with any
       tournament.

       Args:
            player: unique player id to effect. Default None
                    NOTE if "CLEAR" is provided then will clean database
                    of players not in Contestants table
    """
    tourney_db = connect()
    cursor = tourney_db.cursor()
    if player is not None:
        if player.lower() == "clear":
            query = ("DELETE FROM Players WHERE Players.id NOT IN "
                     "(SELECT Contestants.Player_id FROM Contestants);")
            cursor.execute(query)
        else:
            query = "DELETE FROM Players WHERE id = %s;"
            query_add = player
            cursor.execute(query, [query_add])
    else:
        query = "DELETE FROM Players;"
        cursor.execute(query)
    tourney_db.commit()
    tourney_db.close()


def deleteTournaments(tourney=None):
    """If no torunament specified, remove all tournament records from the
       database. Otherwise remove specific tournament

       Args:
            tourney: unique tournament id to effect. Default None
    """
    tourney_db = connect()
    cursor = tourney_db.cursor()
    if tourney is not None:
        query = "DELETE FROM Tourneys WHERE id = %s;"
        query_add = tourney
        cursor.execute(query, [query_add])
    else:
        query = "DELETE FROM Tourneys;"
        cursor.execute(query)
    tourney_db.commit()
    tourney_db.close()
    deletePlayers("clear")


def countPlayers(tourney=None):
    """Returns the number of players currently registered.
       If no torunament specified, counts all the player records from the
       database. Otherwise count all players from specific tournament

       Args:
            tourney: unique tournament id to effect. Default None
    """
    tourney_db = connect()
    cursor = tourney_db.cursor()
    if tourney is not None:
        query = ("SELECT COUNT(player_id) FROM Contestants "
                 "WHERE tourney_id = %s;")
        query_add = tourney
        cursor.execute(query, [query_add])
    else:
        query = "SELECT COUNT(id) FROM Players;"
        cursor.execute(query)
        player_no = cursor.fetchone()[0]
    tourney_db.commit()
    tourney_db.close()
    return player_no


def registerPlayer(player, tourney="free agent"):
    """Adds a player to the tournament database using the name provided,
       the database assigns a unique serial id number for the player.
       If player id is specified instead of a name, registers existing player
       to a tournament.
       If tournament id is provided, will register player to existing
       tournament. If a name is provided instead, creates a new tournament
       using that name. If nothing is specified then the player will be
       registered to the last tournament created (if there are no existing
       tournaments a new one will be created, this is handled in
       getLatestTournament)

    Args:
      player: the player's full name (need not be unique)
              OR the id of the player you would like to register.
      tourney: the name of the tournament you would like to create
               (need not be unique) OR the id of the tournament you would like
               to register to. Default will run getLatestTournament
    """
    tourney_db = connect()
    cursor = tourney_db.cursor()

    # If player id is provided; save it to a variable
    if isinstance(player, int):
        player_id = player

    # If name is provided; add to database and save the new id
    else:
        query = "INSERT INTO Players (name) VALUES (%s);"
        query_add = str(player)
        cursor.execute(query, [query_add])
        tourney_db.commit()
        query = "SELECT MAX(id) FROM Players;"
        cursor.execute(query)
        player_id = cursor.fetchone()[0]

    # If tournament id is provided; register player to this tournament
    if isinstance(tourney, int):
        tourney_id = tourney
        query = ("INSERT INTO Contestants (tourney_id, player_id) "
                 "VALUES (%s, %s);")
        query_add = [tourney_id, player_id]
        cursor.execute(query, query_add)
    else:

        # If tournament name is provided; add it to the database
        if tourney.lower() != "free agent":
            query = "INSERT INTO Tourneys (name) VALUES (%s);"
            query_add = str(tourney)
            cursor.execute(query, [query_add])
            tourney_db.commit()

        # Save id of newest tournament (see getLatestTournamet for details)
        tourney_id = getLatestTournament()
        query = ("INSERT INTO Contestants (tourney_id, player_id) "
                 "VALUES (%s, %s);")
        query_add = [tourney_id, player_id]
        cursor.execute(query, query_add)
    tourney_db.commit()
    tourney_db.close()


def playerStandings(player=None, detail=False):
    """Returns a list of the players and their total records from all
    tournaments.
    Will attempt to sort by highest wins (and then highest ties if detailed).

    Args:
        player: Player id returns only records of this player,
                 returns all player records if no id given
        detail: boolean, returns additional columns (loses, ties) if True

    Returns:
      A list of tuples, each of which contains
      (id, name, matches, wins, [loses, ties]):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        matches: the number of matches the player has played
        wins: the number of matches the player has won
        loses: the number of matches the player has lost
        ties: the number of matches the player has tied
    """
    tourney_db = connect()
    cursor = tourney_db.cursor()

    # If player id provided; return results of that player based on detail
    if player is not None:
        if detail:
            query = ("SELECT player_id, name, SUM(matches), SUM(wins) as wins,"
                     " SUM(loses), SUM(ties) as ties FROM Standings WHERE "
                     "player_id = %s GROUP BY player_id, name "
                     "ORDER BY wins DESC, ties DESC;")
        else:
            query = ("SELECT player_id, name, SUM(matches), SUM(wins) as wins,"
                     " FROM Standings WHERE player_id = %s "
                     "GROUP BY player_id, name ORDER BY wins DESC;")
        query_add = player
        cursor.execute(query, [query_add])

    # Return results of all players based on detail
    else:
        if detail:
            query = ("SELECT player_id, name, SUM(matches), SUM(wins) as wins,"
                     " SUM(loses), SUM(ties) as ties FROM Standings "
                     "GROUP BY player_id, name ORDER BY wins DESC, ties DESC;")
        else:
            query = ("SELECT player_id, name, SUM(matches), SUM(wins) as wins "
                     "FROM Standings GROUP BY player_id, name ORDER BY wins DESC;")
        cursor.execute(query)
    standings = cursor.fetchall()
    tourney_db.commit()
    tourney_db.close()
    return standings


def tournamentStandings(tourney=None, detail=False):
    """Returns a list of player records for each tournament.
    Will attempt to sort by tournament id then highest wins then highest
    ties if detailed

    Args:
        tourney: Tournament id returns only records of players registered
                 in this tournament,
                 returns all player records if no id given
        detail: boolean, returns additional columns
                (tourney_id, tourney_name, loses) if True

    Returns:
      A list of tuples, each of which contains
      ([tourney_id, tourney_name,] id, name, matches, wins, [loses]]):
        tourney_id: the tournament's unique id (assigned by the database)
        tourney_name: the tournament's full name (as registered)
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        matches: the number of matches the player has played
        wins: the number of matches the player has won
        loses: the number of matches the player has lost
        ties: the number of matches the player has tied
    """
    tourney_db = connect()
    cursor = tourney_db.cursor()

    # If tournament id provided; returns only records from that tournament
    # based on detail
    if tourney is not None:
        if detail:
            query = ("SELECT * FROM Standings WHERE "
                     "tourney_id = %s ORDER BY wins DESC, ties DESC;")
        else:
            query = ("SELECT player_id, name, matches, wins, ties "
                     "FROM Standings WHERE tourney_id = %s "
                     "ORDER BY wins DESC, ties DESC;")
        query_add = tourney
        cursor.execute(query, [query_add])

    # returns all records based on detail
    else:
        if detail:
            query = ("SELECT * FROM Standings "
                     "ORDER BY tourney_id, wins DESC, ties DESC;")
        else:
            query = ("SELECT tourney_id, tourney_name, player_id, name, "
                     "matches, wins, ties FROM Standings "
                     "ORDER BY tournament_id, wins DESC, ties DESC;")
        cursor.execute(query)
    standings = cursor.fetchall()
    tourney_db.commit()
    tourney_db.close()
    return standings


def reportMatch(winner, loser, tourney=None, tied=False):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
      tourney: the id number of the tournament for this match,
               records using latest id if none provided
      tied: Boolean True will record winner/loser args as ties instead
    """
    tourney_db = connect()
    cursor = tourney_db.cursor()

    # If no tournament provided; assumes match on most recent tournament
    if tourney is None:
        tourney_id = getLatestTournament()
    else:
        tourney_id = tourney

    # If tied arg is True; record players as having tied the match
    # otherwise record in database as a winner and loser
    if tied:
        query = ("INSERT INTO Matches (tourney_id, id_tie_a, "
                 "id_tie_b) VALUES (%s, %s, %s);")
    else:
        query = ("INSERT INTO Matches (tourney_id, id_winner, "
                 "id_loser) VALUES (%s, %s, %s);")
    query_add = [tourney_id, winner, loser]
    cursor.execute(query, query_add)
    tourney_db.commit()
    tourney_db.close()


def getLatestTournament():
    """Returns the most recently created tournament (tournament with the
    highest id) from the database. If no tournaments are found, then will
    create a tournament called 'Open Tournament' and will return this
    new tournament's id"""
    tourney_db = connect()
    cursor = tourney_db.cursor()

    # Search for most recent tournament id
    query = "SELECT MAX(id) FROM Tourneys;"
    cursor.execute(query)
    tourney_id = cursor.fetchone()[0]

    # If no tournaments then create one
    if tourney_id is None:
        query = "INSERT INTO Tourneys (name) VALUES (%s);"
        query_add = "Open Tournament"
        cursor.execute(query, [query_add])
        tourney_db.commit()
        query = "SELECT MAX(id) FROM Tourneys;"
        cursor.execute(query)
        tourney_id = cursor.fetchone()[0]
    tourney_db.commit()
    tourney_db.close()
    return tourney_id


def swissPairings(tourney=None):
    """Returns a list of pairs of players for the next round of a match.

    Determines maximum number of rounds based on number of entrants in the
    tournament (finds latest tournament if none provided). If maximum rounds
    reached print results, otherwise begin making pairs.

    Creates tiers by grouping players with the same number of wins. If there
    is an odd number of players within a tier, randomly draw from tier below
    with less wins, give a bye (win) to a random player if there is no players
    below to draw from. When drawing from tier below prioritize players with
    highest ties.

    After all tiers are even randomly match opponents within each tier and
    check that no matchups have occured in previous rounds.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    tourney_db = connect()
    cursor = tourney_db.cursor()

    # Save tournament id
    if tourney is None:
        tourney_id = getLatestTournament()
    else:
        tourney_id = tourney

    # Save past matchup records for comparison later
    query_add = tourney_id
    query = ("SELECT id_one, name_one, id_two, name_two "
             "FROM Past_Pairings WHERE tourney_id = %s;")
    cursor.execute(query, [query_add])
    past_pairings = set()
    past_pairings.update(cursor.fetchall())

    # Collect player informaton for processing
    standings = tournamentStandings(tourney_id, False)
    players = []
    for player in standings:
        stats = {'ID': None, 'NAME': None, 'MATCH': None, 'WIN': None, 'TIE': None}
        stats['ID'] = player[0]
        stats['NAME'] = player[1]
        stats['MATCH'] = player[2]
        stats['WIN'] = player[3]
        stats['TIE'] = player[4]
        players.append(stats)

    # Find number of players and determine maximum number of rounds needed
    # to conclude tournament. Find how many matches have occured. Find
    # Highest wins for generating tiers based on wins
    query = ("SELECT COUNT(player_id), MAX(matches), MAX(wins) "
             "FROM Standings WHERE tourney_id = %s;")
    cursor.execute(query, [query_add])
    [(num_players, rounds_past, win_max)] = cursor.fetchall()
    rounds_max = ceil(log(num_players, 2))
    tourney_db.commit()
    tourney_db.close()

    # If maximum rounds not reached begin creating pairings
    player_ids = []
    if rounds_past < rounds_max:
        win_num = int(win_max)
        tiered_ids = []

        # Create tiers grouping by wins
        while win_num >= 0:
            for p in players:
                if p['WIN'] == win_num:
                    tiered_ids.append(p['ID'])
            if tiered_ids != []:
                player_ids.append(tiered_ids)
            tiered_ids = []
            win_num -= 1
        tier_max = len(player_ids) - 1

        # Loop creating pairings. If a matchup exists in previously made
        # matchups then repeat
        infinite_loop = 0
        while True:
            pairings = []
            tier_level = 0
            new_player_ids = [list(key) for key in player_ids]
            bye = None

            # Check each tier for odd number of players and even out
            for tier in new_player_ids:
                if len(tier) % 2 != 0:

                    # Check if this is the last tier
                    if tier_level < tier_max:
                        ties = set()

                        # Check for ties and randomly move player with highest
                        # ties up a tier for matchmaking
                        for player in players:
                            if player['ID'] in new_player_ids[tier_level + 1]:
                                ties.add(player['TIE'])
                        tie_max = max(ties)
                        if tie_max != 0:
                            tie_ids = []
                            for player in players:
                                if player['TIE'] == tie_max and \
                                   player['ID'] in new_player_ids[tier_level + 1]:
                                    tie_ids.append(player['ID'])
                            promote = choice(tie_ids)
                            new_player_ids[tier_level].append(promote)
                            new_player_ids[tier_level + 1].remove(promote)

                        # No ties then move random player up a tier
                        else:
                            promote = choice(new_player_ids[tier_level + 1])
                            new_player_ids[tier_level].append(promote)
                            new_player_ids[tier_level + 1].remove(promote)

                    # If last tier then give a random player a bye
                    else:
                        bye = choice(new_player_ids[tier_level])
                        new_player_ids[tier_level].remove(bye)
                    new_player_ids = [x for x in new_player_ids if x != []]

                tier_level += 1

            # Pick two players within a tier to pair at random
            # Repeat until all players have been matched up
            for tier in new_player_ids:
                while tier:
                    pair_a_i = choice(tier)
                    pair_a_n = [x['NAME'] for x in players if x['ID'] == pair_a_i]
                    tier.remove(pair_a_i)
                    pair_b_i = choice(tier)
                    pair_b_n = [x['NAME'] for x in players if x['ID'] == pair_b_i]
                    tier.remove(pair_b_i)
                    pairings.append((pair_a_i, pair_a_n[0], pair_b_i, pair_b_n[0]),)

            # If the last tier had an odd number of players a player was given
            # a bye. A Bye counts as a win so the match is recorded as
            # a win against no one
            if bye:
                reportMatch(bye, None, tourney_id, False)

            # Safety in place in the event that pairings are unable to be
            # made or the pairing system has encountered repeat matchups
            # an excessive number of times
            infinite_loop += 1
            if infinite_loop > 1000:
                print ('FAILURE: Looped over 1000')
                pairings = []
                break

            # Compare newly created matchups against previously recorded
            # matchups. Break loop if no repeats found.
            check_pairings = set()
            check_pairings.update(pairings)
            if not check_pairings & past_pairings:
                break
        return pairings

    # Print the results of the tournament
    # Return empty pairings to prevent errors (allows running this function
    # repeatedly without effecting a completed tournament)
    else:
        first = "ID: {0}   NAME: {1}"
        for player in players:
            if player['WIN'] == win_max:
                first = first.format(player['ID'], player['NAME'])
        results = "\n\n ~~~ WINNER!! ~~~\n" + first + "\n\n"
        print (results)
        return [None]
