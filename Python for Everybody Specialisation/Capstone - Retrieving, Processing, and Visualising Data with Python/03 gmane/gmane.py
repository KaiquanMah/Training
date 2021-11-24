import sqlite3
import time
import ssl
import urllib.request, urllib.parse, urllib.error
from urllib.parse import urljoin, urlparse
import re
from datetime import datetime, timedelta


# =======#1 Define function to process datetime=======================
# Not all systems have this so conditionally define parser
try:
    #https://dateutil.readthedocs.io/en/stable/parser.html
    import dateutil.parser as parser
except:
    pass

def parsemaildate(md) :
    # See if we have dateutil
    try:
        # (datetime.datetime(2047, 1, 1, 8, 21))
        # Question: should the argument be 'md' instead of 'tdate'?
        pdate = parser.parse(tdate)
        #https://docs.python.org/3/library/datetime.html
        # from datetime import date
        # date(2002, 12, 4).isoformat()
        # '2002-12-04'
        # YYYY-MM-DD
        test_at = pdate.isoformat()
        return test_at
    except:
        pass



    # Non-dateutil version - we try our best
    pieces = md.split()
    notz = " ".join(pieces[:4]).strip()
    #string1 string2 string3 string4

    # Try a bunch of format variations - strptime() is *lame*
    dnotz = None
    #https://www.programiz.com/python-programming/datetime/strptime
    # %d 01; %b Jan %B January; %y 21 %Y 2021;
    for form in [ '%d %b %Y %H:%M:%S', '%d %b %Y %H:%M:%S',
        '%d %b %Y %H:%M', '%d %b %Y %H:%M', '%d %b %y %H:%M:%S',
        '%d %b %y %H:%M:%S', '%d %b %y %H:%M', '%d %b %y %H:%M' ] :
        try:
            #strptime 1st argument = string (that be converted to datetime)
            #2nd argument = datetime format to match with => need to be cautious it is possible to match 'day' and 'month' wrongly
            dnotz = datetime.strptime(notz, form)
            break
        except:
            continue

    #if no match in datetime format from above
    if dnotz is None :
        # print 'Bad Date:',md
        return None

    iso = dnotz.isoformat()

    #instantiate timezone as '+0000'
    tz = "+0000"
    try:
        # assign and process the timezone
        tz = pieces[4]
        ival = int(tz) # Only want numeric timezone values
        if tz == '-0000' : tz = '+0000'
        # e.g. hrs portion '+02'
        tzh = tz[:3]
        # e.g. minutes portion '30'
        tzm = tz[3:]
        #add a ':' colon in between
        tz = tzh + ":" + tzm
    except:
        pass

    #return the ISO format datetime + timezone
    return iso + tz





# =======#2 Handle SSL certificate errors=======================
# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


# =======#3 SQLite DB create table(s)=======================
conn = sqlite3.connect('content.sqlite')
cur = conn.cursor()

baseurl = "http://mbox.dr-chuck.net/sakai.devel/"

cur.execute('''CREATE TABLE IF NOT EXISTS Messages (id INTEGER UNIQUE
                                                   , email TEXT
                                                   , sent_at TEXT
                                                   , subject TEXT
                                                   , headers TEXT
                                                   , body TEXT)''')

# Pick up where we left off
start = None
cur.execute('SELECT max(id) FROM Messages')
try:
    row = cur.fetchone()
    if row is None :
        start = 0
    else:
        #use the retrieved max(id) where we left off
        start = row[0]
except:
    start = 0

if start is None : start = 0


