--ROW_NUMBER()
SELECT
	-- Return the charging_station_location and user_id
    charging_station_location,
    user_id,
    charging_start_time,
    charging_cost,
    
    -- Assign a row number to each record, ordering by charging_cost
    ROW_NUMBER() OVER(ORDER BY charging_cost)
FROM ELECTRIC_VEHICLES.charging;

CHARGING_STATION_LOCATION	USER_ID	CHARGING_START_TIME	CHARGING_COST	ROW_NUMBER() OVER(ORDER BY CHARGING_COST)
Los Angeles	User_377	2024-01-16 16:00:00	0.23	1
Los Angeles	User_522	2024-01-22 17:00:00	0.31	2
New York	User_619	2024-01-26 18:00:00	0.67	3




  
SELECT user_id,
       temperature,
       ROW_NUMBER() OVER (ORDER BY temperature DESC)
FROM COURSE_41767_DB_7EE0D04AC5A64B3089853456ABDDEB84.ELECTRIC_VEHICLES.CHARGING

USER_ID	TEMPERATURE	ROW_NUMBER() OVER (ORDER BY TEMPERATURE DESC)
User_1046	73	1
User_852	69	2
User_36	60	3
User_184	58	4
User_843	51	5
User_833	47	6
User_972	47	7
User_438	46	8

  









--RANK()
--FIRST_VALUE(fieldname)
--LAST_VALUE(fieldname)

SELECT
    user_id,
    charging_station_id,
    charging_duration,
	
    -- Rank records by charging duration
    RANK() OVER(
        ORDER BY charging_duration
    ) AS quickest_charges

FROM ELECTRIC_VEHICLES.charging
WHERE charging_station_id = 'Station_108';

USER_ID	CHARGING_STATION_ID	CHARGING_DURATION	QUICKEST_CHARGES
User_207	Station_108	0.8	1
User_621	Station_108	1.9	2
User_5	Station_108	2.0	3




  
SELECT
    user_id,
    charging_station_id,
    charging_duration,
	
    -- Rank records by charging duration from largest to smallest
    RANK() OVER(
        ORDER BY charging_duration DESC
    ) AS slowest_chargest

FROM ELECTRIC_VEHICLES.charging
WHERE charging_station_id = 'Station_310';

USER_ID	CHARGING_STATION_ID	CHARGING_DURATION	SLOWEST_CHARGEST
User_1129	Station_310	3.9	1
User_593	Station_310	2.7	2
User_259	Station_310	1.0	3








SELECT
    user_id,
    charging_station_location,
    charger_type,
    energy_consumed,
	
    -- Find the least energy consumed in a charging session
    FIRST_VALUE(energy_consumed) OVER(
        -- ORDER IN ASCENDING ORDER -> THEN PICK THE 1ST VALUE 'OUTSIDE'
        ORDER BY energy_consumed
    ) AS least_energy_consumed

FROM ELECTRIC_VEHICLES.charging;

USER_ID	CHARGING_STATION_LOCATION	CHARGER_TYPE	ENERGY_CONSUMED	LEAST_ENERGY_CONSUMED
User_1	Houston	DC Fast Charger	60.712	0.046
User_2	San Francisco	Level 1	12.339	0.046
User_3	San Francisco	Level 2	19.129	0.046




SELECT
    user_id,
    charging_station_location,
    charger_type,
    energy_consumed,
    FIRST_VALUE(energy_consumed) OVER(
        ORDER BY energy_consumed
    ) AS least_energy_consumed,
    
    -- Now, find the maximum energy consumed in a charging session
    LAST_VALUE(energy_consumed) OVER (
    	ORDER BY energy_consumed
    ) AS most_energy_consumed

FROM ELECTRIC_VEHICLES.charging
WHERE energy_consumed IS NOT NULL;

USER_ID	CHARGING_STATION_LOCATION	CHARGER_TYPE	ENERGY_CONSUMED	LEAST_ENERGY_CONSUMED	MOST_ENERGY_CONSUMED
User_1	Houston	DC Fast Charger	60.712	0.046	152.239
User_2	San Francisco	Level 1	12.339	0.046	152.239
User_3	San Francisco	Level 2	19.129	0.046	152.239









  

