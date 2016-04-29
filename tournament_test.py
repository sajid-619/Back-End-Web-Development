#!/usr/bin/env python
#
# Test cases for tournament.py

from tournament import *

def testDeleteMatches():
    deleteWins()
    deleteMatches()
    print "1. Old matches can be deleted."

def testDeleteWins():
    deleteWins()
    print " Old wins can be deleted."

def testDelete():
    deleteWins()
    deleteMatches()
    deleteParticipates()
    deletePlayers()
    deleteTournaments()
    print "2. Player records can be deleted."

def testDeleteTournaments():
    deleteParticipates()
    deleteTournaments()
    print "Tournaments can be deleted."

def testDeleteParticipates():
    deleteParticipates()
    print"Participates can be deleted."

def testCount():
    deleteWins()
    deleteMatches()
    deleteParticipates()
    deletePlayers()
    deleteTournaments()
    c = countPlayers()
    if c == '0':
        raise TypeError(
            "countPlayers() should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "3. After deleting, countPlayers() returns zero."


def testRegister():
    deleteWins()
    deleteMatches()
    deleteParticipates()
    deletePlayers()
    deleteTournaments()
    registerPlayer("Chandra Nalaar")
    c = countPlayers()
    if c != 1:
        raise ValueError(
            "After one player registers, countPlayers() should be 1.")
    print "4. After registering a player, countPlayers() returns 1."


def testRegisterCountDelete():
    deleteWins()
    deleteMatches()
    deleteParticipates()
    deletePlayers()
    deleteTournaments()
    registerPlayer("Markov Chaney")
    registerPlayer("Joe Malik")
    registerPlayer("Mao Tsu-hsi")
    registerPlayer("Atlanta Hope")
    c = countPlayers()
    if c != 4:
        raise ValueError(
            "After registering four players, countPlayers should be 4.")
    deletePlayers()
    c = countPlayers()
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "5. Players can be registered and deleted."


# when checking for amount of columns in playerStandings added 1 more, as I keep track of the tournament we're talking about.
# added t_id as a param to the playerStandings(t_id) function.
# separates player standings per tournament, so the same players can participate multiple years
def testStandingsBeforeMatches():
    deleteWins()
    deleteMatches()
    deleteParticipates()
    deletePlayers()
    deleteTournaments()
    t_id = createTournament("Testy")
    p1_id = registerPlayer("Melpomene Murray")
    p2_id = registerPlayer("Randy Schwartz")
    registerParticipant(t_id,p1_id)
    registerParticipant(t_id,p2_id)
    standings = playerStandings(t_id)
    print "standings length %s" % (len(standings[0]),)
    if len(standings) < 2:
        raise ValueError("Players should appear in playerStandings even before "
                         "they have played any matches.")
    elif len(standings) > 2:
        raise ValueError("Only registered players should appear in standings.")
    if len(standings[0]) != 5:
        raise ValueError("Each playerStandings row should have four columns.")
    [(id1, tournament1, name1, matches1,wins1), (id2,tournament2, name2, matches2,wins2)] = standings
    if matches1 != 0 or matches2 != 0 or wins1 != 0 or wins2 != 0:
        raise ValueError(
            "Newly registered players should have no matches or wins.")
    if set([name1, name2]) != set(["Melpomene Murray", "Randy Schwartz"]):
        raise ValueError("Registered players' names should appear in standings, "
                         "even if they have no matches played.")
    print "6. Newly registered players appear in the standings with no matches."

def testCreateTournament():
    c = countTournaments()
    if c > 0:
        print "We already have %s tournaments" % (c,)
    createTournament("Baloony");
    d = countTournaments()
    if c < d:
        print "It worked! We now have %s tournaments" % (d,)
    else:
        print "Did not work, we still have %s tournaments" % (d,)

def testReportMatches():
    deleteWins()
    deleteMatches()
    deleteParticipates()
    deletePlayers()
    deleteTournaments()

    t_id = createTournament("Testy")
    p1_id = registerPlayer("Bruno Walton")
    p2_id = registerPlayer("Boots O'Neal")
    p3_id = registerPlayer("Cathy Burton")
    p4_id = registerPlayer("Diane Grant")

    registerParticipant(t_id,p1_id)
    registerParticipant(t_id,p2_id)
    registerParticipant(t_id,p3_id)
    registerParticipant(t_id,p4_id)

    reportMatch(p1_id, p2_id, False)
    reportMatch(p3_id, p4_id, False)
    standings = playerStandings(t_id)
    #[id1, id2, id3, id4] = [row[0] for row in standings]
    for (i,t, n, m, w) in standings:
       # print "STARTS"
       # print i
       # print n
       # print w
       # print m
       # print "ENDS"
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (p1_id, p3_id) and w != 1:
            raise ValueError("Each match winner should have one win recorded.")
        elif i in (p2_id, p4_id) and w != 0:
            raise ValueError("Each match loser should have zero wins recorded.")
    print "7. After a match, players have updated standings."


def testPairings():
    deleteWins()
    deleteMatches()
    deleteParticipates()
    deletePlayers()
    deleteTournaments()

    t_id = createTournament("Testy")
    p1_id = registerPlayer("Twilight Sparkle")
    p2_id = registerPlayer("Fluttershy")
    p3_id = registerPlayer("Applejack")
    p4_id = registerPlayer("Pinkie Pie")

    registerParticipant(t_id,p1_id)
    registerParticipant(t_id,p2_id)
    registerParticipant(t_id,p3_id)
    registerParticipant(t_id,p4_id)

    standings = playerStandings(t_id)
    #[id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(p1_id, p2_id, False, t_id)
    reportMatch(p3_id, p4_id, False, t_id)
    pairings = swissPairings()
    if len(pairings) != 2:
        raise ValueError(
            "For four players, swissPairings should return two pairs.")
    [(pid1, pname1,wins1, pid2, pname2,wins2), (pid3, pname3,wins3, pid4, pname4,wins4)] = pairings
    correct_pairs = set([frozenset([p1_id, p3_id]), frozenset([p2_id, p4_id])])
    actual_pairs = set([frozenset([pid1, pid2]), frozenset([pid3, pid4])])
    if correct_pairs != actual_pairs:
        raise ValueError(
            "After one match, players with one win should be paired.")
    print "8. After one match, players with one win are paired."


if __name__ == '__main__':
    testDeleteMatches()
    testDelete()
    testDeleteParticipates()
    testDeleteTournaments()
    testCount()
    testRegister()
    testCreateTournament()
    testRegisterCountDelete()
    testStandingsBeforeMatches()
    testReportMatches()
    testPairings()
    print "Success!  All tests pass!"

