Football/Soccer Database 

Description - This is a football/soccer database to store key information about matches/games, players, teams, leagues, nations, referees and more. This is utilizing a Postgres database to construct a REST API with Flask along with other tools like Alembic, Flask's SQLalchemy and Insomnia. The database has 10 distinct relationships including four many-to-many tables, for one-to-many tables and two one-to-one tables with more details provided below. I decided to use a ORM over raw SQL to better understand how ORMs worked (I essentially wanted to learn more). The REST API has 16 endpoints which include four POST requests, seven GET requests, four DELETE requests and one PATCH/PUT request. 

Please note this is not a complete REST API project and I would still like to work on it more.  

* - Needs Further Review 
*** - High Importance Review 
*(A Number) - Additional Notes 


Database Entity Relationships:
1) Players - Teams (MtM) 
    requires a bridge table named players_teams with PK consisting of a tuple of FKs
2) Players - Nations (1tM): One nation has many players, players can only play for one nation 
    requires a FK in the players table 
3) Teams - Nations (1t1): A nation can only have one (at most) national team, and a team can only represent one nation (at most)
    requires a FK in either table but must be UNIQUE 
    we will place the FK in the nations table 
4) Nations - Stadiums (1tM): One nation has many stadiums, a stadium can be in at most one nation
    requires a FK in the stadiums table 
*5) Teams - Stadiums (MtM): Many teams play in many stadiums
    requires a bridge table named teams_stadiums with PK consisting of a tuple of FKs
*6) Teams - Games (MtM): Teams have many games, and a game has many (2) teams 
    requires a bridge table named teams_games with PK consisting of a tuple of FKs
    Thinking it should be a PK of three items, two teams and one game, all FKs
7) Games - Stadiums (1tM): One game can only be played at one stadium, but a stadium can have many games played in it 
    requires a FK in the games table *1
8) Games - Leagues (1tM): A game can only be played in one league, a League has many games 
    requires a FK in the games table *1
9) Games - Referees (1t1): A game requires one and only one referee, but a referee can ref many games 
    requires a FK in the games table *1
10) Teams - Leagues (MtM): A team plays in many leagues and a league has many teams 
    requires a bridge table named teams_leagues with PK consisting of a tuple of FKs


REST API Endpoints:
1) /players (GET Request) - returns all the players in the database as JSON data
2) /players/<int:id> (GET Request) - returns specific player in the database as JSON data 
3) /players (POST Request) - creates new player entity in database with provided JSON data, returns JSON data
4) /players/<int:id> (PATCH/PUT Request) - edits existing player entity in database with provided JSON data, returns JSON data
5) /players/<int:id> (DELETE Request) - deletes player entity in database with provided JSON data, returns JSON boolean to confirm
6) /teams (GET Request) - returns all the teams in the database as JSON data
7) /teams/<int:id> (GET Request) - returns specific team in the database as JSON data
8) /teams/<int:id> (DELETE Request) - deletes team entity in database with provided JSON data, returns JSON boolean to confirm
9) /leagues (GET Request) - returns all the leagues in the database as JSON data
10) /leagues (POST Request) - creates new league entity in database with provided JSON data, returns JSON data
11) /leagues/<int:id> (DELETE Request) - deletes team entity in database with provided JSON data, returns JSON boolean to confirm
12) /games (GET Request) - returns all the game in the database as JSON data
13) /games (POST Request) - creates new game entity in database with provided JSON data, returns JSON data
14) /stadiums (GET Request) - returns all the stadiums in the database as JSON data
15) /stadiums (POST Request) - creates new stadium entity in database with provided JSON data, returns JSON data
16) /stadiums/<int:id> (DELETE Request) - deletes stadium entity in database with provided JSON data, returns JSON boolean to confirm


Tasks:

Entity Relationship Diagram updates 
X    Create Nations Entity with Attributes: 
X        id, full_name and nation_abbreviation 
X    Create Stadiums Entity with attributes:
X        id, max_capacity, city, nation
Create Team - League Relationship


Additional Notes Below 

*1 Look at Week 1 (p3): Getting to Know SQL
    event = game = many
    film = stadium = one 



Portfolio Project Report

Question 1:

I choose to go with an ORM as I felt it might be more difficult which would provide a better learning experience. I felt as though it might be more scalable as well for building out more functionality in the database and API.

Question 2: 

I am making a football/soccer database to keep track of players and the multiple teams they play for along with the games in multiple leagues. The endpoints (URLs and HTTP verb/methods) I choose was the basic ones like GET all players in a team, GET a particular player with their id, POST a player to create a new player in the database and a DELETE player. 
I think I will add some more endpoints to the API to provide more functionality to the API and to try out some different features that might not be taught in this course. 


Question 3:

It would be interesting to be able to show the tables in the database detailing player stats, listing the players for a particular team or all the games a player has played. These sports databases can be changed slightly to work with almost all sports which I find interesting. I also think learning the tools and applications using sports is a fun way to learn. 

Question 4:

The most challenging part way to conceptualize how a football/soccer database works with an API. Using the Twitter clone example, it made a lot of sense on how to store and retrieve data using an API with requests and responses but bringing this to the football/soccer database was a little challenging. It was a good challenge in the sense that we had to really understand the core concepts in order to use them in our project.
