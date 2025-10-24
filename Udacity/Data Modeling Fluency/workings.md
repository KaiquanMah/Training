# SQL vs NoSQL
<img width="1038" height="834" alt="sqlnosql" src="https://github.com/user-attachments/assets/bc4ed9fb-6259-4c07-84ed-600d0bd02196" />

**NoSQL = Not only SQL / Non-relational**
- high availability
  - because you sacrifice consistency at a point in time
  - BUT **EVENTUALLY CONSISTENT**
- scale horizontally w distributed systems
- supports schema evolution/changes - no need to predefine schema
- Examples
  - Document-oriented
    - **Docs = JSON, BSON (OR JSONB = binary JSON = binary-encoded serialisation of JSON-like docs for efficient storage, scan speed), XML** - self-contained, usu nested, flex, schema-less
    - **retrieve using 'document ID' OR fields (exact match) - content management system**
    - MongoDB (can be document OR k-v), DynamoDB, Apache CouchDB, Couchbase, Firebase Firestore
      - MongoDB
        - MongoDB is a general-purpose, document-based, distributed database
        - Uses **JSON format**
        - Offers Query APIs
        - https://www.mongodb.com/
        - https://en.wikipedia.org/wiki/MongoDB
      - Apache CouchDB
        - Open-source document-oriented NoSQL database, implemented in Erlang
        - CouchDB uses **multiple formats and protocols** to store, transfer, and process its data
        - It uses **JSON to store data**, **JavaScript** as its **query** language using **MapReduce**, and **HTTP for an API**
        - https://couchdb.apache.org/
  - Key-value:
    - collection of k-v pairs
    - **retrieve using 'exact key' (exact match) - session/cache management**
    - DynamoDB (can be document OR k-v), Apache Cassandra (wide column OR wide col), Redis, Memcached, Riak, Amazon ElastiCache
      - Cassandra
        - Open-source, distributed NoSQL database
        - Originally developed internally at Facebook and was released as an open-source project in July 2008
        - continuous availability (zero downtime)
        - high performance
        - linear scalability that modern applications require
        - while also offering operational simplicity and effortless replication across data centers and geographies
        - https://cassandra.apache.org/_/index.html
        - https://www.ibm.com/think/topics/cassandra
  - Wide column:
    - column families
    - **retrieve using 'row key/partition key' then 'clustering columns/column family' then 'column'**
    - **query across rows only for 1 col (eg aggregated match) - time series analysis**
    - **NOT optimised for complex aggregations across many rows/cols**
    - ```cql
      SELECT
        user_id,
        COUNT(*) AS total_visits
      FROM
        user_events
      WHERE
        user_id = 'user_987'
      -- In most wide-column stores, running this query across ALL user_ids
      -- requires an inefficient ALLOW FILTERING or a separate data architecture.
      GROUP BY
        user_id;
      ```
    - Apache HBase, Google Bigtable, ScyllaDB
      - Apache HBase
        - Open-source non-relational distributed database
        - **Modeled after Google's Bigtable and written in Java**
        - Developed as part of Apache Software Foundation's Apache Hadoop project and **runs on top of HDFS**
        - https://hbase.apache.org/
  - Graph stores:
    - stores nodes/entities, edges/relationships
    - **retrieve using path (of start/end nodes AND 1/more edge(s))**
    - traverse relationships (pattern match) - social network connections
    - ```cypher
      -- Find the friends of John's friends (2-hop path) who live in the same City as John.
      MATCH
          (john:Person {name: 'John'})-[:FRIENDS_WITH]->(friend1:Person),
          (friend1)-[:FRIENDS_WITH]->(friend2:Person)
      WHERE
          friend2.name <> 'John'
      -- Use a third pattern match to ensure p2 and john share a City node
      MATCH
          (john)-[:LIVES_IN]->(city:City)<-[:LIVES_IN]-(friend2)
      
      RETURN
          friend2.name AS Recommended_Friend
      ```
    - Neptune Neo4J, Titan, ArangoDB (multi-model)
