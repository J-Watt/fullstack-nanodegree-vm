#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
from math import ceil
from math import log
from random import random
from random import choice


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches(tourney=None):
    """Remove all the match records from the database."""
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
    """Remove all the player records from the database."""
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
    """Remove all the player records from the database."""
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
    """Returns the number of players currently registered."""
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
    print ("Player Count: " + str(player_no))
    return player_no


def registerPlayer(player, tourney="free agent"):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    tourney_db = connect()
    cursor = tourney_db.cursor()
    if isinstance(player, int):
        player_id = player
    else:
        query = "INSERT INTO Players (name) VALUES (%s);"
        query_add = str(player)
        cursor.execute(query, [query_add])
        tourney_db.commit()
        query = "SELECT MAX(id) FROM Players;"
        cursor.execute(query)
        player_id = cursor.fetchone()[0]
    if isinstance(tourney, int):
        tourney_id = tourney
        query = ("INSERT INTO Contestants (tourney_id, player_id) "
                 "VALUES (%s, %s);")
        query_add = [tourney_id, player_id]
        cursor.execute(query, query_add)
    else:
        if tourney.lower() != "free agent":
            query = "INSERT INTO Tourneys (name) VALUES (%s);"
            query_add = str(tourney)
            cursor.execute(query, [query_add])
            tourney_db.commit()
        tourney_id = getLatestTournament()
        query = ("INSERT INTO Contestants (tourney_id, player_id) "
                 "VALUES (%s, %s);")
        query_add = [tourney_id, player_id]
        cursor.execute(query, query_add)
    tourney_db.commit()
    tourney_db.close()
    print ("Tourney id: " + str(tourney_id))
    print ("Player id: " + str(player_id))





def playerStandings(player=None, detail=False):
    """Returns a list of the players and their total records from all
    tournaments, sorted by wins.

    Will attempt to sort by highest wins (and then highest ties if detailed).

    accepts two arguments (player, detail):
        player: return only records of player with this id, returns all player
                records if no id given
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

    Will attempt to sort by tournament id then highest wins
    (and then highest ties if detailed)

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
      tied: Boolean True records above args as ties instead
    """
    tourney_db = connect()
    cursor = tourney_db.cursor()
    if tourney is None:
        tourney_id = getLatestTournament()
    else:
        tourney_id = tourney
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
    tourney_db = connect()
    cursor = tourney_db.cursor()
    query = "SELECT MAX(id) FROM Tourneys;"
    cursor.execute(query)
    tourney_id = cursor.fetchone()[0]
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

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    # find tournament
    # if highest matches >= math.log(players, 2) then declare winner
    # Loop
    # find next highest wins num
    # rndm pair together (attempt deny rematch)
    # if odd number draw from next highest wins
    #   if tied for next highest wins look at leading ties
    #       if tied leading ties, defeated points count
    #       if tied leading ties and pts, rndm move up
    #   if no next highest wins then rndm promote winner
    # Repeat loop for next highest wins



    tourney_db = connect()
    cursor = tourney_db.cursor()
    if tourney is None:
        tourney_id = getLatestTournament()
    else:
        tourney_id = tourney
    query_add = tourney_id

    query = ("SELECT id_one, name_one, id_two, name_two "
             "FROM Past_Pairings WHERE tourney_id = %s;")
    cursor.execute(query, [query_add])
    past_pairings = set()
    past_pairings.update(cursor.fetchall())

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

    # xyz = [x['WIN'] for x in player_stats]

    query = ("SELECT COUNT(player_id), MAX(matches), MAX(wins) "
             "FROM Standings WHERE tourney_id = %s;")
    cursor.execute(query, [query_add])
    [(num_players, rounds_past, win_max)] = cursor.fetchall()
    rounds_max = ceil(log(num_players, 2))

    tourney_db.commit()
    tourney_db.close()
    player_ids = []
    if rounds_past < rounds_max:
        win_num = int(win_max)
        tiered_ids = []
        while win_num >= 0:
            for p in players:
                if p['WIN'] == win_num:
                    tiered_ids.append(p['ID'])
            if tiered_ids != []:
                player_ids.append(tiered_ids)
            tiered_ids = []
            win_num -= 1
        tier_max = len(player_ids) - 1

        infinite_loop = 0
        while True:
            pairings = []
            tier_level = 0
            new_player_ids = [list(key) for key in player_ids]
            print (new_player_ids)
            print (player_ids)
            print (id(player_ids))
            print (id(new_player_ids))
            bye = None

            for tier in new_player_ids:
                if len(tier) % 2 != 0:
                    if tier_level < tier_max:
                        ties = set()
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
                        else:
                            promote = choice(new_player_ids[tier_level + 1])
                            new_player_ids[tier_level].append(promote)
                            new_player_ids[tier_level + 1].remove(promote)
                    else:
                        bye = choice(new_player_ids[tier_level])
                        new_player_ids[tier_level].remove(bye)
                    new_player_ids = [x for x in new_player_ids if x != []]

                tier_level += 1
            print (player_ids)
            for tier in new_player_ids:
                while tier:
                    pair_a_i = choice(tier)
                    pair_a_n = [x['NAME'] for x in players if x['ID'] == pair_a_i]
                    tier.remove(pair_a_i)
                    pair_b_i = choice(tier)
                    pair_b_n = [x['NAME'] for x in players if x['ID'] == pair_b_i]
                    tier.remove(pair_b_i)
                    pairings.append((pair_a_i, pair_a_n[0], pair_b_i, pair_b_n[0]),)
                print (player_ids)

            if bye:
                reportMatch(bye, None, tourney_id, False)
            # debug
            infinite_loop += 1
            print (infinite_loop)
            if infinite_loop > 1000:
                print ('FAILURE: Looped over 1000')
                break
            check_pairings = set()
            check_pairings.update(pairings)
            print (new_player_ids)
            print (player_ids)
            print (pairings)
            print (past_pairings)
            print (check_pairings & past_pairings)
            if not check_pairings & past_pairings:
##            if [val for val in pairings if val in past_pairings]:
                print ('No repeat previous matches')
                break
        return pairings

    else:
        #xyz = [x['WIN'] for x in player_stats]
        first = "ID: {0}   NAME: {1}"
        for player in players:
            if player['WIN'] == win_max:
                first = first.format(player['ID'], player['NAME'])
##        results = "FIRST: {1}\nSECOND: {2}\nTHIRD: {3}"
##        results.format(first, second, third)
        results = "\n\n ~~~ WINNER!! ~~~\n" + first + "\n\n"
        print (results)
        return [None]



