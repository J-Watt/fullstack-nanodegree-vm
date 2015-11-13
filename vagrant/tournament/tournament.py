#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


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
        query = "SELECT MAX(id) FROM Tourneys;"
        cursor.execute(query)
        tourney_id = cursor.fetchone()[0]
        if tourney_id is None:
            query = "INSERT INTO Tourneys (name) VALUES (%s);"
            query_add = "Open Tournament"
            cursor.execute(query, [query_add])
            query = "SELECT MAX(id) FROM Tourneys;"
            cursor.execute(query)
            tourney_id = cursor.fetchone()[0]
        query = ("INSERT INTO Contestants (tourney_id, player_id) "
                 "VALUES (%s, %s);")
        query_add = [tourney_id, player_id]
        cursor.execute(query, query_add)
    tourney_db.commit()
    tourney_db.close()
    print ("Tourney id: " + str(tourney_id))
    print ("Player id: " + str(player_id))





def playerStandings(tourney=None):
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    tourney_db = connect()
    cursor = tourney_db.cursor()
    if tourney is not None:
        query = ("SELECT player_id, name, SUM(wins) as wins, SUM(matches) "
                 "as matches FROM Standings WHERE tourney_id = %s "
                 "GROUP BY player_id, name ORDER BY wins;")
        query_add = tourney
        cursor.execute(query, [query_add])
    else:
        query = ("SELECT player_id, name, SUM(wins) as wins, SUM(matches) "
                 "as matches FROM Standings GROUP BY player_id, name "
                 "ORDER BY wins;")
        cursor.execute(query)
    standings = cursor.fetchall()
    tourney_db.commit()
    tourney_db.close()
    return standings

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    tourney_db = connect()
    cursor = tourney_db.cursor()
    query = " %s;"
    query_add = "" + player
    cursor.execute(query, query_add)
    tourney_db.commit()
    tourney_db.close()


def swissPairings():
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
    tourney_db = connect()
    cursor = tourney_db.cursor()
    query = " %s;"
    query_add = "" + player
    cursor.execute(query, query_add)
    tourney_db.commit()
    tourney_db.close()


