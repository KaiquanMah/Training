CHAPTER 1
Conditional Logic

SELECT
	name,
    composer,
    -- Begin a CASE statement
    CASE
        -- A song priced at 0.99 should be a 'Standard Song'
    	WHEN unit_price = .99 THEN 'Standard Song'
        -- Songs costing 1.99 should be denoted as 'Premium Song'
        WHEN unit_price = 1.99 THEN 'Premium Song'
    END AS song_description
FROM store.track;

NAME	COMPOSER	SONG_DESCRIPTION
For Those About To Rock (We Salute You)	Angus Young; Malcolm Young; Brian Johnson	Standard Song
Fast As a Shark	F. Baltes; S. Kaufman; U. Dirkscneider & W. Hoffman	Standard Song




--Inferring purchase quantity
SELECT
	customer_id,
    total,
    CASE
        -- Check if total is either 0.99 or 1.99 using IN
    	WHEN total IN (0.99, 1.99) THEN '1 Song'
        -- Catch the scenarios when the above is not true
        ELSE '2+ Songs'
    -- End the CASE statement and name the new column
    END AS number_of_songs
FROM store.invoice;


--SONG DURATION
SELECT
	name,
    milliseconds,
    CASE
    	WHEN milliseconds < 180000 THEN 'Short Song'
        WHEN milliseconds BETWEEN 180000 AND 300000 THEN 'Normal Length'
        ELSE 'Long Song'
    END AS song_length
FROM store.track;




SELECT
    name,
    unit_price,
    CASE
        -- Inexpensive Rock and Pop songs are always high-intent
        WHEN unit_price = .99 AND genre_id IN (5, 9) THEN 'High'
        -- Shorter, non-EDM tracks have neutral buyer intent
        -- STORE.genre: genre_id	name
        -- 15	Electronica/Dance
        WHEN milliseconds < 300000 AND genre_id != 15 THEN 'Neutral'
		-- Everything else is low
        ELSE 'Low'
    END AS buyer_intent
FROM store.track;










-- Run this query without editing it.
SELECT
	customer_id,
    total,
    CASE
    	WHEN total IN (0.99, 1.99) THEN '1 Song'
        ELSE '2+ Songs'
    END as number_of_songs
FROM store.invoice;

CUSTOMER_ID	TOTAL	NUMBER_OF_SONGS
2	1.98	2+ Songs
8	5.94	2+ Songs
37	0.99	1 Song

  

SELECT
    CASE
    	WHEN total IN (0.99, 1.99) THEN '1 Song'
        ELSE '2+ Songs'
    END as number_of_songs,
    -- Find the average value of the total field
    AVG(total) AS average_total
FROM store.invoice
-- Group by the field you built using CASE
GROUP BY number_of_songs;

NUMBER_OF_SONGS	AVERAGE_TOTAL
1 Song	1.05779661
2+ Songs	6.41980170




  
SELECT
    track.name,
    track.composer,
    artist.name,
    CASE
    	-- A 'Track Lacks Detail' if the composer field is NULL
        WHEN track.composer IS NULL THEN 'Track Lacks Detail'
        -- Use the composer and artist name to determine if a match exists
        WHEN track.composer = artist.name THEN 'Matching Artist'
        ELSE 'Inconsistent Data'
    END AS data_quality
FROM store.track AS track
LEFT JOIN store.album AS album ON track.album_id = album.album_id
-- Join the album table to artist using the artist_id field
LEFT JOIN store.artist AS artist ON album.artist_id = artist.artist_id;

NAME	COMPOSER	NAME	DATA_QUALITY
For Those About To Rock (We Salute You)	Angus Young; Malcolm Young; Brian Johnson	AC/DC	Inconsistent Data
B to the Wall	null	Accept	Track Lacks Detail
Fast As a Shark	F. Baltes; S. Kaufman; U. Dirkscneider & W. Hoffman	Accept	Inconsistent Data






SELECT *
FROM TRACK
-- 'Protected' media types - their IDs
WHERE media_type_id IN (2,3);

TRACK_ID	NAME	ALBUM_ID	MEDIA_TYPE_ID	GENRE_ID	COMPOSER	MILLISECONDS	BYTES	UNIT_PRICE
2	B to the Wall	2	2	1		342562	5510424	0.99
3	Fast As a Shark	3	2	1	F. Baltes; S. Kaufman; U. Dirkscneider & W. Hoffman	230619	3990994	0.99
4	Restless and Wild	3	2	1	F. Baltes; R.A. Smith-Diesel; S. Kaufman; U. Dirkscneider & W. Hoffman	252051	4331779	0.99


