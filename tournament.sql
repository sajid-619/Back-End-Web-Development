-- Table definitions for the tournament project.

-- Delet any existing DB with name 'tournament' and create new one.
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;

-- connect to database
\c tournament;

-- create players and matches table
CREATE TABLE players (id serial PRIMARY KEY,
                      name text);

CREATE TABLE matches (winner integer REFERENCES players(id),
                      loser integer REFERENCES players(id),
                      PRIMARY KEY (winner, loser));

-- create views to determine wins, total matches, and a combined standings
CREATE VIEW wins AS SELECT id, count(winner) AS wins FROM players
    LEFT JOIN matches ON id = winner GROUP BY id;

CREATE VIEW totalMatches AS SELECT id, count (matches) AS matches FROM players
    LEFT JOIN matches ON id = winner or id = loser GROUP BY id;

CREATE VIEW standings AS SELECT players.id, name, wins, matches,
    row_number() OVER(ORDER BY wins DESC, name) AS row
    FROM players
        LEFT JOIN wins ON players.id = wins.id
        LEFT JOIN totalMatches ON players.id = totalMatches.id
    ORDER BY wins DESC, name;

CREATE VIEW player1 AS SELECT id AS id1, name AS name1, row FROM standings
    WHERE row % 2 = 1;

CREATE VIEW player2 AS SELECT id AS id2, name AS name2, row FROM standings
    EXCEPT SELECT * FROM player1;

CREATE VIEW pairings AS SELECT DISTINCT ON (player1.row) id1, name1, id2, name2
    FROM player1, player2
    WHERE player1.row = (player2.row - 1) ORDER BY player1.row;

insert into players values (default, 'Stephan Koenig');
insert into players values (default, 'Bridgette Clarkston');
insert into players values (default, 'Brodie Lodmell');
insert into players values (default, 'Chris Stark');
insert into players values (default, 'Sebastian Gornik');
insert into players values (default, 'Stella Koenig');
insert into matches values (1, 2);
insert into matches values (3, 4);
insert into matches values (5, 6);
insert into matches values (6, 1);
