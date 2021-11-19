#Sequence
#spider.py (get web pages) > sprank.py (compute page rank)

# resolve BeautifulSoup issue
#https://www.coursera.org/learn/python-network-data/supplement/Wwro5/notes-regarding-the-use-of-beautifulsoup
#https://stackoverflow.com/questions/2915471/install-a-python-package-into-a-different-directory-using-pip
# python -m pip install -U pip
#https://stackoverflow.com/questions/63783587/pip-install-cannot-combine-user-and-target
# pip install --target=C:\<folder path>\Py4e beautifulsoup4 --upgrade --no-user
'''
Collecting beautifulsoup4
  Using cached beautifulsoup4-4.10.0-py3-none-any.whl (97 kB)
Collecting soupsieve>1.2
  Using cached soupsieve-2.3.1-py3-none-any.whl (37 kB)
Installing collected packages: soupsieve, beautifulsoup4
Successfully installed beautifulsoup4-4.10.0 soupsieve-2.3.1
'''

import sqlite3
import ssl
from urllib.parse import urljoin, urlparse
from urllib.request import urlopen
import urllib.error
from bs4 import BeautifulSoup

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

#Create SQLite table
conn = sqlite3.connect('spider.sqlite')
cur = conn.cursor()
cur.executescript('''
CREATE TABLE IF NOT EXISTS Webs (url TEXT UNIQUE);

CREATE TABLE IF NOT EXISTS Pages (id INTEGER PRIMARY KEY,
                                  url TEXT UNIQUE,
                                  html TEXT,
                                  error INTEGER,
                                  old_rank REAL,
                                  new_rank REAL);

CREATE TABLE IF NOT EXISTS Links (from_id INTEGER,
                                  to_id INTEGER,
                                  UNIQUE (from_id, to_id));
''')
#https://www.sqlitetutorial.net/sqlite-unique-constraint/
#Webs table lists the starting URL
#Pages table lists the URLs (including starting URL), their HTML elements (if any), and id#
#Links table lists the from_id and to_id


#delete records from sqlite DB as we check the data at different steps
#https://www.sqlitetutorial.net/sqlite-delete/
# cur.executescript('''
# DELETE FROM Webs;
# DELETE FROM Pages;
# DELETE FROM Links;
# ''')





#=========================STARTING URL====================================
#Pick a record randomly
#Check to see whether we are already in progress of web crawling
#page yet to be retrieved => html is NULL
cur.execute('SELECT id, url FROM Pages WHERE html is NULL AND error is NULL ORDER BY RANDOM() LIMIT 1')
row = cur.fetchone()
if row is not None:
    print("Restart existing crawl. You need to remove spider.sqlite if you wish to start a fresh web crawl")
#initiate web crawler
else:
    starturl = input('Enter web url or press "Enter": ')
    if(len(starturl) < 1) : starturl = 'http://dr-chuck.com/'
    #dont need the last forward slash '/' character
    if(starturl.endswith('/')) : starturl = starturl[:-1]

    web = starturl
    if(starturl.endswith('.htm') or starturl.endswith('.html')):
        pos = starturl.rfind('/')
        web = starturl[:pos]

    if(len(web) > 1):
        cur.execute('INSERT OR IGNORE INTO Webs (url) VALUES (?)', (web,))
        # what are the last 2 items? new_rank instantiate as 1.0; leave html as NULL
        cur.execute('INSERT OR IGNORE INTO Pages (url, html, new_rank) VALUES ( ?, NULL, 1.0 )', (starturl, ) )
        conn.commit()
#========================================================================
#Webs => web = website without file extension
#Pages => starturl = URL with (or without) file extension







#Get the current website
cur.execute('SELECT url FROM Webs')
webs = list()
for row in cur:
    webs.append(str(row[0]))

print(webs)
#1st iteration - ['http://dr-chuck.com']