--wo vs w PARTITION BY
SELECT
    user_id,
    charging_station_id,
    charging_cost,
    
    -- Create a window function to rank each session based on charging cost
    RANK() OVER(
        ORDER BY charging_cost DESC
    ) AS expensive_charges
    
FROM ELECTRIC_VEHICLES.charging;

USER_ID	CHARGING_STATION_ID	CHARGING_COST	EXPENSIVE_CHARGES
User_518	Station_220	69.41	1
User_248	Station_308	68.93	2
User_930	Station_85	60.40	3



SELECT
    user_id,
    charging_station_id,
    charging_cost,
    
    RANK() OVER(
        -- Partition records by charging station to determine
      	-- rankings for each charging station
      	PARTITION BY charging_station_id
      
        ORDER BY charging_cost DESC
    ) AS expensive_charges
    
FROM ELECTRIC_VEHICLES.charging;

USER_ID	CHARGING_STATION_ID	CHARGING_COST	EXPENSIVE_CHARGES
User_1225	Station_51	21.98	1
User_498	Station_51	21.03	2
User_502	Station_51	18.40	3
User_833	Station_51	17.68	4
User_358	Station_51	8.86	5
User_854	Station_195	11.35	1
User_740	Station_256	26.55	1
User_705	Station_256	12.85	2
User_547	Station_289	14.20	1
User_514	Station_289	8.59	2
User_1196	Station_318	30.87	1








SELECT
    user_id,
    charging_station_id,
    charging_cost,
    
    -- Based on the charging_start_time, find the first 
    -- charging cost for each location
	FIRST_VALUE(charging_cost) OVER(
    	PARTITION BY charging_station_id
      	ORDER BY charging_start_time
    ) AS first_charging_cost,

	-- Find the average charging cost for charging station id
    AVG(charging_cost) OVER(
        PARTITION BY charging_station_id
    ) AS average_charging_cost
    
FROM ELECTRIC_VEHICLES.charging
ORDER BY charging_station_id;

USER_ID	CHARGING_STATION_ID	CHARGING_COST	FIRST_CHARGING_COST	AVERAGE_CHARGING_COST
User_794	Station_1	26.22	15.55	25.16000
User_1172	Station_1	33.71	15.55	25.16000
User_89	Station_1	15.55	15.55	25.16000
User_457	Station_10	32.07	6.43	25.81857
User_917	Station_10	13.80	6.43	25.81857
User_412	Station_10	33.46	6.43	25.81857
User_753	Station_10	27.39	6.43	25.81857
User_96	Station_10	38.06	6.43	25.81857
User_18	Station_10	6.43	6.43	25.81857
User_1107	Station_10	29.52	6.43	25.81857
User_1043	Station_100	26.59	21.33	23.96000
User_339	Station_100	21.33	21.33	23.96000











--NTH_VALUE(fieldname, n)   -- value @ 'n'-th record in the window
--DENSE_RANK()

SELECT

	-- Return the vehicle model and battery capacity
    vehicle_model,
    battery_capacity,
    
    -- Use a window function to return a ranking without gaps
    DENSE_RANK() OVER(
      	-- Battery capacity from greatest to least
        ORDER BY battery_capacity DESC
    ) AS battery_capacity_rank
    
FROM ELECTRIC_VEHICLES.charging;

VEHICLE_MODEL	BATTERY_CAPACITY	BATTERY_CAPACITY_RANK
Chevy Bolt	193	1
BMW i3	189	2
Hyundai Kona	179	3
BMW i3	174	4
Nissan Leaf	158	5
BMW i3	147	6
BMW i3	143	7
Tesla Model 3	143	7
BMW i3	141	8
Hyundai Kona	141	8
Nissan Leaf	130	9





  
SELECT
    charger_type,
    charging_duration * 60 AS charging_minutes,
	
    -- Assign a ranking to reach record based on charging
    -- duration, from shortest to longest
    RANK() OVER(
      	-- Segment the result set by charger type
        PARTITION BY charger_type
        ORDER BY charging_duration
    ) AS charging_duration_rank_1

