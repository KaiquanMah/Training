### SQL vs NoSQL
<img width="1038" height="834" alt="sqlnosql" src="https://github.com/user-attachments/assets/bc4ed9fb-6259-4c07-84ed-600d0bd02196" />

NoSQL
- high availability
- scalable
- may not be 'consistent' at a point in time

Relational DB
- MySQL
- PostgreSQL
- Redshift
- Oracle
- MariaDB
- MS SQL Server
- scale vertically
- Define known/static schema, PK-FK
- ACID guarantee - data quality, consistency, integrity
- for legacy (acc, fin, bkg, inv mgt, txn mgt) systems, complex queries

ACID
- Atomicity: **All or nothing for transaction completion**.
- Consistency: The database must be **consistent no matter what happens 100% of the time**
- **Isolation**: **No transaction** should **affect** the existence of **any other transaction**.
<img width="1375" height="666" alt="isol" src="https://github.com/user-attachments/assets/81ff5926-ef9e-4fce-b47f-4eb762d7ff01" />
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



