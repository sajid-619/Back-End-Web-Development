#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import TournamentDBconnect

DB = TournamentDBconnect.TournamentDB('tournament')

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    
    
def deleteMatches():
    """Remove all the match records from the database."""
    # Delete match table and matchresult table
    deletesql = "DELETE FROM match;DELETE FROM matchresult;"
    parameter =""
    sqlexecute = DB.query(deletesql, parameter);
    

def deletePlayers():
    """Remove all the player records from the database."""
    # Delete player table
    sql = "DELETE FROM player"
    data = ""
    sqlexecute = DB.query(sql, data);
        

def countPlayers():
    """Returns the number of players currently registered."""
    # Get count of player
    sqlexecute = DB.fetchonequery("SELECT count(player_id) FROM player")
    return sqlexecute[0];

def registerPlayer(name):
    """Adds a player to the tournament database.
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
    Args:
      name: the player's full name (need not be unique).
    """
    # Add player to player table
    sql = "INSERT INTO player(player_name) VALUES(%s);"
    data = (name,)
    sqlexecute = DB.query(sql, data);

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
    # Get playerStandings(playerid, name, #ofwin, #ofmatch) view table
    sqlexecute = DB.selectquery("SELECT * FROM playerstandings")
    return sqlexecute


def reportMatch(winner, loser, istie):
    """Records the outcome of a single match between two players.
    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    # Add to Match Table
    matchsql = "INSERT INTO match(a_player_id, b_player_id) VALUES(%s, %s);"
    marchparameter = (winner, loser)
    matchsqlexeute = DB.query(matchsql, marchparameter)
    
    # Get Match ID
    matchid = DB.fetchonequery("SELECT LASTVAL()")
    
    # Check Match result is tie or not
    # istie=0, there are win and lose/ istie=1 no winner
    if istie == 0:
        sql = "INSERT INTO matchresult(match_id, player_id, win) values(%s, %s, %s);INSERT INTO matchresult(match_id, player_id, lose) values(%s, %s, %s)"
        parameter = (matchid[0], winner, 1, matchid[0], loser, 1)
        sqlexecute = DB.query(sql, parameter);
    else:
        sql = "INSERT INTO matchresult(match_id, player_id, tie) values(%s, %s, %s);INSERT INTO matchresult(match_id, player_id, tie) values(%s, %s, %s)"
        parameter = (matchid[0], winner, 1, matchid[0], loser, 1)
        sqlexecute = DB.query(sql, parameter);
     
 
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
    # Display Play list (Player ID, Player Name)
    sqlexecute = DB.selectquery("SELECT player_id, player_name FROM player")
    if (len(sqlexecute) > 0):
        playerlist = {}
        playeridonly = []
        pairinglist = []
        for row in sqlexecute:
            playerlist.update({str(row[0]):str(row[1])})
            playeridonly.append(str(row[0]))
        
        #print(playerlist);
        #print(playeridonly);
        playercount = len(playeridonly)
       
        # Match Way: Forward player and Backward player in the list 
        # ex) playerlist = [11,12,13,14,15,16]    Match:[11,16], [12,15], [13,14] 
        for index in xrange(0, (playercount/2), 1):
            opindex = playercount-index-1
            pairinglist.append([playeridonly[index], playerlist[playeridonly[index]], playeridonly[opindex], playerlist[playeridonly[opindex]]])

        #print(pairinglist)
        return pairinglist
