-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Create database named tournament and connect to it
CREATE DATABASE tournament;
\c tournament;

-- Create table Players with 
CREATE TABLE Players (
    id serial PRIMARY KEY,
    name text
);

-- Create table Tourneys with 
CREATE SEQUENCE tourneys_id_seq START 1001;
CREATE TABLE Tourneys (
    id integer DEFAULT nextval('tourneys_id_seq') PRIMARY KEY,
    name text
);
ALTER SEQUENCE tourneys_id_seq OWNED BY Tourneys.id;

-- Create table Contestants with 
CREATE TABLE Contestants (
    tourney_id integer REFERENCES Tourneys (id) ON DELETE CASCADE,
    player_id integer REFERENCES Players (id) ON DELETE CASCADE,
    UNIQUE (tourney_id, player_id)
);

-- Create table Matches with 
CREATE TABLE Matches (
    tourney_id integer REFERENCES Tourneys (id) ON DELETE CASCADE,
    round integer NOT NULL DEFAULT 1,
    id_winner integer NULL DEFAULT NULL REFERENCES Players (id) ON DELETE RESTRICT,
    id_loser integer NULL DEFAULT NULL REFERENCES Players (id) ON DELETE RESTRICT,
    id_tie_a integer NULL DEFAULT NULL REFERENCES Players (id) ON DELETE RESTRICT,
    id_tie_b integer NULL DEFAULT NULL REFERENCES Players (id) ON DELETE RESTRICT,
    CHECK ((id_winner != id_loser) OR (id_winner != id_loser) IS NULL),
    CHECK ((id_tie_a != id_tie_b) OR (id_tie_a != id_tie_b) IS NULL)
);

-- 45678901234567890123456789012345678901234567890123456789012345678901234567890
-- Create view Stats with
CREATE VIEW Standings AS
    SELECT Contestants.tourney_id, Tourneys.name as tourney_name,
           Contestants.player_id, Players.name, matched.matches,
           win.wins, lose.loses, tie.ties
    FROM Contestants
    LEFT JOIN (SELECT Contestants.tourney_id, Contestants.player_id,
               COUNT(Matches.round) as matches
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



-- Player total stats
-- SELECT player_id, name, SUM(matches) as matches, SUM(wins) as wins, SUM(loses) as loses, SUM(ties) as ties FROM standings GROUP BY player_id, name ORDER BY player_id;


-- Tournament total stats
-- SELECT tourney_id, tourney_name, CAST(SUM(matches)/2 as integer), SUM(wins), SUM(loses), SUM(ties) FROM standings GROUP BY tourney_id, tourney_name;