FROM ELECTRIC_VEHICLES.charging;

CHARGER_TYPE	CHARGING_MINUTES	CHARGING_DURATION_RANK_1
DC Fast Charger	6.0	1
DC Fast Charger	24.0	2
DC Fast Charger	24.0	2
DC Fast Charger	30.0	4
DC Fast Charger	30.0	4
DC Fast Charger	30.0	4
DC Fast Charger	30.0	4
DC Fast Charger	36.0	8







SELECT
    charger_type,
    charging_duration * 60 AS charging_minutes,

    RANK() OVER(
        PARTITION BY charger_type
        ORDER BY charging_duration
    ) AS charging_duration_rank_1,
	
    -- Assign a ranking to record based on charging duration
    -- WITHOUT gaps
    DENSE_RANK() OVER(
        PARTITION BY charger_type
        ORDER BY charging_duration
    ) AS charging_duration_rank_2

FROM ELECTRIC_VEHICLES.charging;

CHARGER_TYPE	CHARGING_MINUTES	CHARGING_DURATION_RANK_1	CHARGING_DURATION_RANK_2
DC Fast Charger	6.0	1	1
DC Fast Charger	24.0	2	2
DC Fast Charger	24.0	2	2
DC Fast Charger	30.0	4	3
DC Fast Charger	30.0	4	3
DC Fast Charger	30.0	4	3
DC Fast Charger	30.0	4	3
DC Fast Charger	36.0	8	4








SELECT
	charging_station_location,
	user_id,
	charging_cost,
    
    -- Find the tenth-smallest charging cost
    NTH_VALUE(charging_cost, 10) OVER(
      	-- Segment the data by charging_station_location
		PARTITION BY charging_station_location
    	ORDER BY charging_cost
    -- Alias the result as minimum_cost
    ) AS minimum_cost
    
FROM ELECTRIC_VEHICLES.charging;

CHARGING_STATION_LOCATION	USER_ID	CHARGING_COST	MINIMUM_COST
Houston	User_1	13.09	5.81
San Francisco	User_2	21.13	6.12
San Francisco	User_3	35.67	6.12
Houston	User_4	13.04	5.81










--NTILE(N)  -- create N equally sized buckets 
--add PARTITION BY field1 - to equally distribute field1 values to be representative across buckets - eg 10% records with value1, 20% records with value 2 in each partition

-- CUME_DIST()   -- create a dn for each 'PARTITION BY field1' unique value
--then compare record to the 'cumulative dn' (from L to H) for tt field1's unique value partition

SELECT
    user_id,
    charging_station_location,
    charging_cost,
    
    -- Break records into 100 equally-sized buckets based on
    -- charging_cost
    NTILE(100) OVER(
      ORDER BY charging_cost
    ) AS survey_group
    
FROM ELECTRIC_VEHICLES.charging

-- Order by survey_group and charging_station_location
ORDER BY survey_group, charging_station_location;

USER_ID	CHARGING_STATION_LOCATION	CHARGING_COST	SURVEY_GROUP
User_1250	Chicago	3.71	1
User_308	Houston	5.06	1
User_1251	Houston	3.06	1
User_491	Houston	1.64	1
User_522	Los Angeles	0.31	1
User_377	Los Angeles	0.23	1
User_822	Los Angeles	5.04	1
User_1151	New York	5.11	1
User_270	New York	5.09	1
User_1317	New York	5.07	1
User_1056	New York	3.67	1
User_619	New York	0.67	1
User_465	San Francisco	5.06	1
User_557	San Francisco	2.35	1
User_490	Chicago	5.52	2
User_1282	Chicago	5.39	2
User_444	Chicago	5.38	2
User_1094	Houston	5.56	2
User_226	Houston	5.55	2
User_564	Houston	5.47	2
User_622	Houston	5.45	2
User_495	Houston	5.20	2
User_121	Los Angeles	5.14	2
User_436	Los Angeles	5.16	2
User_1207	Los Angeles	5.43	2
User_468	San Francisco	5.54	2
User_1066	San Francisco	5.55	2
User_764	San Francisco	5.31	2
User_1308	Chicago	5.71	3


  




  
SELECT
    user_id,
    charging_station_location,
    charging_cost,
    
    NTILE(100) OVER(
      -- Evenly distribute records in each bucket by 
      -- charging_station_location
      PARTITION BY charging_station_location
      ORDER BY charging_cost
    ) AS survey_group
    
