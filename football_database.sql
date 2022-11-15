-- WEEK 2 EXAMPLES

-- kill other connections
SELECT pg_terminate_backend(pg_stat_activity.pid)
FROM pg_stat_activity
WHERE pg_stat_activity.datname = 'football_database' AND pid <> pg_backend_pid();
-- (re)create the database
DROP DATABASE IF EXISTS football_database;
CREATE DATABASE football_database;
-- connect via psql
\c football_database

-- database configuration
SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET default_tablespace = '';
SET default_with_oids = false;

-- TABLES

-- PLAYER TABLE
CREATE TABLE players (
    id SERIAL PRIMARY KEY,
    birth_year INT, 
    first_name TEXT NOT NULL, 
    last_name TEXT NOT NULL,
    committed_nation INT,
    club_team INT,
    national_team INT
);

-- BRIDGE TABLE FOR PLAYERS - TEAMS RELATIONSHIP (MtM) 
CREATE TABLE player_teams(
    player_id INT, 
    team_id INT, 
    PRIMARY KEY (player_id, team_id)
);

-- TEAM TABLE 
CREATE TABLE teams (
    id SERIAL PRIMARY KEY, 
    team_name TEXT UNIQUE NOT NULL, 
    national_team BOOL NOT NULL, 
    manager_name TEXT,
    home_stadium INT
);

-- BRIDGE TABLE FOR TEAMS - STADIUMS RELATIONSHIP (MtM)
CREATE TABLE teams_stadiums(
    stadium_id INT,
    teams_id INT,
    PRIMARY KEY (stadium_id, teams_id)
);

-- LEAGUE TABLE
CREATE TABLE leagues (
    id SERIAL PRIMARY KEY, 
    commissioner TEXT,
    calendar_year INT NOT NULL
);

-- BRIDGE TABLE FOR TEAMS - LEAGUES RELATIONSHIP (MtM) 
CREATE TABLE teams_leagues(
    league_id INT, 
    team_id INT, 
    PRIMARY KEY (league_id, team_id)
);

-- GAMES TABLE
CREATE TABLE games (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,  
    attendance INT,
    home_team INT NOT NULL,
    away_team INT NOT NULL, 
    league INT,
    referee INT NOT NULL,
    stadium INT
);

-- REFEREE TABLE 
CREATE TABLE referees (
    id SERIAL PRIMARY KEY, 
    name TEXT NOT NULL, 
    leagues_registered INT
);

-- PLAYABLE STADIUMS 
CREATE TABLE stadiums (
    id SERIAL PRIMARY KEY, 
    stadium_name TEXT NOT NULL,
    max_capcity INT, 
    city TEXT NOT NULL,
    nation INT
);

-- NATIONS TABLE
CREATE TABLE nations (
    id SERIAL PRIMARY KEY, 
    full_name TEXT NOT NULL, 
    nation_abbreviation CHAR(3) NOT NULL, 
    national_team INT UNIQUE
);

-- BRIDGE TABLE FOR GAMES - TEAMS RELATIONSHIP (MtM) 
CREATE TABLE teams_games(
    games_id INT, 
    home_team_id INT,
    away_team_id INT, 
    PRIMARY KEY (games_id, home_team_id, away_team_id)
);

-- ALTER TABLES - FOREIGN KEYS 
ALTER TABLE players
ADD CONSTRAINT fk_nation
    FOREIGN KEY (committed_nation)
    REFERENCES nations(id)
    ON DELETE SET NULL, 
ADD CONSTRAINT fk_club_team
    FOREIGN KEY (club_team)
    REFERENCES teams(id)
    ON DELETE SET NULL,
ADD CONSTRAINT fk_national_team
    FOREIGN KEY (national_team)
    REFERENCES teams(id)
    ON DELETE SET NULL;

ALTER TABLE player_teams
ADD CONSTRAINT fk_player_id
    FOREIGN KEY (player_id)
    REFERENCES players(id)
    ON DELETE SET NULL,
ADD CONSTRAINT fk_team_id
    FOREIGN KEY (team_id)
    REFERENCES teams(id)
    ON DELETE SET NULL;

ALTER TABLE teams
ADD CONSTRAINT fk_stadiums
    FOREIGN KEY (home_stadium)
    REFERENCES stadiums(id)
    ON DELETE SET NULL;

ALTER TABLE teams_stadiums
ADD CONSTRAINT fk_stadium_id
    FOREIGN KEY (stadium_id)
    REFERENCES stadiums(id)
    ON DELETE SET NULL,
ADD CONSTRAINT fk_teams_id
    FOREIGN KEY (teams_id)
    REFERENCES teams(id)
    ON DELETE SET NULL;