many = 0
count = 0
fail = 0
while True:
    #get user input on how many messages to process
    if ( many < 1 ) :
        conn.commit()
        sval = input('How many messages:')
        if ( len(sval) < 1 ) : break
        #otherwise, assign user input 'sval' to 'many'
        many = int(sval)

    #start # is the record 'id' we want to process
    start = start + 1
    cur.execute('SELECT id FROM Messages WHERE id=?', (start,) )
    try:
        row = cur.fetchone()
        #if we retrieved this email before, dont process it
        if row is not None : continue
    except:
        row = None

    #decrement retrieved record by 1
    many = many - 1
    #construct 'url'
    # baseurl = "http://mbox.dr-chuck.net/sakai.devel/"
    # url = "http://mbox.dr-chuck.net/sakai.devel/1/2"; such that the last # is always '+1' of the 2nd last #
    url = baseurl + str(start) + '/' + str(start + 1)


    #connect to URL
    text = "None"
    try:
        # Open with a timeout of 30 seconds
        document = urllib.request.urlopen(url, None, 30, context=ctx)
        text = document.read().decode()
        # HTTP status code 200 is ok/no issues
        if document.getcode() != 200 :
            print("Error code=",document.getcode(), url)
            break
    except KeyboardInterrupt:
        print('')
        print('Program interrupted by user...')
        break
    except Exception as e:
        print("Unable to retrieve or parse page",url)
        print("Error",e)
        fail = fail + 1
        #============'1st 'fail' check===============
        #if fail too many times, terminate executing the code
        #since 'fail' variable is reset within each iteration of the 'while' loop,
        #and there are no 'for' or 'while' loops within the code segments below
        # 2pm: at first, it seems redundant to check for 'if fail > 5 : break' this early in the 'while loop'
        # 3pm: if the 'while' loop keeps encountering errors this early in the 'while loop' before the 'fail' variable gets reset, then this 'fail' check works to let you troubleshoot any errors in your code;
        # so actually on hindsight, the 'fail' check is not redundant
        if fail > 5 : break
        continue

    print(url,len(text))
    # count = count # documents retrived successfully
    count = count + 1

    #because there is no 'From' within the text, the document retrieved is not an email
    # so we do not want to parse this document
    if not text.startswith("From "):
        print(text)
        print("Did not find From ")
        fail = fail + 1
        #============'2nd 'fail' check===============
        if fail > 5 : break
        continue

    # so for emails
    #find the 'empty line' separating the <header></header> and <body></body> of the HTML document
    pos = text.find("\n\n")
    if pos > 0 :
        hdr = text[:pos]
        #'pos' is where the '\n\n' starts
        # pos+1 is where the 2nd '\n' is
        # pos+2 is where the body starts
        body = text[pos+2:]
    else:
        print(text)
        print("Could not find break between headers and body")
        fail = fail + 1
        #============'3rd 'fail' check===============
        if fail > 5 : break
        continue





    # retrieve 'email address' from <header>
    # instantiate 'email' for email address
    email = None
    # find 'From in the <header></header>'
    # \S non-whitespace
    # actual characters 'From :', '<', '>', '@'
    # regex '.*', '\n', '()', '\S+'
    x = re.findall('\nFrom: .* <(\S+@\S+)>\n', hdr)
    if len(x) == 1 :
        #https://docs.python.org/3/library/re.html
        # re.findall(r'\bf[a-z]*', 'which foot or hand fell fastest')
        # ['foot', 'fell', 'fastest']
        # so x = list of ['From: ...', ..., 'From: ...'] or ['From: ...']
        email = x[0];
        # 'From: ...'
        email = email.strip().lower()
        email = email.replace("<","")
    else:
        x = re.findall('\nFrom: (\S+@\S+)\n', hdr)
        if len(x) == 1 :
            email = x[0];
            email = email.strip().lower()
            email = email.replace("<","")


    # retrieve 'date' from <header>
    date = None
    y = re.findall('\Date: .*, (.*)\n', hdr)
    if len(y) == 1 :
        tdate = y[0]
        tdate = tdate[:26]
        try:
            #parse/format the date using the function defined earlier
            sent_at = parsemaildate(tdate)
        except:
            print(text)
            print("Parse fail",tdate)
            fail = fail + 1
            #============'4th 'fail' check===============
            # it seems that there should not be any 'fail' variable >= 5
            # unless, we never get that far to the 'fail' reset code segment below
            if fail > 5 : break
            continue


    # retrieve 'email subject/topic/title' from <header>
    subject = None
    z = re.findall('\Subject: (.*)\n', hdr)
    if len(z) == 1 : subject = z[0].strip().lower();


    # Reset the fail counter
    fail = 0
    print("   ",email,sent_at,subject)
    cur.execute('''INSERT OR IGNORE INTO Messages (id, email, sent_at, subject, headers, body)
        VALUES ( ?, ?, ?, ?, ?, ? )''', ( start, email, sent_at, subject, hdr, body))
    if count % 50 == 0 : conn.commit()
    if count % 100 == 0 : time.sleep(1)


