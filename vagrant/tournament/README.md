  TOURNAMENT RESULTS
======================

Udacity  
Full Stack Web Developer Nanodegree: project two  
By Jordan Alexander Watt

Program and database schema designed to track the results of a Swiss-style
tournament. Capable of creating, reading, updating, and deleting data from
a database, calculating results and pairing matchups for rounds. Includes
a test program to show functionality.


Quick Start
-----------

Create a database using included `tournament.sql` in PostgreSQL. Run
`tournament_test.py` to make sure everything works correctly, it also
gives examples on how to interact with `tournament.py`.


What's Included
---------------

Tournament
* tournament.py
* tournament_test.py
* tournament.sql
* README.md


Usage
-----

**Note:**
Python necessary to run `.py` files. Programs written using Python 3.
Psycopg2 used within python modules. SQL file written using PostgreSQL.

#####SQL Schema:
Edit `tournament.sql` should changes be necessary. Import into PSQL or
copy lines from the file and setup the database for use with `tournament.py`.

#####Tournament:
`tournament.py` can be changed to suit different tournament needs.
follow the comments within the file.

#####Tournament_Test:
Run `touranment_test.py` to ensure the database and program are working
correctly. This file can be used as a guide to see how to make other
programs interact with `tournament.py`, following the comments.


Features
--------

Supported features
* Any size tournaments
  * No maximum number of entrants
  * Can have odd number of entrants
* Automatic matchmaking
  * Pairs entrants based on wins then ties
  * Will avoid pairing entrants who have previously been matched
* Bye capability
  * Can record a win (or loss/tie) with no opponent
  * Automatically assigns byes with odd numbers
* Tie capability
  * Supports tied games and weights ties when matchmaking
* Multiple tournaments
  * Can record multiple tournaments simultaneously
  * An entrant can register and compete in multiple 
    tournaments simultaneously
* Statistics
  * Statistics for players total records or tournament specific records
  * Statistics for all tournaments records or a specific tournament


Planned Features
----------------

Planned for version 1.1
* Final Results
  * Currently:
    * `tournament.py` will only print the first place champion
      at the conclusion of a tournament. Final placements must be 
      determined in the client software by reading the tournament 
      standings output
  * Planned:
    * `tournament.py` will output the results clearly declaring
      First place, Second place, Third place... etc.
* Opponent match wins weighting
  * Currently:
    * During matchmaking when there is an odd number of players
      with `x` wins, it will draw from the players with the
      next highest wins prioritizing players with highest
      ties. It will not take into account OMW. Also when
      printing the champion during the swissPairings function 
      it will not take into account OMW, therefor if players are
      tied with the most wins and the most ties it will print
      one of them without adjusting for OMW or declaring a tie.
  * Planned:
    * Prioritizing OMW when looking at players with an equal
      number of wins and ties.

Planned for future versions
* Hall of Fame
  * Recording First, Second, and Third place after a tournament
    concludes along with their stats in the database.


Bug Reports
-----------

* No currently known bugs.
* **Note:** When players are tied for first place, calling swiss Pairings
  will pick one player to print as the champion. This is not a bug
  as the final results is meant to be determined based on the 
  tournament standings output within the client software using 
  their prefered methods of determing a winner. An output within
  `tournament.py` for calculating the final placements is a 
  "planned feature".

Please report any bugs to JordanAlexWatt@hotmail.com


Versioning
----------

Tournament 1.0
* tournament.py - created *13/11/15*
* tournament_test.py - created *13/11/15*
* tournament.sql - created *13/11/15*



Credits
-------

Tournament Results written by Jordan Alexander Watt (JAW)
following udacity course lectures. - JordanAlexWatt@hotmail.com

`tournament.py` and `tournament_test.py` frame and guidelines created by
Udacity and can be found [here]
(https://github.com/udacity/fullstack-nanodegree-vm)

 
#####Supporting Resources  

[Udacity](http://www.udacity.com)

[Python](https://www.python.org/)

[PostgreSQL](http://www.postgresql.org/)

[Psycopg2](http://initd.org/psycopg/)


***

*Last edited November 26 2015*