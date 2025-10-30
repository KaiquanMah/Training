USE DATABASE COURSE_41769_DB_067839B642724855B35E538829400740;
USE SCHEMA CORE_GYM;

DESC TABLE GYMS;
name	type	kind	null?	default	primary key	unique key	check	expression	comment	policy name	privacy domain
GYM_ID	VARCHAR(16777216)	COLUMN	Y		N	N					
LOCATION	VARCHAR(16777216)	COLUMN	Y		N	N					
GYM_TYPE	VARCHAR(16777216)	COLUMN	Y		N	N					
FACILITIES	VARCHAR(16777216)	COLUMN	Y		N	N					

  
DESC TABLE MEMBERS;
name	type	kind	null?	default	primary key	unique key	check	expression	comment	policy name	privacy domain
USER_ID	VARCHAR(16777216)	COLUMN	Y		N	N					
PERSONAL_INFO	VARIANT	COLUMN	Y		N	N					
SIGN_UP_DATE	DATE	COLUMN	Y		N	N					
USER_LOCATION	VARCHAR(16777216)	COLUMN	Y		N	N					
SUBSCRIPTION_PLAN	VARCHAR(16777216)	COLUMN	Y		N	N					

  
DESC TABLE SUBSCRIPTION_PLANS;
name	type	kind	null?	default	primary key	unique key	check	expression	comment	policy name	privacy domain
SUBSCRIPTION_PLAN	VARCHAR(16777216)	COLUMN	Y		N	N					
PRICE_PER_MONTH	FLOAT	COLUMN	Y		N	N					
FEATURES	VARCHAR(16777216)	COLUMN	Y		N	N					


DESC TABLE VISITS;
name	type	kind	null?	default	primary key	unique key	check	expression	comment	policy name	privacy domain
USER_ID	VARCHAR(16777216)	COLUMN	Y		N	N					
GYM_ID	VARCHAR(16777216)	COLUMN	Y		N	N					
CHECKIN_TIME	TIMESTAMP_NTZ(9)	COLUMN	Y		N	N					
CHECKOUT_TIME	TIMESTAMP_NTZ(9)	COLUMN	Y		N	N					
WORKOUT_TYPE	VARCHAR(16777216)	COLUMN	Y		N	N					
CALORIES_BURNED	NUMBER(38,0)	COLUMN	Y		N	N					






-- VARCHAR, TEXT, STRING
SELECT
    gym_id,
    CASE
        -- Update the locations classified as a Major City
        WHEN location IN ('New York', 'Los Angeles', 'Dallas') 
        THEN 'Major City'
        
        -- Otherwise, it's a Non-Major City
        ELSE 'Non-Major City'
    END AS gym_city
FROM CORE_GYM.gyms
-- Complete the WHERE clause to only return Premium gym types
WHERE gym_type = 'Premium';

GYM_ID	GYM_CITY
gym_1	Major City
gym_4	Non-Major City
gym_7	Non-Major City
gym_9	Major City
gym_10	Non-Major City



-- NUMBER, FLOAT
CREATE OR REPLACE TABLE retail (
  	-- transaction_id stores 16 total digits with 0 right of the decimal point
    transaction_id NUMBER(16, 0),
  	-- pre_tax_amount stores up to 6 digits with 2 right of the decimal point
    pre_tax_amount NUMBER(6,2),
  	-- tax_rate stores up to 5 digits with 3 right of the decimal point
    tax_rate NUMBER(5,3),
    transaction_total NUMBER(6, 2)
);




-- DATE, TIME, DATETIME
SELECT
	-- Return '2007-06-13' as a DATE
    TO_DATE('2007-06-13') AS the_date
;

SELECT
    TO_DATE('2007-06-13') AS the_date,
    
    -- Return '09:53:18' as a TIME
    TO_TIME('09:53:18') AS the_time
;

SELECT
    TO_DATE('2007-06-13') AS the_date,
    TO_TIME('09:53:18') AS the_time,
    
    -- Cast the string to a timestamp
    '2007-06-13 09:53:18'::TIMESTAMP AS the_timestamp