many = 0
while True:
    if ( many < 1 ) :
        sval = input('How many pages:')
        if ( len(sval) < 1 ) : break
        many = int(sval)
    #after 1 webpage, go to the next
    many = many - 1



    #search for a NULL 'html' page
    cur.execute('SELECT id, url FROM Pages WHERE html is NULL and error is NULL ORDER BY RANDOM() LIMIT 1')
    #which we need to crawl
    #iteration 1 - the only record so far
    #id	url	                    html	error	old_rank	new_rank
    # 1	http://dr-chuck.com				                      1.0
    try:
        row = cur.fetchone()
        # print row
        fromid = row[0]
        url = row[1]
    #if 'id' and 'url' were not retrieved
    except:
        print('No unretrieved HTML pages found')
        many = 0
        break

    #https://www.geeksforgeeks.org/gfact-50-python-end-parameter-in-print/
    print(fromid, url, end=' ')
    #1 http://dr-chuck.com


    # If we are retrieving this page, there should be no links from it
    #So wipe out the corresponding 'links'
    cur.execute('DELETE from Links WHERE from_id=?', (fromid, ) )
    #then access the URL
    try:
        document = urlopen(url, context=ctx)

        html = document.read()
        #dont 'decode' here because we will use BeautifulSoup to parse the UTF-8 data later
        #HTTP 200 OK success status response code indicates that the request has succeeded
        #so if HTML document's status code is NOT 200, we have an error
        if document.getcode() != 200 :
            print("Error on page: ",document.getcode())
            cur.execute('UPDATE Pages SET error=? WHERE url=?', (document.getcode(), url) )

        #if what we retrived was not a HTML document
        #remove the url
        if 'text/html' != document.info().get_content_type() :
            print("Ignore non text/html page")
            cur.execute('DELETE FROM Pages WHERE url=?', ( url, ) )
            conn.commit()
            continue

        #not sure why are we printing the length of the <html> string
        #actually it is printing the 'length' of the HTML elements and their content
        print('(' + str(len(html)) + ')', end=' ')
        # 1 http://dr-chuck.com (8386)


        soup = BeautifulSoup(html, "html.parser")
    #KeyboardInterrupt => ctrl C (mac), ctrl z (Windows)
    except KeyboardInterrupt:
        print('')
        print('Program interrupted by user...')
        break
    #https://www.techbeamers.com/use-try-except-python/
    #try-except can have multiple 'except's
    #other exception => BeautifulSoup blew up
    #use error '-1'
    except:
        print("Unable to retrieve or parse page")
        cur.execute('UPDATE Pages SET error=-1 WHERE url=?', (url, ) )
        conn.commit()
        continue


    #url, assign new_rank AND reset its 'html' (if we are crawling the same web page again in future)
    cur.execute('INSERT OR IGNORE INTO Pages (url, html, new_rank) VALUES ( ?, NULL, 1.0 )', ( url, ) )
    #update the reset 'html' with the new 'html' content value
    cur.execute('UPDATE Pages SET html=? WHERE url=?', (memoryview(html), url ) )
    conn.commit()


    # Retrieve all of the anchor tags
    tags = soup('a')
    count = 0
    for tag in tags:
        href = tag.get('href', None)

        #pre-processing steps for URLs
        if ( href is None ) : continue
        # Resolve relative references like href="/contact"
        #https://docs.python.org/3/library/urllib.parse.html
        up = urlparse(href)
        #url 'scheme' => HTTP/S
        if ( len(up.scheme) < 1 ) :
            #https://stackoverflow.com/questions/10893374/python-confusions-with-urljoin
            href = urljoin(url, href)


        #check for an 'anchor'/'#' at the end of a URL
        ipos = href.find('#')
        #throw the 'anchor #' and everything after the anchor away
        if ( ipos > 1 ) : href = href[:ipos]
        #dont process images as we are interested in links/web pages now
        if ( href.endswith('.png') or href.endswith('.jpg') or href.endswith('.gif') ) : continue
        #remove forward slash '/' at the end
        if ( href.endswith('/') ) : href = href[:-1]
        # check href
        if ( len(href) < 1 ) : continue


		# Check if the URL is in any of the webs
        # in 'webs', means we STAYed on the same site
        #so skip crawling the links leaving from this page AGAIN
        found = False
        for web in webs:
            #the 'break' only breaks from this inner IF-statement
            #https://eecs.oregonstate.edu/ecampus-video/CS161/template/chapter_5/nested.html#:~:text=Using%20break%20in%20a%20nested,all%20of%20the%20looping%20stops.
            if ( href.startswith(web) ) :
                found = True
                break
        if not found : continue

        #insert href into Pages
        cur.execute('INSERT OR IGNORE INTO Pages (url, html, new_rank) VALUES ( ?, NULL, 1.0 )', ( href, ) )
        count = count + 1
        conn.commit()

        #extract link/href's id, which is our to_id
        cur.execute('SELECT id FROM Pages WHERE url=? LIMIT 1', ( href, ))
        try:
            row = cur.fetchone()
            toid = row[0]
        except:
            print('Could not retrieve id')
            continue
        # to_id found, so insert (fromid, toid) into the 'Links' table
        cur.execute('INSERT OR IGNORE INTO Links (from_id, to_id) VALUES ( ?, ? )', ( fromid, toid ) )


    print(count)

