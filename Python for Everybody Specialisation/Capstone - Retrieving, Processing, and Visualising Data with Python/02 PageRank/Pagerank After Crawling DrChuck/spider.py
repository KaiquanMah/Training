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
print(document)
<http.client.HTTPResponse object at 0x0000025ABC675FA0>





print(html)
b'<html>\r\n<head>\r\n  <title>Dr. Charles R. Severance Home Page</title>\r\n  <meta name="verify-v1" content="WQuA2ZPREiCyTlgNh/fv0jvzKJxrpzlagjiPaakSNH0=" />\r\n<style type="text/css">\r\nbody { background: black; font-family: Arial,Helvetica,Verdana,Sans-Serif; color: white;}\r\nbody table { font-size: 11pt; }\r\na:link, a:visited, a:active { color: gray; text-decoration: none; font-weight: bold}\r\na:hover { color:orange }\r\nstrong {color: orange; }\r\nem {color: yellow; font-style: normal;}\r\n\r\n#twitter_div {\r\ncolor: yellow;\r\ntext-align: center;\r\n}\r\n#twitter_div ul {\r\ndisplay: inline;\r\nfornt-size: 75%;\r\nmargin:0px 0px 0px 0px;\r\npadding:0px 0px 0px 0px;\r\nlist-style-type: none;\r\n}\r\n#twitter_div p {\r\nmargin:0px 0px 0px 0px;\r\ntext-align: center;\r\n}\r\n</style>\r\n<link rel="alternate" type="application/rss+xml" title="RSS" href="https://www.dr-chuck.com/csev-blog/index.rdf" />\r\n<link rel="alternate" type="application/atom+xml" title="Atom" href="https://www.dr-chuck.com/csev-blog/atom.xml" />\r\n<meta name="google-translate-customization" content="502d2c1a267d1206-8efe060c714e194c-g94a06c6c571083ae-11"></meta>\r\n</head>\r\n<body>\r\n<table border=0>\r\n<tr>\r\n<td align=center valign=top width=180>\r\n<a href="https://www.learnerprivacy.org/">\r\n<img align="center" src="Chuck_Square_B&W.jpg" width="160" style="border: white 2px solid;" alt="Photo Credit: Brent Severance">\r\n</a>\r\n<br>\r\n<br> <a href="https://www.si.umich.edu/" target="_blank">School of Information</a>\r\n<br/>\r\n<a href="https://www.ratemyprofessors.com/ShowRatings.jsp?tid=1159280" target="_blank">\r\n<img src="/images/rate-my-professor.jpg" width="140" alt="Rate This Professor"></a>\r\n<br> &nbsp\r\n<br> <a href=https://www.learnerprivacy.org>Podcast</a>\r\n<br> <a href=https://www.dr-chuck.com/csev-blog/>Blog</a>\r\n<br> <a href=https://www.twitter.com/drchuck/ target=_blank>@drchuck Twitter</a>\r\n<br> <a href="https://www.dr-chuck.com/dr-chuck/resume/speaking.htm" target=_blank>Keynote Speaker</a>\r\n<br/> <a href="https://www.slideshare.net/csev" target="_blank">Slideshare</a>\r\n<br> <a href=/dr-chuck/resume/index.htm target=_blank>Resume and Bio</a>\r\n<br>\r\n<a target="_blank" href="https://amzn.to/1K5Q81K">Amazon Author Page</a>\r\n<br>\r\n<a target="_blank" href="https://www.coursera.org/instructor/drchuck">My Coursera Page</a>\r\n<br> <a href="http://afs.dr-chuck.com/papers/" target=_blank>Chuck\'s Papers</a>\r\n<br> <a href="https://itunes.apple.com/us/podcast/computing-conversations/id731495760" target="_blank">IEEE Audio Podcast</a>\r\n<br> <a href="https://www.youtube.com/playlist?list=PLHJB2bhmgB7dFuY7HmrXLj5BmHGKTD-3R" target="_blank">IEEE Video Interviews</a>\r\n<br> <a href="https://developers.imsglobal.org/" target="_blank">IMS LTI</a>\r\n<br> <a href="https://www.youtube.com/user/csev" target=_blank>YouTube Channel </a>\r\n<br> <a href="https://vimeo.com/drchuck/videos" target=_blank>Video on Vimeo</a>\r\n<br> <a href="https://backpack.openbadges.org/share/4f76699ddb399d162a00b89a452074b3/" target="_blank">My Open Badges</a>\r\n<br>\r\n&nbsp; \r\n<br/>\r\n<a href="https://www.linkedin.com/in/charlesseverance/" target="_blank">\r\n<img src="https://www.linkedin.com/img/webpromo/btn_viewmy_120x33.png" \r\n    width="120" height="33" border="0" alt="View Chuck Severance\'s profile on LinkedIn">\r\n</a>\r\n<br/>\r\n<a title="Charles R. Severance" href="https://www.researchgate.net/profile/Charles_Severance/" target="_blank"><img src="https://www.researchgate.net/images/public/profile_share_badge.png" alt="Charles R. Severance" /></a>\r\n</td>\r\n<td valign=top>\r\n<div style="float: right">\r\n<script data-gittip-username="drchuck"\r\n        data-gittip-widget="button"\r\n        src="//gttp.co/v1.js"></script>\r\n</div>\r\n<strong>\r\nNew:\r\n</strong>\r\n<a href="https://www.learnerprivacy.org/" target="_blank">My LearnerPrivacy.org podcast</a> <br/>\r\n<!--\r\n<strong>\r\nNew:\r\n</strong>\r\n<a href="/office" target="_blank">MOOC Office Hours Around the World</a> <br/>\r\n-->\r\n<p>\r\nFree Courses / Educational Material:\r\n<br> &nbsp;\r\n<a href="https://www.py4e.com/" target="_blank">Python for Everybody</a>\r\n<br> &nbsp;\r\n<a href="https://www.dj4e.com/" target="_blank">Django for Everybody</a>\r\n<br> &nbsp;\r\n<a href="https://www.wa4e.com/" target="_blank">Web Applications for Everybody</a> (PHP/SQL)\r\n<br> &nbsp;\r\n<a href="https://www.coursera.org/course/insidetheinternet" target="_blank">Internet History, Technnology and Security</a>\r\n</p>\r\n<p>\r\nSoftware\r\n<br> &nbsp;\r\n<a href="https://www.sakaiproject.org/" target="_blank">The Sakai Collaboration\r\nand Learning Environment</a>\r\n<br> &nbsp;\r\n<a href="https://www.tsugi.org/" target="_blank">Tsugi: A framework for learning tools</a>\r\n<br> &nbsp;\r\n<a href="https://developers.imsglobal.org/" target="_blank">IMS Learning Tools\r\nInteroperability</a>\r\n</p>\r\n<p>\r\nBooks\r\n<br> &nbsp; <a href="http://www.py4e.com/book" /target="_blank">Python For Everybody: Exploring Data in Python 3</a>  (2016)\r\n<br> &nbsp; <a href="/sakai-book">Sakai: Building an Open Source Community</a> (2011, 2014)\r\n<br> &nbsp; <a href="http://www.amazon.com/gp/product/1624311393/ref=as_li_ss_tl?ie=UTF8&camp=1789&creative=390957&creativeASIN=1624311393&linkCode=as2&tag=drchu02-20" target="_blank">Raspberry Pi (21st Century Skills Innovation Library)</a> (2013)\r\n<br> &nbsp; <a href="http://www.amazon.com/gp/product/059680069X/ref=as_li_ss_tl?ie=UTF8&camp=1789&creative=390957&creativeASIN=059680069X&linkCode=as2&tag=drchu02-20" target="_blank">Using Google App Engine</a> (O\'Reilly 2009)\r\n<br> &nbsp; <a href="http://www.amazon.com/Performance-Computing-Architectures-Optimization-Benchmarks/dp/156592312X/" target="_blank">High Performance Computing</a> (<a href="http://oreilly.com/catalog/9781565923126/" target="_blank">O\'Reilly 1998</a>,  <a href="http://cnx.org/content/col11136/latest/" target=_blank>Connexions 2010</a>)\r\n</p>\r\n<p>\r\nWeb/Multimedia sites\r\n<br> &nbsp;\r\n<a href="http://www.youtube.com/playlist?list=PLHJB2bhmgB7dFuY7HmrXLj5BmHGKTD-3R" target="_blank">\r\nIEEE Computer - Computing Conversations Interviews</a>\r\n(2011-2016)\r\n<br> &nbsp;\r\n<a href=https://www.vimeo.com/17207620 target="_blank">\r\nDr. Chuck sings the blues </a> (2008)\r\n<br> &nbsp;\r\n<a href="https://www.youtube.com/watch?v=BVKpW02hsrU" target="_blank">\r\nDr. Chuck goes motocross racing</a> (2007)\r\n<br> &nbsp;\r\n<a href="https://www.youtube.com/watch?v=sa2WsgCvn7c" target="_blank">\r\nA Film About Brent and His ATV\r\n</a> (2005)\r\n<br> &nbsp;\r\n<a href="https://www.vimeo.com/17213019" target="_blank">\r\nAudition Tape</a> (2003) for TechTV which was\r\nrejected :(.\r\n<br> &nbsp;\r\n<a href="https://www.youtube.com/watch?v=FJ078sO35M0" target="_blank">\r\nDr. Chuck goes stock car racing</a> (2002)\r\n<br> &nbsp;\r\n<a href="http://afs.dr-chuck.com/citoolkit" target=_blank>\r\nThe Community Information Toolkit</a> - A project to provide public libraries and \r\nother organizations a start on using Internet in Commmunity Networking. (1999)\r\n</td>\r\n<td valign=top align=center width=180>\r\n<div id="google_translate_element"></div><script type="text/javascript">\r\nfunction googleTranslateElementInit() {\r\n  new google.translate.TranslateElement({pageLanguage: \'en\', layout: google.translate.TranslateElement.InlineLayout.SIMPLE, gaTrack: true, gaId: \'UA-423997-1\'}, \'google_translate_element\');\r\n}\r\n</script><script type="text/javascript" src="//translate.google.com/translate_a/element.js?cb=googleTranslateElementInit"></script>\r\n<br/>&nbsp;<br/>\r\n<a class="twitter-timeline" href="https://twitter.com/drchuck" data-widget-id="282172185219567616">Tweets by @drchuck</a>\r\n<script>!function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0],p=/^http:/.test(d.location)?\'http\':\'https\';if(!d.getElementById(id)){js=d.createElement(s);js.id=id;js.src=p+"://platform.twitter.com/widgets.js";fjs.parentNode.insertBefore(js,fjs);}}(document,"script","twitter-wjs");</script>\r\n</td>\r\n</tr>\r\n</table>\r\n<br> &nbsp;\r\n<script type="text/javascript">\r\n\r\n  var _gaq = _gaq || [];\r\n  _gaq.push([\'_setAccount\', \'UA-423997-1\']);\r\n  _gaq.push([\'_setDomainName\', \'dr-chuck.com\']);\r\n  _gaq.push([\'_trackPageview\']);\r\n\r\n  (function() {\r\n    var ga = document.createElement(\'script\'); ga.type = \'text/javascript\'; ga.async = true;\r\n    ga.src = (\'https:\' == document.location.protocol ? \'https://ssl\' : \'http://www\') + \'.google-analytics.com/ga.js\';\r\n    var s = document.getElementsByTagName(\'script\')[0]; s.parentNode.insertBefore(ga, s);\r\n  })();\r\n\r\n</script>\r\n</body>\r\n</html>\r\n'






