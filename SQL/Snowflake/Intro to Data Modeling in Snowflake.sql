Chapter 1

-- Describe the ecommerceonlineretail entity
DESC TABLE ecommerceonlineretail;

name	type	kind	null?	default	primary key	unique key	check	expression	comment	policy name	privacy domain
INVOICENO	VARCHAR(10)	COLUMN	Y	null	N	N	null	null	null	null	null
STOCKCODE	VARCHAR(15)	COLUMN	Y	null	N	N	null	null	null	null	null
DESCRIPTION	VARCHAR(255)	COLUMN	Y	null	N	N	null	null	null	null	null
QUANTITY	NUMBER(38,0)	COLUMN	Y	null	N	N	null	null	null	null	null
INVOICEDATE	TIMESTAMP_NTZ(9)	COLUMN	Y	null	N	N	null	null	null	null	null
UNITPRICE	NUMBER(10,2)	COLUMN	Y	null	N	N	null	null	null	null	null
CUSTOMERID	NUMBER(38,0)	COLUMN	Y	null	N	N	null	null	null	null	null
COUNTRY	VARCHAR(255)	COLUMN	Y	null	N	N	null	null	null	null	null


invoiceno	stockcode	description	quantity	invoicedate	unitprice	customerid	country
536365.0	21730	GLASS STAR FROSTED T-LIGHT HOLDER	6	2010-12-01 08:26:00	4.25	17850	United Kingdom
536365.0	22752	SET 7 BABUSHKA NESTING BOXES	2	2010-12-01 08:26:00	7.65	17850	United Kingdom





Conceptual data model
- entities
- relationships

Logical data model
- fields
- cardinality (btw entities) - one-to-one, one-to-many, many-to-many
- CREATE OR REPLACE TABLE

Physical data model
- data types
- PK FK



-- Create a new products entity
CREATE OR REPLACE TABLE products(
	-- List the entity's attributes
	stockcode VARCHAR(255),
    description VARCHAR(255)
);


-- Create a new 'orders' entity
CREATE OR REPLACE TABLE orders (
	-- List the invoice attributes
	invoiceno VARCHAR(10),
  invoicedate TIMESTAMP_NTZ(9),
  
  -- List the attributes related to price and quantity
	-- 10 digits b4 decimal pt, 2dp
  unitprice NUMBER(10,2),
	-- 38 digits b4 decimal, no dp
  quantity NUMBER(38,0)
  -- ALTERNATIVELY
  -- quantity INTEGER
);




-- Create customers table 
CREATE OR REPLACE TABLE customers (
  -- Define unique identifier
  customerid NUMBER(38,0) PRIMARY KEY,
  country VARCHAR(255)
);



-- Re-create orders table
CREATE OR REPLACE TABLE orders (
  -- Assign unique identifier column
  invoiceno VARCHAR(10) PRIMARY KEY,
  invoicedate TIMESTAMP_NTZ(9),
  unitprice NUMBER(10,2),
  quantity NUMBER(38,0),
  customerid NUMBER(38,0)
);

CREATE OR REPLACE TABLE orders (
  	invoiceno VARCHAR(10) PRIMARY KEY,
  	invoicedate TIMESTAMP_NTZ(9),
  	unitprice NUMBER(10,2),
  	quantity NUMBER(38,0),
  	-- Add columns that will refer the foreign key 
	customerid NUMBER(38,0),
  	stockcode VARCHAR(255)
);





CREATE OR REPLACE TABLE orders (
  	invoiceno VARCHAR(10) PRIMARY KEY,
  	invoicedate TIMESTAMP_NTZ(9),
  	unitprice NUMBER(10,2),
  	quantity NUMBER(38,0),
  	customerid NUMBER(38,0),
  	stockcode VARCHAR(255),
  	-- Add foreign key refering to the foreign tables
	FOREIGN KEY (customerid) REFERENCES customers(customerid),
  	FOREIGN KEY (stockcode) REFERENCES products(stockcode)
);







==============



Chapter 2
Data relationships, normalisation


CREATE OR REPLACE TABLE suppliers (
    name VARCHAR(255),
    location VARCHAR(255)
);



