import sqlite3
import time
import re
import zlib
from datetime import datetime, timedelta

# Not all systems have this
try:
    import dateutil.parser as parser
except:
    pass

dnsmapping = dict()
mapping = dict()


#so far, only 1 argument passed in => 'sender'
# e.g. old => s.swinsburg@lancaster.ac.uk, new => steve.swinsburg@swinsborg.com
def fixsender(sender,allsenders=None) :
    global dnsmapping
    global mapping
    if sender is None : return None
    sender = sender.strip().lower()
    sender = sender.replace('<','').replace('>','')

    # Check if we have a hacked gmane.org from address
    if allsenders is not None and sender.endswith('gmane.org') :
        pieces = sender.split('-')

        realsender = None
        for s in allsenders:
            if s.startswith(pieces[0]) :
                #sender into our function => realsender
                realsender = sender
                #sender in 'allsenders' => fake sender
                #with ('gmane.org') at the end + a 'fake sender prefix' at the start
                sender = s
                print("for loop 1", realsender, sender)
                break

        #  'realsender is None' when the 'realsender'/'sender' u are evaluating is not in the 'allsenders fake senders list'
        if realsender is None :
            #then evaluate the old-to-new email 'mapping' DB
            # mapping is a dict => {'old sender email' : 'new sender email', ...}
            # key,value pair
            for s in mapping:
                #find whether ''
                if s.startswith(pieces[0]) :
                    realsender = sender
                    sender = mapping[s]
                    print("for loop 2", realsender, sender)
                    break

        #if realsender still cant be found
        if realsender is None : sender = pieces[0]


    mpieces = sender.split("@")
    #not sure when this would happen, when we either have 'abcdef' or 'iupui.edu'
    if len(mpieces) != 2 : return sender

    dns = mpieces[1]    #'iupui.edu'
    x = dns
    pieces = dns.split(".") #['iupui', 'edu']

    #https://codingbat.com/doc/python-strings.html
    # refresh negative indexes
    #   s = 'Hello'
    # s[-2:]  ## 'lo', begin slice with 2nd from the end
    # s[:-3]  ## 'He', end slice 3rd from the end
    if dns.endswith(".edu") or dns.endswith(".com") or dns.endswith(".org") or dns.endswith(".net") :
        #recall pieces = ['iupui', 'edu']
        # dns = iupui.edu
        dns = ".".join(pieces[-2:])
    else:
        # dns = abcdef.idk.co
        dns = ".".join(pieces[-3:])
    # if dns != x : print(x,dns)
    # if dns != dnsmapping.get(dns,dns) : print(dns,dnsmapping.get(dns,dns))
    dns = dnsmapping.get(dns,dns)   #dict.get(key, valueIfNotFound); get 'mapped dns', otherwise use 'existing dns'
    # abc@abcdef.idk.co
    return mpieces[0] + '@' + dns




def parsemaildate(md) :
    # See if we have dateutil
    try:
        pdate = parser.parse(md)
        test_at = pdate.isoformat()
        return test_at
    except:
        pass

    # Non-dateutil version - we try our best

    pieces = md.split()
    notz = " ".join(pieces[:4]).strip()

    # Try a bunch of format variations - strptime() is *lame*
    dnotz = None
    for form in [ '%d %b %Y %H:%M:%S', '%d %b %Y %H:%M:%S',
        '%d %b %Y %H:%M', '%d %b %Y %H:%M', '%d %b %y %H:%M:%S',
        '%d %b %y %H:%M:%S', '%d %b %y %H:%M', '%d %b %y %H:%M' ] :
        try:
            dnotz = datetime.strptime(notz, form)
            break
        except:
            continue

    if dnotz is None :
        # print('Bad Date:',md)
        return None

    iso = dnotz.isoformat()

    tz = "+0000"
    try:
        tz = pieces[4]
        ival = int(tz) # Only want numeric timezone values
        if tz == '-0000' : tz = '+0000'
        tzh = tz[:3]
        tzm = tz[3:]
        tz = tzh+":"+tzm
    except:
        pass

    return iso+tz



# Parse out the info...
def parseheader(hdr, allsenders=None):
    if hdr is None or len(hdr) < 1 : return None
    sender = None
    x = re.findall('\nFrom: .* <(\S+@\S+)>\n', hdr)
    if len(x) >= 1 :
        sender = x[0]
    else:
        x = re.findall('\nFrom: (\S+@\S+)\n', hdr)
        if len(x) >= 1 :
            sender = x[0]

    # normalize the domain name of Email addresses
    sender = fixsender(sender, allsenders)

    date = None
    y = re.findall('\nDate: .*, (.*)\n', hdr)
    sent_at = None
    if len(y) >= 1 :
        tdate = y[0]
        tdate = tdate[:26]
        try:
            sent_at = parsemaildate(tdate)
        except Exception as e:
            # print('Date ignored ',tdate, e)
            return None

    subject = None
    z = re.findall('\nSubject: (.*)\n', hdr)
    if len(z) >= 1 : subject = z[0].strip().lower()

    guid = None
    z = re.findall('\nMessage-ID: (.*)\n', hdr)
    if len(z) >= 1 : guid = z[0].strip().lower()

    if sender is None or sent_at is None or subject is None or guid is None :
        return None
    return (guid, sender, subject, sent_at)




# ==========connection 1 to index.sqlite============
conn = sqlite3.connect('index.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Messages ')
cur.execute('DROP TABLE IF EXISTS Senders ')
cur.execute('DROP TABLE IF EXISTS Subjects ')
cur.execute('DROP TABLE IF EXISTS Replies ')

# guid = global unique ID
# blob = binary large objects
cur.execute('''CREATE TABLE IF NOT EXISTS Messages (id INTEGER PRIMARY KEY
                                                    , guid TEXT UNIQUE
                                                    , sent_at INTEGER
                                                    , sender_id INTEGER
                                                    , subject_id INTEGER
                                                    , headers BLOB
                                                    , body BLOB)''')
