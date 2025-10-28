--CHAPTER 1

-- Select pizza_type_id, pizza_size, and price from pizzas table
SELECT pizza_type_id,
	pizza_size,
    price
FROM pizzas

PIZZA_TYPE_ID	PIZZA_SIZE	PRICE
bbq_ckn	S	12.75
bbq_ckn	M	16.75
bbq_ckn	L	20.75
cali_ckn	S	12.75
cali_ckn	M	16.75
spinach_fet	L	20.25
veggie_veg	S	12
veggie_veg	M	16
veggie_veg	L	20.25
Showing 96 out of 96 rows








-- Count all pizza entries
SELECT COUNT(*) AS count_all_pizzas
FROM pizza_type

COUNT_ALL_PIZZAS
32








-- Count all pizza entries
SELECT COUNT(*) AS count_all_pizzas
FROM pizza_type
-- Apply filter on category for Classic pizza types
WHERE category = 'Classic'


COUNT_ALL_PIZZAS
8









-- Get information about the orders table
DESC TABLE orders

name	type	kind	null?	default	primary key	unique key	check	expression	comment	policy name	privacy domain
ORDER_ID	NUMBER(38,0)	COLUMN	N	null	Y	N	null	null	null	null	null
ORDER_DATE	DATE	COLUMN	Y	null	N	N	null	null	null	null	null
ORDER_TIME	TIME(9)	COLUMN	Y	null	N	N	null	null	null	null	null



-- Convert order_id to VARCHAR aliasing to order_id_string
SELECT CAST(order_id AS STRING) AS order_id_string
FROM orders




SELECT price, 
-- Convert price to NUMBER data type
CAST(price AS NUMBER) AS price_dollars
FROM pizzas

PRICE	PRICE_DOLLARS
12.75	13
16.75	17
20.75	21
20.25	20
Showing 96 out of 96 rows






-- Capitalize each word in pizza_type_id
SELECT INITCAP(pizza_type_id) AS capitalized_pizza_id 
FROM pizza_type;

CAPITALIZED_PIZZA_ID
Bbq_Ckn
Cali_Ckn
Ckn_Alfredo
Ckn_Pesto
Southw_Ckn
Thai_Ckn



-- Combine the name and category columns
SELECT CONCAT(name, ' - ', category) AS name_and_category
FROM pizza_type

NAME_AND_CATEGORY
The Barbecue Chicken Pizza - Chicken
The California Chicken Pizza - Chicken
The Chicken Alfredo Pizza - Chicken






-- Select the current date, current time
SELECT current_date, current_time;

CURRENT_DATE	CURRENT_TIME
2025-10-27	23:34:44.133000







-- Count the number of orders per day
SELECT COUNT(*) AS orders_per_day, 
-- Extract the day of the week and alias to order_day
	EXTRACT(WEEKDAY FROM order_date) AS order_day
FROM orders
GROUP BY order_day
ORDER BY orders_per_day DESC

ORDERS_PER_DAY	ORDER_DAY
3538	5
3239	4
3158	6
3024	3
2973	2
2794	1
2624	0
Showing 7 out of 7 rows







-- Get the month from order_date
SELECT EXTRACT(MONTH FROM order_date) AS order_month, 
    p.pizza_size, 
    -- Calculate revenue
    SUM(p.price * od.quantity) AS revenue
FROM orders o
INNER JOIN order_details od USING(order_id)
INNER JOIN pizzas p USING(pizza_id)
-- Appropriately group the query
-- GROUP BY order_month, pizza_size
GROUP BY ALL
-- Sort by revenue in descending order
ORDER BY revenue DESC

ORDER_MONTH	PIZZA_SIZE	REVENUE
7	L	33583.05
5	L	32970.5
6	XXL	71.9
12	XXL	35.95
Showing 59 out of 59 rows



=============================================

--CHAPTER 2


NATURAL JOIN
- deduplicates cols
- no need to specify JOIN key(s)
- JOINs on ALL MATCHING COLS -> this might pose a problem if your JOIN uses a different set of JOIN keys (eg JOIN using subset of common/matching cols OR diff cols)

Example 1: Unintended extra join condition
```
-- employees
employee_id | department_id | name
1           | 10            | Alice
2           | 20            | Bob

-- projects
project_id | department_id | employee_id | project_name
100        | 10            | 1           | Alpha
101        | 10            | 2           | Beta   -- Bob is temporarily in dept 10 for this project

✅ Correct explicit join:
SELECT * 
FROM employees e
JOIN projects p ON e.employee_id = p.employee_id;
-- → Returns both Alice (on Alpha) and Bob (on Beta)


❌ But with NATURAL JOIN:
SELECT * 
FROM employees
NATURAL JOIN projects;

This joins on both employee_id and department_id (since both columns exist in both tables).
So:
Alice: employee_id=1, department_id=10 → matches project Alpha ✅
Bob: employee_id=2, department_id=20 → but project Beta has department_id=10 → no match ❌
→ Bob disappears from results!
Even though he is assigned to project Beta, the extra department_id condition filters him out.
```