cur.close()

#end output in PowerShell
#1 http://dr-chuck.com (8386) 2













'''
Maybe not enough web pages linking to and from this site

#=========running the full spider.py script=================
PS C:\...\Py4e> python .\spider.py
Enter web url or press "Enter": https://www.getparity.ai/
['https://www.getparity.ai']

# sval = input('How many pages:')
How many pages:100


# print(fromid, url, end=' ')
#on the same line
# print('(' + str(len(html)) + ')', end=' ')
#on the same line
# print(count)
1 https://www.getparity.ai (189589) 22
6 https://www.getparity.ai/contact-us (61585) 19
2 https://www.getparity.ai/cart (54411) 19
3 https://www.getparity.ai/how-it-works (124408) 20
5 https://www.getparity.ai/careers (62431) 19
4 https://www.getparity.ai/about (121647) 19
No unretrieved HTML pages found
#======================================================

Webs table - 1 record
url
https://www.getparity.ai


Links table - 36 records
from_id	to_id
1	2
1	1
1	3
...
4	5
4	6




Pages table - 2,195 records
id	url	                                 html	                       error	old_rank	new_rank
1	https://www.getparity.ai                 <html tags and content....>                         1.0
2	https://www.getparity.ai/cart                 <html tags and content....>				     1.0                                       1.0
3   https://www.getparity.ai/how-it-works                 <html tags and content....>            1.0
4   https://www.getparity.ai/about                 <html tags and content....>                   1.0
5   https://www.getparity.ai/careers                 <html tags and content....>                 1.0
6   https://www.getparity.ai/contact-us                 <html tags and content....>              1.0
'''












'''
Run on TigerGraph's site
Maybe TigerGraph site cant be crawled


PS C:\...\Py4e> python .\spider.py
Enter web url or press "Enter": https://www.tigergraph.com/
['https://www.tigergraph.com']
How many pages:100
1 https://www.tigergraph.com Unable to retrieve or parse page
No unretrieved HTML pages found
'''






