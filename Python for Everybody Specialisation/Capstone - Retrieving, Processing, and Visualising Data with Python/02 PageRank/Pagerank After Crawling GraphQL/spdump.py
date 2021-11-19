import sqlite3

conn = sqlite3.connect('spider.sqlite')
cur = conn.cursor()

cur.execute('''SELECT COUNT(from_id) AS inbound, old_rank, new_rank, id, url
     FROM Pages JOIN Links ON Pages.id = Links.to_id
     WHERE html IS NOT NULL
     GROUP BY id ORDER BY inbound DESC''')

count = 0
print('Column Headers: COUNT(from_id) AS inbound, old_rank, new_rank, id, url')
for row in cur :
    if count < 50 : print(row)
    count = count + 1

print(count, 'rows.')
cur.close()




'''
Visualise Outputs

#Spdump on parity
#only 6 'Pages' records with 'html' field value not being NULL

Column Headers: COUNT(from_id) AS inbound, old_rank, new_rank, id, url
(6, 1.0, 1.0, 6, 'https://www.getparity.ai/contact-us')
(6, 1.0, 1.0, 5, 'https://www.getparity.ai/careers')
(6, 1.0, 1.0, 4, 'https://www.getparity.ai/about')
(6, 1.0, 1.0, 3, 'https://www.getparity.ai/how-it-works')
(6, 1.0, 1.0, 2, 'https://www.getparity.ai/cart')
(6, 1.0, 1.0, 1, 'https://www.getparity.ai')
6 rows.
'''