Example 2: Accidental join on irrelevant column
```
-- customers
customer_id | name | created_at
1           | Kai  | 2023-01-01

-- orders
order_id | customer_id | created_at | amount
100      | 1           | 2023-01-01 | 50.00
101      | 1           | 2023-02-01 | 30.00

--You want to join on customer_id only.
✅ Correct:
SELECT * FROM customers c JOIN orders o ON c.customer_id = o.customer_id;
→ Returns 2 rows (both orders)




❌ NATURAL JOIN:
SELECT * FROM customers NATURAL JOIN orders;

Joins on both customer_id and created_at.
Only the order with created_at = '2023-01-01 matches → you lose the second order!



✅ Best Practice:
Avoid NATURAL JOIN in production code.
Always prefer explicit joins for correctness, readability, and maintainability.
```







LATERAL JOIN
- right_hand_expression inline view/subquery can reference cols from left_hand_expression tables/views/subquery
- RHS can perform more complex queries
- Can the LHS reference the RHS? What does the sentence mean?
  - ❌ No, the LHS cannot reference the RHS. 
  - The dependency is strictly one-way:
  - LHS → RHS (allowed), 
  - but RHS → LHS (not applicable, since RHS is evaluated after LHS row is known)


SELECT ...
FROM <left_hand_expression> AS lhs,
LATERAL (<right_hand_expression>);

SELECT p.pizza_id, lat.name, lat.category
FROM pizzas AS p,
LATERAL (SELECT * 
         FROM pizza_type AS t
         -- Referencing LHS/outer query column: p.pizza_type_id
         WHERE p.pizza_type_id = t.pizza_type_id
        ) AS lat;


SELECT *
FROM orders AS o,
LATERAL (-- Subquery calculating total_spent
         SELECT SUM(p.price * od.quantity) AS total_spent
         FROM order_details AS od
         JOIN pizzas AS p ON od.pizza_id = p.pizza_id
         -- reference LHS col: o.order_id
         WHERE o.order_id = od.order_id
        ) AS t
ORDERBY o.order_id;




-------

Standard SQL vs Snowflake


In **standard SQL**, subqueries in the FROM clause (also called derived tables) must be self-contained — they cannot refer to tables that appear elsewhere in the same FROM clause. 
For example, this is not allowed:
Here, the subquery tries to use o.order_id, 
but o is defined in the same FROM clause—it’s not visible inside the subquery.
```
-- ❌ Invalid in standard SQL
SELECT *
FROM orders o,
     (SELECT * FROM order_items oi WHERE oi.order_id = o.order_id) AS items;
```


vs

BUT IN Snowflake
LATERAL changes this rule. It tells the SQL engine:
“Evaluate this right-hand subquery once for each row of the left-hand table, and allow it to see the columns from that row.” 

The query below processes one row at a time from orders (LHS).
For each row, it runs the RHS subquery, which can now use values from that specific row (e.g., o.order_id).
It’s conceptually similar to a correlated subquery, but in the FROM clause instead of SELECT or WHERE.
```
-- ✅ Valid with LATERAL
SELECT *
FROM orders o,
LATERAL (SELECT * FROM order_items oi WHERE oi.order_id = o.order_id) AS items;
```





-------



NATURAL JOIN exercise

schema
orders >> order_details >> pizzas >> pizza_type

SELECT
	-- Get the pizza category
    category,
    SUM(p.price * od.quantity) AS total_revenue
FROM order_details AS od
NATURAL JOIN pizzas AS p
-- NATURAL JOIN the pizza_type table
NATURAL JOIN pizza_type AS pt
-- GROUP the records by category
GROUP BY category
-- ORDER by total_revenue and limit the records
ORDER BY total_revenue DESC
LIMIT 1;

CATEGORY	TOTAL_REVENUE
Classic		220053.1






-- LEFT JOIN, RIGHT JOIN
SELECT COUNT(o.order_id) AS total_orders,
        AVG(p.price) AS average_price,
        -- Calculate total revenue
        SUM(od.quantity * p.price) AS total_revenue	
FROM orders AS o
LEFT JOIN order_details AS od
ON o.order_id = od.order_id
-- Use an appropriate JOIN with the pizzas table
RIGHT JOIN pizzas AS p
ON od.pizza_id = p.pizza_id;