cur.execute('''CREATE TABLE IF NOT EXISTS Senders (id INTEGER PRIMARY KEY
                                                    , sender TEXT UNIQUE)''')
cur.execute('''CREATE TABLE IF NOT EXISTS Subjects (id INTEGER PRIMARY KEY
                                                    , subject TEXT UNIQUE)''')
#replies - from message id, to message id
cur.execute('''CREATE TABLE IF NOT EXISTS Replies (from_id INTEGER
                                                    , to_id INTEGER)''')






# ==========connection 2 to mapping.sqlite============
conn_1 = sqlite3.connect('mapping.sqlite')
cur_1 = conn_1.cursor()

cur_1.execute('SELECT old,new FROM DNSMapping')
for message_row in cur_1 :
    # message_row[0] => old DNS
    # message_row[1] => new DNS
    dnsmapping[message_row[0].strip().lower()] = message_row[1].strip().lower()

#mapping of email addresses, if email addresses were changed
mapping = dict()
cur_1.execute('SELECT old,new FROM Mapping')
for message_row in cur_1 :
    # fixsender function defined earlier
    old = fixsender(message_row[0])
    new = fixsender(message_row[1])
    mapping[old] = fixsender(new)
    # print("message_row", message_row)

# Done with mapping.sqlite
conn_1.close()






# ==========connection 3 to content.sqlite============
# Open the main content (Read only)
conn_1 = sqlite3.connect('file:content.sqlite?mode=ro', uri=True)
cur_1 = conn_1.cursor()

allsenders = list()
cur_1.execute('SELECT email FROM Messages')
for message_row in cur_1 :
    #sender email
    sender = fixsender(message_row[0])
    if sender is None : continue
    if 'gmane.org' in sender : continue
    if sender in allsenders: continue
    allsenders.append(sender)

print("Loaded allsenders",len(allsenders),"and mapping",len(mapping),"dns mapping",len(dnsmapping))
# print("allsenders")
# print(allsenders)

cur_1.execute('SELECT headers, body, sent_at FROM Messages ORDER BY sent_at')

senders = dict()
subjects = dict()
guids = dict()

count = 0

for message_row in cur_1 :
    hdr = message_row[0]
    parsed = parseheader(hdr, allsenders)
    if parsed is None: continue
    (guid, sender, subject, sent_at) = parsed
    # print(parsed)



    # Apply the sender mapping
    sender = mapping.get(sender,sender)

    count = count + 1
    if count % 250 == 1 : print(count,sent_at, sender)
    # print(guid, sender, subject, sent_at)

    if 'gmane.org' in sender:
        print("Error in sender ===", sender)


    #before preparing dictionaries
    # print(senders)
    # print(subjects)
    # print(guids)

    #instantiate for the table insertions below
    sender_id = senders.get(sender,None)
    subject_id = subjects.get(subject,None)
    guid_id = guids.get(guid,None)

    #after 'preparing' dictionaries
    # print(senders)
    # print(subjects)
    # print(guids)


    if sender_id is None :
        cur.execute('INSERT OR IGNORE INTO Senders (sender) VALUES ( ? )', ( sender, ) )
        conn.commit()
        cur.execute('SELECT id FROM Senders WHERE sender=? LIMIT 1', ( sender, ))
        try:
            row = cur.fetchone()
            sender_id = row[0]
            senders[sender] = sender_id
        except:
            print('Could not retrieve sender id',sender)
            break

    if subject_id is None :
        cur.execute('INSERT OR IGNORE INTO Subjects (subject) VALUES ( ? )', ( subject, ) )
        conn.commit()
        cur.execute('SELECT id FROM Subjects WHERE subject=? LIMIT 1', ( subject, ))
        try:
            row = cur.fetchone()
            subject_id = row[0]
            subjects[subject] = subject_id
        except:
            print('Could not retrieve subject id',subject)
            break

    # print(sender_id, subject_id)
    cur.execute('INSERT OR IGNORE INTO Messages (guid,sender_id,subject_id,sent_at,headers,body) VALUES ( ?,?,?,datetime(?),?,? )',
            ( guid, sender_id, subject_id, sent_at,
            zlib.compress(message_row[0].encode()), zlib.compress(message_row[1].encode())) )
    conn.commit()
    cur.execute('SELECT id FROM Messages WHERE guid=? LIMIT 1', ( guid, ))
    try:
        row = cur.fetchone()
        message_id = row[0]
        guids[guid] = message_id
    except:
        print('Could not retrieve guid id',guid)
        break

    # print("iteration: ", count)
    # print(senders)
    # print(subjects)
    # print(guids)
    # print("\n")




#for exercise
print("allsenders")
print(allsenders)

cur.close()
cur_1.close()