- NoSQL data modeling principles
  - denormalised, no JOINs
  - Work backwards
  - **1 Understand the business problem first, before creating schemas**
    - You have to **know the application and future requirements**
    - Qns to ask
      - SQL vs NoSQL
        - nature, type of dataset
        - vol of data, vol growth pattern
        - how apps query ur data / Understand ur application's access patterns
        - filters
        - keys
        - expressions/aggregations
        - can app handle eventual consistency? YES
        - prioritise HA, scalability over strong consistency? YES
        - little OR many schema changes over time? many schema changes (NoSQL)
      - which NoSQL DB
        - cloud-native vs self-managed data centre
        - which type of NoSQL DB - 4 types above
        - data encryption, compliance
        - SLA
        - existing contracts w NoSQL vendors
      - tips
        - application monitoring, alert - spike in traffic
        - load test b4 deploy application, simulate forseeable failure scenarios
        - **set your Read Capacity Unit (RCU) / Write Capacity Unit (WCU) for provisioned capacity mode tables**
          - **= number of strongly consistent reads/writes per second for ur application**
          - **capacity mode = {on-demand, provisioned}**
            - https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/capacity-mode.html
  - **2 create/design initial table schemas**
    - **Create AS FEW SCHEMAS** as possible
  - **3 evolve/update data model iteratively**
    - **Data model can change as needs change**
    - Be willing to iterate and be agile with the process



Relational DB
- Easier to use - SQL
- Flexibility for writing in SQL queries- 
- Easier to change to business requirements
- Modeling the actual data, not modeling queries (i.e. the dataset/results u want)
- Ability to do JOINS
- Ability to do aggregations and analytics
- Smaller data volumes
- Secondary Indexes available
  - primary index = PK
  - The Problem: **If you search the table using a column that is not the primary key** (e.g., searching for a user by their email_address), the database has to scan the entire table, row by row. This is called a **full table scan and is very slow on large tables.**
  - The Secondary Index Solution: The **secondary index creates a separate, sorted list of values from the secondary-indexed column**. Next to each of those values, it stores a pointer (often the Primary Key value) to the full row in the main table.
  - When you run a **search query**:
    - The database **first searches the small, sorted secondary index (a very fast operation).**
    - It **finds the relevant Primary Key(s)** for the matching rows.
    - It then uses the Primary Key(s) to **fetch the complete row data from the main table**
  - Gd
    - Faster read/search
      - Filter by secondary index, then retrieve primary index and the relevant rows
      - Reads traverses through the **secondary index col (which is ald sorted)** - so no need to sort again **(i.e. no need to ORDER BY secondary idx col in ur query)**
  - Bad
    - Slower write - insert, update, delete
    - inc storage
    - inc maintenance overhead - update secondary idx col every time data in the col changes
      - INSERT - insert row >> write new row into 'every secondary index' col
        ```
        Main Table
        user_id PK|firstname|email 2IDX
        1|alice|alice@a.com
        2|bob|bob@b.com      <- INSERTED
        ---------------
        Secondary Index
        email   Index Key | user_id   Pointer to main table row
        alice@a.com       |  1
        bob@b.com         |  2      <- INSERTED
        ```
      - UPDATE
        - dont update secondary idx col >> no impact
        ```
        Main Table
        user_id PK|firstname|email 2IDX
        1|alice|alice@a.com
        2|BOBBY|bob@b.com <- UPDATED
        ---------------
        Secondary Index   <- NO CHANGE
        email   Index Key | user_id   Pointer to main table row
        alice@a.com       |  1
        bob@b.com         |  2
        ```
        - update secondary idx col >> delete old seondary idx, insert new secondary idx
        ```
        Main Table
        user_id PK|firstname|email 2IDX
        1|alice|alice@new.com   <- UPDATED
        2|BOBBY|bob@b.com
        ---------------
        Secondary Index
        email   Index Key | user_id   Pointer to main table row
        alice@a.com       |  1   <- DELETED
        alice@new.com     |  1   <- INSERTED
        bob@b.com         |  2
        ```
      - DELETE - delete row >> delete tt row from 'every secondary index'
        ```
        Main Table
        user_id PK|firstname|email 2IDX
        1|alice|alice@a.com
        2|BOBBY|bob@b.com      <- DELETE
        ---------------
        Secondary Index
        email   Index Key | user_id   Pointer to main table row
        alice@a.com       |  1
        bob@b.com         |  2      <- DELETE
        ```
      - You do not need to "rerun an index query." The database system automatically and immediately updates the index structure as part of the transaction when the row is modified. This is done to ensure the index is always accurate for subsequent read queries. The overhead is the cost of these extra write/update operations for every index defined on the table.