-- Alter suppliers table
ALTER TABLE suppliers
-- Add new column
ADD COLUMN IF NOT EXISTS region VARCHAR(255);

-- Alter suppliers table
ALTER TABLE suppliers
-- Add the new column
ADD COLUMN IF NOT EXISTS contact VARCHAR(255);


-- Alter suppliers table
ALTER TABLE suppliers
-- Assign the unique identifier
ADD PRIMARY KEY (supplier_id);








-- Create entity
CREATE OR REPLACE TABLE batchdetails (
	-- Add numerical attribute
	batch_id NUMBER(10,0),
	-- Add characters attributes
    batch_number VARCHAR(255),
    production_notes VARCHAR(255)
);

-- SET 'batch_id' as a unique identifier
ALTER TABLE batchdetails
ADD PRIMARY KEY (batch_id);

-- Modify the entity
ALTER TABLE productqualityrating
-- Add new column
ADD COLUMN IF NOT EXISTS batch_id NUMBER(10,0);











Identifying Data Redundancy
-- List all values from the attribute
SELECT manufacturer, company_location
-- Read all these values from the entity 
FROM productqualityrating;

MANUFACTURER	COMPANY_LOCATION
5150	U.S.A.
5150	U.S.A.




SELECT manufacturer, 
	company_location,
	-- Add a count of all the records, and set an alias for it
	COUNT(1) AS product_count
FROM productqualityrating 
-- Aggregate the results
GROUP BY manufacturer, company_location;

MANUFACTURER	COMPANY_LOCATION	PRODUCT_COUNT
Bar Au Chocolat	U.S.A.	7
Animas	U.S.A.	3
Benoit Nihant	Belgium	6




SELECT manufacturer, 
	company_location, 
	COUNT(*) AS product_count
FROM productqualityrating
GROUP BY manufacturer, 
	company_location
-- Add a filter for occurrence count greater than 1
HAVING product_count > 1;

MANUFACTURER	COMPANY_LOCATION	PRODUCT_COUNT
Aelan	Vanuatu	4
AMMA	Brazil	5
Bakau	Peru	2








-- Select the different values for the attributes list
SELECT DISTINCT manufacturer,
	cocoa_percent, 
    ingredients
FROM productqualityrating
-- Add filter for attribute referring to name
WHERE bar_name = 'Arriba'
	-- Add filter for attribute referring to year
	AND year_reviewed > 2006;

MANUFACTURER	COCOA_PERCENT	INGREDIENTS
Hachez	77.0	B;S;C;V
Hoja Verde (Tulicorp)	72.0	B;S
Hoja Verde (Tulicorp)	80.0	B;S;C;L
Hoja Verde (Tulicorp)	58.0	B;S;C;L
Chchukululu (Tulicorp)	55.0	B;S;C




SELECT manufacturer, 
	-- Add count of distinct combinations, and add alias to it
	COUNT(DISTINCT cocoa_percent, ingredients) AS distinct_combinations 
FROM productqualityrating
WHERE bar_name = 'Arriba' 
    AND year_reviewed > 2006 
-- Group the results    
GROUP BY manufacturer;

MANUFACTURER	DISTINCT_COMBINATIONS
Hoja Verde (Tulicorp)	3
Chchukululu (Tulicorp)	1
Hachez	1




SELECT manufacturer, 
	COUNT(DISTINCT cocoa_percent, ingredients) AS distinct_combinations
FROM productqualityrating
WHERE bar_name = 'Arriba' 
    AND year_reviewed > 2006 
GROUP BY manufacturer
-- Add the clause to filter
HAVING distinct_combinations > 1;

MANUFACTURER	DISTINCT_COMBINATIONS
Hoja Verde (Tulicorp)	3












Creating 1NF entities
-- Create a new entity
CREATE OR REPLACE TABLE ingredients (
	-- Add unique identifier 
    -- ingredient_id NUMBER(10,0) UNIQUE,
    ingredient_id NUMBER(10,0) PRIMARY KEY,
  	-- Add other attributes 
    ingredient VARCHAR(255)
);



-- Create a new entity
CREATE OR REPLACE TABLE reviews (
	-- Add unique identifier 
    review_id NUMBER(10,0) PRIMARY KEY,
  	-- Add other attributes 
    review VARCHAR(255)
);

















