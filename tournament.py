#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the tournament database, create the database and cursor objects"""
    db = psycopg2.connect(dbname='tournament', user='vagrant')
    cursor = db.cursor()
    return db,cursor 


def deleteMatches():
    """Remove all the match records from the database."""
    db, cursor = connect()
    cursor.execute("DELETE FROM matches; DELETE FROM matchResults")
    db.commit()


def deletePlayers():
    """Remove all the player records from the database."""
    db, cursor = connect()
    cursor.execute("DELETE FROM players")
    db.commit()


def countPlayers():
    """Returns the number of players currently registered."""
    db, cursor = connect()
    cursor.execute("SELECT COUNT(player_id) FROM players")
    player_count = cursor.fetchall()

    if player_count is not None:
        player_count = player_count[0][0] 
    else:
        player_count = 0      
    return player_count


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    db, cursor = connect()
    cursor.execute("INSERT INTO players(player_name) VALUES(%s)",(name,))
    db.commit()


def playerStandings():
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
    db, cursor = connect()
    cursor.execute("SELECT * FROM playerStandings")
    standings = cursor.fetchall()
    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.
    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db, cursor = connect()

    # Add a match to the table matches. 
    cursor.execute("INSERT INTO matches(id_player_a, id_player_b) VALUES(%s, %s)", (winner, loser))
    db.commit()

    # Get the match id from matches
    cursor.execute("SELECT match_id from matches")
    current_match_id = cursor.fetchone()

    # Add the results of the matches to the matchResults table.
    cursor.execute("INSERT INTO matchResults(match_id, player_id, match_win) VALUES(%s, %s, %s);INSERT INTO matchResults(match_id, player_id, match_loss) VALUES(%s, %s, %s)", (current_match_id[0], winner, 1, current_match_id[0], loser, 1))
    db.commit()
 
 
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

    db, cursor = connect()

    cursor.execute("SELECT id, name, sum(wins) as num FROM playerStandings GROUP BY id, name ORDER BY num DESC")
    player_win_count = cursor.fetchall()

    if len(player_win_count) > 0:

        player_list = []
        pairing_list = []

        # the SELECT statment above creates a list of tuples (player_win_count) with 3 elements - 
        # id, name, and wins (a,b,c), we only need id and player_name (a,b), so a new list of 
        # tuples is created ('player_list') by appending only id and name from 'player_win_count' 

        for a,b,c in player_win_count: 
            player_list.append((a,b))

        # once we have a list of tuples containing id and name for each player, the players
        # can get paired by looping through the range of the 'player_list' and appending the 
        # results to a new list of tuples each containing 4 elements (id1,name1,id2,name2). The 
        # players in 'player_list' were ordered by win numbers with the SELECT statment above, so 
        # players with the same/similar win numbers are already next to each other in the list. 
        # This allows the loop to pair the players by using ('player', 'player + 1') for each 
        # iteration. 

        for player in range(0, len(player_list) - 1,2): 
            pairing_list.append((player_list[player][0],player_list[player][1], player_list[player + 1][0], player_list[player+1][1]))
        return pairing_list



# data used for testing: 

# swissPairings()

# INSERT INTO players(player_name) VALUES ('Twilight Sparkle'), ('Fluttershy'), ('Applejack'), ('Pinkie Pie'), ('Rarity'), ('Rainbow Dash'), ('Princess Celestia'), ('Princess Luna');
# INSERT INTO matches(match_id, id_player_a, id_player_b) VALUES (1,1,2),(2,3,4),(3,5,6),(4,7,8),(5,1,3),(6,2,4),(7,5,7),(8,6,8);
# INSERT INTO matchResults(match_id, player_id, match_win) VALUES (1,1,1),(1,2,0),(2,3,1),(2,4,0),(3,5,1),(3,6,0),(4,7,1),(4,8,0),(5,1,1),(5,3,0),(6,2,1),(6,4,0),(7,5,1),(7,7,0),(8,6,1),(8,8,0);