- scale vertically
- Define known/static schema, PK-FK
- ACID Transactions/guarantee - data quality, consistency, integrity
- for legacy (acc, fin, bkg, inv mgt, txn mgt) systems, complex queries
- Examples
  - MySQL
  - PostgreSQL, Supabase
  - Amazon Redshift (OLAP), Amazon Aurora DB (OLTP)
    - https://aws.amazon.com/rds/aurora/global-database/
  - Google Spanner
    - **relational DB, BUT horizontally scalable (data centres, global)**
    - https://cloud.google.com/spanner
  - Oracle
  - MariaDB
  - MS SQL Server


## ACID
- Atomicity: **Whole/All or nothing for transaction completion**.
  - eg xfer amt from A to B = {withdraw from A, deposit into B}
  - if any sub-item fails => the whole txn fails
  - if ALL sub-item succceeds => the whole txn succeeds
- Consistency: The database must be **consistent no matter what happens 100% of the time**
  - Move DB from 1 'valid state' to another 'valid state'
  - If txn violates any integrity constraint/rules -> DB rejects/rolls back txn to 'previous valid state'
  - **Eventual Consistency** = NoSQL databases offer the idea of eventual consistency. Eventual Consistency means - **when a transaction is executed, it might not update all the copies of the data right away. But the data would be eventually be updated.**
- **Isolation**: **No transaction** should **affect the integrity/existence** of **any other transaction**.
  - **each txn can run independently**
  - **order does not matter**
  - **low isolation - simultaneous 'dirty reads of intermediate results', 'lost updates' by many users**
    ```
    txn A, B - simultaneous read, update, commit
    the last txn overwrites the earlier txn
    A read 100, B read 100
    A +10, commit (total: 110)   -> lost
    B +20, commit (total: 120)  -> B overwrites A
    ---------------------------
    vs Correct total: 130 (from A's +10 and B's +20)
    ```
  - **vs high isolation - use more resources/resource locks, txns block each other**
    - **even if txns happened in parallel**
    - **system behaves as if txns ran sequentially**
    - **people cannot see intermediate results**
      ```
      txn A locks resource/table, blocks txn B (from starting/seeing incorrect intermediate data until txn A is completed)
      txn A completed
      txn B locks resource
      txn B completed
      Correct total: 130 (from A's +10 and B's +20)
      ```
  - <img width="1375" height="666" alt="isol" src="https://github.com/user-attachments/assets/81ff5926-ef9e-4fce-b47f-4eb762d7ff01" />
  - Isolation ensures that multiple transactions can occur concurrently without leading to the inconsistency of the database state. Transactions occur independently without interference.
  - **Changes occurring in a particular transaction will not be visible to any other transaction until that particular change in that transaction is written to memory or has been committed.**
  - This property ensures that the **execution of transactions concurrently will result in an 'equivalent state achieved if txns were executed serially in some order'.**
  - Let X= 500 and Y = 500. Consider two transactions T and T”.
  - Suppose T has been executed till Read statement and then T’’ starts.
  - As a result, interleaving of operations takes place due to which T’’ reads the correct value of X but the incorrect value of Y and sum computed by T’’: (X+Y = 50,000+500=50,500) is thus not consistent with the sum at end of the transaction: T: (X+Y = 50,000 + 450 = 50,450)
  - This is where Isolation comes in: this behavior results in database inconsistency, due to a loss of 50 units. Hence, transactions must take place in isolation and **changes should be visible only after they have been made to the main memory**.
- Durability: The database should be able to handle all transactions **even if there is a failure somewhere during the transaction processing**

What is a transaction?
- Single unit of work that accesses databases through **Read and Write operations.**
- Every read, write, or **query** of a database is a transaction.