1NF
SELECT
	-- Clean empty values
	TRIM(f.value)
FROM productqualityrating,
-- Add function to split values separated by comma
LATERAL FLATTEN(INPUT => SPLIT(productqualityrating.ingredients, ';')) f;

TRIM(F.VALUE)
B
S
C
B
S
C
B
S
C
...


SELECT
	-- Create a sequential number
	ROW_NUMBER() OVER (ORDER BY TRIM(f.value)),
	TRIM(f.value)
FROM productqualityrating,
LATERAL FLATTEN(INPUT => SPLIT(productqualityrating.ingredients, ';')) f
-- Group the data
-- GROUP BY DEDUPES THE 'TRIM(f.value)' COL
GROUP BY TRIM(f.value);

ROW_NUMBER() OVER (ORDER BY TRIM(F.VALUE))	TRIM(F.VALUE)
1	B
2	C
3	L
4	S
5	S*
6	Sa
7	V
Showing 7 out of 7 rows




-- Add command to insert data
INSERT INTO ingredients(ingredient_id, ingredient)
SELECT
	ROW_NUMBER() OVER (ORDER BY TRIM(f.value)),
	TRIM(f.value)
FROM productqualityrating,
LATERAL FLATTEN(INPUT => SPLIT(productqualityrating.ingredients, ';')) f
GROUP BY TRIM(f.value);




-- Modify script for review
INSERT INTO reviews(review_id, review)
SELECT
	ROW_NUMBER() OVER (ORDER BY TRIM(f.value)),
	TRIM(f.value)
FROM productqualityrating,
LATERAL FLATTEN(INPUT => SPLIT(productqualityrating.review, ';')) AS f
GROUP BY TRIM(f.value);


review_id	review
1	
2	""Andes"" mint
3	"oily
4	"silky
5	Cadbury egg
100	burnt caramel














2NF
-- Add new entity
CREATE OR REPLACE TABLE manufacturers (
  	-- Assign unique identifier
  	manufacturer_id NUMBER(10,0) PRIMARY KEY,
  	--Add other attributes
  	manufacturer VARCHAR(255),
  	company_location VARCHAR(255)
);



-- Add values to manufacturers
INSERT INTO manufacturers (manufacturer_id, manufacturer, company_location)
SELECT 
	-- Generate a sequential number
    -- THIS WORKS
	ROW_NUMBER() OVER (ORDER BY manufacturer, company_location) AS manufacturer_id,
	-- BUT DATACAMP WAS LOOKING FOR THIS ANSWER BELOW WITHOUT ALIAS
	-- ROW_NUMBER() OVER (ORDER BY manufacturer, company_location),
    manufacturer, 
	company_location
FROM productqualityrating
-- Aggregate data by the other attributes
GROUP BY manufacturer, 
	company_location;























3NF
-- Create entity
CREATE OR REPLACE TABLE locations (
	-- Add unique identifier
  	location_id NUMBER(10,0) PRIMARY KEY,
  	-- Add main attribute
  	location VARCHAR(255)
);



manufacturers table example
manufacturer_id	manufacturer	company_location
1	Aelan	Vanuatu
2	AMMA	Brazil
3	Bakau	Peru



-- Populate entity from other entity's data
INSERT INTO locations (location_id, location)
SELECT 
	-- Generate unique sequential number
	ROW_NUMBER() OVER (ORDER BY company_location),
    -- Select the main attribute
	company_location
FROM manufacturers
-- Aggregate data by main attribute
GROUP BY company_location;



-- DROP FIELD FROM PREVIOUS TABLE
-- Modify entity
ALTER TABLE manufacturers
-- Remove attribute
DROP COLUMN IF EXISTS company_location;






==============



Chapter 3
--Data modeling

-- Create new entity
CREATE OR REPLACE TABLE employee_training_details (
    -- Assign a unique identifier for the entity
    employee_training_id NUMBER(10,0) PRIMARY KEY,
    -- Add new attribute
    year NUMBER(4,0),
    -- Add new attributes to reference foreign entities
    employee_id NUMBER(38,0),
    training_id NUMBER(38,0),
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id),
    FOREIGN KEY (training_id) REFERENCES trainings(training_id)
);


