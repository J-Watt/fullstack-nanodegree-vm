-- ----------------------------------------------------------------------------
-- 
-- Name: tournament
-- Purpose: Hosting multiple swiss style tournaments and showing results
-- 
-- Author: Jordan Alexander Watt
-- 
-- Modified: 24-11-2015
-- Created: 13-11-2015
-- 
-- ----------------------------------------------------------------------------

-- Create database named tournament and connect to it
CREATE DATABASE tournament;
\c tournament;

-- Create table Players including automatic unique id keys
CREATE TABLE Players (
    id serial PRIMARY KEY,
    name text
);

-- Create table Tourneys with automatic unique id keys
CREATE SEQUENCE tourneys_id_seq START 1001;
CREATE TABLE Tourneys (
    id integer DEFAULT nextval('tourneys_id_seq') PRIMARY KEY,
    name text
);
ALTER SEQUENCE tourneys_id_seq OWNED BY Tourneys.id;

-- Create table Contestants referencing foreign id key in Players and Tourneys
CREATE TABLE Contestants (
    tourney_id integer REFERENCES Tourneys (id) ON DELETE CASCADE,
    player_id integer REFERENCES Players (id) ON DELETE CASCADE,
    UNIQUE (tourney_id, player_id)
);

-- Create table Matches referencing foreign id key in Players and Tourneys
CREATE TABLE Matches (
    tourney_id integer REFERENCES Tourneys (id) ON DELETE CASCADE,
    id_winner integer NULL DEFAULT NULL REFERENCES Players (id) ON DELETE RESTRICT,
    id_loser integer NULL DEFAULT NULL REFERENCES Players (id) ON DELETE RESTRICT,
    id_tie_a integer NULL DEFAULT NULL REFERENCES Players (id) ON DELETE RESTRICT,
    id_tie_b integer NULL DEFAULT NULL REFERENCES Players (id) ON DELETE RESTRICT,
    CHECK ((id_winner != id_loser) OR (id_winner != id_loser) IS NULL),
    CHECK ((id_tie_a != id_tie_b) OR (id_tie_a != id_tie_b) IS NULL)
);

-- Create view Past_Pairings to view all previous matchups
CREATE VIEW Past_Pairings AS
    SELECT previous.tourney_id, previous.id_one, pa.name as name_one, 
           previous.id_two, pb.name as name_two 
    FROM (SELECT tourney_id, 
          COALESCE(id_winner, id_tie_a) as id_one, 
          COALESCE(id_loser, id_tie_b) as id_two FROM Matches) as previous 
    JOIN Players AS pa ON previous.id_one = pa.id 
    JOIN Players AS pb ON previous.id_two = pb.id;
    
-- Create view Standings to view player statistics from matchups
CREATE VIEW Standings AS
    SELECT Contestants.tourney_id, Tourneys.name as tourney_name,
           Contestants.player_id, Players.name, matched.matches,
           win.wins, lose.loses, tie.ties
    FROM Contestants
    LEFT JOIN (SELECT Contestants.tourney_id, Contestants.player_id,
               COUNT(Matches.*) as matches
               FROM Contestants
               LEFT JOIN Matches 
               ON Contestants.tourney_id = Matches.tourney_id
               AND Contestants.player_id
               IN (Matches.id_winner, Matches.id_loser, Matches.id_tie_a,
                   Matches.id_tie_b)
               GROUP BY Contestants.player_id, Contestants.tourney_id)
    as matched ON Contestants.tourney_id = matched.tourney_id
               AND Contestants.player_id = matched.player_id
    LEFT JOIN (SELECT Contestants.tourney_id, Contestants.player_id,
               COUNT(Matches.id_winner) as wins
               FROM Contestants
               LEFT JOIN Matches
               ON Contestants.tourney_id = Matches.tourney_id
               AND Contestants.player_id = Matches.id_winner
               GROUP BY Contestants.tourney_id, Contestants.player_id)
    as win ON Contestants.tourney_id = win.tourney_id
           AND Contestants.player_id = win.player_id
    LEFT JOIN (SELECT Contestants.tourney_id, Contestants.player_id,
               COUNT(Matches.id_loser) as loses
               FROM Contestants
               LEFT JOIN Matches
               ON Contestants.tourney_id = Matches.tourney_id
               AND Contestants.player_id = Matches.id_loser
               GROUP BY Contestants.tourney_id, Contestants.player_id)
    as lose ON Contestants.tourney_id = lose.tourney_id
            AND Contestants.player_id = lose.player_id
    LEFT JOIN (SELECT Contestants.tourney_id, Contestants.player_id,
               COUNT(ma.id_tie_a) + COUNT(mb.id_tie_b) as ties
               FROM Contestants
               LEFT JOIN Matches as ma
               ON Contestants.tourney_id = ma.tourney_id
               AND Contestants.player_id = ma.id_tie_a
               LEFT JOIN Matches as mb
               ON Contestants.tourney_id = mb.tourney_id
               AND Contestants.player_id = mb.id_tie_b
               GROUP BY Contestants.tourney_id, Contestants.player_id)
    as tie ON Contestants.tourney_id = tie.tourney_id
           AND Contestants.player_id = tie.player_id
    JOIN Tourneys ON Contestants.tourney_id = Tourneys.id
    JOIN Players ON Contestants.player_id = Players.id
    ORDER BY Contestants.tourney_id, Contestants.player_id;
