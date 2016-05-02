#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


class DB:
    def __init__(self, db_conn_str="dbname=tournament"):
        """
        Creates a SQL database connection with the connection string provided.
        :param str db_con_str: Contains the database connection string, with a
        default value when no argument is passed to the parameter
        """
        self._conn = psycopg2.connect(db_conn_str)


    def cursor(self):
        """Returns the current cursor of the database."""
        return (self._conn).cursor()


    def execute(self, sql_query_string, param_for_query=(),
                fetch=None, commit=False):
        """
        Executes and optionally fetches SQL queries, then closes database
        connection.
        :param str sql_query_string: Contains the query string to be executed
        :param tuple param_for_query: Contains any additional param enclosed
        in tuple to be passed to query
        :param str fetch: for database query, returns fetchone() for str
        "one", returns fetchall() for str "all", or None for any other str
        :param bool commit: If True commit changes to connected database
        """
        cursor = self.cursor()
        cursor.execute(sql_query_string, param_for_query)
        if fetch == "one":
            fetched = cursor.fetchone()
        elif fetch == "all":
            fetched = cursor.fetchall()
        else:
            fetched = None
        if commit:
            self._conn.commit()
        self.close()
        return fetched


    def close(self):
        """
        Closes the current database connection.
        """
        self._conn.close()


def deleteMatches():
    """Remove all the match records from the database."""
    DB().execute("DELETE FROM matches;", (), None, True)


def deletePlayers():
    """Remove all the player records from the database."""
    DB().execute("DELETE FROM players;", (), None, True)


def countPlayers():
    """Returns the number of players currently registered."""
    player_number = DB().execute("SELECT COUNT(*) FROM players;", (), "one",
                                 False)
    return player_number[0]


def registerPlayer(name):
    """
    Adds a player to the tournament database.
    The SQL database assigns a unique serial id number for the player.
    param str name: the player's full name (need not be unique).
    """
    DB().execute("INSERT INTO players (name) VALUES (%s);", (name,), None,
                 True)


def playerStandings():
    """
    Returns a list of the players and their win records, sorted by wins.
    The first entry in the list is the player in first place, or a
    player tied for first place if there is currently a tie.
    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    standings = DB().execute("SELECT * FROM standings;", (), "all", False)
    standings = [(int(row[0]), str(row[1]), int(row[2]), int(row[3]))
                 for row in standings]
    return standings


def reportMatch(winner, loser):
    """
    Records the outcome of a single match between two players.
    :param int winner: the id number of the player who won
    :param int loser: the id number of the player who lost
    """
    DB().execute("INSERT INTO matches (winner, loser) VALUES (%s, %s);",
                 (winner, loser), None, True)


def swissPairings():
    """
    Returns a list of pairs of players for the next round of a match.
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
    pairings = DB().execute("SELECT * FROM pairings;", (), "all", False)
    pairings = [(int(row[0]), str(row[1]), int(row[2]), str(row[3])) for row
                in pairings]
    return pairings
