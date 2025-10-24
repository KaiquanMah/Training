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
    - MongoDB (can be document OR k-v), DynamoDB, CouchDB, Couchbase, Firebase Firestore
  - Key-value:
    - collection of k-v pairs
    - **retrieve using 'exact key' (exact match) - session/cache management**
    - DynamoDB (can be document OR k-v), Apache Cassandra (wide column OR wide col), Redis, Memcached, Riak, Amazon ElastiCache
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
    - Apache Hbase, Google Bigtable, ScyllaDB
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
  - Redshift
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
  
  