-- ALTERNATIVE SOL - condense from 4 lines to 2 lines
CREATE OR REPLACE TABLE employee_training_details (
    employee_training_id NUMBER(10,0) PRIMARY KEY,
    year                 NUMBER(4,0),
    employee_id          NUMBER(38,0) REFERENCES employees(employee_id),
    training_id          NUMBER(38,0) REFERENCES trainings(training_id)
);









--Retrieving data from ER model
SELECT 
	-- Add attributes to select
	e.employee_id, 
    t.avg_training_score
FROM employees e
	-- Merge entities on common keys
	JOIN trainings t
	ON e.employee_id = t.employee_id
LIMIT 50;


EMPLOYEE_ID	AVG_TRAINING_SCORE
42639	46
42996	58



SELECT 
	employees.employee_id, 
    trainings.avg_training_score
FROM employees
	JOIN trainings 
	ON employees.employee_id = trainings.employee_id
-- Add filter
WHERE trainings.avg_training_score > 65
LIMIT 50;

EMPLOYEE_ID	AVG_TRAINING_SCORE
60889	83
44159	84


SELECT 
	employees.employee_id, 
    trainings.avg_training_score
FROM employees
	JOIN trainings 
	ON employees.employee_id = trainings.employee_id
    -- Merge new entity
    JOIN departments
    ON employees.department_id = departments.department_id
WHERE trainings.avg_training_score > 65
	-- Add extra filter
	AND departments.department_name = 'Operations'
LIMIT 50;

EMPLOYEE_ID	AVG_TRAINING_SCORE
6411	74
68388	74
20992	71










--Preparing dimension tables
--Modify entity
ALTER TABLE IF EXISTS employees
RENAME TO dim_employees;

ALTER TABLE IF EXISTS departments 
RENAME TO dim_departments;

ALTER TABLE IF EXISTS trainings
RENAME TO dim_trainings;


--Create dimension table
-- Create new entity
CREATE OR REPLACE TABLE dim_date (
  	-- Add unique identifier
    date_id NUMBER(10,0) PRIMARY KEY,
  	-- Add new attributes to register date
    year NUMBER(4,0),
    month NUMBER(2,0)
);











--Retrieving data from dimensional model
SELECT
	-- Retrieve all attributes from the dimension
	dim_employees.*
FROM fact_employee_trainings 
	-- Merge fact table with dimension
	JOIN dim_employees
    ON fact_employee_trainings.employee_id = dim_employees.employee_id;
EMPLOYEE_ID	DEPARTMENT_ID	EDUCATION	GENDER	AGE
13734	2	Bachelor's	f	34
45860	3	Bachelor's	m	43


SELECT 
	dim_employees.*,
    -- Retrieve average training scores
    dim_trainings.avg_training_score
FROM fact_employee_trainings 
	JOIN dim_employees
    ON fact_employee_trainings.employee_id = dim_employees.employee_id
    -- Merge fact table with dimension
    JOIN dim_trainings
    ON fact_employee_trainings.training_id = dim_trainings.training_id
-- Add filter
WHERE dim_trainings.avg_training_score < 100;

EMPLOYEE_ID	DEPARTMENT_ID	EDUCATION	GENDER	AGE	AVG_TRAINING_SCORE
30075	1	Bachelor's	f	31	45
13619	1	Master's & above	m	46	47


	
SELECT 
	dim_employees.*,
    dim_trainings.avg_training_score,
    -- Add new attribute
    dim_departments.department_name
FROM fact_employee_trainings 
	JOIN dim_employees
    ON fact_employee_trainings.employee_id = dim_employees.employee_id
    JOIN dim_trainings 
    ON fact_employee_trainings.training_id = dim_trainings.training_id
    -- Add dimension needed
	JOIN dim_departments
    ON fact_employee_trainings.department_id = dim_departments.department_id
WHERE dim_trainings.avg_training_score < 100;

EMPLOYEE_ID	DEPARTMENT_ID	EDUCATION	GENDER	AGE	AVG_TRAINING_SCORE	DEPARTMENT_NAME
55409	2	Below Secondary	f	25	52	Finance
55409	6	Below Secondary	m	25	52	Finance





	
dim_date table
date_id	year	month
1	2023	5
2	2023	8
	