print(soup)
<head>
<title>Dr. Charles R. Severance Home Page</title>
<meta content="WQuA2ZPREiCyTlgNh/fv0jvzKJxrpzlagjiPaakSNH0=" name="verify-v1"/>
<style type="text/css">
body { background: black; font-family: Arial,Helvetica,Verdana,Sans-Serif; color: white;}
body table { font-size: 11pt; }
a:link, a:visited, a:active { color: gray; text-decoration: none; font-weight: bold}
a:hover { color:orange }
strong {color: orange; }
em {color: yellow; font-style: normal;}

#twitter_div {
color: yellow;
text-align: center;
}
#twitter_div ul {
display: inline;
fornt-size: 75%;
margin:0px 0px 0px 0px;
padding:0px 0px 0px 0px;
list-style-type: none;
}
#twitter_div p {
margin:0px 0px 0px 0px;
text-align: center;
}
</style>
<link href="https://www.dr-chuck.com/csev-blog/index.rdf" rel="alternate" title="RSS" type="application/rss+xml"/>
<link href="https://www.dr-chuck.com/csev-blog/atom.xml" rel="alternate" title="Atom" type="application/atom+xml"/>
<meta content="502d2c1a267d1206-8efe060c714e194c-g94a06c6c571083ae-11" name="google-translate-customization"/>
</head>
<body>
<table border="0">
<tr>
<td align="center" valign="top" width="180">
<a href="https://www.learnerprivacy.org/">
<img align="center" alt="Photo Credit: Brent Severance" src="Chuck_Square_B&amp;W.jpg" style="border: white 2px solid;" width="160"/>
</a>
<br/>
<br/> <a href="https://www.si.umich.edu/" target="_blank">School of Information</a>
<br>
<a href="https://www.ratemyprofessors.com/ShowRatings.jsp?tid=1159280" target="_blank">
<img alt="Rate This Professor" src="/images/rate-my-professor.jpg" width="140"/></a>
<br/>  
<br/> <a href="https://www.learnerprivacy.org">Podcast</a>
<br/> <a href="https://www.dr-chuck.com/csev-blog/">Blog</a>
<br/> <a href="https://www.twitter.com/drchuck/" target="_blank">@drchuck Twitter</a>
<br/> <a href="https://www.dr-chuck.com/dr-chuck/resume/speaking.htm" target="_blank">Keynote Speaker</a>
<br> <a href="https://www.slideshare.net/csev" target="_blank">Slideshare</a>
<br/> <a href="/dr-chuck/resume/index.htm" target="_blank">Resume and Bio</a>
<br/>
<a href="https://amzn.to/1K5Q81K" target="_blank">Amazon Author Page</a>
<br/>
<a href="https://www.coursera.org/instructor/drchuck" target="_blank">My Coursera Page</a>
<br/> <a href="http://afs.dr-chuck.com/papers/" target="_blank">Chuck's Papers</a>
<br/> <a href="https://itunes.apple.com/us/podcast/computing-conversations/id731495760" target="_blank">IEEE Audio Podcast</a>
<br/> <a href="https://www.youtube.com/playlist?list=PLHJB2bhmgB7dFuY7HmrXLj5BmHGKTD-3R" target="_blank">IEEE Video Interviews</a>
<br/> <a href="https://developers.imsglobal.org/" target="_blank">IMS LTI</a>
<br/> <a href="https://www.youtube.com/user/csev" target="_blank">YouTube Channel </a>
<br/> <a href="https://vimeo.com/drchuck/videos" target="_blank">Video on Vimeo</a>
<br/> <a href="https://backpack.openbadges.org/share/4f76699ddb399d162a00b89a452074b3/" target="_blank">My Open Badges</a>
<br/>
 