## CAP Theorem
- Note: Consistency in CAP theorem is not the same as Consistency in RDBMS ACID.
- **CAP consistency talks about data consistency across a CLUSTER OF NODES** and not on a single server/node
- Side Note: The CAP theorem is also called Brewer’s Theorem because it was first advanced by Professor Eric A. Brewer during a talk he gave on distributed computing in 2000. Two years later, MIT professors Seth Gilbert and Nancy Lynch published a proof of “Brewer’s Conjecture.”

CAP
- Consistency: **Every read** receives the **most recent write or an error**
- Availability: Every request receives a **(non-error) response, without the guarantee** that it contains the **most recent write**
  - operate even when **1/more nodes fail; continues to serve a user**
- Partition tolerance: The system **continues to operate despite an arbitrary number of messages being dropped (or delayed) by the network between nodes**
  - operate even when **1/more network paths fail**
  - **distributed system OR horizontal scaling**
<img width="797" height="783" alt="cap" src="https://github.com/user-attachments/assets/db6c16d3-ed63-478a-ac97-4247fb093ef4" />


CAP theorem suggests that we can only ever have 2 of the 3 properties achieved at the same time.
**Relational DB (RDBMS)**
- CA only: Single Node database server that is **typically not networked (NOT FAULT TOLERANT).** 
vs
**NoSQL**
- CP: Consistency and Partition Tolerance
  - **Nodes not available sometimes to users** - until node/partition is up again AND consistent
- **AP**: Availability and Partition Tolerance
  - **Might not be consistent**
  - **the usual choice**
- CA: Consistency and Availability
  - 2 sides of a network cant guarantee the most recent write to each other
  - to maintain C/A - system faces a dilemma it cannot solve
    - **sacrifice A/availability by shutting down and restarting**
    - **sacrifice C/consistency - 2 indpt sides accept conflicting writes**
  - **possible BUT NOT PRACTICAL for a NoSQL/distributed system**
<img width="1135" height="717" alt="cap-ca-cp-ap" src="https://github.com/user-attachments/assets/fad680c1-20b8-4831-8b6e-2fff9026bcc3" />
- RDBMS vs MongoDB vs Cassandra - CAP Theorem https://bikas-katwal.medium.com/mongodb-vs-cassandra-vs-rdbms-where-do-they-stand-in-the-cap-theorem-1bae779a7a15
- CAP theorem
  - https://www.ibm.com/think/topics/cap-theorem
  - https://dzone.com/articles/understanding-the-cap-theorem
  - https://en.wikipedia.org/wiki/CAP_theorem
  - https://ravindraelicherla.medium.com/cap-theorem-simplified-28499a67eab4



## SQL vs NoSQL Recap
| SQL | NoSQL |
| :--- | :--- |
| 1. **Complex queries with joins, aggregations** | 1. Large number of **simple look-up queries, fast reads** |
| 2. Structured data with **relations** | 2. Structured/semi-structured, no relations, **need to be able to store different data type formats** |
| 3. **Predefined table schema** | 3. No need of predefined table schema |
| 4. **ACID** Guarantee on each transaction | 4. Follows **CAP Theorem** |
| 5. Scales vertically | 5. **Scales Horizontally** |
| 6. Upgrades/maintenance without downtime is hard | 6. **Seamless Upgrades/maintenance without downtime, high availability** |
| 7. Can become very costly over time | 7. **Cheaper than SQL** over time |
| 8. Smaller dataset | 8. **Large dataset** |



# Databases
- Database: A set of related data and the way it is organized
- Database Management System: Computer software that allows users to interact with the database and provides access to all of the data.
- The term database is often used to refer to both the database and the DBMS used.
- conceptual level (tables) >> logical level (fields) >> physical level (DDL)

Importance of Relational Databases / what makes a database system **a valid relational model**
- Standardization of data model
- Flexibility in adding and altering tables
- Data Integrity
- Structured Query Language (SQL)
- Simplicity
- Intuitive Organization

**Codd's 12 rules**
- https://en.wikipedia.org/wiki/Codd%27s_12_rules
- Rule 1: The information rule
  - All **information** in a relational database is **represented explicitly at the logical level** and in exactly one way – **by values in tables**.