SELECT 
	dim_employees.*,
    dim_trainings.avg_training_score,
    dim_departments.department_name
FROM fact_employee_trainings 
	JOIN dim_employees
    ON fact_employee_trainings.employee_id = dim_employees.employee_id
    JOIN dim_trainings 
    ON fact_employee_trainings.training_id = dim_trainings.training_id
    JOIN dim_departments 
    ON fact_employee_trainings.department_id = dim_departments.department_id
    -- Add dimension needed
    JOIN dim_date
    ON fact_employee_trainings.date_id = dim_date.date_id
WHERE dim_trainings.avg_training_score < 100   
    -- Add extra filter
    AND dim_date.year = 2023;

EMPLOYEE_ID	DEPARTMENT_ID	EDUCATION	GENDER	AGE	AVG_TRAINING_SCORE	DEPARTMENT_NAME
71565	2	Bachelor's	m	27	77	Procurement
71565	2	Bachelor's	f	27	77	Procurement














Data vault
- hub (each main 'entity'/topic)
- link (relationships between 'hub' entities)
- satellite (changing fields for each 'hub' entity)

Creating hubs
-- Create a new hub entity
CREATE OR REPLACE TABLE hub_employee (
	-- Assign automated values to the hub key
	hub_employee_key NUMBER(10,0) AUTOINCREMENT PRIMARY KEY,
	employee_id NUMBER(38,0),
	-- Add attributes for historical tracking
	load_date TIMESTAMP,
	record_source VARCHAR(255)
);


CREATE OR REPLACE TABLE hub_department (
	-- Assign automated values to the hub key
	hub_department_id NUMBER(10,0) AUTOINCREMENT PRIMARY KEY,
  	-- Add hubs key reference
	-- 2025.10.29: 'hub_department_id' is a PK for this table
	-- WHICH IS DIFFERENT FROM 'department_id' BELOW
	-- SO NUMBER PRECISION IS DIFFERENT
	department_id NUMBER(38,0),
	-- Add attributes for historical tracking
	load_date TIMESTAMP,
	record_source VARCHAR(255)
);



CREATE OR REPLACE TABLE hub_training (
	-- Add hub key
	hub_training_key NUMBER(10,0) AUTOINCREMENT PRIMARY KEY,
    -- Add the key attribute of trainings
	training_id NUMBER(38,0),
	-- Add history tracking attributes
	load_date TIMESTAMP,
	record_source VARCHAR(255)
);








Creating satellites
-- Create a new satellite
CREATE OR REPLACE TABLE sat_employee (
	sat_employee_key NUMBER(10,0) AUTOINCREMENT PRIMARY KEY,
	hub_employee_key NUMBER(10,0),
   	employee_name VARCHAR(255),
    gender CHAR(1),
    age NUMBER(3,0),
	-- Add history tracking attributes
	load_date TIMESTAMP,
    record_source VARCHAR(255),
	-- Add a reference to foreign hub
    FOREIGN KEY (hub_employee_key) REFERENCES hub_employee(hub_employee_key)
);


CREATE OR REPLACE TABLE sat_department (
	-- Add the satellite's unique identifier
	sat_department_key NUMBER(10,0) AUTOINCREMENT PRIMARY KEY,
	-- Add the hub's key attribute
	hub_department_key NUMBER(10,0),
	department_name VARCHAR(255),
	region VARCHAR(255),
    -- Add history tracking attributes
    load_date TIMESTAMP,
    record_source VARCHAR(255),
	-- Add a reference to foreign hub
	FOREIGN KEY (hub_department_key) REFERENCES hub_department(hub_department_key)
);



CREATE OR REPLACE TABLE sat_training (
	sat_training_key NUMBER(10,0) AUTOINCREMENT PRIMARY KEY,
	-- Add the hub's key reference
	hub_training_key NUMBER(10,0),
	training_type VARCHAR(255),
    duration NUMBER(4,0),
    trainer_name VARCHAR(255),
    load_date TIMESTAMP,
    record_source VARCHAR(255),
	-- Add a reference to foreign hub
	FOREIGN KEY (hub_training_key) REFERENCES hub_training(hub_training_key)
);