SELECT COUNT(*)
FROM TRACK
-- 'Protected' media types - their IDs
WHERE media_type_id IN (2,3);

COUNT(*)
372



  
  

===========================================================

CHAPTER 2
Subqueries and Common Table Expressions




SELECT
	-- Find the genre name and average milliseconds
    genre_name,
    AVG(milliseconds) AS average_milliseconds
-- Retrieve records from the result of the subquery
FROM (
    SELECT
        genre.name AS genre_name,
        track.genre_id,
        track.milliseconds
    FROM store.track
    JOIN store.genre ON track.genre_id = genre.genre_id
)
-- Group the results by the genre name
GROUP BY genre_name;

GENRE_NAME	AVERAGE_MILLISECONDS
Science Fiction	2625549.076923
Sci Fi & Fantasy	2922740.454545





  
-- LARGE TXN (ie more than 10 invoice lines)
SELECT
    invoice_id,
    COUNT(invoice_id) AS total_invoice_lines
FROM store.invoiceline
GROUP BY invoice_id
-- Only pull records with more than 10 total invoice lines
HAVING total_invoice_lines > 10;

SELECT
  -- from outer query
	billing_country,
  -- 'total' comes from STORE.invoice table (in the LHS/outer query)
  SUM(total) AS total_invoice_amount
FROM store.invoice
-- subquery is only used to match 'invoice_id'
WHERE invoice_id IN (
  SELECT
      invoice_id,
  FROM store.invoiceline
  GROUP BY invoice_id
  HAVING COUNT(invoice_id) > 10
)
GROUP BY billing_country;

BILLING_COUNTRY	TOTAL_INVOICE_AMOUNT
Austria	18.86
Finland	13.86
Poland	13.86









  
-- Create a CTE named track_lengths
WITH track_lengths AS (
	SELECT
        genre.name,
        track.genre_id,
        track.milliseconds / 1000 AS num_seconds
    FROM store.track
    JOIN store.genre ON track.genre_id = genre.genre_id
)

SELECT
    track_lengths.name,
    -- Find the average length of each track in seconds
    AVG(track_lengths.num_seconds) AS avg_track_length
FROM track_lengths
GROUP BY track_lengths.name
-- Sort the results by average track_length
ORDER BY avg_track_length DESC;

NAME	AVG_TRACK_LENGTH
Sci Fi & Fantasy	2922.740454545455
Science Fiction	2625.549076923077







  
-- Create a CTE called track_metrics, convert milliseconds to seconds
WITH track_metrics AS (
    SELECT 
        composer,
        milliseconds / 1000 AS num_seconds,
        unit_price
    FROM store.track
 	-- Retrieve records where composer is not NULL
    WHERE composer IS NOT NULL
)

SELECT
    composer,
    -- Find the average price-per-second
    AVG(unit_price/num_seconds) AS cost_per_second
FROM track_metrics
GROUP BY composer
ORDER BY cost_per_second DESC;

COMPOSER	COST_PER_SECOND
Samuel Rosa	0.087411695455
L. Muggerud	0.085671670000












USE DATABASE COURSE_40931_DB_60DB189FEEA84DC191E47F55C6FE16B1;
USE SCHEMA STORE;
WITH usa_invoices AS (
SELECT invoice_id, billing_state
FROM invoice
WHERE billing_country='USA'
)

SELECT *
FROM usa_invoices;

INVOICE_ID	BILLING_STATE
5	MA
13	CA

DESC TABLE invoice;
name	type	kind	null?	default	primary key	unique key	check	expression	comment	policy name	privacy domain
INVOICE_ID	NUMBER(38,0)	COLUMN	Y		N	N					
CUSTOMER_ID	NUMBER(38,0)	COLUMN	Y		N	N					
INVOICE_DATE	TIMESTAMP_NTZ(9)	COLUMN	Y		N	N					
BILLING_ADDRESS	VARCHAR(16777216)	COLUMN	Y		N	N					
BILLING_CITY	VARCHAR(16777216)	COLUMN	Y		N	N					
BILLING_STATE	VARCHAR(16777216)	COLUMN	Y		N	N					
BILLING_COUNTRY	VARCHAR(16777216)	COLUMN	Y		N	N					
BILLING_POSTAL_CODE	VARCHAR(16777216)	COLUMN	Y		N	N					
TOTAL	NUMBER(5,2)	COLUMN	Y		N	N					
  