;

THE_DATE	THE_TIME	THE_TIMESTAMP
2007-06-13	09:53:18	2007-06-13 09:53:18

-- TIMEZONE
YES - TIMESTAMP_NTZ stores data without a timestamp, and is the default implementation of TIMESTAMP.
YES - Using the TIMESTAMP_LTZ data type relies on the local timezone when operating on datetime data.
YES - Data is stored in UTC with a provided time zone when using the TIMESTAMP_TZ data type.

SELECT
    checkin_time,
    -- Cast checkin_time to DATE
    checkin_time::DATE AS the_date,
    -- Cast checkin_time to TIME
    checkin_time::TIME AS the_time
FROM CORE_GYM.visits
;

CHECKIN_TIME	THE_DATE	THE_TIME
2023-09-10 15:55:00	2023-09-10	15:55:00
2023-04-13 20:07:00	2023-04-13	20:07:00





-- Managing display length
SELECT SUBSCRIPTION_PLAN, LEN(features), FEATURES
FROM COURSE_41769_DB_067839B642724855B35E538829400740.CORE_GYM.SUBSCRIPTION_PLANS
ORDER BY 2 DESC,1;

SUBSCRIPTION_PLAN	LEN(FEATURES)	FEATURES
Pro	105	Access to all facilities; Unlimited class access; 5 guest passes per month; Free personal trainer session
Student	97	Access to basic facilities; Limited class access; 1 guest pass per month; Discounted for students
Basic	76	Access to basic gym facilities; Limited class access; 1 guest pass per month


-- Transforming text data
CORE_GYM.members table
user_id	personal_info	sign_up_date	user_location	subscription_plan
user_1	{
  "age": "56",
  "gender": "Female",
  "name": {
    "first": "Chris",
    "last": "Wilson"
  }
}	                      2023-02-06	  Denver	      Basic

  
SELECT
    user_id,
    -- Return all the text after user_ in the user_id field
    SPLIT(user_id, '_')[1] AS split_user_id
FROM CORE_GYM.members;

USER_ID	SPLIT_USER_ID
user_1	"1"


  
SELECT
    user_id,
    SPLIT(user_id, '_')[1] AS split_user_id,
    -- Use a different function to remove all data after 
    -- user_ in the user_id field
    TRIM(user_id, 'user_') AS trimmed_user_id
FROM CORE_GYM.members;


SELECT
    user_id,
    SPLIT(user_id, '_')[1] AS split_user_id,
    TRIM(user_id, 'user_') AS trimmed_user_id,
    
    -- Create a new member ID using the user_location,
    -- subscription_plan, and the second half of the SPLIT user_id
    CONCAT(
        user_location,
        subscription_plan,
        SPLIT(user_id, '_')[1]
    ) AS new_member_id
    
FROM CORE_GYM.members;

USER_ID	SPLIT_USER_ID	TRIMMED_USER_ID	NEW_MEMBER_ID
user_1	    "1"	        1	            DenverBasic1




  
SELECT
    v.user_id,
    g.location,
    
    -- Concatenate the following strings to create a sentence
    CONCAT(
        'Congrats! On ', 
        DATE(v.checkin_time), 
        ' you burned ', 
        v.calories_burned,  -- Add the calories burned
        ' calories via ', 
        v.workout_type  -- Add the workout type
    ) AS message

FROM CORE_GYM.visits AS v
JOIN CORE_GYM.gyms AS g
    ON v.gym_id = g.gym_id;

USER_ID	LOCATION	MESSAGE
user_3291	Philadelphia	Congrats! On 2023-09-10 you burned 462 calories via Weightlifting
user_1944	Los Angeles	Congrats! On 2023-04-13 you burned 1278 calories via Yoga
user_958	San Antonio	Congrats! On 2023-06-10 you burned 858 calories via Cardio
user_1534	Phoenix	Congrats! On 2023-02-05 you burned 1482 calories via CrossFit





