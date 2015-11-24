# ------------------------------------------------------------------------------
# Name:         tournament_test
# Purpose:      Multiple functions for testing & debugging tournament.py
#
# Author:       Jordan Alexander Watt
#
# Modified:     24-11-2015
# Created:      13-11-2015
# ------------------------------------------------------------------------------

from tournament import *

# Test functions below will always delete previous database information
# and test different functions of tournament.py on a clean database


def testDeleteMatches():
    """Deletes all previous matches"""
    deleteMatches()
    print ("1. Old matches can be deleted.")


def testDeletePlayers():
    """Deletes all players"""
    deleteMatches()
    deletePlayers()
    print ("2. Player records can be deleted.")


def testDeleteTournaments():
    """Deletes all tournaments"""
    deleteTournaments()
    print ("3. Tournament records can be deleted.")


def testCount():
    """Test to see if countPlayers function works correctly"""
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
    """Test to see if registerPlayer function works correctly"""
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
    """Test to see if countPlayers function works correctly
       after editing players"""
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
    """Test to see if playerStandings function works correctly"""
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    registerPlayer("Melpomene Murray")
    registerPlayer("Randy Schwartz")
    standings = playerStandings()
    if len(standings) < 2:
        raise ValueError("Players should appear in playerStandings even before"
                         " they have played any matches.")
    elif len(standings) > 2:
        raise ValueError("Only registered players should appear in standings.")
    if len(standings[0]) != 4:
        raise ValueError("Each playerStandings row should have four columns.")
    [(id1, name1, matches1, wins1), (id2, name2, matches2, wins2)] = standings
    if matches1 != 0 or matches2 != 0 or wins1 != 0 or wins2 != 0:
        raise ValueError(
            "Newly registered players should have no matches or wins.")
    if set([name1, name2]) != set(["Melpomene Murray", "Randy Schwartz"]):
        raise ValueError("Registered players' names should appear in standings,"
                         " even if they have no matches played.")
    print ("7. Newly registered players appear in the standings with no matches.")


def testReportMatches():
    """Test to see if reportMatch function works correctly"""
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
    """Test to see if swissPairings function works correctly"""
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


def testSmallTournament(ties=False):
    """Simulates a 16 player tournament to test functionality

       Args:
            ties: True allows possible random ties. Default False
    """
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    registerPlayer("Alpha", "Small Tournament")

    # Saves id of new tournament created above
    tourney_id = getLatestTournament()
    contestants = ["Beta", "Gamma", "Delta", "Epsilon", "Zeta", "Eta",
                   "Theta", "Iota", "Kappa", "Lambda", "Mu", "Nu", "Xi",
                   "Omicron", "Pi"]

    # Registers every player in above list in the same tournament
    for name in contestants:
        registerPlayer(name, tourney_id)
    printTournamentStandings(tourney_id)

    # Repeats rounds until tournament concluded and False is returned
    while True:
        if not randomRound(tourney_id, ties):
            break


def testLargeTournament(ties=False):
    """Simulates a 64 player tournament to test functionality

       Args:
            ties: True allows possible random ties. Default False
    """
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    registerPlayer("Andromeda", "Large Tournament")

    # Saves id of new tournament created above
    tourney_id = getLatestTournament()
    contestants = ["Antilia", "Aquarius", "Aries", "Auriga", "Bootes",
                   "Caelum", "Camelopardalis", "Cancer", "Canis Major",
                   "Canis Minor", "Capricornus", "Carina", "Cassiopeia",
                   "Centaurus", "Cepheus", "Cetus", "Corona Australis",
                   "Corona Borealis", "Corvus", "Crater", "Cygnus",
                   "Delphinus", "Dorado", "Draco", "Equuleus", "Eridanus",
                   "Fornax", "Gemini", "Hercules", "Horologium", "Hydra",
                   "Indus", "Lacerta", "Leo", "Libra", "Lupus", "Lynx", "Lyra",
                   "Mensa", "Monoceros", "Norma", "Octans", "Ophiuchus",
                   "Orion", "Pegasus", "Perseus", "Pheonix", "Pisces", "Pyxis",
                   "Sagittarius", "Scorpius", "Sculptor", "Serpens", "Taurus",
                   "Telescopium", "Triangulum", "Tucana", "Ursa Major",
                   "Ursa Minor", "Vela", "Virgo", "Volans", "Vulpecula"]

    # Registers every player in above list in the same tournament
    for name in contestants:
        registerPlayer(name, tourney_id)
    printTournamentStandings(tourney_id)

    # Repeats rounds until tournament concluded and False is returned
    while True:
        if not randomRound(tourney_id, ties):
            break