TOTAL_ORDERS	AVERAGE_PRICE			TOTAL_REVENUE
48620			16.494004113110538		817860.05






SELECT COUNT(o.order_id) AS total_orders,
        AVG(p.price) AS average_price,
        -- Calculate total revenue
        SUM(p.price * od.quantity) AS total_revenue,
        -- Get the name from the pizza_type table
		pt.name AS pizza_name
FROM orders AS o
LEFT JOIN order_details AS od
ON o.order_id = od.order_id
-- Use an appropriate JOIN with the pizzas table
RIGHT JOIN pizzas p
ON od.pizza_id = p.pizza_id
-- NATURAL JOIN the pizza_type table
NATURAL JOIN pizza_type AS pt
GROUP BY pt.name, pt.category
ORDER BY total_revenue desc, total_orders desc

TOTAL_ORDERS	AVERAGE_PRICE	TOTAL_REVENUE	PIZZA_NAME
2315	18.28606911447084	43434.25	The Thai Chicken Pizza
2372	17.57293423271501	42768	The Barbecue Chicken Pizza
2302	17.448523023457863	41409.5	The California Chicken Pizza
2416	15.575951986754967	38180.5	The Classic Deluxe Pizza
923	16.42795232936078	15360.5	The Mediterranean Pizza
940	16.08936170212766	15277.75	The Spinach Supreme Pizza
987	14.001519756838906	13955.75	The Green Garden Pizza
480	23.65	11588.5	The Brie Carre Pizza












-----------------


Subqueries

-- find the pizza types ordered less frequently than the average for all types.
SELECT pt.name,
    pt.category,
    SUM(od.quantity) AS total_orders
FROM pizza_type pt
JOIN pizzas p
    ON pt.pizza_type_id = p.pizza_type_id
JOIN order_details od
    ON p.pizza_id = od.pizza_id
GROUP BY ALL
HAVING SUM(od.quantity) < (
  -- Calculate AVG of total_quantity from 'SUM'
  SELECT AVG(total_quantity)
  FROM (
    -- Calculate total_quantity
    SELECT SUM(od.quantity) AS total_quantity
    FROM pizzas p
    JOIN order_details od 
    	ON p.pizza_id = od.pizza_id
    GROUP BY p.pizza_id
    -- Alias as subquery
  ) subquery
)


NAME					CATEGORY	TOTAL_ORDERS
The Brie Carre Pizza	Supreme		490










Common Table Expressions
1 spotlight their most popular pizza based on total orders.
2 introducing a value meal featuring their least expensive pizza.

-- Create a CTE named most_ordered and limit the results 
WITH most_ordered AS (
    SELECT pizza_id, SUM(quantity) AS total_qty 
    FROM order_details GROUP BY pizza_id ORDER BY total_qty DESC
    LIMIT 1
)
-- Create CTE cheapest_pizza where price is equal to min price from pizzas table
, cheapest_pizza AS (
    SELECT pizza_id, price
    FROM pizzas 
    WHERE price = (SELECT MIN(price) FROM pizzas)
    LIMIT 1
)

SELECT pizza_id, 'Most Ordered' AS Description, total_qty AS metric
-- Select from the most_ordered CTE
FROM most_ordered
UNION ALL
SELECT pizza_id, 'Cheapest' AS Description, price AS metric
-- Select from the cheapest_pizza CTE
FROM cheapest_pizza;

PIZZA_ID		DESCRIPTION		METRIC
big_meat_s		Most Ordered	1914
pepperoni_s		Cheapest		9.75














Early filtering

WITH filtered_orders AS (
  SELECT order_id, order_date 
  FROM orders 
  -- Filter records where order_date is greater than November 1, 2015
  WHERE order_date > '2015-11-01'
)

, filtered_pizza_type AS (
  SELECT name, pizza_type_id 
  FROM pizza_type 
  -- Filter the pizzas which are in the Veggie category
    WHERE category = 'Veggie'
)

SELECT fo.order_id, fo.order_date, fpt.name, od.quantity
-- Get the details from filtered_orders CTE
FROM filtered_orders AS fo
JOIN order_details AS od ON fo.order_id = od.order_id
JOIN pizzas AS p ON od.pizza_id = p.pizza_id
-- JOIN the filtered_pizza_type CTE on pizza_type_id
JOIN filtered_pizza_type AS fpt ON p.pizza_type_id = fpt.pizza_type_id;



ORDER_ID	ORDER_DATE	NAME	QUANTITY
17934	2015-11-02	The Vegetables + Vegetables Pizza	1
17940	2015-11-02	The Green Garden Pizza	1
17940	2015-11-02	The Mexicana Pizza	1














Querying JSON data from a cell

