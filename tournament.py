#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#


import psycopg2
import bleach


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

def get_cursor():
    DB = connect()
    #print "Opened database succesfully"
    return DB, DB.cursor()

def createTournaments(tournament, name):
    """Adds a tournament to the tournament database."""

    DB, c = get_cursor()
    c_tournament = bleach.clean(tournament)
    c_name = bleach.clean(name)
    c.execute("INSERT INTO players(name) VALUES(%s) RETURNING player_id;",(c_name,))
    player_id = c.fetchall()[0][0]

    c.execute("INSERT INTO tournaments (tournament_name, player_id, bye_win) \
                VALUES (%s, %s, %s)",(c_tournament, player_id, "false"))
    
    c.close()
    DB.commit()
    DB.close()

def countTournaments():
    
    DB, c = get_cursor()
    c.execute ("SELECT count(player_id) FROM tournaments;")
    result = c.fetchall()[0][0]

    c.close()
    DB.close()
    return int(result)


def deleteMatches(tournament, choice):
    """If choice = 0, remove all the match records from the specified tournament.
    else remove all the match records from all tournament."""
    DB, c = get_cursor()

    c_tournament = bleach.clean(tournament)
    if choice == 0:
        c.execute("DELETE FROM tournament_games WHERE tournament_name = %s;", (c_tournament,))
    else:
        c.execute("DELETE FROM tournament_games;")


    c.close()
    DB.commit()
    DB.close()


def registerPlayer(tournament, player_id, name):
    """Adds a player to the tournament database(In specific tournamemts).
  
    The database assigns a unique serial id number for the player.  (This
    should be  handled by your SQL database schema, not in your Python code.)
  
    Returns:
      A dictionary with:
        player_id: An integer storing the player's id. This can be used for
                   registering the player in future tournaments.
        tournament: An integer representing the tournament id the player is registered
                    for. This can be used to register other players in the same
                    tournament.
    Args:
        tournament: specifies the tournament.
        player_id:  A player_id of 0 means the player is new and needs to be created.
        name: the player's full name (need not be unique).
    """
    DB, c = get_cursor()
    
    c_tournament = bleach.clean(tournament)
    c_name = bleach.clean(name)
  
    if player_id == 0:
        c.execute("INSERT INTO players(name) VALUES(%s) RETURNING player_id;",(c_name,))
        player_id = c.fetchall()[0][0]

    c.execute("INSERT INTO tournaments (tournament_name, player_id, bye_win) \
                VALUES (%s, %s, %s)",(c_tournament, player_id, "false",))
    
    c.close()
    DB.commit()
    DB.close()
    return {'player_id': player_id, 'tournament': tournament}


def countPlayers(tournament, choice):
    """If choice = 0, returns all players in the specified tournament.
        else returns all players in all tournaments."""

    DB, c = get_cursor()
    c_tournament = bleach.clean(tournament)

    if choice == 0:
        c.execute("SELECT count(player_id) FROM tournaments \
                    WHERE tournament_name = %s",(c_tournament,))
    else:
        c.execute("SELECT count(*) FROM players")
    
    result = c.fetchall()[0][0]

    c.close()
    DB.close()
    return int(result)


def deletePlayers(tournament,choice):
    """If choice = 0 remove all the player records from the specified tournament.
        Else delete all players records in all tournaments"""

    deleteMatches(tournament, choice)
    DB, c = get_cursor()
    
    c_tournament = bleach.clean(tournament)
    if choice == 0:
        c.execute("DELETE FROM tournaments WHERE tournament_name = %s",(c_tournament,))
    else:   
        c.execute("DELETE FROM tournaments")
        c.execute("DELETE FROM players")


    DB.commit()
    c.close()
    DB.close()




def playerStandings(tournament):
    """Returns a list of the players and their win records for a specified tournament.
    A draw counts as 1/2 a win.
    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.
    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won.
        matches: the number of matches the player has played
    """

    DB, c = get_cursor()

    c_tournament = bleach.clean(tournament)
    c.execute("SELECT standings.player_id, players.name, standings.wins, standings.matches\
                FROM standings, players \
                WHERE standings.tournament_name = %s AND standings.player_id = players.player_id \
                ORDER BY points DESC",(c_tournament,))
    data = c.fetchall()
    print data
    print("\n")

    c.close()
    DB.close()
    return data




#NOTES FROM BASIC MODULE USAGE ---> http://initd.org/psycopg/docs/usage.html#query-parameters

#The correct way to pass variables in a SQL command is using the second argument of the execute() method:
#SQL = "INSERT INTO authors (name) VALUES (%s);" # Note: no quotes
#data = ("O'Reilly", )
#cur.execute(SQL, data) # Note: no % operator

def reportMatch(tournament, winner, loser, draw):
    """Records the outcome of a single match between two players.
    Args:
      winner:  id of the winner.
      loser:  id of the loser.
      draw: specifies if the match was a draw.(TRUE / FALSE)
      tournament: specifies the game's tournament
    Draw: winner and loser identify the players
    """
    DB, c = get_cursor()

    # Record the game
    c_winner = bleach.clean(winner)
    c_loser = bleach.clean(loser)
    c_tournament = bleach.clean(tournament)

    
    if draw:
        query = "INSERT INTO tournament_games(tournament_name, player1_id, player2_id, draw)\
                 VALUES (%s, %s, %s, %s)"
        data = (c_tournament, c_winner, c_loser, "true")
        print data
        print ("\n")
        c.execute(query, data)
    else:
        query = "INSERT INTO tournament_games(tournament_name, player1_id, player2_id, draw, winner_id)\
                 VALUES (%s, %s, %s, %s, %s)"
        data = (c_tournament, c_winner, c_loser, "false", c_winner)
        print data
        print ("\n")
        c.execute(query, data)


    DB.commit()

    c.close()
    DB.close()


 
def swissPairings(tournament):
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
    EXTRA : Supports odd number of players and nye win for a player. 
            One bye win for a player per tournament
    """
    DB, c = get_cursor()
    
    c_tournament = bleach.clean(tournament)
    standings = playerStandings(c_tournament)
    pairlist = []

    if len(standings) % 2 == 1:
        c.execute("SELECT players.player_id, players.name FROM tournaments, players \
                    WHERE tournaments.tournament_name = %s AND NOT bye_win\
                     AND tournamemts.player_id = players.player_id \
                    ORDER BY RAND() LIMIT 1",(c_tournament,))
        results = c.fetchall()
        bye_id = results[0][0]
        bye_name = results[0][1]
        for player in standings:
            pairlist.append((bye_id, bye_name, 0 , "BYE WIN"))
            standings.remove(player)
            break

    pairlist.extend([(standings[i][0], standings[i][1], standings[i+1][0], standings[i+1][1]) for i in range(0,len(standings),2)])
    
    return pairlist

    #DB, c = get_cursor()
    #pairs = countPlayers()/2
    #pairlist = []
    #for x in range(0, pairs): 
    #    c.execute("select id, name from standings limit 2 offset (%s);",(x*2,))
    #    nextpair = c.fetchall()
    #    pairlist.append(nextpair[0]+nextpair[1])
    #DB.close()    
    #return pairlist

