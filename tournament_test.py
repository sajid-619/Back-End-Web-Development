#!/usr/bin/env python
#
# Test cases for tournament.py


#I added 2 more test cases in this file in order to check
#createTournaments and countTournaments methos in tournament.

#Every test case has been modified. Every case contains arguments.
#


from tournament import *

def testCreateAndDeleteTournament():

    tournament = "Tennis"
    createTournaments(tournament,"Markov Chaney")
    records = countTournaments()
    #print records
    if records == 0:
        raise ValueError("No tournament was created.")
    #if records[0][0] != tournament or records[0][1] != "chess":
    #    raise ValueError("Error in tournament creation.")
    print "New test case 1 -> Tournaments created."

   
    deletePlayers(tournament, 1) # 1 refers to argument choice in deletePlayers.
    records = countTournaments()    
    #print records

    if records != 0:
        raise ValueError("Errors in individual tournament delete's process.")
    print "New test case 2 ->  Individual tournaments deleted."

def testDeleteMatches():
    tournament = "Tennis"
    deleteMatches(tournament, 0) # 0 refers to argument choice in deleteMatches.
    print "1. Old matches can be deleted."


def testDelete():
    tournament = "Tennis"
    #deleteMatches(tournament, 0) # 0 refers to argument choice in deleteMatches.
    deletePlayers(tournament, 0) # 0 refers to argument choice in deletePlayers.
    print "2. Player records can be deleted."


def testCount():
    tournament = "Tennis"
    #deleteMatches(tournament, 0) 
    deletePlayers(tournament, 0) # 0 refers to argument choice in deletePlayers.
    c = countPlayers(tournament, 0)
    if c == '0':
        raise TypeError(
            "countPlayers() should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "3. After deleting, countPlayers() returns zero."


def testRegister():
    tournament = "Tennis"
    #deleteMatches(tournament, 0)
    deletePlayers(tournament, 0) # 0 refers to argument choice in deletePlayers.
    registerPlayer(tournament, 0, "Chandra Nalaar")
    c = countPlayers(tournament, 0)
    if c != 1:
        raise ValueError(
            "After one player registers, countPlayers() should be 1.")
    print "4. After registering a player, countPlayers() returns 1."


def testRegisterCountDelete():
    tournament = "Tennis"
    #deleteMatches(tournament, 0)
    deletePlayers(tournament, 0) # 0 refers to argument choice in deletePlayers.
    registerPlayer(tournament, 0, "Markov Chaney")
    registerPlayer(tournament, 0, "Joe Malik")
    registerPlayer(tournament, 0, "Mao Tsu-hsi")
    registerPlayer(tournament, 0, "Atlanta Hope")
    c = countPlayers(tournament,0)
    if c != 4:
        raise ValueError(
            "After registering four players, countPlayers should be 4.")
    deletePlayers(tournament, 0)
    c = countPlayers(tournament, 0)
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "5. Players can be registered and deleted."


def testStandingsBeforeMatches():
    tournament = "Tennis"
    #deleteMatches(tournament, 0)
    deletePlayers(tournament, 0) # 0 refers to argument choice in deletePlayers.
    registerPlayer(tournament, 0, "Melpomene Murray")
    registerPlayer(tournament, 0, "Randy Schwartz")
    standings = playerStandings(tournament)
    if len(standings) < 2:
        raise ValueError("Players should appear in playerStandings even before "
                         "they have played any matches.")
    elif len(standings) > 2:
        raise ValueError("Only registered players should appear in standings.")
    if len(standings[0]) != 4:
        raise ValueError("Each playerStandings row should have four columns.")
    [(id1, name1, wins1, matches1), (id2, name2, wins2, matches2)] = standings
    if matches1 != 0 or matches2 != 0 or wins1 != 0 or wins2 != 0:
        raise ValueError(
            "Newly registered players should have no matches or wins.")
    if set([name1, name2]) != set(["Melpomene Murray", "Randy Schwartz"]):
        raise ValueError("Registered players' names should appear in standings, "
                         "even if they have no matches played.")
    print "6. Newly registered players appear in the standings with no matches."


def testReportMatches():
    tournament = "Tennis"
    #deleteMatches(tournament, 0)
    deletePlayers(tournament, 0) # 0 refers to argument choice in deletePlayers.
    registerPlayer(tournament, 0, "Bruno Walton")
    registerPlayer(tournament, 0, "Boots O'Neal")
    registerPlayer(tournament, 0, "Cathy Burton")
    registerPlayer(tournament, 0, "Diane Grant")
    standings = playerStandings(tournament)
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(tournament, id1, id2, 0) # 0 refers to NOT DRAW
    reportMatch(tournament, id3, id4, 0) # 0 refers to NOT DRAW
    standings = playerStandings(tournament)
    for (i, n, w, m) in standings:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (id1, id3) and w != 1:
            raise ValueError("Each match winner should have one win recorded.")
        elif i in (id2, id4) and w != 0:
            raise ValueError("Each match loser should have zero wins recorded.")
    print "7. After a match, players have updated standings."


def testPairings():
    tournament = "Tennis"
    #deleteMatches(tournament, 0)
    deletePlayers(tournament, 0) # 0 refers to argument choice in deletePlayers.
    registerPlayer(tournament, 0, "Twilight Sparkle")
    registerPlayer(tournament, 0, "Fluttershy")
    registerPlayer(tournament, 0, "Applejack")
    registerPlayer(tournament, 0, "Pinkie Pie")
    standings = playerStandings(tournament)
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(tournament, id1, id2, 0) # 0 refers to NOT DRAW
    reportMatch(tournament, id3, id4, 0) # 0 refers to NOT DRAW
    pairings = swissPairings(tournament)
    if len(pairings) != 2:
        raise ValueError(
            "For four players, swissPairings should return two pairs.")
    [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4)] = pairings
    correct_pairs = set([frozenset([id1, id3]), frozenset([id2, id4])])
    actual_pairs = set([frozenset([pid1, pid2]), frozenset([pid3, pid4])])
    if correct_pairs != actual_pairs:
        raise ValueError(
            "After one match, players with one win should be paired.")
    print "8. After one match, players with one win are paired."


if __name__ == '__main__':
    testCreateAndDeleteTournament()
    testDeleteMatches()
    testDelete()
    testCount()
    testRegister()
    testRegisterCountDelete()
    testStandingsBeforeMatches()
    testReportMatches()
    testPairings()
    print "Success!  All tests pass!"