conn.commit()
cur.close()




'''
# E2E run
How many messages:10
http://mbox.dr-chuck.net/sakai.devel/1/2 2662
    ggolden@umich.edu 2005-12-08T23:34:30-06:00 call for participation: developers documentation
http://mbox.dr-chuck.net/sakai.devel/2/3 2434
    csev@umich.edu 2005-12-09T00:58:01-05:00 report from the austin conference:  sakai developers break into song
http://mbox.dr-chuck.net/sakai.devel/3/4 3055
    kevin.carpenter@rsmart.com 2005-12-09T09:01:49-07:00 cas and sakai 1.5
http://mbox.dr-chuck.net/sakai.devel/4/5 11721
    michael.feldstein@suny.edu 2005-12-09T09:43:12-05:00 re: lms/vle rants/comments
http://mbox.dr-chuck.net/sakai.devel/5/6 9443
    john@caret.cam.ac.uk 2005-12-09T13:32:29+00:00 re: lms/vle rants/comments
http://mbox.dr-chuck.net/sakai.devel/6/7 3586
    s-githens@northwestern.edu 2005-12-09T13:32:31-06:00 re: sakaiportallogin and presense
http://mbox.dr-chuck.net/sakai.devel/7/8 10600
    john@caret.cam.ac.uk 2005-12-09T13:42:24+00:00 re: lms/vle rants/comments
http://mbox.dr-chuck.net/sakai.devel/8/9 4892
    s-githens@northwestern.edu 2005-12-09T15:23:09-06:00 re: sakaiportallogin and presense
http://mbox.dr-chuck.net/sakai.devel/9/10 3206
    ys2n@virginia.edu 2005-12-09T17:54:17+00:00 sakaiportallogin and presense
http://mbox.dr-chuck.net/sakai.devel/10/11 4993
    ys2n@virginia.edu 2005-12-09T21:16:39+00:00 re: sakaiportallogin and presense


How many messages:40
http://mbox.dr-chuck.net/sakai.devel/11/12 3298
    slt@columbia.edu 2005-12-09T23:16:40-05:00 re: cas and sakai 1.5
http://mbox.dr-chuck.net/sakai.devel/12/13 3096
    dgcotton@ucdavis.edu 2005-12-10T20:55:54-08:00 memory error with 2.1
http://mbox.dr-chuck.net/sakai.devel/13/14 4307
    vyu2@yahoo.com 2005-12-10T23:34:43-08:00 re: memory error with 2.1
http://mbox.dr-chuck.net/sakai.devel/14/15 4935
    winstonw.tw@gmail.com 2005-12-11T03:07:29+08:00 re: sakai ldap authentication
http://mbox.dr-chuck.net/sakai.devel/15/16 4374
    ajpoland@iupui.edu 2005-12-11T12:08:15-05:00 re: memory error with 2.1
http://mbox.dr-chuck.net/sakai.devel/16/17 2475
    caseyd1@stanford.edu 2005-12-12T07:02:36-08:00 re: sakai 2.1 provider examples
http://mbox.dr-chuck.net/sakai.devel/17/18 3931
    aaronz@vt.edu 2005-12-12T08:55:09-05:00 sakai 2.1 provider examples
http://mbox.dr-chuck.net/sakai.devel/18/19 3828
    j.higham@hull.ac.uk 2005-12-12T09:49:16+00:00 re: sakai 2.1 - lone zero block error
http://mbox.dr-chuck.net/sakai.devel/19/20 2839
    aaronz@vt.edu 2005-12-12T10:13:38-05:00 re: sakai 2.1 provider examples
http://mbox.dr-chuck.net/sakai.devel/20/21 8505
    jeffrey.beeman@asu.edu 2005-12-12T11:14:55-07:00 re: sakai logo
http://mbox.dr-chuck.net/sakai.devel/21/22 2625
    csev@umich.edu 2005-12-12T11:33:29-05:00 sepp library discussion group renamed - now with open membership
http://mbox.dr-chuck.net/sakai.devel/22/23 2960
    pgoldweic@northwestern.edu 2005-12-12T13:16:12-06:00 problems accessing the collab site with internet explorer...
http://mbox.dr-chuck.net/sakai.devel/23/24 4715
    pgoldweic@northwestern.edu 2005-12-12T14:20:41-06:00 re: problems accessing the collab site with internet
http://mbox.dr-chuck.net/sakai.devel/24/25 2705
    andrew@caret.cam.ac.uk 2005-12-12T14:23:12+00:00 file picker for non-legacy tools
http://mbox.dr-chuck.net/sakai.devel/25/26 4378
    john.ellis@rsmart.com 2005-12-12T14:24:48-07:00 re: file picker for non-legacy tools
http://mbox.dr-chuck.net/sakai.devel/26/27 3403
    aaronz@vt.edu 2005-12-12T14:42:01-05:00 sakai 2.01 vt provider code
http://mbox.dr-chuck.net/sakai.devel/27/28 3932
    aaronz@vt.edu 2005-12-12T14:54:49-05:00 re: problems accessing the collab site with internet explorer...
http://mbox.dr-chuck.net/sakai.devel/28/29 5170
    jxf@immagic.com 2005-12-12T16:41:04-05:00 re: worksite taxonomy
http://mbox.dr-chuck.net/sakai.devel/29/30 3845
    ray@media.berkeley.edu 2005-12-12T17:03:51-08:00 re: sakai 2.1 samigo
http://mbox.dr-chuck.net/sakai.devel/30/31 5262
    dave.ross@gmail.com 2005-12-12T17:49:13-05:00 re: memory error with 2.1
http://mbox.dr-chuck.net/sakai.devel/31/32 5043
    clayf@bu.edu 2005-12-12T18:31:23-05:00 re: memory error with 2.1
http://mbox.dr-chuck.net/sakai.devel/32/33 2910
    ggolden@umich.edu 2005-12-12T20:02:00-05:00 sakai 2.1 conversion - an update
http://mbox.dr-chuck.net/sakai.devel/33/34 3512
    ys2n@virginia.edu 2005-12-12T21:15:22+00:00 worksite taxonomy
http://mbox.dr-chuck.net/sakai.devel/34/35 5362
    lfernandez@weber.edu 2005-12-13T01:08:01-07:00 re: memory error with 2.1
http://mbox.dr-chuck.net/sakai.devel/35/36 2270
    lfernandez@weber.edu 2005-12-13T01:29:49-07:00 audio recordings of austin presentations
http://mbox.dr-chuck.net/sakai.devel/36/37 6958
    ys2n@virginia.edu 2005-12-13T02:46:51+00:00 re: worksite taxonomy
http://mbox.dr-chuck.net/sakai.devel/37/38 8425
    jleasia@umich.edu 2005-12-13T08:02:47-05:00 re: worksite taxonomy
http://mbox.dr-chuck.net/sakai.devel/38/39 3014
    csev@umich.edu 2005-12-13T08:12:08-05:00 re: audio recordings of austin presentations
http://mbox.dr-chuck.net/sakai.devel/39/40 9459
    gsilver@umich.edu 2005-12-13T08:58:10-05:00 re: worksite taxonomy
http://mbox.dr-chuck.net/sakai.devel/40/41 4796
    jrm@jhu.edu 2005-12-13T09:32:39-05:00 sakai 2.1 db error?
http://mbox.dr-chuck.net/sakai.devel/41/42 2692
    slt@columbia.edu 2005-12-13T10:15:28-05:00 re: sakai 2.1 conversion - an update
http://mbox.dr-chuck.net/sakai.devel/42/43 2640
    ray@media.berkeley.edu 2005-12-13T12:07:02-08:00 big news in jsf land
http://mbox.dr-chuck.net/sakai.devel/43/44 3016
    antranig@caret.cam.ac.uk 2005-12-13T14:06:13+00:00 "direct urls"
http://mbox.dr-chuck.net/sakai.devel/44/45 2988
    jmpease@syr.edu 2005-12-13T14:45:24-05:00 entity model
http://mbox.dr-chuck.net/sakai.devel/45/46 9703
    gwang3@unlnotes.unl.edu 2005-12-13T14:50:25-06:00 error to run sakai 2.1
http://mbox.dr-chuck.net/sakai.devel/46/47 9703
    gwang3@unlnotes.unl.edu 2005-12-13T14:50:25-06:00 error to run sakai 2.1
http://mbox.dr-chuck.net/sakai.devel/47/48 15775
    bkirschn@umich.edu 2005-12-13T14:55:24-05:00 utf-8 problem on sakai 2.1 with mysql
http://mbox.dr-chuck.net/sakai.devel/48/49 3230
    vrajgopalan@ucmerced.edu 2005-12-13T15:02:42-08:00 regarding the section manager and other section related api's
http://mbox.dr-chuck.net/sakai.devel/49/50 3214
    vrajgopalan@ucmerced.edu 2005-12-13T15:23:15-08:00 regarding the section manager and other section related api's
http://mbox.dr-chuck.net/sakai.devel/50/51 2848
    wchang@dri.edu 2005-12-13T15:23:26-08:00 password forgotten feature





id	email	            sent_at	                    subject	                                            headers	      body
1	ggolden@umich.edu	2005-12-08T23:34:30-06:00	call for participation: developers documentation	<header>     <body>
...

<Header example>
From news@gmane.org Tue Mar 04 03:33:20 2003
From: "Glenn R. Golden" <ggolden@umich.edu>
Subject: call for participation: developers documentation
Date: Thu, 8 Dec 2005 23:34:30 -0600
Lines: 28
Message-ID: <B7EAF76E-3366-4AE3-BDD6-6743707FEBA9@umich.edu>
Mime-Version: 1.0
Content-Type: text/plain; charset=US-ASCII; delsp=yes; format=flowed
Content-Transfer-Encoding: 7bit
X-From: postmaster@collab.sakaiproject.org Fri Dec 09 06:38:09 2005
Return-path: <postmaster@collab.sakaiproject.org>
Received: from bonecollector.mr.itd.umich.edu ([141.211.93.140])
	by ciao.gmane.org with esmtp (Exim 4.43)
	id 1EkawZ-0002jO-37
	for gccsd-sakai-dev@m.gmane.org; Fri, 09 Dec 2005 06:37:19 +0100
Received: FROM sharkfin.ds.itd.umich.edu (sharkfin.ds.itd.umich.edu [141.211.253.161])
	BY bonecollector.mr.itd.umich.edu ID 4399180C.A1939.12235 ;
	 9 Dec 2005 00:37:16 -0500
Received: from sharkfin.ds.itd.umich.edu ([127.0.0.1])
          by sharkfin.ds.itd.umich.edu (JAMES SMTP Server 2.1.3) with SMTP ID 423
          for <sakai-dev@collab.sakaiproject.org>;
          Fri, 9 Dec 2005 00:34:25 -0500 (EST)
Received: from relay1.mail.twtelecom.net (ns-map.ds.itd.umich.edu [141.211.253.192])
	by sharkfin.ds.itd.umich.edu (Postfix) with ESMTP id A4AB01C02F
	for <sakai-dev@collab.sakaiproject.org>; Fri,  9 Dec 2005 00:34:25 -0500 (EST)
Received: from [172.29.173.27] (unknown [66.194.95.2])
	by relay1.mail.twtelecom.net (Postfix) with ESMTP id AE54C5037
	for <sakai-dev@collab.sakaiproject.org>; Thu,  8 Dec 2005 23:29:25 -0600 (CST)
X-Content-Type-Outer-Envelope: text/plain; charset=US-ASCII; delsp=yes; format=flowed
To: sakai-dev <sakai-dev@collab.sakaiproject.org>
X-Mailer: Apple Mail (2.746.2)
X-Content-Type-Message-Body: text/plain; charset=US-ASCII; delsp=yes; format=flowed















print(parsed)
('<b7eaf76e-3366-4ae3-bdd6-6743707feba9@umich.edu>', 'ggolden@umich.edu', 'call for participation: developers documentation', '2005-12-08T23:34:30-06:00')
('<bb7ce631-ccf0-40a3-b076-683f9d03e0c9@umich.edu>', 'csev@umich.edu', 'report from the austin conference:  sakai developers break into song', '2005-12-09T00:58:01-05:00')
('<16703710.1134144397398.javamail.tomcat5@sharkfin.ds.itd.umich.edu>', 'kevin.carpenter@rsmart.com', 'cas and sakai 1.5', '2005-12-09T09:01:49-07:00')
('<9622225.1134139564303.javamail.tomcat5@mahimahi.ds.itd.umich.edu>', 'michael.feldstein@suny.edu', 're: lms/vle rants/comments', '2005-12-09T09:43:12-05:00')
('<22585576.1134135343809.javamail.tomcat5@mahimahi.ds.itd.umich.edu>', 'john@cam.ac.uk', 're: lms/vle rants/comments', '2005-12-09T13:32:29+00:00')
('<29494755.1134157064976.javamail.tomcat5@sharkfin.ds.itd.umich.edu>', 's-githens@northwestern.edu', 're: sakaiportallogin and presense', '2005-12-09T13:32:31-06:00')
('<20623058.1134135893412.javamail.tomcat5@mahimahi.ds.itd.umich.edu>', 'john@cam.ac.uk', 're: lms/vle rants/comments', '2005-12-09T13:42:24+00:00')
('<14721465.1134163692331.javamail.tomcat5@mahimahi.ds.itd.umich.edu>', 's-githens@northwestern.edu', 're: sakaiportallogin and presense', '2005-12-09T15:23:09-06:00')
('<31872472.1134150954615.javamail.tomcat5@mahimahi.ds.itd.umich.edu>', 'ys2n@virginia.edu', 'sakaiportallogin and presense', '2005-12-09T17:54:17+00:00')
('<1304695.1134163143767.javamail.tomcat5@mahimahi.ds.itd.umich.edu>', 'ys2n@virginia.edu', 're: sakaiportallogin and presense', '2005-12-09T21:16:39+00:00')
('<3598962.1134188359277.javamail.tomcat5@sharkfin.ds.itd.umich.edu>', 'slt@columbia.edu', 're: cas and sakai 1.5', '2005-12-09T23:16:40-05:00')
('<590808.1134277104504.javamail.tomcat5@mahimahi.ds.itd.umich.edu>', 'dgcotton@ucdavis.edu', 'memory error with 2.1', '2005-12-10T20:55:54-08:00')
('<27775220.1134286694278.javamail.tomcat5@sharkfin.ds.itd.umich.edu>', 'vyu2@yahoo.com', 're: memory error with 2.1', '2005-12-10T23:34:43-08:00')
('<18541911.1134241825684.javamail.tomcat5@sharkfin.ds.itd.umich.edu>', 'winstonw.tw@gmail.com', 're: sakai ldap authentication', '2005-12-11T03:07:29+08:00')
('<20021180.1134321068392.javamail.tomcat5@sharkfin.ds.itd.umich.edu>', 'ajpoland@indiana.edu', 're: memory error with 2.1', '2005-12-11T12:08:15-05:00')
('<28266638.1134399879087.javamail.tomcat5@sharkfin.ds.itd.umich.edu>', 'caseyd1@stanford.edu', 're: sakai 2.1 provider examples', '2005-12-12T07:02:36-08:00')
('<1755944.1134395859482.javamail.tomcat5@mahimahi.ds.itd.umich.edu>', 'aaronz@vt.edu', 'sakai 2.1 provider examples', '2005-12-12T08:55:09-05:00')
('<10733551.1134381175177.javamail.tomcat5@mahimahi.ds.itd.umich.edu>', 'j.higham@hull.ac.uk', 're: sakai 2.1 - lone zero block error', '2005-12-12T09:49:16+00:00')
('<13486694.1134400555513.javamail.tomcat5@sharkfin.ds.itd.umich.edu>', 'aaronz@vt.edu', 're: sakai 2.1 provider examples', '2005-12-12T10:13:38-05:00')
('<25165005.1134413878170.javamail.tomcat5@mahimahi.ds.itd.umich.edu>', 'jeffrey.beeman@asu.edu', 're: sakai logo', '2005-12-12T11:14:55-07:00')
('<d3dc4255-5936-4582-9aa1-05b298302dfa@umich.edu>', 'csev@umich.edu', 'sepp library discussion group renamed - now with open membership', '2005-12-12T11:33:29-05:00')
('<6.0.1.1.2.20051212130514.0277fce8@casbah.it.northwestern.edu>', 'pgoldweic@northwestern.edu', 'problems accessing the collab site with internet explorer...', '2005-12-12T13:16:12-06:00')
('<6.0.1.1.2.20051212140958.027c5e10@casbah.it.northwestern.edu>', 'pgoldweic@northwestern.edu', 're: problems accessing the collab site with internet', '2005-12-12T14:20:41-06:00')
('<2931210.1134397540283.javamail.tomcat5@sharkfin.ds.itd.umich.edu>', 'andrew@cam.ac.uk', 'file picker for non-legacy tools', '2005-12-12T14:23:12+00:00')
('<23677089.1134422832868.javamail.tomcat5@mahimahi.ds.itd.umich.edu>', 'john.ellis@rsmart.com', 're: file picker for non-legacy tools', '2005-12-12T14:24:48-07:00')
('<21409905.1134416675058.javamail.tomcat5@sharkfin.ds.itd.umich.edu>', 'aaronz@vt.edu', 'sakai 2.01 vt provider code', '2005-12-12T14:42:01-05:00')
('<11878072.1134417436961.javamail.tomcat5@sharkfin.ds.itd.umich.edu>', 'aaronz@vt.edu', 're: problems accessing the collab site with internet explorer...', '2005-12-12T14:54:49-05:00')
('<4785696.1134423981953.javamail.tomcat5@sharkfin.ds.itd.umich.edu>', 'jxf@immagic.com', 're: worksite taxonomy', '2005-12-12T16:41:04-05:00')
('<6.2.1.2.2.20051212165645.03248338@calmail.berkeley.edu>', 'ray@berkeley.edu', 're: sakai 2.1 samigo', '2005-12-12T17:03:51-08:00')
('<30572893.1134427916370.javamail.tomcat5@sharkfin.ds.itd.umich.edu>', 'dave.ross@gmail.com', 're: memory error with 2.1', '2005-12-12T17:49:13-05:00')
('<2997944.1134430430365.javamail.tomcat5@mahimahi.ds.itd.umich.edu>', 'clayf@bu.edu', 're: memory error with 2.1', '2005-12-12T18:31:23-05:00')
('<e7802fd3-0d98-4ff2-b6ff-6cfba6042572@umich.edu>', 'ggolden@umich.edu', 'sakai 2.1 conversion - an update', '2005-12-12T20:02:00-05:00')
('<23957896.1134422219097.javamail.tomcat5@sharkfin.ds.itd.umich.edu>', 'ys2n@virginia.edu', 'worksite taxonomy', '2005-12-12T21:15:22+00:00')
('<439e1eec020000a0000063dc@gwvsmta2.weber.edu>', 'lfernandez@weber.edu', 're: memory error with 2.1', '2005-12-13T01:08:01-07:00')
('<439e240b020000a0000063e8@gwvsmta2.weber.edu>', 'lfernandez@weber.edu', 'audio recordings of austin presentations', '2005-12-13T01:29:49-07:00')
('<3663045.1134442112243.javamail.tomcat5@mahimahi.ds.itd.umich.edu>', 'ys2n@virginia.edu', 're: worksite taxonomy', '2005-12-13T02:46:51+00:00')
('<28791933.1134479146616.javamail.tomcat5@sharkfin.ds.itd.umich.edu>', 'jleasia@umich.edu', 're: worksite taxonomy', '2005-12-13T08:02:47-05:00')
('<e5ffc1d2-e42b-4f6d-baf3-4d7770c97070@umich.edu>', 'csev@umich.edu', 're: audio recordings of austin presentations', '2005-12-13T08:12:08-05:00')
('<30816444.1134482570622.javamail.tomcat5@sharkfin.ds.itd.umich.edu>', 'gsilver@umich.edu', 're: worksite taxonomy', '2005-12-13T08:58:10-05:00')
('<23078937.1134484534715.javamail.tomcat5@sharkfin.ds.itd.umich.edu>', 'jrm@jhu.edu', 'sakai 2.1 db error?', '2005-12-13T09:32:39-05:00')
('<3165698.1134487079017.javamail.tomcat5@sharkfin.ds.itd.umich.edu>', 'slt@columbia.edu', 're: sakai 2.1 conversion - an update', '2005-12-13T10:15:28-05:00')
('<6.2.1.2.2.20051213120224.03297468@calmail.berkeley.edu>', 'ray@berkeley.edu', 'big news in jsf land', '2005-12-13T12:07:02-08:00')
('<29281715.1134482926801.javamail.tomcat5@mahimahi.ds.itd.umich.edu>', 'antranig@cam.ac.uk', '"direct urls"', '2005-12-13T14:06:13+00:00')
('<s39ede97.048@gwia201.syr.edu>', 'jmpease@syr.edu', 'entity model', '2005-12-13T14:45:24-05:00')
('<1757601.1134507203941.javamail.tomcat5@mahimahi.ds.itd.umich.edu>', 'gwang3@unl.edu', 'error to run sakai 2.1', '2005-12-13T14:50:25-06:00')
('<12381679.1134507555999.javamail.tomcat5@mahimahi.ds.itd.umich.edu>', 'gwang3@unl.edu', 'error to run sakai 2.1', '2005-12-13T14:50:25-06:00')
('<771907be-6323-4dca-bfbf-61c85f193f0b@umich.edu>', 'bkirschn@umich.edu', 'utf-8 problem on sakai 2.1 with mysql', '2005-12-13T14:55:24-05:00')
('<26468860.1134524742049.javamail.tomcat5@sharkfin.ds.itd.umich.edu>', 'vrajgopalan@ucmerced.edu', "regarding the section manager and other section related api's", '2005-12-13T15:02:42-08:00')
('<13782164.1134516394730.javamail.tomcat5@mahimahi.ds.itd.umich.edu>', 'vrajgopalan@ucmerced.edu', "regarding the section manager and other section related api's", '2005-12-13T15:23:15-08:00')
('<6334332.1134524741759.javamail.tomcat5@sharkfin.ds.itd.umich.edu>', 'wchang@dri.edu', 'password forgotten feature', '2005-12-13T15:23:26-08:00')
'''