'''
Run on graphql's site
Allows crawling and has sufficient webpages to create a pagerank POC

#=========running the full spider.py script=================
PS C:\...\Py4e> python .\spider.py
Enter web url or press "Enter": https://graphql.org/
['www.tigergraph.com', 'https://graphql.org']

# sval = input('How many pages:')
How many pages:100


# print(fromid, url, end=' ')
#on the same line
# print('(' + str(len(html)) + ')', end=' ')
#on the same line
# print(count)
2 https://graphql.org (117490) 34
10 https://graphql.org/learn/best-practices (75428) 69
8 https://graphql.org/blog (82496) 120
42 https://graphql.org/blog/2020-04-02-announcing-the-first-graphql-foundation-annual-report (73287) 61
25 https://graphql.org/learn/authorization (78664) 62
3 https://graphql.org/learn (75018) 60
47 https://graphql.org/tags/in-the-news (72155) 73
60 https://graphql.org/tags/spec (69507) 65
53 https://graphql.org/blog/2018-11-06-linux-foundation-announces-intent-to-form-new-foundation-to-support-graphql (78566) 63
54 https://graphql.org/blog/2017-11-08-programmableweb-graphql-moving-to-neutral-open-source-foundation (70556) 61
30 https://graphql.org/blog/2021-04-30-graphql-foundation-monthly-newsletter-april-2021 (76706) 71
26 https://graphql.org/learn/global-object-identification (108342) 69
43 https://graphql.org/blog/2019-10-31-linux-foundation-training-announces-free-online-course-exploring-graphql (74183) 63
4 https://graphql.org/code (544743) 87
41 https://graphql.org/blog/2020-04-03-web-based-graphql-ides-for-the-win (79438) 68
50 https://graphql.org/blog/2018-11-07-the-register (69930) 60
11 https://graphql.org/community/users (83415) 63
48 https://graphql.org/blog/2018-11-07-datanami-will-graphql-become-a-standard-for-the-new-data-economy (70116) 60
39 https://graphql.org/blog/2020-06-30-gsoc-2020-participant-naman (73846) 60
17 https://graphql.org/learn/serving-over-http (78379) 67
19 https://graphql.org/learn/pagination (80081) 65
16 https://graphql.org/foundation/contact (70191) 54
28 https://graphql.org/blog/2021-06-30-graphql-foundation-monthly-newsletter-june-2021 (78463) 77
51 https://graphql.org/blog/2018-11-06-eweek-graphql-api-specification-moving-forward-with-independent-foundation (70508) 60
52 https://graphql.org/blog/2018-11-06-infoworld-graphql-gets-its-own-foundation (70218) 60
12 https://graphql.org/community/upcoming-events (78670) 59
67 https://graphql.org/packages/graphql-hooks-ssr Unable to retrieve or parse page
62 https://graphql.org/blog/rss.xml Ignore non text/html page
69 https://graphql.org/community/developers (79148) 71
34 https://graphql.org/tags/announcements (73852) 79
72 https://graphql.org/foundation/join (76850) 58
14 https://graphql.org/brand (72981) 27
71 https://graphql.org/foundation/annual-reports (67543) 44
73 https://graphql.org/foundation/members (64752) 28
20 https://graphql.org/learn/thinking-in-graphs (75469) 64
44 https://graphql.org/blog/2019-10-28-graphql-foundation-launches-interactive-landscape-welcomes-new-members (78066) 66
38 https://graphql.org/blog/2020-09-11-graphql-foundation-monthly-newsletter-august-2020 (78905) 69
75 https://graphql.org/files/LF_Membership-Preview.pdf Ignore non text/html page
40 https://graphql.org/blog/2020-06-13-graphql-joins-google-season-of-docs (73929) 64
61 https://graphql.org/blog/graphql-a-query-language (78282) 63
56 https://graphql.org/tags/blog (70804) 71
45 https://graphql.org/blog/2019-03-12-graphql-foundation-announces-collaboration-with-jdf (82774) 62
13 https://graphql.org/foundation/community-grant (73133) 53
36 https://graphql.org/blog/2020-10-15-graphql-foundation-monthly-newsletter-september-2020 (78389) 70
32 https://graphql.org/blog/2021-02-15-graphql-foundation-monthly-newsletter-february-2021 (79100) 72
23 https://graphql.org/learn/execution (89972) 67
15 https://graphql.org/codeofconduct (70503) 33
22 https://graphql.org/learn/validation (72226) 59
55 https://graphql.org/blog/production-ready (72254) 62
66 https://graphql.org/graphql-js/running-an-express-graphql-server (80550) 93
86 https://graphql.org/graphql-js/graphql (80124) 119
85 https://graphql.org/graphql-js/express-graphql (76130) 94
76 https://graphql.org/files/GraphQL_Foundation-Participation_Agreement-Preview.pdf Ignore non text/html page
31 https://graphql.org/blog/2021-03-31-graphql-foundation-monthly-newsletter-march-2021 (75969) 65
87 https://graphql.org/graphql-js/error (82758) 102
58 https://graphql.org/blog/mocking-with-graphql (108137) 65
64 https://graphql.org/graphql-js/authentication-and-express-middleware (81943) 92
24 https://graphql.org/learn/introspection (72936) 59
35 https://graphql.org/blog/2020-11-12-graphql-foundation-monthly-newsletter-october-2020 (78035) 69
46 https://graphql.org/blog/2018-11-12-channel-futures-graphql-api-query-language-growing (70644) 60
29 https://graphql.org/tags/newsletter (72048) 73
6 https://graphql.org/faq (98865) 115
7 https://graphql.org/foundation (70401) 48
84 https://graphql.org/graphql-js/constructing-types (96984) 92
49 https://graphql.org/blog/2018-11-07-sd-times-lf-announces-plans-to-form-graphql-foundation (70170) 60
88 https://graphql.org/graphql-js/execution (78225) 96
80 https://graphql.org/graphql-js/basic-types (83666) 93
89 https://graphql.org/graphql-js/language (98682) 116
59 https://graphql.org/blog/subscriptions-in-graphql-and-relay (81663) 64
93 https://graphql.org/error Unable to retrieve or parse page
21 https://graphql.org/learn/queries (87119) 77
91 https://graphql.org/graphql-js/validation (76357) 97
74 https://graphql.org/blog/rss.xml Ignore non text/html page
27 https://graphql.org/learn/caching (71487) 62
33 https://graphql.org/blog/2020-12-08-improving-latency-with-defer-and-stream-directives (90524) 64
9 https://graphql.org/users (64452) 25
65 https://graphql.org/graphql-js (79438) 95
82 https://graphql.org/graphql-js/object-types (100372) 94
37 https://graphql.org/blog/2020-09-21-gsod-carolyn-stransky (75027) 61
63 https://graphql.org/foundation/annual-reports/2019 (103246) 71
70 https://graphql.org/community/project-resources (75049) 61
78 https://graphql.org/graphql-js/type (160980) 149
68 https://graphql.org/packages/graphql-hooks-memcache Unable to retrieve or parse page
83 https://graphql.org/graphql-js/mutations-and-input-types (110003) 93
81 https://graphql.org/graphql-js/passing-arguments (99458) 94
90 https://graphql.org/graphql-js/utilities (90226) 120
18 https://graphql.org/learn/schema (108875) 71
95 https://graphql.org/blog/rss.xml Ignore non text/html page
5 https://graphql.org/community (71398) 63
92 https://graphql.org/type Unable to retrieve or parse page
97 https://graphql.org/join Unable to retrieve or parse page
57 https://graphql.org/blog/rest-api-graphql-wrapper (181627) 73
98 https://graphql.org/blog/rss.xml Ignore non text/html page
79 https://graphql.org/graphql-js/graphql-clients (86676) 96
96 https://graphql.org/news/2019/03/12/the-graphql-foundation-announces-collaboration-with-the-joint-development-foundation-to-drive-open-source-and-open-standards Unable to retrieve or parse page
94 https://graphql.org/introspection Unable to retrieve or parse page
77 https://graphql.org/faq/graphql-foundation (69935) 35
No unretrieved HTML pages found
#======================================================



Webs table - 2 records
url
www.tigergraph.com
https://graphql.org


Links table - 2894 records
from_id	to_id
2	2
2	3
2	4
2	5
...
77	14
77	15




Pages table - 92 records
id	url	                                         html	                       error	old_rank	new_rank
1	https://graphql.org                          <html tags and content....>                         1.0
2	https://graphql.org/learn                    <html tags and content....>				         1.0                                       1.0
3   https://graphql.org/code                     <html tags and content....>                         1.0
4   https://graphql.org/community                <html tags and content....>                         1.0
5   https://graphql.org/foundation               <html tags and content....>                         1.0
6   https://graphql.org/learn/best-practices     <html tags and content....>                         1.0
'''
