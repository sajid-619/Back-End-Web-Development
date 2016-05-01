-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP TABLE IF EXISTS player CASCADE;
create table player (
	player_id bigserial  NOT NULL,
	player_name varchar(100) NOT NULL,

	CONSTRAINT player_pk PRIMARY KEY(player_id)
);

DROP TABLE IF EXISTS match CASCADE;
create table match (
	match_id bigserial  NOT NULL,
	a_player_id integer NOT NULL,
	b_player_id integer NOT NULL,
	match_datetime timestamp with time zone NULL DEFAULT now(),
	CONSTRAINT match_pk PRIMARY KEY(match_id)
);

DROP TABLE IF EXISTS matchresult CASCADE;
create table matchresult (
	matchresult_id bigserial  NOT NULL,
	match_id integer NOT NULL,
	player_id integer NOT NULL,
	win integer NOT NULL default 0,
	lose integer NOT NULL default 0,
	tie integer NOT NULL default 0,
	CONSTRAINT matchresult_pk PRIMARY KEY(matchresult_id)
);

DROP TABLE IF EXISTS playerstandings CASCADE;
CREATE VIEW playerstandings as
(
	SELECT player.player_id, player.player_name, coalesce(playersummary.winno,0) as wins, coalesce(playersummary.matchno,0) as matches  
	FROM player LEFT JOIN
	(SELECT player_id, sum(win) as winno, count(player_id) as matchno 
	FROM matchresult GROUP BY player_id) playersummary 
	ON player.player_id = playersummary.player_id
	ORDER BY playersummary.winno DESC
);
