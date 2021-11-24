import sqlite3
import time
import zlib

conn = sqlite3.connect('index.sqlite')
cur = conn.cursor()

cur.execute('SELECT id, sender FROM Senders')
senders = dict()
for message_row in cur :
    senders[message_row[0]] = message_row[1]

cur.execute('SELECT id, guid,sender_id,subject_id,sent_at FROM Messages')
messages = dict()
for message_row in cur :
    messages[message_row[0]] = (message_row[1],message_row[2],message_row[3],message_row[4])

print("Loaded messages=",len(messages),"senders=",len(senders))




#=============Top 10 orgs (using DNS)=================
sendorgs = dict()
for (message_id, message) in list(messages.items()):
    #messages dict
    # {'message_id' : [guid,sender_id,subject_id,sent_at]}
    # message[1] = sender_id
    sender = message[1]
    #senders dict
    # senders[sender] = abcdef@iupui.edu
    pieces = senders[sender].split("@")
    if len(pieces) != 2 : continue
    dns = pieces[1]
    sendorgs[dns] = sendorgs.get(dns,0) + 1

# pick the top schools
orgs = sorted(sendorgs, key=sendorgs.get, reverse=True)
orgs = orgs[:10]
print("Top 10 Organizations")
print(orgs)




#===========Count of (emails from each) DNS by year=================
counts = dict()
years = list()
# cur.execute('SELECT id, guid,sender_id,subject_id,sent_at FROM Messages')
for (message_id, message) in list(messages.items()):
    sender = message[1]
    pieces = senders[sender].split("@")
    if len(pieces) != 2 : continue
    dns = pieces[1]
    if dns not in orgs : continue

    # message[3] = sent_at
    year = message[3][:4]
    if year not in years : years.append(year)
    #key = ('2021-01', 'dns1') => used for viz later when retrieving the specific count combo for a particular year and dns
    key = (year, dns)
    counts[key] = counts.get(key,0) + 1


#list.sort() => sort based on the year#; used later to sort our dict
years.sort()
# print counts
# print years



#==========Prepare JavaScript file====================
fhand = open('gline.js','w')
#x-asis
fhand.write("gline = [ ['Year'")
#y-axis
#orgs = list of ['dns1', ...]
for org in orgs:
    fhand.write(",'" + org + "'")
fhand.write("]")

#prep the data for visualisation
for year in years:
    #within each year in rows
    fhand.write(",\n['" + year + "'")

    #within each org in 'cols'
    for org in orgs:
        #key = ('2021-01', 'dns1')
        key = (year, org)
        #retrieve the earlier 'count' from the 'counts' dict
        val = counts.get(key,0)
        fhand.write(","+str(val))
    fhand.write("]");

fhand.write("\n];\n")
fhand.close()

print("Output written to gline.js")
print("Open gline.htm to visualize the data")



'''
E2E run

PS C:\...\Py4e\gmane> python .\gline.py
Loaded messages= 999 senders= 143
Top 10 Organizations
['umich.edu', 'ucdavis.edu', 'berkeley.edu', 'indiana.edu', 'ufp.pt', 'uct.ac.za', 'columbia.edu', 'gmail.com', 'etudes.org', 'mac.com']
Output written to gline.js
Open gline.htm to visualize the data



# gline.js annually
gline = [ ['Year','umich.edu','ucdavis.edu','berkeley.edu','indiana.edu','ufp.pt','uct.ac.za','columbia.edu','gmail.com','etudes.org','mac.com'],
['2005',57,11,12,12,10,14,13,10,5,12],
['2006',117,37,35,34,35,29,29,26,30,19]
];

'''