<br>
<a href="https://www.linkedin.com/in/charlesseverance/" target="_blank">
<img alt="View Chuck Severance's profile on LinkedIn" border="0" height="33" src="https://www.linkedin.com/img/webpromo/btn_viewmy_120x33.png" width="120"/>
</a>
<br>
<a href="https://www.researchgate.net/profile/Charles_Severance/" target="_blank" title="Charles R. Severance"><img alt="Charles R. Severance" src="https://www.researchgate.net/images/public/profile_share_badge.png"/></a>
</br></br></br></br></td>
<td valign="top">
<div style="float: right">
<script data-gittip-username="drchuck" data-gittip-widget="button" src="//gttp.co/v1.js"></script>
</div>
<strong>
New:
</strong>
<a href="https://www.learnerprivacy.org/" target="_blank">My LearnerPrivacy.org podcast</a> <br>
<!--
<strong>
New:
</strong>
<a href="/office" target="_blank">MOOC Office Hours Around the World</a> <br/>
-->
<p>
Free Courses / Educational Material:
<br/>  
<a href="https://www.py4e.com/" target="_blank">Python for Everybody</a>
<br/>  
<a href="https://www.dj4e.com/" target="_blank">Django for Everybody</a>
<br/>  
<a href="https://www.wa4e.com/" target="_blank">Web Applications for Everybody</a> (PHP/SQL)
<br/>  
<a href="https://www.coursera.org/course/insidetheinternet" target="_blank">Internet History, Technnology and Security</a>
</p>
<p>
Software
<br/>  
<a href="https://www.sakaiproject.org/" target="_blank">The Sakai Collaboration
and Learning Environment</a>
<br/>  
<a href="https://www.tsugi.org/" target="_blank">Tsugi: A framework for learning tools</a>
<br/>  
<a href="https://developers.imsglobal.org/" target="_blank">IMS Learning Tools
Interoperability</a>
</p>
<p>
Books
<br/>   <a href="http://www.py4e.com/book" target="_blank">Python For Everybody: Exploring Data in Python 3</a>  (2016)
<br/>   <a href="/sakai-book">Sakai: Building an Open Source Community</a> (2011, 2014)
<br/>   <a href="http://www.amazon.com/gp/product/1624311393/ref=as_li_ss_tl?ie=UTF8&amp;camp=1789&amp;creative=390957&amp;creativeASIN=1624311393&amp;linkCode=as2&amp;tag=drchu02-20" target="_blank">Raspberry Pi (21st Century Skills Innovation Library)</a> (2013)
<br/>   <a href="http://www.amazon.com/gp/product/059680069X/ref=as_li_ss_tl?ie=UTF8&amp;camp=1789&amp;creative=390957&amp;creativeASIN=059680069X&amp;linkCode=as2&amp;tag=drchu02-20" target="_blank">Using Google App Engine</a> (O'Reilly 2009)
<br/>   <a href="http://www.amazon.com/Performance-Computing-Architectures-Optimization-Benchmarks/dp/156592312X/" target="_blank">High Performance Computing</a> (<a href="http://oreilly.com/catalog/9781565923126/" target="_blank">O'Reilly 1998</a>,  <a href="http://cnx.org/content/col11136/latest/" target="_blank">Connexions 2010</a>)
</p>
<p>
Web/Multimedia sites
<br/>  
<a href="http://www.youtube.com/playlist?list=PLHJB2bhmgB7dFuY7HmrXLj5BmHGKTD-3R" target="_blank">
IEEE Computer - Computing Conversations Interviews</a>
(2011-2016)
<br/>  
<a href="https://www.vimeo.com/17207620" target="_blank">
Dr. Chuck sings the blues </a> (2008)
<br/>  
<a href="https://www.youtube.com/watch?v=BVKpW02hsrU" target="_blank">
Dr. Chuck goes motocross racing</a> (2007)
<br/>  
<a href="https://www.youtube.com/watch?v=sa2WsgCvn7c" target="_blank">
A Film About Brent and His ATV
</a> (2005)
<br/>  
<a href="https://www.vimeo.com/17213019" target="_blank">
Audition Tape</a> (2003) for TechTV which was
rejected :(.
<br/>  
<a href="https://www.youtube.com/watch?v=FJ078sO35M0" target="_blank">
Dr. Chuck goes stock car racing</a> (2002)
<br/>  
<a href="http://afs.dr-chuck.com/citoolkit" target="_blank">
The Community Information Toolkit</a> - A project to provide public libraries and
other organizations a start on using Internet in Commmunity Networking. (1999)
</p></br></td>
<td align="center" valign="top" width="180">
<div id="google_translate_element"></div><script type="text/javascript">
function googleTranslateElementInit() {
  new google.translate.TranslateElement({pageLanguage: 'en', layout: google.translate.TranslateElement.InlineLayout.SIMPLE, gaTrack: true, gaId: 'UA-423997-1'}, 'google_translate_element');
}
</script><script src="//translate.google.com/translate_a/element.js?cb=googleTranslateElementInit" type="text/javascript"></script>
<br> <br>
<a class="twitter-timeline" data-widget-id="282172185219567616" href="https://twitter.com/drchuck">Tweets by @drchuck</a>
<script>!function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0],p=/^http:/.test(d.location)?'http':'https';if(!d.getElementById(id)){js=d.createElement(s);js.id=id;js.src=p+"://platform.twitter.com/widgets.js";fjs.parentNode.insertBefore(js,fjs);}}(document,"script","twitter-wjs");</script>
</br></br></td>
</tr>
</table>
<br/>  
<script type="text/javascript">

  var _gaq = _gaq || [];
  _gaq.push(['_setAccount', 'UA-423997-1']);
  _gaq.push(['_setDomainName', 'dr-chuck.com']);
  _gaq.push(['_trackPageview']);

  (function() {
    var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
    ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
  })();

</script>
</body>
</html>










print(up)
ParseResult(scheme='https', netloc='www.learnerprivacy.org', path='/', params='', query='', fragment='')
ParseResult(scheme='https', netloc='www.si.umich.edu', path='/', params='', query='', fragment='')
ParseResult(scheme='https', netloc='www.ratemyprofessors.com', path='/ShowRatings.jsp', params='', query='tid=1159280', fragment='')
ParseResult(scheme='https', netloc='www.learnerprivacy.org', path='', params='', query='', fragment='')
ParseResult(scheme='https', netloc='www.dr-chuck.com', path='/csev-blog/', params='', query='', fragment='')
ParseResult(scheme='https', netloc='www.twitter.com', path='/drchuck/', params='', query='', fragment='')
ParseResult(scheme='https', netloc='www.dr-chuck.com', path='/dr-chuck/resume/speaking.htm', params='', query='', fragment='')
ParseResult(scheme='https', netloc='www.slideshare.net', path='/csev', params='', query='', fragment='')
ParseResult(scheme='', netloc='', path='/dr-chuck/resume/index.htm', params='', query='', fragment='')
ParseResult(scheme='https', netloc='amzn.to', path='/1K5Q81K', params='', query='', fragment='')
ParseResult(scheme='https', netloc='www.coursera.org', path='/instructor/drchuck', params='', query='', fragment='')
ParseResult(scheme='http', netloc='afs.dr-chuck.com', path='/papers/', params='', query='', fragment='')
ParseResult(scheme='https', netloc='itunes.apple.com', path='/us/podcast/computing-conversations/id731495760', params='', query='', fragment='')
ParseResult(scheme='https', netloc='www.youtube.com', path='/playlist', params='', query='list=PLHJB2bhmgB7dFuY7HmrXLj5BmHGKTD-3R', fragment='')
ParseResult(scheme='https', netloc='developers.imsglobal.org', path='/', params='', query='', fragment='')
ParseResult(scheme='https', netloc='www.youtube.com', path='/user/csev', params='', query='', fragment='')
ParseResult(scheme='https', netloc='vimeo.com', path='/drchuck/videos', params='', query='', fragment='')
ParseResult(scheme='https', netloc='backpack.openbadges.org', path='/share/4f76699ddb399d162a00b89a452074b3/', params='', query='', fragment='')
ParseResult(scheme='https', netloc='www.linkedin.com', path='/in/charlesseverance/', params='', query='', fragment='')
ParseResult(scheme='https', netloc='www.researchgate.net', path='/profile/Charles_Severance/', params='', query='', fragment='')
ParseResult(scheme='https', netloc='www.learnerprivacy.org', path='/', params='', query='', fragment='')
ParseResult(scheme='https', netloc='www.py4e.com', path='/', params='', query='', fragment='')
ParseResult(scheme='https', netloc='www.dj4e.com', path='/', params='', query='', fragment='')
ParseResult(scheme='https', netloc='www.wa4e.com', path='/', params='', query='', fragment='')
ParseResult(scheme='https', netloc='www.coursera.org', path='/course/insidetheinternet', params='', query='', fragment='')
ParseResult(scheme='https', netloc='www.sakaiproject.org', path='/', params='', query='', fragment='')
ParseResult(scheme='https', netloc='www.tsugi.org', path='/', params='', query='', fragment='')
ParseResult(scheme='https', netloc='developers.imsglobal.org', path='/', params='', query='', fragment='')
ParseResult(scheme='http', netloc='www.py4e.com', path='/book', params='', query='', fragment='')
ParseResult(scheme='', netloc='', path='/sakai-book', params='', query='', fragment='')
ParseResult(scheme='http', netloc='www.amazon.com', path='/gp/product/1624311393/ref=as_li_ss_tl', params='', query='ie=UTF8&camp=1789&creative=390957&creativeASIN=1624311393&linkCode=as2&tag=drchu02-20', fragment='')
ParseResult(scheme='http', netloc='www.amazon.com', path='/gp/product/059680069X/ref=as_li_ss_tl', params='', query='ie=UTF8&camp=1789&creative=390957&creativeASIN=059680069X&linkCode=as2&tag=drchu02-20', fragment='')
ParseResult(scheme='http', netloc='www.amazon.com', path='/Performance-Computing-Architectures-Optimization-Benchmarks/dp/156592312X/', params='', query='', fragment='')
ParseResult(scheme='http', netloc='oreilly.com', path='/catalog/9781565923126/', params='', query='', fragment='')
ParseResult(scheme='http', netloc='cnx.org', path='/content/col11136/latest/', params='', query='', fragment='')
ParseResult(scheme='http', netloc='www.youtube.com', path='/playlist', params='', query='list=PLHJB2bhmgB7dFuY7HmrXLj5BmHGKTD-3R', fragment='')
ParseResult(scheme='https', netloc='www.vimeo.com', path='/17207620', params='', query='', fragment='')
ParseResult(scheme='https', netloc='www.youtube.com', path='/watch', params='', query='v=BVKpW02hsrU', fragment='')
ParseResult(scheme='https', netloc='www.youtube.com', path='/watch', params='', query='v=sa2WsgCvn7c', fragment='')
ParseResult(scheme='https', netloc='www.vimeo.com', path='/17213019', params='', query='', fragment='')
ParseResult(scheme='https', netloc='www.youtube.com', path='/watch', params='', query='v=FJ078sO35M0', fragment='')
ParseResult(scheme='http', netloc='afs.dr-chuck.com', path='/citoolkit', params='', query='', fragment='')
ParseResult(scheme='https', netloc='twitter.com', path='/drchuck', params='', query='', fragment='')






print(href)
http://dr-chuck.com (8386) https://www.learnerprivacy.org/
https://www.si.umich.edu/
https://www.ratemyprofessors.com/ShowRatings.jsp?tid=1159280
https://www.learnerprivacy.org
https://www.dr-chuck.com/csev-blog/
https://www.twitter.com/drchuck/
https://www.dr-chuck.com/dr-chuck/resume/speaking.htm
https://www.slideshare.net/csev
http://dr-chuck.com/dr-chuck/resume/index.htm
https://amzn.to/1K5Q81K
https://www.coursera.org/instructor/drchuck
http://afs.dr-chuck.com/papers/
https://itunes.apple.com/us/podcast/computing-conversations/id731495760
https://www.youtube.com/playlist?list=PLHJB2bhmgB7dFuY7HmrXLj5BmHGKTD-3R
https://developers.imsglobal.org/
https://www.youtube.com/user/csev
https://vimeo.com/drchuck/videos
https://backpack.openbadges.org/share/4f76699ddb399d162a00b89a452074b3/
https://www.linkedin.com/in/charlesseverance/
https://www.researchgate.net/profile/Charles_Severance/
https://www.learnerprivacy.org/
https://www.py4e.com/
https://www.dj4e.com/
https://www.wa4e.com/
https://www.coursera.org/course/insidetheinternet
https://www.sakaiproject.org/
https://www.tsugi.org/
https://developers.imsglobal.org/
http://www.py4e.com/book
http://dr-chuck.com/sakai-book
http://www.amazon.com/gp/product/1624311393/ref=as_li_ss_tl?ie=UTF8&camp=1789&creative=390957&creativeASIN=1624311393&linkCode=as2&tag=drchu02-20
http://www.amazon.com/gp/product/059680069X/ref=as_li_ss_tl?ie=UTF8&camp=1789&creative=390957&creativeASIN=059680069X&linkCode=as2&tag=drchu02-20
http://www.amazon.com/Performance-Computing-Architectures-Optimization-Benchmarks/dp/156592312X/
http://oreilly.com/catalog/9781565923126/
http://cnx.org/content/col11136/latest/
http://www.youtube.com/playlist?list=PLHJB2bhmgB7dFuY7HmrXLj5BmHGKTD-3R
https://www.vimeo.com/17207620
https://www.youtube.com/watch?v=BVKpW02hsrU
https://www.youtube.com/watch?v=sa2WsgCvn7c
https://www.vimeo.com/17213019
https://www.youtube.com/watch?v=FJ078sO35M0
http://afs.dr-chuck.com/citoolkit
https://twitter.com/drchuck






#to simulate 'no HTTP/S scheme' found in
#if ( len(up.scheme) < 1 ) :
print(urljoin(url, href[8:]))
http://dr-chuck.com/www.learnerprivacy.org/
http://dr-chuck.com/www.si.umich.edu/
http://dr-chuck.com/www.ratemyprofessors.com/ShowRatings.jsp?tid=1159280
http://dr-chuck.com/www.learnerprivacy.org
http://dr-chuck.com/www.dr-chuck.com/csev-blog/
http://dr-chuck.com/www.twitter.com/drchuck/
'''




'''
E2E flow after iteration 1

Webs table
url
http://dr-chuck.com


Links table
from_id	to_id
1	2
1	3
1	4
1	5
1	6
1	7
1	8
1	9
1	10
1	11
1	12
1	13
1	14
1	15
1	16
1	17
1	18
1	19
1	20
1	21
1	22
1	23
1	24
1	25
1	26
1	27
1	28
1	29
1	30
1	31
1	32
1	33
1	34
1	35
1	36
1	37
1	38
1	39
1	40


Pages table
id	url	                     html	                       error	old_rank	new_rank
1	http://dr-chuck.com       <html tags and content....>                         1.0
2	https://www.learnerprivacy.org				1.0
3	https://www.si.umich.edu				1.0
4	https://www.ratemyprofessors.com/ShowRatings.jsp?tid=1159280				1.0
5	https://www.dr-chuck.com/csev-blog				1.0
6	https://www.twitter.com/drchuck				1.0
7	https://www.dr-chuck.com/dr-chuck/resume/speaking.htm				1.0
8	https://www.slideshare.net/csev				1.0
9	http://dr-chuck.com/dr-chuck/resume/index.htm				1.0
10	https://amzn.to/1K5Q81K				1.0
11	https://www.coursera.org/instructor/drchuck				1.0
12	http://afs.dr-chuck.com/papers				1.0
13	https://itunes.apple.com/us/podcast/computing-conversations/id731495760				1.0
14	https://www.youtube.com/playlist?list=PLHJB2bhmgB7dFuY7HmrXLj5BmHGKTD-3R				1.0
15	https://developers.imsglobal.org				1.0
16	https://www.youtube.com/user/csev				1.0
17	https://vimeo.com/drchuck/videos				1.0
18	https://backpack.openbadges.org/share/4f76699ddb399d162a00b89a452074b3				1.0
19	https://www.linkedin.com/in/charlesseverance				1.0
20	https://www.researchgate.net/profile/Charles_Severance				1.0
21	https://www.py4e.com				1.0
22	https://www.dj4e.com				1.0
23	https://www.wa4e.com				1.0
24	https://www.coursera.org/course/insidetheinternet				1.0
25	https://www.sakaiproject.org				1.0
26	https://www.tsugi.org				1.0
27	http://www.py4e.com/book				1.0
28	http://dr-chuck.com/sakai-book				1.0
29	http://www.amazon.com/gp/product/1624311393/ref=as_li_ss_tl?ie=UTF8&camp=1789&creative=390957&creativeASIN=1624311393&linkCode=as2&tag=drchu02-20				1.0
30	http://www.amazon.com/gp/product/059680069X/ref=as_li_ss_tl?ie=UTF8&camp=1789&creative=390957&creativeASIN=059680069X&linkCode=as2&tag=drchu02-20				1.0
31	http://www.amazon.com/Performance-Computing-Architectures-Optimization-Benchmarks/dp/156592312X				1.0
32	http://oreilly.com/catalog/9781565923126				1.0
33	http://cnx.org/content/col11136/latest				1.0
34	http://www.youtube.com/playlist?list=PLHJB2bhmgB7dFuY7HmrXLj5BmHGKTD-3R				1.0
35	https://www.vimeo.com/17207620				1.0
36	https://www.youtube.com/watch?v=BVKpW02hsrU				1.0
37	https://www.youtube.com/watch?v=sa2WsgCvn7c				1.0
38	https://www.vimeo.com/17213019				1.0
39	https://www.youtube.com/watch?v=FJ078sO35M0				1.0
40	http://afs.dr-chuck.com/citoolkit				1.0
41	https://twitter.com/drchuck				1.0
















#=========running the full spider.py script=================
PS C:\...\Py4e> python .\spider.py
Restart existing crawl. You need to remove spider.sqlite if you wish to start a fresh web crawl
# print(webs)
['', 'http://dr-chuck.com']

# sval = input('How many pages:')
How many pages:100

# print(fromid, url, end=' ')
#on the same line
# print('(' + str(len(html)) + ')', end=' ')
#on the same line
# print(count)
25 https://www.sakaiproject.org (580331) 32
9 http://dr-chuck.com/dr-chuck/resume/index.htm (1889) 12
11 https://www.coursera.org/instructor/drchuck (543093) 184
186 https://www.coursera.org/articles/web-developer (741698) 141
241 https://www.instagram.com/coursera (202600) 0
174 https://www.coursera.org/collections/marketing-skills (540702) 148
162 https://www.coursera.org/courses?query=english%20speaking (709286) 191
19 https://www.linkedin.com/in/charlesseverance Unable to retrieve or parse page
140 https://www.coursera.org/professional-certificates/facebook-social-media-marketing (851135) 153
228 https://www.coursera.org/about/privacy (491371) 173
268 https://www.coursera.org/business/learn-more?utm_medium=coursera&utm_source=collection-pages&utm_campaign=marketing-skills-collection-page&utm_content=c2b-collection-page-contact (73449) 81
316 https://www.coursera.org/specializations/facebook-social-media-marketing (844517) 153
61 http://dr-chuck.com/dr-chuck/resume/teach2017-08.docx Ignore non text/html page
323 https://www.coursera.org/facebook (553568) 182
257 https://www.coursera.org/learn/marketing-digital (831239) 159
238 https://www.linkedin.com/company/coursera Unable to retrieve or parse page
242 https://www.coursera.org/articles/web-developer?authMode=login (735941) 137
382 https://www.coursera.org/business/product-teams/?utm_campaign=website&utm_content=product-teams-collection&utm_medium=coursera&utm_source=enterprise (91338) 84
102 https://www.coursera.org/learn/introcss (829958) 161
91 https://www.coursera.org/learn/python-network-data-ru (776999) 151
437 https://www.coursera.org/learn/conclusao-do-marketing-de-midias-sociais-do-facebook (729265) 151
406 http://twitter.com/coursera (86055) 6
254 https://www.coursera.org/business/marketing-teams?utm_medium=coursera&utm_source=collection-pages&utm_campaign=marketing-skills-collection-page&utm_content=c2b-collection-page-cp (90995) 84
402 https://coursera.community (63872) 1
378 https://www.coursera.org/business/engineering-teams/?utm_campaign=website&utm_content=engineering-teams-collection&utm_medium=coursera&utm_source=enterprise (90201) 84
329 https://www.coursera.org/about/cookies (376956) 132
143 https://www.coursera.org/professional-certificates/salesforce-sales-operations (802820) 156
197 https://www.coursera.org/degrees/social-sciences (426554) 140
350 https://es.coursera.org/professional-certificates/soporte-de-tecnologias-de-informacion-google (815359) 151
47 https://www.sakailms.org/sakai-news (761461) 50
376 https://www.coursera.org/business/cloud-it-academy/?utm_campaign=website&utm_content=cloud-it-academy&utm_medium=coursera&utm_source=enterprise (86268) 85
557 https://es.coursera.org/professional-certificates/gcp-cloud-architect (813246) 151
623 https://www.sakailms.org/post/sakai-elevates-teaching-at-universidad-publica-de-navarro (831909) 29
388 https://www.coursera.org/business/webcast (101272) 146
16 https://www.youtube.com/user/csev (463241) 14
455 https://www.coursera.org/instructor/aricrindfleisch (471681) 148
572 https://es.coursera.org/courses?query=hr (730792) 204
98 https://www.coursera.org/learn/python-network-data-es (768130) 150
690 https://www.youtube.com/about/policies (112017) 143
513 https://www.coursera.org/learn/opportunity-management-in-salesforce?specialization=salesforce-sales-operations (814828) 160
467 https://www.coursera.org/learn/introcss?authMode=signup (824239) 159
195 https://www.coursera.org/degrees/data-analytics (447481) 147
709 https://es.coursera.org/courses?query=human%20resource%20management (727244) 189
164 https://www.coursera.org/courses?query=full%20stack%20web%20development (733986) 201
571 https://es.coursera.org/courses?query=cybersecurity (731193) 204
643 https://es.coursera.org/learn/gcp-infrastructure-core-services?specialization=gcp-cloud-architect (909630) 155
568 https://es.coursera.org/courses?query=cursos%20gratis (681741) 181
536 https://es.coursera.org/learn/asistencia-tecnica?specialization=soporte-de-tecnologias-de-informacion-google (878102) 158
973 https://es.coursera.org/learn/it-security (861746) 154
757 https://es.coursera.org/browse/business (1412195) 356
759 https://es.coursera.org/browse/data-science (1301071) 320
889 https://www.coursera.org/articles/gmat-vs-gre-which-exam-is-right-for-me (755486) 140
937 https://www.coursera.org/search?query=full stack web development en español Unable to retrieve or parse page
1078 https://es.coursera.org/degrees/imba (534931) 153
138 https://www.coursera.org/professional-certificates/ibm-data-engineer (946953) 165
1070 https://es.coursera.org/browse/business/leadership-and-management (1367616) 358
85 https://www.coursera.org/learn/intermediate-postgresql (795273) 159
1040 https://es.coursera.org/learn/negotiation (914950) 159
869 https://socialimpact.youtube.com (51463) 88
123 https://www.coursera.org/browse/information-technology (1273386) 326
722 https://es.coursera.org/learn/organizational-behavior (829560) 155
680 https://www.youtube.com (612435) 14
1013 https://es.coursera.org/lecture/gcp-infrastructure-core-services/module-overview-jPfvH (812610) 134
494 https://support.twitter.com/articles/20170514 (79968) 101
205 https://www.coursera.org/articles/how-long-does-a-masters-degree-take (763335) 155
453 https://www.coursera.org/specializations/digital-marketing (831583) 160
775 https://www.youtube.com/howyoutubeworks/our-mission (68617) 102
412 https://www.coursera.org/facebook?authMode=signup (555516) 183
1465 https://es.coursera.org/learn/gcp-infrastructure-core-services (908091) 154
696 http://business.illinois.edu/profile/aric-rindfleisch (55953) 132
232 https://www.coursera.org/articles (575898) 141
322 https://www.coursera.org/instructor/dan-kob (470647) 148
126 https://www.coursera.org/browse/personal-development (1165935) 272
1551 https://support.twitter.com/cs.html (79699) 86
1376 https://www.coursera.org/degrees/unt-online-bachelor-completion (592431) 151
867 https://www.youtube.com/creators-for-change (155108) 105
1716 https://www.coursera.org/courses?query=professional%20development (693576) 181
1580 https://www.coursera.org/learn/digital-analytics?specialization=digital-marketing (822530) 159
263 https://www.coursera.org/learn/user-experience-design (793709) 155
844 https://www.youtube.com/about/  /howyoutubeworks/policies/legal-removals Unable to retrieve or parse page
942 https://www.coursera.org/courses?query=full%20stack%20web%20development&page=6&index=prod_all_launched_products_term_optimization (1003351) 143
12 http://afs.dr-chuck.com/papers (1018) 13
363 https://coursera.org/business (102997) 102
728 https://es.coursera.org/professional-certificates/icpm-certified-supervisor (778218) 150
1362 https://support.google.com/youtube/answer/3545195?hl=en (854351) 114
1646 http://business.illinois.edu/course/BADM/537 (30356) 110
1065 https://es.coursera.org/lecture/it-security/intro-to-defense-in-depth-3FPzh (889794) 140
1159 https://es.coursera.org/learn/bridging-strategy-design-delivery-gap (908735) 159
489 https://www.coursera.org/lecture/conclusao-do-marketing-de-midias-sociais-do-facebook/introducao-semanal-DI2S3 (749109) 134
909 https://es.coursera.org/courses?query=human%20resource%20management&page=39&index=prod_all_launched_products_term_optimization (1890031) 175
1358 https://socialimpact.youtube.com/how-to (54746) 88
614 https://www.sakailms.org/post/where-is-sakai-going-from-2022-to-2024 (833971) 28
1864 https://www.coursera.org/learn/digital-analytics/reviews (624456) 139
1444 https://www.coursera.org/learn/usable-security (817836) 160
1170 https://es.coursera.org/browse/data-science/machine-learning (1247564) 314
1915 https://www.coursera.org/business/essential-skills-playbook/?utm_campaign=c4b&utm_content=essential-skills-playbook-hp&utm_medium=website&utm_source=enterprise (104653) 90
336 mailto:privacyshield@coursera.org Unable to retrieve or parse page
67 https://www.coursera.org (1035802) 244
1210 https://es.coursera.org/learn/ciencia-computacao-python-conceitos (861630) 158
1157 https://es.coursera.org/specializations/innovation-creativity-entrepreneurship (838688) 161
#======================================================

Webs table - 2 records
url

http://dr-chuck.com

Links table - 11,252 records
from_id	to_id
1	      2
1	      3

Pages table - 2,195 records
id	url	                                 html	                       error	old_rank	new_rank
1	http://dr-chuck.com                  <html tags and content....>                         1.0
2	https://www.learnerprivacy.org				                                             1.0
'''