**OLAP vs OLTP**
* OLAP - complex **analytical**/adhoc queries - incl **aggregations. Optimised for reads**
* OLTP - **less complex queries, alot records/txns**. **Read, write/insert/update, delete**
* https://stackoverflow.com/questions/21900185/what-are-oltp-and-olap-what-is-the-difference-between-them

 **Normalise vs denormalise**
 - Normalise - Reduce copies of data / dec data redundancy, inc data integrity, by structuring relational DB according to a series of 'Normal Forms'
   - song table
     - <img width="469" height="244" alt="table4" src="https://github.com/user-attachments/assets/241927b2-5a7e-48bd-a0ba-dcadc6582d97" />
   - album table
     - <img width="467" height="138" alt="table5" src="https://github.com/user-attachments/assets/c9476087-26a0-4edb-bf05-1e852658623b" />
   - artist table
     - <img width="590" height="206" alt="table6" src="https://github.com/user-attachments/assets/dc488046-a233-4206-bce3-b163baa5e7bc" />
 - Denormalise - For read-heavy workloads to inc pf
   - <img width="960" height="540" alt="use-this-version-data-modeling-lesson-2" src="https://github.com/user-attachments/assets/37fe3a71-631e-43ed-ba67-2d31b0cf0316" />
- Normal Form
  - 4 objectives
    - To **free the database from unwanted insertions, updates, & deletion dependencies**
    - To **reduce the need for refactoring** the database as new types of data are introduced
    - To make the relational model **more informative to users**
    - To make the **database neutral to the query statistics**
    - https://en.wikipedia.org/wiki/Database_normalization
  - How to reach **First Normal Form (1NF)**:
    - Atomic values: **each cell contains unique and single values**
      - **Single => cant divide into smaller units/parts**
      - **NOT a list/array/nested structure**
        - list - of phone numbers - 555-1234, 555-5678
        - composite value - address - 123 Main St, Anytown, SG 90210
        - nested/repeating groups of items - { "Math": 85, "Science": 92 }
      - eg what we want
        ```
        Before
        Table (Before 1NF)	Student_ID	Courses
        Row 1	              101	        Math, History, Art
        vs
        After
        Table (After 1NF)	Student_ID	Course
        Row 1	            101	        Math
        Row 2	            101	        History
        Row 3	            101	        Art
        ```
    - Be able to add data records without altering tables (ie add/remove cols)
    - **Separate different relations into different tables** - eg customer table, customer ID table, sales table
      ```
      customer table - customer_id|customer_name|customer_email
      customer_id table - store_id|customer_id
      sales table - customer_name|amount
      music_awards table - music_award|year|winning_bandname
      lead_singer table - bandname|lead_singer
      ```
    - Keep relationships between tables together with **foreign keys**
  - **Second Normal Form (2NF):**
    - Have reached 1NF
    - All columns in the table must rely on the **Primary Key** - **NO COMPOSITE KEYS**
  - **Third Normal Form (3NF):**
    - Must be in 2nd Normal Form
    - **No transitive dependencies**. Remember, "transitive dependencies you are trying to maintain" is that to get from A-> C, you want to avoid going through B.
      - ```
        music_awards table - music_award|year|winning_bandname
        lead_singer table - bandname|lead_singer
        ```
      - eg we use music_award AND year to get to winning_bandname, not to get to lead_singer in the same table
        - **dont want dupe 'lead_singer'/data in a col in the same table (like below)**
        - ```
          denormalised awards table - music_award|year|winning_bandname|lead_singer
          ```
  - When to use 3NF:
    - When you want to update data, we want to be able to do in just 1 place. We want to **avoid updating 'multiple dupe/related records' in a 'denormalised Customers Detail' table**
    - **Maximum normal form to attempt = 3NF**
- **Denormalisation**
  - https://en.wikipedia.org/wiki/Denormalization
  - **improve read performance by losing some write (insert, update, delete) performance**
  - eg
    ```
    denormalised customer table - customer_name|country|city|amount
    denormalised shipping table - customer_name|country|city|item -> we repeat customer_name, country, city information across tables
    ```
  - data modeler/designer is responsible to keep the data consistent
  


**Dimension vs Fact Tables**
- **Dimension table**
  - when (eg date table), where (eg store_location table), what (eg pdt table) <something> happened
  - https://en.wikipedia.org/wiki/Dimension_(data_warehouse)