FROM ELECTRIC_VEHICLES.charging
-- Order by survey_group and charging_station_location
ORDER BY survey_group, charging_station_location;

USER_ID	CHARGING_STATION_LOCATION	CHARGING_COST	SURVEY_GROUP
User_1250	Chicago	3.71	1
User_444	Chicago	5.38	1
User_1282	Chicago	5.39	1
User_308	Houston	5.06	1
User_1251	Houston	3.06	1
User_491	Houston	1.64	1
User_522	Los Angeles	0.31	1
User_377	Los Angeles	0.23	1
User_822	Los Angeles	5.04	1
User_619	New York	0.67	1
User_1056	New York	3.67	1
User_1317	New York	5.07	1
User_557	San Francisco	2.35	1
User_465	San Francisco	5.06	1
User_764	San Francisco	5.31	1
User_1308	Chicago	5.71	2
User_578	Chicago	5.58	2
User_490	Chicago	5.52	2
User_564	Houston	5.47	2
User_622	Houston	5.45	2
User_495	Houston	5.20	2
User_436	Los Angeles	5.16	2
User_1207	Los Angeles	5.43	2
User_121	Los Angeles	5.14	2
User_270	New York	5.09	2
User_757	New York	5.64	2
User_1151	New York	5.11	2
User_468	San Francisco	5.54	2
User_1066	San Francisco	5.55	2
User_1126	San Francisco	5.59	2
User_18	Chicago	6.43	3












SELECT
    user_id,
    charging_station_id,
    charging_duration * 60,
	
    -- Find the cumulative distribution of records in the result set
    CUME_DIST() OVER(
      	-- Segment records by charging station id
        PARTITION BY charging_station_id
      	-- Create the cumulative distribution using charging duration ASC
        ORDER BY charging_duration
    ) AS charging_duration_dist

FROM ELECTRIC_VEHICLES.charging
ORDER BY charging_station_id, charging_duration_dist;

USER_ID	CHARGING_STATION_ID	CHARGING_DURATION * 60	CHARGING_DURATION_DIST
User_1172	Station_1	36.0	0.3333333333333333
User_794	Station_1	84.0	0.6666666666666666
User_89	Station_1	90.0	1
User_457	Station_10	24.0	0.14285714285714285
User_18	Station_10	48.0	0.2857142857142857
User_1107	Station_10	54.0	0.5714285714285714
User_917	Station_10	54.0	0.5714285714285714
User_412	Station_10	66.0	0.7142857142857143
User_96	Station_10	84.0	0.8571428571428571
User_753	Station_10	174.0	1
User_1043	Station_100	78.0	0.5
User_339	Station_100	174.0	1
User_766	Station_101	132.0	0.25
User_739	Station_101	216.0	0.75
User_146	Station_101	216.0	0.75
User_191	Station_101	222.0	1







SELECT user_id,
       distance_driven,
       NTILE(100) OVER(
         ORDER BY distance_driven DESC
       )
FROM COURSE_41767_DB_3D1C4A386D4746079272FB098A72764A.ELECTRIC_VEHICLES.CHARGING
WHERE distance_driven IS NOT NULL;

USER_ID,DISTANCE_DRIVEN,"NTILE(100) OVER(ORDER BY DISTANCE_DRIVEN DESC)"
User_91,398,1
User_1091,398,1
User_1156,385,1
User_1005,370,1
User_893,327,1
User_1027,325,1
User_190,312,1
User_735,303,1
User_443,300,1
User_1157,300,1
User_934,300,1
User_778,299,1
User_815,299,1
User_725,299,2
User_1050,299,2
User_625,299,2
User_761,299,2
User_570,298,2
User_104,298,2
User_616,298,2
User_23,298,2
User_628,298,2
User_1124,297,2
User_1069,297,2
User_347,296,2
User_65,296,2
User_1218,296,3
User_340,296,3
User_1126,296,3
User_452,296,3
User_236,296,3
User_797,296,3
User_1073,295,3
User_1087,295,3
User_1001,294,3
User_1003,294,3
User_1154,294,3
User_1,294,3
User_292,294,3