sample dataset
business_id	name	address	city	state	postal_code	latitude	longitude	stars	review_count	is_open	attributes	categories	hours
Pns2l4eNsfO8kk83dixA6A	Abby Rappoport, LAC, CMQ	1616 Chapala St, Ste 2	Santa Barbara	CA	93101	34.4266787	-119.7111968	5	7	0	{
  "ByAppointmentOnly": "True"
}	Doctors, Traditional Chinese Medicine, Naturopathic/Holistic, Acupuncture, Health & Medical, Nutritionists	null

mpf3x-BjTdTEA3yCZrAYPw	The UPS Store	87 Grasso Plaza Shopping Center	Affton	MO	63123	38.551126	-90.335695	3	15	1	{
  "BusinessAcceptsCreditCards": "True"
}	Shipping Centers, Local Services, Notaries, Mailbox Centers, Printing Services	{
  "Friday": "8:0-18:30",
  "Monday": "0:0-0:0",
  "Saturday": "8:0-14:0",
  "Thursday": "8:0-18:30",
  "Tuesday": "8:0-18:30",
  "Wednesday": "8:0-18:30"
}

tUFrWirKiKi_TAnsVWINQQ	Target	5255 E Broadway Blvd	Tucson	AZ	85711	32.223236	-110.880452	3.5	22	0	{
  "BikeParking": "True",
  "BusinessAcceptsCreditCards": "True",
  "BusinessParking": "{'garage': False, 'street': False, 'validated': False, 'lot': True, 'valet': False}",
  "ByAppointmentOnly": "False",
  "Caters": "False",
  "CoatCheck": "False",
  "DogsAllowed": "False",
  "HappyHour": "False",
  "HasTV": "False",
  "OutdoorSeating": "False",
  "RestaurantsDelivery": "False",
  "RestaurantsPriceRange2": "2",
  "RestaurantsReservations": "False",
  "RestaurantsTakeOut": "False",
  "WheelchairAccessible": "True",
  "WiFi": "u'no'"
}	Department Stores, Shopping, Fashion, Home & Garden, Electronics, Furniture Stores	{
  "Friday": "8:0-23:0",
  "Monday": "8:0-22:0",
  "Saturday": "8:0-23:0",
  "Sunday": "8:0-22:0",
  "Thursday": "8:0-22:0",
  "Tuesday": "8:0-22:0",
  "Wednesday": "8:0-22:0"
}

SELECT name,
    review_count,
    -- Retrieve the Saturday hours
    hours:Saturday,
    -- Retrieve the Sunday hours
    hours:Sunday
FROM yelp_business_data
-- Filter for Restaurants
WHERE categories ILIKE '%Restaurant%'
    AND (hours:Saturday IS NOT NULL AND hours:Sunday IS NOT NULL)
    AND city = 'Philadelphia'
    AND stars = 5
ORDER BY review_count DESC

NAME					REVIEW_COUNT	HOURS:SATURDAY	HOURS:SUNDAY
Tortilleria San Roman	219				"9:0-17:0"		"9:0-17:0"
Hikari Sushi			155				"16:30-23:0"	"16:0-21:30"
Bad Brother				92				"17:0-2:0"		"17:0-0:0"








-- DO NOT USE DOUBLE QUOTES " "
-- USE SINGLE QUOTES ' '
SELECT business_id, name
FROM yelp_business_data
WHERE categories ILIKE '%Restaurant%'
	-- Filter where DogsAllowed is '%True%'
	AND attributes:DogsAllowed ILIKE '%True%'
    -- Filter where BusinessAcceptsCreditCards is '%True%'
    -- note this is a string, not boolean
    AND attributes:BusinessAcceptsCreditCards ILIKE '%True%'
    AND city ILIKE '%Philadelphia%'
    AND stars = 5

BUSINESS_ID				NAME
JAMmjTFdUGBpV24K1riSjQ	Yellow Bicycle Canteen
YA4OQvZFowHG4_78xis7sg	Boricua Restaurant
99zoELPcbwRBUqiPoaPqiQ	Bold Coffee Bar
faSi7EoZ38xMPJEpp7-pqg	Algorithm Restaurants
GIAgyEwEQITK7wZI_vhXIA	Bangin' Curry Franklin
SJJaIBGBBB3T_OX7iy-D4g	Authentik Byrek
2_Uog4hABJRkEqwWx87vaQ	Goubaa Grub
8qr1cXhqYGOXFNStgcMvhw	HomeGrown Coffee and Creations
hxPnlWZmirx7neooZykmtg	Sutton's
s5nduiTPNps4_2p9ZoHDbA	2 Street Sammies
Showing 10 out of 10 rows




