import psycopg2, re


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        conn = psycopg2.connect("dbname=tournament")
        print "Connected!"
        return conn
    except psycopg2.Error as e:
        print e

def deleteWins():
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE FROM wins;")
    DB.commit()
    c.close()
    DB.close()
    print "Task Done!"

def deleteMatches():
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE FROM matches;")
    DB.commit()
    c.close()
    DB.close()
    print "Task Done!"

def deletePlayers():
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE FROM players;")
    DB.commit()
    c.close()
    DB.close()


def countWins():
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT COUNT(*) FROM wins;")
    result = int(c.fetchone()[0])
    c.close()
    DB.close()
    return result


def countPlayers():
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT COUNT(*) FROM players;")
    result = int(c.fetchone()[0])
    c.close()
    DB.close()
    return result


#In the next two functions I try to escape ' by adding two of them, noticed the name O'Neil needed it.
#I am aware psycopg offers a way to do it with this code : c.execute("INSERT INTO players (name) VALUES(%s) RETURNING id;", (name,))
#I just wanted to do it with regexp which were taught to us in this course
def registerPlayer(name):
    DB = connect()
    c = DB.cursor()
    chars_to_remove = ["'"]
    rx = '[' + re.escape(''.join(chars_to_remove))+']'
    name = re.sub(rx, '"', name)
    c.execute("INSERT INTO players (name) VALUES ('%s') RETURNING id;" % ( name,))
    DB.commit()
    returnable = int(c.fetchone()[0])
    c.close()
    DB.close()
    return returnable

#creates a new tournament for the players to have fun in
def createTournament(name):
    DB = connect()
    c = DB.cursor()
    chars_to_remove = ["'"]
    rx = '[' + re.escape(''.join(chars_to_remove))+']'
    name = re.sub(rx, "''", name)
    c.execute("INSERT INTO tournaments (name) VALUES ('%s') RETURNING id;" % (name,))
    DB.commit()
    returnable = int(c.fetchone()[0])
    c.close()
    DB.close()
    return returnable

def deleteTournaments():
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE FROM tournaments;")
    DB.commit()
    c.close()
    DB.close()

def countTournaments():
    
    DB, c = get_cursor()
    c.execute ("SELECT count(player_id) FROM tournaments;")
    result = c.fetchall()[0][0]

    c.close()
    DB.close()
    return int(result)

# registers a participant to a tournament from the already existing tournaments and players.
def registerParticipant(t_id, p_id):
    DB = connect()
    c = DB.cursor()
    c.execute("INSERT INTO participates (t_id, p_id) VALUES (%s, %i);" % (t_id, p_id,))
    DB.commit()
    c.close()
    DB.close()

def deleteParticipates():
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE FROM participates")
    DB.commit()
    c.close()
    DB.close()

def countParticipates():
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT COUNT(*) FROM participates;")
    result = int(c.fetchone()[0])
    c.close()
    DB.close()
    return result

# has a tournament id to take players standings from a certain tournament
def playerStandings(t_id):
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT * FROM player_info where tournaments = %s;" % (t_id,))
    result = c.fetchall()
    c.close()
    DB.close()
    return result

# added the boolean for tie, which if true, adds a win for the other player as well.
# first argumment, if the game is not a tie, should be considered as the winner
# used
def reportMatch(first, second, tie,t_id):
    DB = connect()
    c = DB.cursor()
    c.execute("INSERT INTO matches (round, p_one_id, p_two_id, t_id) VALUES( %s, %i, %d, %f) RETURNING id;" % (0,first, second, t_id ))
    match_id = int(c.fetchone()[0])
    c.execute("INSERT INTO wins (m_id, p_id) VALUES(%s, %i);" % (match_id, first,))
    if tie:
        c.execute("INSERT INTO wins (m_id, p_id) VALUES (%s, %i);" % (match_id, second,))
    DB.commit()
    c.close()
    DB.close()

#used to setup preliminary matches
def setupMatch(first, second, t_id):
    DB = connect()
    c = DB.cursor()
    c.execute("INSERT INTO matches (round, p_one_id, p_two_id t_id) VALUES( %s, %i, %d, %f) RETURNING id;" % (0,first, second, t_id ))
    DB.commit()
    c.close()
    DB.close()

#used to report wins separately from creating matches
def reportWin(player_id, match_id):
    DB = connect()
    c = DB.cursor()
    c.execute("INSERT INTO wins (m_id, p_id) VALUES(%s, %i);" % (match_id, player_id,))
    c.close()
    DB.close()

# added the boolean for tie, which if true, adds a win for the other player as well.
# first argumment, if the game is not a tie, should be considered as the winner
# the round argumment is to keep track when the match happen.
def reportMatchWithRound(round, first, second, tie,t_id):
    DB = connect()
    c = DB.cursor()
    c.execute("INSERT INTO matches (round, p_one_id, p_two_id, t_id) VALUES( %s, %i, %d, %f) RETURNING id;" % (round,first, second, t_id ))
    match_id = int(c.fetchone()[0])
    c.execute("INSERT INTO wins (m_id, p_id) VALUES(%s, %i);" % (match_id, first,))
    if tie:
        c.execute("INSERT INTO wins (m_id, p_id) VALUES (%s, %i);" % (match_id, second,))
    DB.commit()
    c.close()
    DB.close()

#put docstring inside because that's how python says we should
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
        wins1: the amount of wins the first player has
        id2: the second player's unique id
        name2: the second player's name
        wins2: the amount of wins the second player has
    """
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT * FROM player_pairs;")
    result = c.fetchall()
    c.close()
    DB.close()
    return result
