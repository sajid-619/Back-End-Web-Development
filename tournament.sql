DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament

DROP TABLE IF EXISTS tournaments;
DROP TABLE IF EXISTS players;
DROP TABLE IF EXISTS participates;
DROP TABLE IF EXISTS matches;
DROP TABLE IF EXISTS wins;
DROP VIEW IF EXISTS player_pairs;
DROP VIEW IF EXISTS player_info;


CREATE TABLE tournaments (
                            id SERIAL PRIMARY KEY,
                            name VARCHAR(250)
                         );
CREATE TABLE players (
                            id SERIAL PRIMARY KEY,
                            name VARCHAR(250)
                     );

CREATE TABLE participates (
                            id SERIAL PRIMARY KEY,
                            t_id INT NOT NULL,
                            p_id INT NOT NULL,

                            CONSTRAINT fk_tournament
                            FOREIGN KEY (t_id)
                            REFERENCES tournaments (id),

                            CONSTRAINT fk_player
                            FOREIGN KEY (p_id)
                            REFERENCES players (id)
                          );

--second player id is not forcing to have a value so that we can do the swiss pairing of odd number of players, where a player can win against no one, and this way we'd keep track so that this happens only once, simply seeing if they have any matches against no one.
CREATE TABLE matches (
                            id SERIAL PRIMARY KEY,
                            round INT NOT NULL,
                            p_one_id INT NOT NULL,
                            p_two_id INT,
                            t_id INT NOT NUll,

                            CONSTRAINT fk_p_one_id
                            FOREIGN KEY (p_one_id)
                            REFERENCES players (id),

                            CONSTRAINT fk_t_id
                            FOREIGN KEY(t_id)
                            REFERENCES tournaments (id),

                            CONSTRAINT fk_p_two_id
                            FOREIGN KEY (p_two_id)
                            REFERENCES players (id)
                     );

CREATE TABLE wins (
                            id SERIAL PRIMARY KEY,
                            m_id INT NOT NULL,
                            p_id INT NOT NULL,

                            CONSTRAINT fk_m_id
                            FOREIGN KEY (m_id)
                            REFERENCES matches (id),

                            CONSTRAINT fk_p_id
                            FOREIGN KEY (p_id)
                            REFERENCES players(id)
                  );

CREATE VIEW player_info AS SELECT
                            p.id,
                            par.t_id AS tournaments,
                            p.name,
                                (SELECT COUNT(m.*) AS matches
                                FROM matches m
                                WHERE m.p_one_id = p.id OR m.p_two_id = p.id),
                            COUNT(wins.*) AS wins
                            FROM players p
                            LEFT JOIN participates par ON par.p_id = p.id
                            LEFT JOIN wins ON wins.p_id = p.id
                            GROUP BY p.id, par.t_id
                            ORDER BY wins;

CREATE VIEW player_pairs AS WITH seq AS
                            (SELECT
                                    p.id,
                                    p.name,
                                    p.wins,
                                    row_number() OVER (ORDER BY p.wins) AS seq
                                    FROM player_info p
                            )
			                SELECT
			                        p1.id AS id1,
			                        p1.name AS name1,
			                        p1.wins AS wins1,
			                        p2.id AS id2,
			                        p2.name AS name2,
			                        p2.wins AS wins2
		                            FROM seq p1
		                            JOIN seq p2
		                            ON p1.seq % 2 = 1
		                            AND p2.seq = p1.seq+1;
