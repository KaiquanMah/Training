runs table
duration_mins	week	month	year	park_name	city_name	distance_km	route_name
24.5	3	May	2019	Prospect Park	Brooklyn	5	Simple Loop
61	3	May	2019	Central Park	New York City	8	Resevoir Loop


Out of these possible answers, what would be the best way to organize the fact table and dimensional tables?
Possible answers
YES - A fact table holding duration_mins, distance_km and foreign keys to dimension tables holding route details and week details, respectively.
NO - A fact table holding week,month, year and foreign keys to dimension tables holding route details and duration details, respectively.
NO - A fact table holding route_name,park_name,city_name, and foreign keys to dimension tables holding week details and duration details, respectively.


-- Create a route dimension table
CREATE TABLE route(
	route_id INTEGER PRIMARY KEY,
    park_name VARCHAR(160) NOT NULL,
    city_name VARCHAR(160) NOT NULL,
    distance_km FLOAT NOT NULL,
    route_name VARCHAR(160) NOT NULL
);
-- Create a week dimension table
CREATE TABLE week(
	week_id INTEGER PRIMARY KEY,
    week INTEGER NOT NULL,
    month VARCHAR(160) NOT NULL,
    year INTEGER NOT NULL
);







SELECT 
	-- Select the sum of the duration of all runs
	SUM(duration_mins)
FROM 
	runs_fact;

SELECT 
	-- Get the total duration of all runs
	SUM(duration_mins)
FROM 
	runs_fact
-- Get all the week_id's that are from July, 2019
INNER JOIN week_dim ON runs_fact.week_id = week_dim.week_id
WHERE month = 'July' and year = '2019';