'''
#Spdump on graphql

Column Headers: COUNT(from_id) AS inbound, old_rank, new_rank, id, url
(84, 1.0, 3.8870906575357127, 15, 'https://graphql.org/codeofconduct')
(84, 1.0, 3.8870906575357127, 14, 'https://graphql.org/brand')
(84, 1.0, 3.939792095129702, 13, 'https://graphql.org/foundation/community-grant')
(84, 1.0, 3.924421117181356, 12, 'https://graphql.org/community/upcoming-events')
(84, 1.0, 3.9866355653162824, 11, 'https://graphql.org/community/users')
(84, 1.0, 4.018487891523265, 10, 'https://graphql.org/learn/best-practices')
(84, 1.0, 4.0986118821084965, 8, 'https://graphql.org/blog')
(84, 1.0, 3.939792095129703, 7, 'https://graphql.org/foundation')
(84, 1.0, 4.018487891523265, 6, 'https://graphql.org/faq')
(84, 1.0, 3.924421117181356, 5, 'https://graphql.org/community')
(84, 1.0, 3.924421117181356, 4, 'https://graphql.org/code')
(84, 1.0, 4.018487891523265, 3, 'https://graphql.org/learn')
(84, 1.0, 3.9070004012785313, 2, 'https://graphql.org')
(83, 1.0, 3.9350726163703054, 16, 'https://graphql.org/foundation/contact')
(36, 1.0, 0.560082785945487, 61, 'https://graphql.org/blog/graphql-a-query-language')
(36, 1.0, 0.560082785945487, 59, 'https://graphql.org/blog/subscriptions-in-graphql-and-relay')
(36, 1.0, 0.560082785945487, 58, 'https://graphql.org/blog/mocking-with-graphql')
(36, 1.0, 0.560082785945487, 57, 'https://graphql.org/blog/rest-api-graphql-wrapper')
(35, 1.0, 0.36516104930717747, 60, 'https://graphql.org/tags/spec')
(35, 1.0, 0.36516104930717747, 56, 'https://graphql.org/tags/blog')
(35, 1.0, 0.560082785945487, 55, 'https://graphql.org/blog/production-ready')
(35, 1.0, 0.36532097134935965, 53, 'https://graphql.org/blog/2018-11-06-linux-foundation-announces-intent-to-form-new-foundation-to-support-graphql')
(35, 1.0, 0.36516104930717747, 47, 'https://graphql.org/tags/in-the-news')
(35, 1.0, 0.36516104930717747, 45, 'https://graphql.org/blog/2019-03-12-graphql-foundation-announces-collaboration-with-jdf')
(35, 1.0, 0.36532097134935965, 44, 'https://graphql.org/blog/2019-10-28-graphql-foundation-launches-interactive-landscape-welcomes-new-members')
(35, 1.0, 0.36516104930717747, 43, 'https://graphql.org/blog/2019-10-31-linux-foundation-training-announces-free-online-course-exploring-graphql')
(35, 1.0, 0.36516104930717747, 41, 'https://graphql.org/blog/2020-04-03-web-based-graphql-ides-for-the-win')
(35, 1.0, 0.36516104930717747, 40, 'https://graphql.org/blog/2020-06-13-graphql-joins-google-season-of-docs')
(35, 1.0, 0.36532097134935965, 38, 'https://graphql.org/blog/2020-09-11-graphql-foundation-monthly-newsletter-august-2020')
(35, 1.0, 0.36532097134935965, 36, 'https://graphql.org/blog/2020-10-15-graphql-foundation-monthly-newsletter-september-2020')
(35, 1.0, 0.36532097134935965, 35, 'https://graphql.org/blog/2020-11-12-graphql-foundation-monthly-newsletter-october-2020')
(35, 1.0, 0.36516104930717747, 34, 'https://graphql.org/tags/announcements')
(35, 1.0, 0.36516104930717747, 33, 'https://graphql.org/blog/2020-12-08-improving-latency-with-defer-and-stream-directives')
(35, 1.0, 0.36532097134935965, 32, 'https://graphql.org/blog/2021-02-15-graphql-foundation-monthly-newsletter-february-2021')
(35, 1.0, 0.36516104930717747, 31, 'https://graphql.org/blog/2021-03-31-graphql-foundation-monthly-newsletter-march-2021')
(35, 1.0, 0.36516104930717747, 30, 'https://graphql.org/blog/2021-04-30-graphql-foundation-monthly-newsletter-april-2021')
(35, 1.0, 0.36516104930717747, 29, 'https://graphql.org/tags/newsletter')
(35, 1.0, 0.36532097134935965, 28, 'https://graphql.org/blog/2021-06-30-graphql-foundation-monthly-newsletter-june-2021')
(34, 1.0, 0.36516104930717747, 54, 'https://graphql.org/blog/2017-11-08-programmableweb-graphql-moving-to-neutral-open-source-foundation')
(34, 1.0, 0.36516104930717747, 52, 'https://graphql.org/blog/2018-11-06-infoworld-graphql-gets-its-own-foundation')
(34, 1.0, 0.36516104930717747, 51, 'https://graphql.org/blog/2018-11-06-eweek-graphql-api-specification-moving-forward-with-independent-foundation')
(34, 1.0, 0.36516104930717747, 50, 'https://graphql.org/blog/2018-11-07-the-register')
(34, 1.0, 0.36516104930717747, 49, 'https://graphql.org/blog/2018-11-07-sd-times-lf-announces-plans-to-form-graphql-foundation')
(34, 1.0, 0.36516104930717747, 48, 'https://graphql.org/blog/2018-11-07-datanami-will-graphql-become-a-standard-for-the-new-data-economy')
(34, 1.0, 0.36516104930717747, 46, 'https://graphql.org/blog/2018-11-12-channel-futures-graphql-api-query-language-growing')
(34, 1.0, 0.36532097134935965, 42, 'https://graphql.org/blog/2020-04-02-announcing-the-first-graphql-foundation-annual-report')
(34, 1.0, 0.36516104930717747, 39, 'https://graphql.org/blog/2020-06-30-gsoc-2020-participant-naman')
(34, 1.0, 0.36516104930717747, 37, 'https://graphql.org/blog/2020-09-21-gsod-carolyn-stransky')
(19, 1.0, 0.4790320412887979, 65, 'https://graphql.org/graphql-js')
(19, 1.0, 0.25780455161557114, 64, 'https://graphql.org/graphql-js/authentication-and-express-middleware')
84 rows.
'''