'''
Visualise output

print("dnsmapping")
print(dnsmapping)
dnsmapping
{'iupui.edu': 'indiana.edu'}



print("message_row", message_row)
message_row ('s.swinsburg@lancaster.ac.uk ', 'steve.swinsburg@swinsborg.com')
message_row ('sswinsb2@une.edu.au ', 'steve.swinsburg@swinsborg.com')
message_row ('a.fish@lancaster.ac.uk ', 'adrian.r.fish@gmail.com')
message_row ('jonespm@umich.edu ', 'matthew@longsight.com')
message_row ('sinouvivian@foothill.edu ', 'sinou@etudes.org')
message_row ('sinouvivie@foothill.edu ', 'sinou@etudes.org')
message_row ('maheshwarirashmi@foothill.edu ', 'rashmi@etudes.org')
message_row ('rashmi@foothillglobalaccess.org ', 'rashmi@etudes.org')
message_row ('tannirumurthy@fhda.edu ', 'murthy@etudes.org')
message_row ('tannirumurthy@foothill.edu ', 'murthy@etudes.org')
message_row ('mallikamt@foothillglobalaccess.org ', 'mallika@etudes.org')
message_row ('thoppaymallika@fhda.edu ', 'mallika@etudes.org')
message_row ('ggolden@umich.edu', 'ggolden22@mac.com\n')
message_row ('aaronz@vt.edu', 'azeckoski@unicon.net')
message_row ('clayf@bu.edu', 'clay.fenlason@gatech.edu')
message_row ('nangell@rsmart.com', 'nate.angell@rsmart.com')
message_row ('anthony.atkins@vt.edu', 'tony.atkins@uhi.ac.uk')
message_row ('smkeesle@syr.edu', 'sean.keesler@threecanoes.com')
message_row ('carl.hall@et.gatech.edu', 'carl@hallwaytech.com')
message_row ('carl.hall@gatech.edu', 'carl@hallwaytech.com')
message_row ('njbotime@svsu.edu', 'botimer@umich.edu')
message_row ('jbush@rsmart.com', 'john.bush@rsmart.com')
message_row ('duffy@email.arizona.edu', 'duffy@rsmart.com')
message_row ('melledge@umich.edu', 'elledge@msu.edu')
message_row ('zach.thomas@txstate.edu', 'zach@aeroplanesoftware.com\n')
message_row ('zach.thomas@gmail.com', 'zach@aeroplanesoftware.com\n')
message_row ('sgithens@caret.cam.ac.uk', 'swgithen@mtu.edu\n')
message_row ('s-githens@northwestern.edu', 'swgithen@mtu.edu')
message_row ('ieb@tfd.co.uk', 'ian@cam.ac.uk')
message_row ('sgithens@cam.ac.uk', 'swgithen@mtu.edu')
message_row ('carl.hall@gatech.edu', 'carl@hallwaytech.com')
message_row ('steve.swinsburg@gmail.com', 'steve.swinsburg@swinsborg.com')




#iteration 1
print("Loaded allsenders",len(allsenders),"and mapping",len(mapping),"dns mapping",len(dnsmapping))
Loaded allsenders 33 and mapping 29 dns mapping 1

print("allsenders")
print(allsenders)
allsenders
['ggolden@umich.edu', 'csev@umich.edu', 'kevin.carpenter@rsmart.com', 'michael.feldstein@suny.edu', 'john@cam.ac.uk', 's-githens@northwestern.edu', 'ys2n@virginia.edu', 'slt@columbia.edu', 'dgcotton@ucdavis.edu', 'vyu2@yahoo.com', 'winstonw.tw@gmail.com', 'ajpoland@indiana.edu', 'caseyd1@stanford.edu', 'aaronz@vt.edu', 'j.higham@hull.ac.uk', 'jeffrey.beeman@asu.edu', 'pgoldweic@northwestern.edu', 'andrew@cam.ac.uk', 'john.ellis@rsmart.com', 'jxf@immagic.com', 'ray@berkeley.edu', 'dave.ross@gmail.com', 'clayf@bu.edu', 'lfernandez@weber.edu', 'jleasia@umich.edu', 'gsilver@umich.edu', 'jrm@jhu.edu', 'antranig@cam.ac.uk', 'jmpease@syr.edu', 'gwang3@unl.edu', 'bkirschn@umich.edu', 'vrajgopalan@ucmerced.edu', 'wchang@dri.edu']


#before preparing dictionaries
# print(senders)
# print(subjects)
# print(guids)
{}
{}
{}


#after 'preparing' dictionaries
# print(senders)
# print(subjects)
# print(guids)
{}
{}
{}
#dictionaries are still empty because we have not inserted values into the dictionaries












print("iteration: ", count)
print(senders)
print(subjects)
print(guids)
print("\n")
iteration:  1
{'ggolden22@mac.com': 1}
{'call for participation: developers documentation': 1}
{'<b7eaf76e-3366-4ae3-bdd6-6743707feba9@umich.edu>': 1}


iteration:  2
{'ggolden22@mac.com': 1, 'csev@umich.edu': 2}
{'call for participation: developers documentation': 1, 'report from the austin conference:  sakai developers break into song': 2}
{'<b7eaf76e-3366-4ae3-bdd6-6743707feba9@umich.edu>': 1, '<bb7ce631-ccf0-40a3-b076-683f9d03e0c9@umich.edu>': 2}


iteration:  3
{'ggolden22@mac.com': 1, 'csev@umich.edu': 2, 'kevin.carpenter@rsmart.com': 3}
{'call for participation: developers documentation': 1, 'report from the austin conference:  sakai developers break into song': 2, 'cas and sakai 1.5': 3}
{'<b7eaf76e-3366-4ae3-bdd6-6743707feba9@umich.edu>': 1, '<bb7ce631-ccf0-40a3-b076-683f9d03e0c9@umich.edu>': 2, '<16703710.1134144397398.javamail.tomcat5@sharkfin.ds.itd.umich.edu>': 3}


iteration:  4
{'ggolden22@mac.com': 1, 'csev@umich.edu': 2, 'kevin.carpenter@rsmart.com': 3, 'michael.feldstein@suny.edu': 4}
{'call for participation: developers documentation': 1, 'report from the austin conference:  sakai developers break into song': 2, 'cas and sakai 1.5': 3, 're: lms/vle rants/comments': 4}
{'<b7eaf76e-3366-4ae3-bdd6-6743707feba9@umich.edu>': 1, '<bb7ce631-ccf0-40a3-b076-683f9d03e0c9@umich.edu>': 2, '<16703710.1134144397398.javamail.tomcat5@sharkfin.ds.itd.umich.edu>': 3, '<9622225.1134139564303.javamail.tomcat5@mahimahi.ds.itd.umich.edu>': 4}


iteration:  5
{'ggolden22@mac.com': 1, 'csev@umich.edu': 2, 'kevin.carpenter@rsmart.com': 3, 'michael.feldstein@suny.edu': 4, 'john@cam.ac.uk': 5}
{'call for participation: developers documentation': 1, 'report from the austin conference:  sakai developers break into song': 2, 'cas and sakai 1.5': 3, 're: lms/vle rants/comments': 4}
{'<b7eaf76e-3366-4ae3-bdd6-6743707feba9@umich.edu>': 1, '<bb7ce631-ccf0-40a3-b076-683f9d03e0c9@umich.edu>': 2, '<16703710.1134144397398.javamail.tomcat5@sharkfin.ds.itd.umich.edu>': 3, '<9622225.1134139564303.javamail.tomcat5@mahimahi.ds.itd.umich.edu>': 4, '<22585576.1134135343809.javamail.tomcat5@mahimahi.ds.itd.umich.edu>': 5}


iteration:  6
{'ggolden22@mac.com': 1, 'csev@umich.edu': 2, 'kevin.carpenter@rsmart.com': 3, 'michael.feldstein@suny.edu': 4, 'john@cam.ac.uk': 5, 'swgithen@mtu.edu': 6}
{'call for participation: developers documentation': 1, 'report from the austin conference:  sakai developers break into song': 2, 'cas and sakai 1.5': 3, 're: lms/vle rants/comments': 4, 're: sakaiportallogin and presense': 5}
{'<b7eaf76e-3366-4ae3-bdd6-6743707feba9@umich.edu>': 1, '<bb7ce631-ccf0-40a3-b076-683f9d03e0c9@umich.edu>': 2, '<16703710.1134144397398.javamail.tomcat5@sharkfin.ds.itd.umich.edu>': 3, '<9622225.1134139564303.javamail.tomcat5@mahimahi.ds.itd.umich.edu>': 4, '<22585576.1134135343809.javamail.tomcat5@mahimahi.ds.itd.umich.edu>': 5, '<29494755.1134157064976.javamail.tomcat5@sharkfin.ds.itd.umich.edu>': 6}


iteration:  7
{'ggolden22@mac.com': 1, 'csev@umich.edu': 2, 'kevin.carpenter@rsmart.com': 3, 'michael.feldstein@suny.edu': 4, 'john@cam.ac.uk': 5, 'swgithen@mtu.edu': 6}
{'call for participation: developers documentation': 1, 'report from the austin conference:  sakai developers break into song': 2, 'cas and sakai 1.5': 3, 're: lms/vle rants/comments': 4, 're: sakaiportallogin and presense': 5}
{'<b7eaf76e-3366-4ae3-bdd6-6743707feba9@umich.edu>': 1, '<bb7ce631-ccf0-40a3-b076-683f9d03e0c9@umich.edu>': 2, '<16703710.1134144397398.javamail.tomcat5@sharkfin.ds.itd.umich.edu>': 3, '<9622225.1134139564303.javamail.tomcat5@mahimahi.ds.itd.umich.edu>': 4, '<22585576.1134135343809.javamail.tomcat5@mahimahi.ds.itd.umich.edu>': 5, '<29494755.1134157064976.javamail.tomcat5@sharkfin.ds.itd.umich.edu>': 6, '<20623058.1134135893412.javamail.tomcat5@mahimahi.ds.itd.umich.edu>': 7}


iteration:  8
{'ggolden22@mac.com': 1, 'csev@umich.edu': 2, 'kevin.carpenter@rsmart.com': 3, 'michael.feldstein@suny.edu': 4, 'john@cam.ac.uk': 5, 'swgithen@mtu.edu': 6}
{'call for participation: developers documentation': 1, 'report from the austin conference:  sakai developers break into song': 2, 'cas and sakai 1.5': 3, 're: lms/vle rants/comments': 4, 're: sakaiportallogin and presense': 5}
{'<b7eaf76e-3366-4ae3-bdd6-6743707feba9@umich.edu>': 1, '<bb7ce631-ccf0-40a3-b076-683f9d03e0c9@umich.edu>': 2, '<16703710.1134144397398.javamail.tomcat5@sharkfin.ds.itd.umich.edu>': 3, '<9622225.1134139564303.javamail.tomcat5@mahimahi.ds.itd.umich.edu>': 4, '<22585576.1134135343809.javamail.tomcat5@mahimahi.ds.itd.umich.edu>': 5, '<29494755.1134157064976.javamail.tomcat5@sharkfin.ds.itd.umich.edu>': 6, '<20623058.1134135893412.javamail.tomcat5@mahimahi.ds.itd.umich.edu>': 7, '<14721465.1134163692331.javamail.tomcat5@mahimahi.ds.itd.umich.edu>': 8}


iteration:  9
{'ggolden22@mac.com': 1, 'csev@umich.edu': 2, 'kevin.carpenter@rsmart.com': 3, 'michael.feldstein@suny.edu': 4, 'john@cam.ac.uk': 5, 'swgithen@mtu.edu': 6, 'ys2n@virginia.edu': 7}
{'call for participation: developers documentation': 1, 'report from the austin conference:  sakai developers break into song': 2, 'cas and sakai 1.5': 3, 're: lms/vle rants/comments': 4, 're: sakaiportallogin and presense': 5, 'sakaiportallogin and presense': 6}
{'<b7eaf76e-3366-4ae3-bdd6-6743707feba9@umich.edu>': 1, '<bb7ce631-ccf0-40a3-b076-683f9d03e0c9@umich.edu>': 2, '<16703710.1134144397398.javamail.tomcat5@sharkfin.ds.itd.umich.edu>': 3, '<9622225.1134139564303.javamail.tomcat5@mahimahi.ds.itd.umich.edu>': 4, '<22585576.1134135343809.javamail.tomcat5@mahimahi.ds.itd.umich.edu>': 5, '<29494755.1134157064976.javamail.tomcat5@sharkfin.ds.itd.umich.edu>': 6, '<20623058.1134135893412.javamail.tomcat5@mahimahi.ds.itd.umich.edu>': 7, '<14721465.1134163692331.javamail.tomcat5@mahimahi.ds.itd.umich.edu>': 8, '<31872472.1134150954615.javamail.tomcat5@mahimahi.ds.itd.umich.edu>': 9}


iteration:  10
{'ggolden22@mac.com': 1, 'csev@umich.edu': 2, 'kevin.carpenter@rsmart.com': 3, 'michael.feldstein@suny.edu': 4, 'john@cam.ac.uk': 5, 'swgithen@mtu.edu': 6, 'ys2n@virginia.edu': 7}
{'call for participation: developers documentation': 1, 'report from the austin conference:  sakai developers break into song': 2, 'cas and sakai 1.5': 3, 're: lms/vle rants/comments': 4, 're: sakaiportallogin and presense': 5, 'sakaiportallogin and presense': 6}
{'<b7eaf76e-3366-4ae3-bdd6-6743707feba9@umich.edu>': 1, '<bb7ce631-ccf0-40a3-b076-683f9d03e0c9@umich.edu>': 2, '<16703710.1134144397398.javamail.tomcat5@sharkfin.ds.itd.umich.edu>': 3, '<9622225.1134139564303.javamail.tomcat5@mahimahi.ds.itd.umich.edu>': 4, '<22585576.1134135343809.javamail.tomcat5@mahimahi.ds.itd.umich.edu>': 5, '<29494755.1134157064976.javamail.tomcat5@sharkfin.ds.itd.umich.edu>': 6, '<20623058.1134135893412.javamail.tomcat5@mahimahi.ds.itd.umich.edu>': 7, '<14721465.1134163692331.javamail.tomcat5@mahimahi.ds.itd.umich.edu>': 8, '<31872472.1134150954615.javamail.tomcat5@mahimahi.ds.itd.umich.edu>': 9, '<1304695.1134163143767.javamail.tomcat5@mahimahi.ds.itd.umich.edu>': 10}

...
...
...

iteration:  49
{'ggolden22@mac.com': 1, 'csev@umich.edu': 2, 'kevin.carpenter@rsmart.com': 3, 'michael.feldstein@suny.edu': 4, 'john@cam.ac.uk': 5, 'swgithen@mtu.edu': 6, 'ys2n@virginia.edu': 7, 'slt@columbia.edu': 8, 'dgcotton@ucdavis.edu': 9, 'vyu2@yahoo.com': 10, 'winstonw.tw@gmail.com': 11, 'ajpoland@indiana.edu': 12, 'caseyd1@stanford.edu': 13, 'azeckoski@unicon.net': 14, 'j.higham@hull.ac.uk': 15, 'jeffrey.beeman@asu.edu': 16, 'pgoldweic@northwestern.edu': 17, 'andrew@cam.ac.uk': 18, 'john.ellis@rsmart.com': 19, 'jxf@immagic.com': 20, 'ray@berkeley.edu': 21, 'dave.ross@gmail.com': 22, 'clay.fenlason@gatech.edu': 23, 'lfernandez@weber.edu': 24, 'jleasia@umich.edu': 25, 'gsilver@umich.edu': 26, 'jrm@jhu.edu': 27, 'antranig@cam.ac.uk': 28, 'jmpease@syr.edu': 29, 'gwang3@unl.edu': 30, 'bkirschn@umich.edu': 31, 'vrajgopalan@ucmerced.edu': 32}
{'call for participation: developers documentation': 1, 'report from the austin conference:  sakai developers break into song': 2, 'cas and sakai 1.5': 3, 're: lms/vle rants/comments': 4, 're: sakaiportallogin and presense': 5, 'sakaiportallogin and presense': 6, 're: cas and sakai 1.5': 7, 'memory error with 2.1': 8, 're: memory error with 2.1': 9, 're: sakai ldap authentication': 10, 're: sakai 2.1 provider examples': 11, 'sakai 2.1 provider examples': 12, 're: sakai 2.1 - lone zero block error': 13, 're: sakai logo': 14, 'sepp library discussion group renamed - now with open membership': 15, 'problems accessing the collab site with internet explorer...': 16, 're: problems accessing the collab site with internet': 17, 'file picker for non-legacy tools': 18, 're: file picker for non-legacy tools': 19, 'sakai 2.01 vt provider code': 20, 're: problems accessing the collab site with internet explorer...': 21, 're: worksite taxonomy': 22, 're: sakai 2.1 samigo': 23, 'sakai 2.1 conversion - an update': 24, 'worksite taxonomy': 25, 'audio recordings of austin presentations': 26, 're: audio recordings of austin presentations': 27, 'sakai 2.1 db error?': 28, 're: sakai 2.1 conversion - an update': 29, 'big news in jsf land': 30, '"direct urls"': 31, 'entity model': 32, 'error to run sakai 2.1': 33, 'utf-8 problem on sakai 2.1 with mysql': 34, "regarding the section manager and other section related api's": 35}
{'<b7eaf76e-3366-4ae3-bdd6-6743707feba9@umich.edu>': 1, '<bb7ce631-ccf0-40a3-b076-683f9d03e0c9@umich.edu>': 2, '<16703710.1134144397398.javamail.tomcat5@sharkfin.ds.itd.umich.edu>': 3, '<9622225.1134139564303.javamail.tomcat5@mahimahi.ds.itd.umich.edu>': 4, '<22585576.1134135343809.javamail.tomcat5@mahimahi.ds.itd.umich.edu>': 5, '<29494755.1134157064976.javamail.tomcat5@sharkfin.ds.itd.umich.edu>': 6, '<20623058.1134135893412.javamail.tomcat5@mahimahi.ds.itd.umich.edu>': 7, '<14721465.1134163692331.javamail.tomcat5@mahimahi.ds.itd.umich.edu>': 8, '<31872472.1134150954615.javamail.tomcat5@mahimahi.ds.itd.umich.edu>': 9, '<1304695.1134163143767.javamail.tomcat5@mahimahi.ds.itd.umich.edu>': 10, '<3598962.1134188359277.javamail.tomcat5@sharkfin.ds.itd.umich.edu>': 11, '<590808.1134277104504.javamail.tomcat5@mahimahi.ds.itd.umich.edu>': 12, '<27775220.1134286694278.javamail.tomcat5@sharkfin.ds.itd.umich.edu>': 13, '<18541911.1134241825684.javamail.tomcat5@sharkfin.ds.itd.umich.edu>': 14, '<20021180.1134321068392.javamail.tomcat5@sharkfin.ds.itd.umich.edu>': 15, '<28266638.1134399879087.javamail.tomcat5@sharkfin.ds.itd.umich.edu>': 16, '<1755944.1134395859482.javamail.tomcat5@mahimahi.ds.itd.umich.edu>': 17, '<10733551.1134381175177.javamail.tomcat5@mahimahi.ds.itd.umich.edu>': 18, '<13486694.1134400555513.javamail.tomcat5@sharkfin.ds.itd.umich.edu>': 19, '<25165005.1134413878170.javamail.tomcat5@mahimahi.ds.itd.umich.edu>': 20, '<d3dc4255-5936-4582-9aa1-05b298302dfa@umich.edu>': 21, '<6.0.1.1.2.20051212130514.0277fce8@casbah.it.northwestern.edu>': 22, '<6.0.1.1.2.20051212140958.027c5e10@casbah.it.northwestern.edu>': 23, '<2931210.1134397540283.javamail.tomcat5@sharkfin.ds.itd.umich.edu>': 24, '<23677089.1134422832868.javamail.tomcat5@mahimahi.ds.itd.umich.edu>': 25, '<21409905.1134416675058.javamail.tomcat5@sharkfin.ds.itd.umich.edu>': 26, '<11878072.1134417436961.javamail.tomcat5@sharkfin.ds.itd.umich.edu>': 27, '<4785696.1134423981953.javamail.tomcat5@sharkfin.ds.itd.umich.edu>': 28, '<6.2.1.2.2.20051212165645.03248338@calmail.berkeley.edu>': 29, '<30572893.1134427916370.javamail.tomcat5@sharkfin.ds.itd.umich.edu>': 30, '<2997944.1134430430365.javamail.tomcat5@mahimahi.ds.itd.umich.edu>': 31, '<e7802fd3-0d98-4ff2-b6ff-6cfba6042572@umich.edu>': 32, '<23957896.1134422219097.javamail.tomcat5@sharkfin.ds.itd.umich.edu>': 33, '<439e1eec020000a0000063dc@gwvsmta2.weber.edu>': 34, '<439e240b020000a0000063e8@gwvsmta2.weber.edu>': 35, '<3663045.1134442112243.javamail.tomcat5@mahimahi.ds.itd.umich.edu>': 36, '<28791933.1134479146616.javamail.tomcat5@sharkfin.ds.itd.umich.edu>': 37, '<e5ffc1d2-e42b-4f6d-baf3-4d7770c97070@umich.edu>': 38, '<30816444.1134482570622.javamail.tomcat5@sharkfin.ds.itd.umich.edu>': 39, '<23078937.1134484534715.javamail.tomcat5@sharkfin.ds.itd.umich.edu>': 40, '<3165698.1134487079017.javamail.tomcat5@sharkfin.ds.itd.umich.edu>': 41, '<6.2.1.2.2.20051213120224.03297468@calmail.berkeley.edu>': 42, '<29281715.1134482926801.javamail.tomcat5@mahimahi.ds.itd.umich.edu>': 43, '<s39ede97.048@gwia201.syr.edu>': 44, '<1757601.1134507203941.javamail.tomcat5@mahimahi.ds.itd.umich.edu>': 45, '<12381679.1134507555999.javamail.tomcat5@mahimahi.ds.itd.umich.edu>': 46, '<771907be-6323-4dca-bfbf-61c85f193f0b@umich.edu>': 47, '<26468860.1134524742049.javamail.tomcat5@sharkfin.ds.itd.umich.edu>': 48, '<13782164.1134516394730.javamail.tomcat5@mahimahi.ds.itd.umich.edu>': 49}


iteration:  50
{'ggolden22@mac.com': 1, 'csev@umich.edu': 2, 'kevin.carpenter@rsmart.com': 3, 'michael.feldstein@suny.edu': 4, 'john@cam.ac.uk': 5, 'swgithen@mtu.edu': 6, 'ys2n@virginia.edu': 7, 'slt@columbia.edu': 8, 'dgcotton@ucdavis.edu': 9, 'vyu2@yahoo.com': 10, 'winstonw.tw@gmail.com': 11, 'ajpoland@indiana.edu': 12, 'caseyd1@stanford.edu': 13, 'azeckoski@unicon.net': 14, 'j.higham@hull.ac.uk': 15, 'jeffrey.beeman@asu.edu': 16, 'pgoldweic@northwestern.edu': 17, 'andrew@cam.ac.uk': 18, 'john.ellis@rsmart.com': 19, 'jxf@immagic.com': 20, 'ray@berkeley.edu': 21, 'dave.ross@gmail.com': 22, 'clay.fenlason@gatech.edu': 23, 'lfernandez@weber.edu': 24, 'jleasia@umich.edu': 25, 'gsilver@umich.edu': 26, 'jrm@jhu.edu': 27, 'antranig@cam.ac.uk': 28, 'jmpease@syr.edu': 29, 'gwang3@unl.edu': 30, 'bkirschn@umich.edu': 31, 'vrajgopalan@ucmerced.edu': 32, 'wchang@dri.edu': 33}
{'call for participation: developers documentation': 1, 'report from the austin conference:  sakai developers break into song': 2, 'cas and sakai 1.5': 3, 're: lms/vle rants/comments': 4, 're: sakaiportallogin and presense': 5, 'sakaiportallogin and presense': 6, 're: cas and sakai 1.5': 7, 'memory error with 2.1': 8, 're: memory error with 2.1': 9, 're: sakai ldap authentication': 10, 're: sakai 2.1 provider examples': 11, 'sakai 2.1 provider examples': 12, 're: sakai 2.1 - lone zero block error': 13, 're: sakai logo': 14, 'sepp library discussion group renamed - now with open membership': 15, 'problems accessing the collab site with internet explorer...': 16, 're: problems accessing the collab site with internet': 17, 'file picker for non-legacy tools': 18, 're: file picker for non-legacy tools': 19, 'sakai 2.01 vt provider code': 20, 're: problems accessing the collab site with internet explorer...': 21, 're: worksite taxonomy': 22, 're: sakai 2.1 samigo': 23, 'sakai 2.1 conversion - an update': 24, 'worksite taxonomy': 25, 'audio recordings of austin presentations': 26, 're: audio recordings of austin presentations': 27, 'sakai 2.1 db error?': 28, 're: sakai 2.1 conversion - an update': 29, 'big news in jsf land': 30, '"direct urls"': 31, 'entity model': 32, 'error to run sakai 2.1': 33, 'utf-8 problem on sakai 2.1 with mysql': 34, "regarding the section manager and other section related api's": 35, 'password forgotten feature': 36}
{'<b7eaf76e-3366-4ae3-bdd6-6743707feba9@umich.edu>': 1, '<bb7ce631-ccf0-40a3-b076-683f9d03e0c9@umich.edu>': 2, '<16703710.1134144397398.javamail.tomcat5@sharkfin.ds.itd.umich.edu>': 3, '<9622225.1134139564303.javamail.tomcat5@mahimahi.ds.itd.umich.edu>': 4, '<22585576.1134135343809.javamail.tomcat5@mahimahi.ds.itd.umich.edu>': 5, '<29494755.1134157064976.javamail.tomcat5@sharkfin.ds.itd.umich.edu>': 6, '<20623058.1134135893412.javamail.tomcat5@mahimahi.ds.itd.umich.edu>': 7, '<14721465.1134163692331.javamail.tomcat5@mahimahi.ds.itd.umich.edu>': 8, '<31872472.1134150954615.javamail.tomcat5@mahimahi.ds.itd.umich.edu>': 9, '<1304695.1134163143767.javamail.tomcat5@mahimahi.ds.itd.umich.edu>': 10, '<3598962.1134188359277.javamail.tomcat5@sharkfin.ds.itd.umich.edu>': 11, '<590808.1134277104504.javamail.tomcat5@mahimahi.ds.itd.umich.edu>': 12, '<27775220.1134286694278.javamail.tomcat5@sharkfin.ds.itd.umich.edu>': 13, '<18541911.1134241825684.javamail.tomcat5@sharkfin.ds.itd.umich.edu>': 14, '<20021180.1134321068392.javamail.tomcat5@sharkfin.ds.itd.umich.edu>': 15, '<28266638.1134399879087.javamail.tomcat5@sharkfin.ds.itd.umich.edu>': 16, '<1755944.1134395859482.javamail.tomcat5@mahimahi.ds.itd.umich.edu>': 17, '<10733551.1134381175177.javamail.tomcat5@mahimahi.ds.itd.umich.edu>': 18, '<13486694.1134400555513.javamail.tomcat5@sharkfin.ds.itd.umich.edu>': 19, '<25165005.1134413878170.javamail.tomcat5@mahimahi.ds.itd.umich.edu>': 20, '<d3dc4255-5936-4582-9aa1-05b298302dfa@umich.edu>': 21, '<6.0.1.1.2.20051212130514.0277fce8@casbah.it.northwestern.edu>': 22, '<6.0.1.1.2.20051212140958.027c5e10@casbah.it.northwestern.edu>': 23, '<2931210.1134397540283.javamail.tomcat5@sharkfin.ds.itd.umich.edu>': 24, '<23677089.1134422832868.javamail.tomcat5@mahimahi.ds.itd.umich.edu>': 25, '<21409905.1134416675058.javamail.tomcat5@sharkfin.ds.itd.umich.edu>': 26, '<11878072.1134417436961.javamail.tomcat5@sharkfin.ds.itd.umich.edu>': 27, '<4785696.1134423981953.javamail.tomcat5@sharkfin.ds.itd.umich.edu>': 28, '<6.2.1.2.2.20051212165645.03248338@calmail.berkeley.edu>': 29, '<30572893.1134427916370.javamail.tomcat5@sharkfin.ds.itd.umich.edu>': 30, '<2997944.1134430430365.javamail.tomcat5@mahimahi.ds.itd.umich.edu>': 31, '<e7802fd3-0d98-4ff2-b6ff-6cfba6042572@umich.edu>': 32, '<23957896.1134422219097.javamail.tomcat5@sharkfin.ds.itd.umich.edu>': 33, '<439e1eec020000a0000063dc@gwvsmta2.weber.edu>': 34, '<439e240b020000a0000063e8@gwvsmta2.weber.edu>': 35, '<3663045.1134442112243.javamail.tomcat5@mahimahi.ds.itd.umich.edu>': 36, '<28791933.1134479146616.javamail.tomcat5@sharkfin.ds.itd.umich.edu>': 37, '<e5ffc1d2-e42b-4f6d-baf3-4d7770c97070@umich.edu>': 38, '<30816444.1134482570622.javamail.tomcat5@sharkfin.ds.itd.umich.edu>': 39, '<23078937.1134484534715.javamail.tomcat5@sharkfin.ds.itd.umich.edu>': 40, '<3165698.1134487079017.javamail.tomcat5@sharkfin.ds.itd.umich.edu>': 41, '<6.2.1.2.2.20051213120224.03297468@calmail.berkeley.edu>': 42, '<29281715.1134482926801.javamail.tomcat5@mahimahi.ds.itd.umich.edu>': 43, '<s39ede97.048@gwia201.syr.edu>': 44, '<1757601.1134507203941.javamail.tomcat5@mahimahi.ds.itd.umich.edu>': 45, '<12381679.1134507555999.javamail.tomcat5@mahimahi.ds.itd.umich.edu>': 46, '<771907be-6323-4dca-bfbf-61c85f193f0b@umich.edu>': 47, '<26468860.1134524742049.javamail.tomcat5@sharkfin.ds.itd.umich.edu>': 48, '<13782164.1134516394730.javamail.tomcat5@mahimahi.ds.itd.umich.edu>': 49, '<6334332.1134524741759.javamail.tomcat5@sharkfin.ds.itd.umich.edu>': 50}
'''




