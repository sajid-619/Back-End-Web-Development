-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;

\c tournament

DROP TABLE IF EXISTS players CASCADE;
DROP TABLE IF EXISTS tournaments CASCADE;
DROP TABLE IF EXISTS tournament_games CASCADE;
--DROP VIEW IF EXISTS matches CASCADE;
--DROP VIEW IF EXISTS wins CASCADE;
DROP VIEW IF EXISTS standings CASCADE;


-- Stores player names with their ids. Names not unique
CREATE TABLE players (
						player_id serial primary key,
						name varchar not null
					);


-- Lists players for each tournament.The player has a bye win or not.
CREATE TABLE tournaments (
  							tournament_name text,
  							player_id integer references players,
  							bye_win BOOLEAN DEFAULT false,
  							PRIMARY KEY (tournament_name, player_id) 
						);


--Results of all matches for all tournament_games. Draw is supported.

CREATE TABLE tournament_games (
						tournament_name varchar,
						game_id serial,
						player1_id integer,
						player2_id integer,
						winner_id integer default null,
						draw BOOLEAN default false,
						CONSTRAINT winner CHECK((draw AND winner_id IS NULL) OR (NOT draw AND winner_id IS NOT NULL)),
						PRIMARY KEY (tournament_name, game_id),
						FOREIGN KEY (tournament_name, player1_id) references tournaments,
						FOREIGN KEY (tournament_name, player2_id) references tournaments
					);

--CREATE TABLE tournament_records (

--						tournament varchar references tournaments (name),
--						players_id varchar references players (id),
--					);
--


-- Aggregates data for each player in each tournament. Wins are calculated as 2 points per win, 1 per draw.
CREATE VIEW standings AS 
		SELECT tournaments.tournament_name, tournaments.player_id,
		count(CASE WHEN (tournaments.player_id = tournament_games.player1_id OR tournaments.player_id = tournament_games.player2_id) THEN 1 END) AS matches,
		count(CASE WHEN tournament_games.winner_id = tournaments.player_id THEN 1 END) AS wins,
		count(CASE WHEN tournament_games.winner_id = tournaments.player_id THEN 1 END) AS draws,
		count(CASE WHEN tournament_games.winner_id = tournaments.player_id THEN 2 WHEN tournament_games.draw = true THEN 1 END) AS points
		FROM tournaments left join tournament_games
		ON tournament_games.tournament_name = tournaments.tournament_name 
		AND (tournaments.player_id = tournament_games.player1_id OR tournaments.player_id = tournament_games.player2_id)
		GROUP BY tournaments.tournament_name, tournaments.player_id
		ORDER BY tournament_name ASC, points DESC;



--LEFT JOIN tournament_games 
--ON tournaments.tournament_name = tournament_games.tournament_name 
--AND (tournaments.player_id = tournament_games.player1_id OR tournaments.player_id = tournaments_games.player2_id)