def testDoubleTournament(ties=False):
    """Simultaneously simulates a 64 player tournament alongside a 16 player
       tournament alternating rounds to test ability to run multiple
       tournaments at once

       Args:
            ties: True allows possible random ties. Default False
    """
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    registerPlayer("Andromeda", "Large Tournament")

    # Saves id of new tournament created above seperate from second tournament
    tourney_id_l = getLatestTournament()
    contestants = ["Antilia", "Aquarius", "Aries", "Auriga", "Bootes",
                   "Caelum", "Camelopardalis", "Cancer", "Canis Major",
                   "Canis Minor", "Capricornus", "Carina", "Cassiopeia",
                   "Centaurus", "Cepheus", "Cetus", "Corona Australis",
                   "Corona Borealis", "Corvus", "Crater", "Cygnus",
                   "Delphinus", "Dorado", "Draco", "Equuleus", "Eridanus",
                   "Fornax", "Gemini", "Hercules", "Horologium", "Hydra"]

    # Registers every player in above list in the large tournament
    for name in contestants:
        registerPlayer(name, tourney_id_l)
    registerPlayer("Alpha", "Small Tournament")

    # Saves id of new tournament created above seperate from first tournament
    tourney_id_s = getLatestTournament()
    contestants = ["Beta", "Gamma", "Delta", "Epsilon", "Zeta", "Eta",
                   "Theta", "Iota", "Kappa", "Lambda", "Mu", "Nu", "Xi",
                   "Omicron", "Pi"]

    # Registers every player in above list in the small tournament
    for name in contestants:
        registerPlayer(name, tourney_id_s)
    contestants = ["Indus", "Lacerta", "Leo", "Libra", "Lupus", "Lynx", "Lyra",
                   "Mensa", "Monoceros", "Norma", "Octans", "Ophiuchus",
                   "Orion", "Pegasus", "Perseus", "Pheonix", "Pisces", "Pyxis",
                   "Sagittarius", "Scorpius", "Sculptor", "Serpens", "Taurus",
                   "Telescopium", "Triangulum", "Tucana", "Ursa Major",
                   "Ursa Minor", "Vela", "Virgo", "Volans", "Vulpecula"]

    # Registers second half of players for large tournament to show players
    # can be registered for any tournament in any order
    for name in contestants:
        registerPlayer(name, tourney_id_l)
    printTournamentStandings(tourney_id_l)
    printTournamentStandings(tourney_id_s)

    # Runs 7 rounds of both tournaments alternating between the two
    # after 4 rounds a winner will be determined for the small tournament
    # after 6 rounds a winner will be determined for the large tournament
    # shows that running rounds after a tournament has concluded will have
    # no effect and simply display the winner
    for i in range(7):
        if randomRound(tourney_id_l, ties):
            pass
        if randomRound(tourney_id_s, ties):
            pass


def printTournamentStandings(tourney_id):
    """Prints out tournamentStandings results in a clear format. This
       function is run every round to show tournament is running correctly

       Args:
            tourney_id: passes the unique id of a tournament so only results
                        from that tournament are returned
    """
    standings = tournamentStandings(tourney_id, False)
    print ("\n~~ TOURNAMENT STANDINGS ~~")
    for (i, n, m, w, t) in standings:
        output = ("MATCHES: {0}   WINS: {1}   TIES: {2}   ID: {3}   "
                  "NAME: {4}").format(m, w, t, i, n)
        print (output)


def randomRound(tourney_id, ties=False):
    """If swissPairings returns empty then there are no more possible rounds
       for the tournament. Otherwise will take every player pair and determine
       a winner and loser (or tie if enabled)

       Args:
            tourney_id: the unique id of the tournament this match is in
            ties: True allows possible random ties. Default False

       Returns:
            Boolean: False if no pairs are returned, True after a round
    """
    pairings = swissPairings(tourney_id)
    if pairings == [None]:
        return False
    else:
        for pair in pairings:

            # ties is false; no tied matches can occur tie will always be False
            # ties is True; tied matches can randomly occur
            # and will be reflected in variable tie being True
            [winner, loser, tie] = randomWinner(pair[0], pair[2], ties)

            # reportMatch will determine what to do if there is a tied match
            reportMatch(winner, loser, tourney_id, tie)
        printTournamentStandings(tourney_id)
        return True


def randomWinner(one, two, ties=False):
    """randomly determine a winner and loser (or tied match if enabled)

       Args:
            one: the unique id of a player in this match
            two: the unique id of the other player in this match
            ties: True has %10 chance of tied match occuring. Default False

       Returns:
            Returns the two unique ids in order, first "winner" of the match
            then "loser" of the match second. If boolean True is returned after
            ids then a tied match has occured.
    """
    rnd_no = random()
    if ties:
        if rnd_no < 0.45:
            return [one, two, False]
        elif rnd_no < 0.9:
            return [two, one, False]
        else:
            return [one, two, True]
    else:
        if rnd_no < 0.5:
            return [one, two, False]
        else:
            return [two, one, False]


if __name__ == '__main__':

    # Runs test functions and prints results
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
    print ("Success!  Small Tournament concluded")

    print ("Attempting randomly generated Large Tournament")
    testLargeTournament()
    print ("Success!  Large Tournament concluded")

    print ("Attempting Small Tournament with random ties")
    testSmallTournament(True)
    print ("Success!  Small Tournament concluded")

    print ("Attempting Small & Large Tournaments with random ties")
    testDoubleTournament(True)
    print ("Success!  both Tournaments concluded")
    print ("Success!  All tournaments successfully concluded!")