'''
Visualise SQLite tables after E2E run

Senders
id	sender
1	ggolden22@mac.com
2	csev@umich.edu
3	kevin.carpenter@rsmart.com
4	michael.feldstein@suny.edu
5	john@cam.ac.uk
6	swgithen@mtu.edu
7	ys2n@virginia.edu
8	slt@columbia.edu
9	dgcotton@ucdavis.edu
10	vyu2@yahoo.com
11	winstonw.tw@gmail.com
12	ajpoland@indiana.edu
13	caseyd1@stanford.edu
14	azeckoski@unicon.net
15	j.higham@hull.ac.uk
16	jeffrey.beeman@asu.edu
17	pgoldweic@northwestern.edu
18	andrew@cam.ac.uk
19	john.ellis@rsmart.com
20	jxf@immagic.com
21	ray@berkeley.edu
22	dave.ross@gmail.com
23	clay.fenlason@gatech.edu
24	lfernandez@weber.edu
25	jleasia@umich.edu
26	gsilver@umich.edu
27	jrm@jhu.edu
28	antranig@cam.ac.uk
29	jmpease@syr.edu
30	gwang3@unl.edu
31	bkirschn@umich.edu
32	vrajgopalan@ucmerced.edu
33	wchang@dri.edu


Subjects
id	subject
1	call for participation: developers documentation
2	report from the austin conference:  sakai developers break into song
3	cas and sakai 1.5
4	re: lms/vle rants/comments
5	re: sakaiportallogin and presense
6	sakaiportallogin and presense
7	re: cas and sakai 1.5
8	memory error with 2.1
9	re: memory error with 2.1
10	re: sakai ldap authentication
11	re: sakai 2.1 provider examples
12	sakai 2.1 provider examples
13	re: sakai 2.1 - lone zero block error
14	re: sakai logo
15	sepp library discussion group renamed - now with open membership
16	problems accessing the collab site with internet explorer...
17	re: problems accessing the collab site with internet
18	file picker for non-legacy tools
19	re: file picker for non-legacy tools
20	sakai 2.01 vt provider code
21	re: problems accessing the collab site with internet explorer...
22	re: worksite taxonomy
23	re: sakai 2.1 samigo
24	sakai 2.1 conversion - an update
25	worksite taxonomy
26	audio recordings of austin presentations
27	re: audio recordings of austin presentations
28	sakai 2.1 db error?
29	re: sakai 2.1 conversion - an update
30	big news in jsf land
31	"direct urls"
32	entity model
33	error to run sakai 2.1
34	utf-8 problem on sakai 2.1 with mysql
35	regarding the section manager and other section related api's
36	password forgotten feature







Messages
id	guid	                                            sent_at	                sender_id	subject_id	headers	   body
1	<b7eaf76e-3366-4ae3-bdd6-6743707feba9@umich.edu>	2005-12-09 05:34:30	     1	            1         <null>    <null>
2	<bb7ce631-ccf0-40a3-b076-683f9d03e0c9@umich.edu>	2005-12-09 05:58:01	     2	            2
3	<16703710.1134144397398.javamail.tomcat5@sharkfin.ds.itd.umich.edu>	2005-12-09 16:01:49	3	3
4	<9622225.1134139564303.javamail.tomcat5@mahimahi.ds.itd.umich.edu>	2005-12-09 14:43:12	4	4
5	<22585576.1134135343809.javamail.tomcat5@mahimahi.ds.itd.umich.edu>	2005-12-09 13:32:29	5	4
6	<29494755.1134157064976.javamail.tomcat5@sharkfin.ds.itd.umich.edu>	2005-12-09 19:32:31	6	5
7	<20623058.1134135893412.javamail.tomcat5@mahimahi.ds.itd.umich.edu>	2005-12-09 13:42:24	5	4
8	<14721465.1134163692331.javamail.tomcat5@mahimahi.ds.itd.umich.edu>	2005-12-09 21:23:09	6	5
9	<31872472.1134150954615.javamail.tomcat5@mahimahi.ds.itd.umich.edu>	2005-12-09 17:54:17	7	6
10	<1304695.1134163143767.javamail.tomcat5@mahimahi.ds.itd.umich.edu>	2005-12-09 21:16:39	7	5
...
49	<13782164.1134516394730.javamail.tomcat5@mahimahi.ds.itd.umich.edu>	2005-12-13 23:23:15	32	35
50	<6334332.1134524741759.javamail.tomcat5@sharkfin.ds.itd.umich.edu>	2005-12-13 23:23:26	33	36

Replies
<empty table>
'''