SELECT
    m.user_id,
    m.sign_up_date,
    m.subscription_plan,
    sp.price_per_month AS original_price,

	-- Add a 25% uplift to the existing price per month
    -- AUTOGRADER WANTS THE TYPO 'uplist' instead of 'uplift'
    -- sp.price_per_month * 1.25 AS twenty_five_percent_uplift,
    sp.price_per_month * 1.25 AS twenty_five_percent_uplist,
    -- Increase the price_per_month by $5.00 
    sp.price_per_month + 5.00 AS plus_five_dollars, 
    -- Divide the price per month by 2
    -- AUTOGRADER WANTS '/2' INSTEAD OF '/2.00'
    -- '0.5*' IS ALSO ACCEPTED
    -- sp.price_per_month / 2.00 AS half_off
    sp.price_per_month / 2 AS half_off

FROM CORE_GYM.subscription_plans AS sp
JOIN CORE_GYM.members AS m
    ON sp.subscription_plan = m.subscription_plan;

USER_ID	SIGN_UP_DATE	SUBSCRIPTION_PLAN	ORIGINAL_PRICE	TWENTY_FIVE_PERCENT_UPLIST	PLUS_FIVE_DOLLARS	HALF_OFF
user_1	2023-02-06	Basic	19.99	24.987499999999997	24.99	9.995
user_2	2023-08-08	Pro	49.99	62.487500000000004	54.99




  

SELECT
    workout_type,
    
    -- Find the total number of calories burned
    SUM(calories_burned) AS total_calories_burned,
    -- Store the average calories burned
    AVG(calories_burned) AS avg_calories_burned,
    -- Round the average calories burned to 2 decimal points
    ROUND(AVG(calories_burned), 2) AS rounded_avg_calories_burned
    
FROM CORE_GYM.visits
-- Aggregate records by workout_type
GROUP BY workout_type;

WORKOUT_TYPE	TOTAL_CALORIES_BURNED	AVG_CALORIES_BURNED	ROUNDED_AVG_CALORIES_BURNED
CrossFit	14887929	887.612771	887.61
Swimming	14827899	888.110865	888.11








-- TIMESTAMP COMPONENTS
YEAR(timestamp_field)
MONTH(timestamp_field)
DAY(timestamp_field)
MONTHNAME(timestamp_field)
DAYNAME(timestamp_field)

HOUR(timestamp_field)
MINUTE(timestamp_field)
SECOND(timestamp_field)

DATEDIFF(<1>, <2>, <3>)   -- unit, first timestamp, second timestamp
DATEDIFF(DAY, start_timestamp, end_timestamp)
--unit: MINUTE, HOUR, DAY, WEEK, YEAR

DATEADD(DAY, 90, start_date) --unit, amount, start_date


  
SELECT
    v.user_id,
    m.user_location,
    v.checkin_time,
    -- Extract the day name from checkin_time
    DAYNAME(checkin_time) AS day_name
FROM CORE_GYM.visits AS v
JOIN CORE_GYM.members AS m
    ON v.user_id = m.user_id;
  
SELECT
    v.user_id,
    m.user_location,
    v.checkin_time,
    DAYNAME(v.checkin_time) AS day_name,
    -- Extract the month name from checkin_time
    MONTHNAME(checkin_time) AS month_name
FROM CORE_GYM.visits AS v
JOIN CORE_GYM.members AS m
    ON v.user_id = m.user_id;

SELECT
    v.user_id,
    m.user_location,
    v.checkin_time,
    DAYNAME(v.checkin_time) AS day_name,
    MONTHNAME(v.checkin_time) AS month_name,
    -- Extract the numeric day from checkin_time
    DAY(v.checkin_time) AS numeric_day
FROM CORE_GYM.visits AS v
JOIN CORE_GYM.members AS m
    ON v.user_id = m.user_id;

USER_ID	USER_LOCATION	CHECKIN_TIME	DAY_NAME	MONTH_NAME	NUMERIC_DAY
user_3291	Atlanta	2023-09-10 15:55:00	Sun	Sep	10
user_1944	Las Vegas	2023-04-13 20:07:00	Thu	Apr	13