--LOOK BACKWARDS/PREVIOUS VALUE
-- LAG(field1, n_records_to_look_back, default_field_or_value_else_null)   -- retrieve a previous/earlier record's value
-- vs
-- field1 - LAG(field1, 1, field1) if a previous/earlier 'field1' value does not exist (eg NULL / 1st record) -> default to the current row's 'field1' value
-- above, we use the current record/row's 'field1' value to COMPARE or MINUS a previous record/row's 'field1' value

-- LOOK FORWARD / VALUE BELOW/LATER
-- LEAD(field1, n_records_to_look_ahead, default_field_or_value_else_null)


SELECT
    user_id,
    charging_station_location,
    charging_start_time,
    charging_rate,
	
    -- Difference between current charging rate versus three sessions ago
    charging_rate - LAG(charging_rate, 3, 0) OVER(
      	-- Make sure results are partitioned by charging_station_location
        PARTITION BY charging_station_location
      	-- Sessions should be ordered by when charging began ASC
        ORDER BY charging_start_time
      
    ) AS change_in_charging_rate

FROM ELECTRIC_VEHICLES.charging;
-- ORDER BY charging_station_location, charging_start_time;

USER_ID	CHARGING_STATION_LOCATION	CHARGING_START_TIME	CHARGING_RATE	CHANGE_IN_CHARGING_RATE
User_5	Los Angeles	2024-01-01 04:00:00	10	10         <- LAG(charging_rate, 3, 0) returns 0. So charging_rate - LAG(charging_rate, 3, 0) returns charging_rate
User_8	Los Angeles	2024-01-01 07:00:00	27	27        <- LAG(charging_rate, 3, 0) returns 0. So charging_rate - LAG(charging_rate, 3, 0) returns charging_rate
User_9	Los Angeles	2024-01-01 08:00:00	14	14        <- LAG(charging_rate, 3, 0) returns 0. So charging_rate - LAG(charging_rate, 3, 0) returns charging_rate
User_11	Los Angeles	2024-01-01 10:00:00	10	0        <- LAG(charging_rate, 3, 0) returns 10. So charging_rate 10 - LAG(charging_rate, 3, 0) 10 returns 0
User_16	Los Angeles	2024-01-01 15:00:00	11	-16        <- LAG(charging_rate, 3, 0) returns2711. So charging_rate 11 - LAG(charging_rate, 3, 0) 27 returns -16
User_20	Los Angeles	2024-01-01 19:00:00	45	31
User_21	Los Angeles	2024-01-01 20:00:00	30	20
User_29	Los Angeles	2024-01-02 04:00:00	49	38


  





SELECT
    user_id,
    charging_station_id,
    charging_start_time,
    
    -- Retrieve the time_of_day, charging_rate and energy_consumed fields
	time_of_day,
    charging_rate,
    energy_consumed,
	
    -- "Look ahead" to the energy consumed in the next session
    LEAD(energy_consumed,1,0) OVER(
      
      	-- Segment the records by charging station and sequence
      	-- records by the start time of the charge
        PARTITION BY charging_station_id
        ORDER BY charging_start_time
      
    ) AS next_session_energy_consumed

FROM ELECTRIC_VEHICLES.charging;

USER_ID	CHARGING_STATION_ID	CHARGING_START_TIME	TIME_OF_DAY	CHARGING_RATE	ENERGY_CONSUMED	NEXT_SESSION_ENERGY_CONSUMED
User_358	Station_51	2024-01-15 21:00:00	Afternoon	31	62.096	79.418
User_498	Station_51	2024-01-21 17:00:00	Morning	41	79.418	39.067
User_502	Station_51	2024-01-21 21:00:00	Night	17	39.067	62.634
User_833	Station_51	2024-02-04 16:00:00	Evening	9	62.634	8.641
