- **Fact table**
  - measurement/**metric**/facts of a biz process
  - **how many** units, etc (eg sales table)
  - can be aggregates
  - values are usu int/numbers
  - https://en.wikipedia.org/wiki/Fact_table
- ```
  Dim_Date    Id (PK)|Date|Day|Day_of_Week|Month|Month_Name|Quarter|Quarter_Name|Year
  Dim_Store   Id (PK)|Store_Number|State_Province|Country
  Dim_Product Id (PK)|EAN_Code|Product_Name|Brand|Product_Category
  Fact_Sales  Date_Id (FK)|Store_Id (FK)|Product_Id (FK)|Units_Sold
  ```
- <img width="1002" height="648" alt="dimension-fact-tables" src="https://github.com/user-attachments/assets/cedfde76-5fd6-464b-ad8b-ceb25702cde8" />
- https://en.wikipedia.org/wiki/Entity%E2%80%93relationship_model
- dimension and fact tables fit in well with a star schema


**Star vs snowflake schema**
- star schema
  - simplest 'data mart' style
  - resembles a star shape
  - **fact table @ the centre, dimension table surround the fact table**
    - **star points = the set of dimension tables** = {Dim_Date, Dim_Store, Dim_Product}
  - **1/more fact tables** tt reference **ANY NUMBER OF dimension tables**
  - https://en.wikipedia.org/wiki/Star_schema
  - Gd
    - Getting a table into 3NF is a lot of hard work, JOINs can be complex even on simple data
    - **Star schema allows for the relaxation of these rules and makes queries easier with simple JOINS**
    - **Denormalise tables, simplify queries/JOINs**
    - **Fast aggregations**
      - **Aggregations** perform calculations and clustering of our data, **so we can reuse AND do not have to do aggregations again in our application**. Examples : COUNT, GROUP BY etc
    - <img width="960" height="540" alt="use-this-version-data-modeling-lesson-2-1" src="https://github.com/user-attachments/assets/4add1bed-4df6-46f8-ac46-9b0b80a16c15" />
  - Bad
    - **Issues w denormalisation - dec data quality/integrity, dec query flexibility (cuz u design ur data model according to ur queries -> difficult to do other types of queries / adhoc queries)**
    - supports 1-to-1 relationships
      - abstract away/simplify many-to-many relationships to fit the data model
- snowflake schema
  - Star Schema is a special, simplified case of the snowflake schema
  - **Snowflake schema (usu 3NF) is more normalised than Star schema (usu at least 1NF, usu not 2NF/3NF)**
  - fact table connected to multiple dimension tables
    - **immediate dimension tables connected to dimension tables @ a subsequent layer**
    - **multiple levels of relationships, child tables have multiple parents**
    - <img width="1459" height="881" alt="Snowflake-schema" src="https://github.com/user-attachments/assets/be513dbb-2143-4f58-9a00-b9d140d7af4c" />
    - <img width="1185" height="645" alt="Snowflake-schema-example" src="https://github.com/user-attachments/assets/acee5c93-7088-4280-a245-6bf728b550cd" />
  - Gd
    - supports many-to-many relationships
  - https://en.wikipedia.org/wiki/Snowflake_schema
  - https://bluepi-in.medium.com/deep-diving-in-the-world-of-data-warehousing-78c0d52f49a




# DynamoDB
- Amazon DynamoDB is a fully managed proprietary NoSQL database service
- Supports key-value and document data structures
- **serverless database, no need to provision or manage the underlying infrastructure**
- can handle millions of requests per second (2-4 milisecond queries on well-designed DynamoDB tables)
  - **in-memory caching** (microsecond queries)
- Use cases
  - [CX] Customer facing application - fast request-responses, dec latency - mobile, web app
  - [CX] AB test / personalisation - adtech
  - [Big data collection] collect huge vol of data from mobile apps - IoT, gaming
- Creating a table in DynamoDB
  - **Requires only a table name and a Primary Key** (no need to know the whole schema)
  - **PK data types: string/number/binary**
  - Click 'Create table'
  - <img width="462" height="235" alt="image" src="https://github.com/user-attachments/assets/569c78c3-05bc-4902-96b0-88ef464ef731" />