SELECT
    -- Retrieve the user_id, as well as check in/out times
    user_id,
    checkin_time,
    checkout_time,
    -- Find the number of minutes each member was at the gym for
    -- AUTOGRADER is not looking for 'TIME'
    -- DATEDIFF(MINUTE, TIME(checkin_time), TIME(checkout_time)) AS workout_duration
    DATEDIFF(MINUTE, checkin_time, checkout_time) AS workout_duration
FROM CORE_GYM.visits;

USER_ID	  CHECKIN_TIME	        CHECKOUT_TIME    	    WORKOUT_DURATION
user_3291	2023-09-10 15:55:00	  2023-09-10 16:34:00	  39
user_1944	2023-04-13 20:07:00	  2023-04-13 22:43:00	  156




SELECT
    m.personal_info:name.first AS first_name,
    m.personal_info:name.last AS last_name,
    v.gym_id,
    v.checkin_time AS last_appointment,
    -- Propose a next appointment in one week
    DATEADD(WEEK, 1, v.checkin_time) AS in_one_week,
    -- Propose a next appointment in two weeks
    DATEADD(WEEK, 2, v.checkin_time) AS SELECT
    m.personal_info:name.first AS first_name,
    m.personal_info:name.last AS last_name,
    v.gym_id,
    v.checkin_time AS last_appointment,
    -- Propose a next appointment in one week
    DATEADD(WEEK, 1, v.checkin_time) AS in_one_week,
    -- Propose a next appointment in two weeks
    DATEADD(WEEK, 2, v.checkin_time) AS in_two_weeks,
    -- Propose a next appointment in one month
    DATEADD(MONTH, 1, v.checkin_time) AS in_one_month
FROM CORE_GYM.visits AS v
JOIN CORE_GYM.members AS m
    ON v.user_id = m.user_id;
,
    -- Propose a next appointment in one month
    DATEADD(MONTH, 1, v.checkin_time) AS in_one_month
FROM CORE_GYM.visits AS v
JOIN CORE_GYM.members AS m
    ON v.user_id = m.user_id;

FIRST_NAME	LAST_NAME	GYM_ID	LAST_APPOINTMENT	IN_ONE_WEEK	IN_TWO_WEEKS	IN_ONE_MONTH
"Michael"	"Rodriguez"	gym_6	2023-09-10 15:55:00	2023-09-17 15:55:00	2023-09-24 15:55:00	2023-10-10 15:55:00
"Michael"	"Garcia"	gym_2	2023-04-13 20:07:00	2023-04-20 20:07:00	2023-04-27 20:07:00	2023-05-13 20:07:00










-- Creating your own Snowflake function
-- calories_per_minute should take a start_time, end_time, and calories_burned
CREATE OR REPLACE FUNCTION calories_per_minute(
    start_time TIMESTAMP, 
    end_time TIMESTAMP, 
    calories_burned NUMBER
)

-- Make sure the function returns a NUMBER
RETURNS NUMBER

AS

$$
-- Use DATEDIFF to calculate the efficiency of a workout
DATEDIFF(MINUTE, start_time, end_time) / calories_burned
$$;

status
Function CALORIES_PER_MINUTE successfully created.

  



  
SELECT
    user_id,
    gym_id,
    checkin_time,

	-- Determine workout efficiency for each user using the check in/out
    -- time, as well as the number of calories burned
    calories_per_minute(
        checkin_time, 
        checkout_time, 
        calories_burned
    ) AS workout_efficiency  -- Alias the results as workout_efficiency

FROM CORE_GYM.visits

-- Order the results by workout_efficiency
ORDER BY workout_efficiency DESC;

USER_ID	GYM_ID	CHECKIN_TIME	WORKOUT_EFFICIENCY
user_1507	gym_1	2023-07-03 14:13:00	1.148387
user_4028	gym_6	2023-09-05 16:07:00	1.140127







