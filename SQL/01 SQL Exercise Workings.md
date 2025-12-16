Data Sanity
(Write your checks — what's broken, what's missing, what's weird?)
- Anyone not at this place today, yet in the system? Not sure how to check
- Records before 1 Feb 2758? Yes. Should we remove those records?
- Is there a way to check which colonizers are active/inactive? No, no flag available


Interpretation & Conclusions
- Earliest date of arrival - 3 Mar 2756
- Latest date of arrival - 6 Jul 2783
- Today's date - 6 Feb 2783 -> so there were records in the future added to the database -> should we remove those records?
- Number of records - 503



```sql
SELECT MIN(date_of_arrival), MAX(date_of_arrival)
FROM arrivals;
-- 2756-03-03T00:00:00.000Z
-- 2783-07-06T00:00:00.000Z

SELECT COUNT(1)
FROM arrivals;
-- 503
```