- Data in DynamoDB
  - **Table = Collection of items**
  - **Item = Equivalent to a "row"** or a "record" in relational database
    - **= Collection of attributes, w PK/unique identifier**
  - **Attributes = Group of attributes** makes up an item. Similar to "fields" or "columns" in a relational database
    - <img width="241" height="272" alt="image" src="https://github.com/user-attachments/assets/f08518f6-6a2b-4015-b467-9a4e95e96f18" />
    - <img width="224" height="154" alt="image" src="https://github.com/user-attachments/assets/a0b3c274-e350-49f0-a9a0-9b7517750730" />
    - Change from 'tree' to 'text' to check your 'item data' in JSON format
      - <img width="257" height="158" alt="image" src="https://github.com/user-attachments/assets/e70fcf4c-f88e-4671-bf7e-b57fbb7fad85" />
    - DynamoDB JSON
      - AttributeName >> datatype (eg 'S') >> value
      - <img width="187" height="181" alt="image" src="https://github.com/user-attachments/assets/4f04be0b-3232-49b2-993a-bc45bf1bce20" />
  - **Maximum Record/Item size in DynamoDB is 400 KB**
  - Unlimited num of items per table
  - You should **not be storing large objects** such as **images** in DynamoDB (DynamoDB does not support **Blob data types**)
  - DynamoDB **seamlessly handles schema evolution**
    - **each record/item can have diff attributes**
      - <img width="805" height="288" alt="image" src="https://github.com/user-attachments/assets/c98e6683-f405-45c5-97b3-8e3fd966095c" />
  - <img width="1366" height="660" alt="tablenosql" src="https://github.com/user-attachments/assets/bb947d08-7aab-4a40-9384-933041433168" />
  - <img width="1367" height="687" alt="itemnosql" src="https://github.com/user-attachments/assets/90ab1369-5dc5-47bf-927f-774a6e5aef22" />
  - <img width="1360" height="691" alt="attriburesnosql" src="https://github.com/user-attachments/assets/d2f301e5-9ed9-40e3-a698-112fb2b5072a" />
  - <img width="1386" height="631" alt="primakeynosql" src="https://github.com/user-attachments/assets/9b12d61a-2a9c-463a-8cd7-b99036e841b7" />
- https://aws.amazon.com/dynamodb/
- https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf


DynamoDB Keys
- **simple PK = partition key = hash attribute**
  - <img width="543" height="257" alt="pk" src="https://github.com/user-attachments/assets/46965606-e7a0-488a-adfe-bc05fc675c46" />
  - DynamoDB uses hash fn to distribute data across ALL PARTITIONS
    - **Input to hash fn: PK/partition key values**
    - **Output from hash fn: partition_num**
    - **items w same partition_num -> store tgt**
  - 1 DynamoDB data partition = 10GB
- **composite PK = {partition key AND sort/range key}**
  - <img width="539" height="171" alt="composite-pk" src="https://github.com/user-attachments/assets/1061a93c-087a-47d9-ad4b-a2c9e1a41a41" />
  - NoSQL 'sort key' -> equivalent to relationalDB's 'FK'
  - if 2 items have the same 'partition key' => they must have diff 'sort key'
  - **items w same 'partition key' are close tgt**
    - **then sort on 'sort key'**
  - partition key and sort key
    - <img width="612" height="394" alt="partitionkey-and-sortkey" src="https://github.com/user-attachments/assets/4ac56e41-bcfc-492f-aafd-55f3fa72fb84" />
  - 2 mandatory attributes (partition key and sort key) needed at the start
    - <img width="186" height="119" alt="2-mandatory-attributes" src="https://github.com/user-attachments/assets/c068918f-3ee4-44d4-a98d-b35ca2f68c35" />
  - same PK, diff sort key
    - <img width="628" height="258" alt="same-pk-diff-sortkey" src="https://github.com/user-attachments/assets/75c4b537-c29e-4bfa-8c8e-9d8444959d3f" />
  - AWS DynamoDB item query screen - change from 'scan' to 'query'
    - <img width="801" height="368" alt="dynamodb-item-query-screen" src="https://github.com/user-attachments/assets/67f88c3e-2491-45f9-94d4-86e4fc62fdf8" />






