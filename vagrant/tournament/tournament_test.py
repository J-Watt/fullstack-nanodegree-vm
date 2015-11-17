#!/usr/bin/env python
#
# Test cases for tournament.py
# Switched order of standings matches now after name

from tournament import *

def testDeleteMatches():
    deleteMatches()
    print ("1. Old matches can be deleted.")


def testDeletePlayers():
    deleteMatches()
    deletePlayers()
    print ("2. Player records can be deleted.")


def testDeleteTournaments():
    deleteTournaments()
    print ("3. Tournament records can be deleted.")


def testCount():
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    c = countPlayers()
    if c == '0':
        raise TypeError(
            "countPlayers() should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print ("4. After deleting, countPlayers() returns zero.")


def testRegister():
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    registerPlayer("Chandra Nalaar")
    c = countPlayers()
    if c != 1:
        raise ValueError(
            "After one player registers, countPlayers() should be 1.")
    print ("5. After registering a player, countPlayers() returns 1.")


def testRegisterCountDelete():
    deleteMatches()
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
    print ("6. Players can be registered and deleted.")


def testStandingsBeforeMatches():
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    registerPlayer("Melpomene Murray")
    registerPlayer("Randy Schwartz")
    standings = playerStandings()
    if len(standings) < 2:
        raise ValueError("Players should appear in playerStandings even before "
                         "they have played any matches.")
    elif len(standings) > 2:
        raise ValueError("Only registered players should appear in standings.")
    if len(standings[0]) != 4:
        raise ValueError("Each playerStandings row should have four columns.")
    [(id1, name1, matches1, wins1), (id2, name2, matches2, wins2)] = standings
    if matches1 != 0 or matches2 != 0 or wins1 != 0 or wins2 != 0:
        raise ValueError(
            "Newly registered players should have no matches or wins.")
    if set([name1, name2]) != set(["Melpomene Murray", "Randy Schwartz"]):
        raise ValueError("Registered players' names should appear in standings, "
                         "even if they have no matches played.")
    print ("7. Newly registered players appear in the standings with no matches.")


def testReportMatches():
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    registerPlayer("Bruno Walton")
    registerPlayer("Boots O'Neal")
    registerPlayer("Cathy Burton")
    registerPlayer("Diane Grant")
    standings = playerStandings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(id1, id2)
    reportMatch(id3, id4)
    standings = playerStandings()
    for (i, n, m, w) in standings:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (id1, id3) and w != 1:
            raise ValueError("Each match winner should have one win recorded.")
        elif i in (id2, id4) and w != 0:
            raise ValueError("Each match loser should have zero wins recorded.")
    print ("8. After a match, players have updated standings.")


def testPairings():
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    registerPlayer("Twilight Sparkle")
    registerPlayer("Fluttershy")
    registerPlayer("Applejack")
    registerPlayer("Pinkie Pie")
    standings = playerStandings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(id1, id2)
    reportMatch(id3, id4)
    pairings = swissPairings()
    if len(pairings) != 2:
        raise ValueError(
            "For four players, swissPairings should return two pairs.")
    [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4)] = pairings
    correct_pairs = set([frozenset([id1, id3]), frozenset([id2, id4])])
    actual_pairs = set([frozenset([pid1, pid2]), frozenset([pid3, pid4])])
    if correct_pairs != actual_pairs:
        raise ValueError(
            "After one match, players with one win should be paired.")
    print ("9. After one match, players with one win are paired.")


def testSmallTournament():
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    registerPlayer("Alpha", "Small Tournament")
    tourney_id = getLatestTournament()
    contestants = ["Beta", "Gamma", "Delta", "Epsilon", "Zeta", "Eta",
                   "Theta", "Iota", "Kappa", "Lambda", "Mu", "Nu", "Xi",
                   "Omicron", "Pi"]
    for name in contestants:
        registerPlayer(name, tourney_id)
    printTournamentStandings(tourney_id)
    while True:
        if not randomRound(tourney_id):
            break



def printTournamentStandings(tourney_id):
    standings = tournamentStandings(tourney_id, False)
    print ("\n~~ TOURNAMENT STANDINGS ~~")
    for (i, n, m, w, t) in standings:
        output = ("MATCHES: {0}   WINS: {1}   TIES: {2}   ID: {3}   "
                  "NAME: {4}").format(m, w, t, i, n)
        print (output)

def randomRound(tourney_id):
    pairings = swissPairings(tourney_id)
    if pairings == [None]:
        return False
    else:
        for pair in pairings:
            [winner, loser] = randomWinner(pair[0], pair[2])
            reportMatch(winner, loser, tourney_id, False)
        printTournamentStandings(tourney_id)
        return True

def randomWinner(one, two):
    if random() < 0.5:
        return [one, two]
    else:
        return [two, one]

if __name__ == '__main__':
    testDeleteMatches()
    testDeletePlayers()
    testDeleteTournaments()
    testCount()
    testRegister()
    testRegisterCountDelete()
    testStandingsBeforeMatches()
    testReportMatches()
    testPairings()
    print ("Success!  All tests pass!")
    print ("Attempting randomly generated Small Tournament")
    testSmallTournament()
##    print ("Success!  Small Tournament concluded")
##    print ("Attempting randomly generated Large Tournament")
##    testLargeTournament()
##    print ("Success!  Large Tournament concluded")
##    print ("Attempting simultaneous Small & Large Tournaments")
##    testDoubleTournament()
##    print ("Success!  both Tournaments concluded")


