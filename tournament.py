import psycopg2

def connect(database_name="tournament"):
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except:
        print("<error message>")

def registerPlayer(name):
    db, cursor = connect()

    query = "INSERT INTO players (name) VALUES (%s);"
    parameter = (name,)
    cursor.execute(query, parameter)

    db.commit()
    db.close()

def deleteMatches():
    """Remove all the match records from the database."""
    try:
        db = connect()
        cursor = db.cursor()
        cursor.execute('DELETE FROM match;')
        db.commit()
        db.close()
    except psycopg2.Error as e:
        print(e)

def deletePlayers():
    """Remove all the player records from the database."""
    try:
        db = connect()
        cursor = db.cursor()
        cursor.execute('DELETE FROM player;')
        db.commit()
        db.close()
    except psycopg2.Error as e:
        print(e)


def countPlayers():
    """Returns the number of players currently registered."""
    count = None
    try:
        db = connect()
        cursor = db.cursor()
        cursor.execute('SELECT count(*) FROM player;')
        count = cursor.fetchone()[0]
        db.close()
    except psycopg2.Error as e:
        print(e)

    return count


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    try:
        db = connect()
        cursor = db.cursor()
        command = "INSERT INTO player (name) VALUES (%(name)s)"
        variables = {'name': name}
        cursor.execute(command, variables)
        db.commit()
        db.close()
    except psycopg2.Error as e:
        print(e)

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
    standings = []
    try:
        db = connect()
        cursor = db.cursor()
        sql_string = """select player.id, player.name, count(match.winner) 
                        as win, count(match.loser + match.winner) as matches 
                        from player left join match on player.id=match.winner 
                        group by player.id;"""
        cursor.execute(sql_string)
        results = cursor.fetchall()
        db.close()
    except psycopg2.Error as e:
        print(e)

    return results



def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.
    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """

    try:
        db = connect()
        cursor = db.cursor()

        cursor.execute("SELECT round from match ORDER BY round DESC;")
        result = cursor.fetchone()
        next_round = None
        #import pdb; pdb.set_trace()
        if result:
            latest_round = result[0]
            next_round = latest_round + 1
        else:
            next_round = 1


        command = """INSERT INTO match (round, winner, loser) VALUES 
                    (%(next_round)s, %(winner)s, %(loser)s)"""
        variables = {'next_round': next_round,'winner': winner, 'loser': loser}
        cursor.execute(command, variables)

        db.commit()
        db.close()
    except psycopg2.Error as e:
        print(e)
 
 
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

    players = []

    try:
        db = connect()
        cursor = db.cursor()
        #cursor.execute('SELECT id, name FROM player order by(matches);')
        cursor.execute('SELECT id, name FROM player order by(wins);')
        results = cursor.fetchall()
        db.close()
    except psycopg2.Error as e:
        print(e)


    while results:
        player2 = results.pop()
        player1 = results.pop()
        player_tuple = (player1[0], player1[1], player2[0], player2[1])
        players.append(player_tuple)
    #import pdb; pdb.set_trace()

    players.reverse()
    return players