Creating links
-- Create a new entity
CREATE OR REPLACE TABLE link_all (
	-- Add a unique identifier to the link
	link_key NUMBER(10,0) AUTOINCREMENT PRIMARY KEY,
    -- Add history tracking attributes
	load_date TIMESTAMP,
    record_source VARCHAR(255)
);

CREATE OR REPLACE TABLE link_all (
	link_key NUMBER(10,0) AUTOINCREMENT PRIMARY KEY,
    -- Add the hub's key attribute
	hub_employee_key NUMBER(10,0),
  	load_date TIMESTAMP,
    record_source VARCHAR(255),
  	-- Add a relationship with the foreign hub
	FOREIGN KEY (hub_employee_key) REFERENCES hub_employee(hub_employee_key)
);

CREATE OR REPLACE TABLE link_all (
	link_key NUMBER(10,0) AUTOINCREMENT PRIMARY KEY,
	hub_employee_key NUMBER(10,0),
  	-- Add the hub's key attributes
  	hub_training_key NUMBER(10,0),
  	hub_department_key NUMBER(10,0),
  	load_date TIMESTAMP,
    record_source VARCHAR(255),
	FOREIGN KEY (hub_employee_key) REFERENCES hub_employee(hub_employee_key),
  	-- Add a relationship with the foreign hubs
	FOREIGN KEY (hub_training_key) REFERENCES hub_training(hub_training_key),
  	FOREIGN KEY (hub_department_key) REFERENCES hub_department(hub_department_key)
);







SELECT
	-- Add the attribute from employees
    hub_e.hub_employee_key,
    -- Add the attribute from the department
    sat_d.department_name
FROM hub_employee AS hub_e
	-- Merge hub with link
	JOIN link_all AS li
    ON hub_e.hub_employee_key = li.hub_employee_key
	-- Merge link with satellite
    JOIN sat_department AS sat_d
    ON li.hub_department_key = sat_d.hub_department_key;


HUB_EMPLOYEE_KEY	DEPARTMENT_NAME
1	Sales & Marketing
1	Analytics
1	Sales & Marketing




	

SELECT
    hub_e.hub_employee_key,
    sat_d.department_name,
    -- Add the new attribute
	sat_t.avg_training_score
FROM hub_employee AS hub_e
	JOIN link_all AS li 
    ON hub_e.hub_employee_key = li.hub_employee_key
    JOIN sat_department AS sat_d 
    ON li.hub_department_key = sat_d.hub_department_key
    -- Merge the satellite, even if there is no data for that employee
    LEFT JOIN sat_training AS sat_t
    ON li.hub_training_key = sat_t.hub_training_key;

HUB_EMPLOYEE_KEY	DEPARTMENT_NAME	AVG_TRAINING_SCORE
1	Legal	50
1	Analytics	50
1	Legal	67




	
SELECT
    hub_e.hub_employee_key,
    sat_d.department_name,
    sat_t.avg_training_score
FROM hub_employee AS hub_e
	JOIN link_all AS li 
    ON hub_e.hub_employee_key = li.hub_employee_key
    JOIN sat_department AS sat_d 
    ON li.hub_department_key = sat_d.hub_department_key
    LEFT JOIN sat_training AS sat_t 
    ON li.hub_training_key = sat_t.hub_training_key
-- Add filter for training
WHERE sat_t.awards_won = 1;

HUB_EMPLOYEE_KEY	DEPARTMENT_NAME	AVG_TRAINING_SCORE
1	Legal	67
1	Analytics	67




SELECT
    hub_e.hub_employee_key,
    sat_d.department_name,
    -- Aggregate the attribute
    MAX(sat_t.avg_training_score) AS average_training
FROM hub_employee hub_e
	JOIN link_all AS li 
    ON hub_e.hub_employee_key = li.hub_employee_key
    JOIN sat_department AS sat_d 
    ON li.hub_department_key = sat_d.hub_department_key
    LEFT JOIN sat_training AS sat_t 
    ON li.hub_training_key = sat_t.hub_training_key