ALTER TABLE teams_leagues
ADD CONSTRAINT fk_league_id
    FOREIGN KEY (league_id)
    REFERENCES leagues(id)
    ON DELETE SET NULL,
ADD CONSTRAINT fk_team_id
    FOREIGN KEY (team_id)
    REFERENCES teams(id)
    ON DELETE SET NULL;

ALTER TABLE games 
ADD CONSTRAINT fk_league
    FOREIGN KEY (league)
    REFERENCES leagues(id)
    ON DELETE SET NULL,
ADD CONSTRAINT fk_referee  
    FOREIGN KEY (referee)
    REFERENCES referees(id)
    ON DELETE SET NULL,
ADD CONSTRAINT fk_stadiums  
    FOREIGN KEY (stadium)
    REFERENCES stadiums(id)
    ON DELETE SET NULL;

ALTER TABLE referees
ADD CONSTRAINT fk_leagues_registered
    FOREIGN KEY (leagues_registered)
    REFERENCES leagues(id)
    ON DELETE SET NULL;

ALTER TABLE stadiums 
ADD CONSTRAINT fk_nation
    FOREIGN KEY (nation)
    REFERENCES nations(id)
    ON DELETE SET NULL;

ALTER TABLE nations 
ADD CONSTRAINT fk_national_team 
    FOREIGN KEY (national_team)
    REFERENCES nations(id)
    ON DELETE SET NULL;

ALTER TABLE teams_games
ADD CONSTRAINT fk_games_id
    FOREIGN KEY (games_id)
    REFERENCES games(id)
    ON DELETE SET NULL,
ADD CONSTRAINT fk_home_team_id
    FOREIGN KEY (home_team_id)
    REFERENCES teams(id)
    ON DELETE SET NULL,
ADD CONSTRAINT fk_away_team_id
    FOREIGN KEY (away_team_id)
    REFERENCES teams(id)
    ON DELETE SET NULL;

-- INSERT INTO TABLES

INSERT INTO nations (full_name, nation_abbreviation)
VALUES ('Canada', 'CAN'), 
('United States of America', 'USA'), 
('Germany', 'GER'), 
('England', 'GBR'),
('Portugal', 'POR'), 
('Spain', 'ESP'),
('Belgium', 'BEL');

INSERT INTO stadiums (stadium_name, max_capcity, city, nation)
VALUES('BMO Field', 45000, 'Toronto', 1), 
('Robert F. Kennedy Memorial Stadium', 45596, 'Washington', 2),
('Allianz Arena', 75024, 'Munich', 3),
('Wembley Stadium', 90000, 'London', 4), 
('Estádio do Sport Lisboa e Benfica', 65000, 'Lisbon', 5),
('Santiago Bernabéu Stadium', 81044, 'Madrid', 6),
('Estádio do Dragão', 52000, 'Porto', 5),
('Jan Breydel Stadium', 29062, 'Bruges', 7);


INSERT INTO teams (team_name, national_team, manager_name, home_stadium)
VALUES ('Canadian National Team', TRUE, 'John Herdman', 1), 
('American National Team', TRUE, 'Gregg Berhalter', 2), 
('German National Team', TRUE, 'Hansi Flick', 3), 
('English National Team', TRUE, 'Gareth Southgate', 4),
('Portuguese National Team', TRUE, 'Fernando Santos', 5), 
('Spanish National Team', TRUE, 'Luis Enrique', 6), 
('FC Bayern Munich', FALSE, 'Julian Nagelsman', 3),
('FC Porto', FALSE, 'Sérgio Conceição', 7), 
('Club Brugge KV', FALSE, '	Carl Hoefkens', 8);

-- ('FC Barcelona', FALSE, 'Xavier Hernández Creus', 'Camp Nou'),
-- ('Chelsea FC', FALSE, 'Graham Potter', 'Stamford Bridge'), 
-- ('Manchester City FC', FALSE, 'Pep Guardiola', 'City of Manchester Stadium'), 


INSERT INTO players (birth_year, first_name, last_name, committed_nation, club_team, national_team)
VALUES (2000, 'Alphonso', 'Davies', 1, 7, 1),
    (1999, 'Tajon', 'Buchanan', 1, 9, 1),
    (1996, 'Stephen', 'Eustáquio', 1, 8, 1);

-- (1994, 'Maxime', 'Crépeau', 1, 'Los Angeles FC', 'Canadian National Team'), 
-- (1997, 'Dayne', 'St. Clair', 1, 'Minnesota United', 'Canadian National Team'),
-- (1987, 'Milan', 'Borjan', 1, 'Red Star Belgrade', 'Canadian National Team');





