DROP DATABASE IF EXISTS tournament; 
CREATE DATABASE tournament; 

DROP TABLE IF EXISTS players CASCADE;
create table players (
	player_id serial  PRIMARY KEY NOT NULL,
	player_name varchar(100) NOT NULL
	);

DROP TABLE IF EXISTS matches CASCADE;
create table matches (
	match_id serial PRIMARY KEY NOT NULL,
	id_player_a integer NOT NULL,
	id_player_b integer NOT NULL
	);

DROP TABLE IF EXISTS matchResults CASCADE;
create table matchResults (
	match_result_id serial PRIMARY KEY NOT NULL,
	match_id integer NOT NULL,
	player_id integer NOT NULL REFERENCES players(player_id),
	match_win integer NOT NULL default 0,
	match_loss integer NOT NULL default 0
	);

DROP VIEW IF EXISTS playerStandings CASCADE;
CREATE VIEW playerStandings AS (
	SELECT players.player_id AS id, players.player_name AS name, coalesce(playerSummary.wins,0) AS wins, coalesce(playerSummary.matches,0) AS matches  
	FROM players LEFT JOIN (SELECT player_id, SUM(match_win) AS wins, COUNT(player_id) AS matches 
		FROM matchResults GROUP BY player_id) playerSummary
	ON players.player_id = playerSummary.player_id
	ORDER BY playerSummary.wins DESC
	);