WHERE sat_t.awards_won = 1
-- Group the results 
GROUP BY hub_e.hub_employee_key, sat_d.department_name;

HUB_EMPLOYEE_KEY	DEPARTMENT_NAME	AVERAGE_TRAINING
3	Procurement	67
5	Operations	67
7	Analytics	67




============

CHAPTER 4 Snowflake

Tables
These are made up of rows and columns.
	
Schemas
They can group multiple tables.
They act like folders for better organization and data retrieval.
It defines containers for database objects.
	
Databases
They can provide administrative boundaries for access control, resource allocation, and usage management.

	


-- Create a view customer_financial_summary
CREATE OR REPLACE VIEW customer_financial_summary AS
SELECT c.customerid, 
	c.estimatedsalary,
	cp.productid
FROM customers AS c
-- Merge entity
LEFT JOIN customerproducts AS cp 
ON c.customerid = cp.customerid;



CREATE OR REPLACE VIEW customer_financial_summary AS
SELECT c.customerid, 
	-- Create a new conditional attribute
    CASE 
        WHEN AVG(c.estimatedsalary) > 150000 THEN 'Top Income'
        WHEN AVG(c.estimatedsalary) > 90000 THEN 'High Income'
        WHEN AVG(c.estimatedsalary) > 20000 THEN 'Average Income'
        ELSE 'Low Income'
    END AS customer_category,
    -- Add aggregation to the attributes
    COUNT(DISTINCT cp.productid) AS product_count
FROM customers AS c
	LEFT JOIN customerproducts AS cp 
	ON c.customerid = cp.customerid
-- Group the results
GROUP BY c.customerid;









Query execution order
FROM
JOIN ON
WHERE
GROUP BY
HAVING
ORDER BY
LIMIT





	
-- CTE AND Subquery
WITH customer_status AS (
	SELECT c.customerid,
  		c.age,
        c.tenure,
        CASE 
            WHEN ch.customerid IS NOT NULL THEN 'Churned' 
            ELSE 'Active' 
        END AS status
    FROM customers AS c
    	LEFT JOIN churn AS ch 
  		ON c.customerid = ch.customerid
    GROUP BY c.customerid, c.age, c.tenure, status
)
-- Extract attribute from CTE
SELECT status
FROM customer_status
-- Filter results
WHERE customerid IN (SELECT customerid
                   FROM customers
                   WHERE estimatedsalary > 175000);


STATUS
Churned
Active
Churned
Churned
Churned
Churned
Churned










WITH customer_status AS (
	SELECT c.customerid,
  		c.age,
        c.tenure,
        CASE 
            WHEN ch.customerid IS NOT NULL THEN 'Churned' 
            ELSE 'Active' 
        END AS status
    FROM customers AS c
    	LEFT JOIN churn AS ch 
  		ON c.customerid = ch.customerid
    GROUP BY c.customerid, c.age, c.tenure, status
)
SELECT status,
	-- Count customers
	COUNT(customerid) AS unique_customers
FROM customer_status
WHERE customerid IN (SELECT customerid 
                     FROM customers 
                     WHERE estimatedsalary > 175000)
-- Aggregate values
GROUP BY status;

STATUS	UNIQUE_CUSTOMERS
Churned	620
Active	640











	
WITH customer_status AS (
	SELECT c.customerid,
  		c.age,
        c.tenure,
        CASE 
            WHEN ch.customerid IS NOT NULL THEN 'Churned' 
            ELSE 'Active' 
        END AS status
    FROM customers AS c
    	LEFT JOIN churn AS ch 
  		ON c.customerid = ch.customerid
    GROUP BY c.customerid, c.age, c.tenure, status
)
SELECT status,
	COUNT(customerid) AS unique_customers,
    -- Calculate averages
    AVG(age) AS average_age,
    AVG(tenure) AS average_tenure
FROM customer_status
WHERE customerid IN (SELECT customerid 
                     FROM customers 
                     WHERE estimatedsalary > 175000)
GROUP BY status
-- Filter data
HAVING average_tenure >2;


STATUS	UNIQUE_CUSTOMERS	AVERAGE_AGE	AVERAGE_TENURE
Churned	620	38.816129	4.961290
Active	640	38.934375	5.054688