DESC TABLE invoiceline;
name	type	kind	null?	default	primary key	unique key	check	expression	comment	policy name	privacy domain
INVOICE_LINE_ID	NUMBER(38,0)	COLUMN	Y		N	N					
INVOICE_ID	NUMBER(38,0)	COLUMN	Y		N	N					
TRACK_ID	NUMBER(38,0)	COLUMN	Y		N	N					
UNIT_PRICE	NUMBER(5,2)	COLUMN	Y		N	N					
QUANTITY	NUMBER(38,0)	COLUMN	Y		N	N						





WITH usa_invoices AS (
SELECT invoice_id, billing_state
FROM invoice
WHERE billing_country='USA'
)

SELECT billing_state,
COUNT(1) AS n_songs
FROM usa_invoices US
JOIN INVOICELINE LINE
ON US.INVOICE_ID = LINE.INVOICE_ID
GROUP BY billing_state
ORDER BY n_songs DESC;

BILLING_STATE	N_SONGS
CA	114
WA	38
TX	38
IL	38
UT	38
WI	38
MA	38
NV	38
NY	38
FL	38
AZ	38























-- Create the cleaned_invoices CTE
WITH cleaned_invoices AS (
    SELECT
        invoice_id,
        invoice_date
    FROM store.invoice
    WHERE billing_country = 'Germany'
)

SELECT * FROM cleaned_invoices;
INVOICE_ID	INVOICE_DATE
1	2009-01-01 00:00:00
6	2009-01-19 00:00:00






WITH cleaned_invoices AS (
    SELECT
        invoice_id,
        invoice_date
    FROM store.invoice
    WHERE billing_country = 'Germany'

) 
-- Create the detailed_invoice_lines CTE
, detailed_invoice_lines AS (
  
    SELECT
        invoiceline.invoice_id,
        invoiceline.invoice_line_id,
        track.name,
        invoiceline.unit_price,
        invoiceline.quantity,
    FROM store.invoiceline
    LEFT JOIN store.track ON invoiceline.track_id = track.track_id
)

SELECT * FROM detailed_invoice_lines;
INVOICE_ID	INVOICE_LINE_ID	NAME	UNIT_PRICE	QUANTITY
108	579	For Those About To Rock (We Salute You)	0.99	1
1	1	B to the Wall	0.99	1








  

WITH cleaned_invoices AS (
    SELECT
        invoice_id,
        invoice_date
    FROM store.invoice
    WHERE billing_country = 'Germany'
), 

detailed_invoice_lines AS (
    SELECT
        invoiceline.invoice_id,
        invoiceline.invoice_line_id,
        track.name,
        invoiceline.unit_price,
        invoiceline.quantity,
    FROM store.invoiceline
    LEFT JOIN store.track ON invoiceline.track_id = track.track_id
)

SELECT
    ci.invoice_id,
    ci.invoice_date,
    dil.name,
    -- Find the total amount for the line
    dil.unit_price * dil.quantity AS line_amount
FROM detailed_invoice_lines AS dil

-- JOIN the cleaned_invoices and detailed_invoice_lines CTEs
LEFT JOIN cleaned_invoices AS ci ON dil.invoice_id = ci.invoice_id
ORDER BY ci.invoice_id, line_amount;


INVOICE_ID	INVOICE_DATE	NAME	LINE_AMOUNT
1	2009-01-01 00:00:00	B to the Wall	0.99
1	2009-01-01 00:00:00	Restless and Wild	0.99








  

-- Create an artist_info CTE, JOIN the artist and album tables
WITH artist_info AS (
    SELECT
        album.album_id,
        artist.name AS artist_name
    FROM store.album
    JOIN store.artist ON album.artist_id = artist.artist_id

-- Define a track_sales CTE to assign an album_id, name,
-- and number of seconds for each track
), track_sales AS (
    SELECT
        track.album_id,
        track.name,
        track.milliseconds / 1000 AS num_seconds
    FROM store.invoiceline
    JOIN store.track ON invoiceline.track_id = track.track_id
)

SELECT
    ai.artist_name,
    -- Calculate total minutes listed
    SUM(num_seconds) / 60 AS minutes_listened
FROM track_sales AS ts
JOIN artist_info AS ai ON ts.album_id = ai.album_id
-- Group the results by the non-aggregated column
GROUP BY ai.artist_name
ORDER BY minutes_listened DESC;

ARTIST_NAME	MINUTES_LISTENED
Lindsay Lohan	802.958766666667
Whitney	530.874516666667



