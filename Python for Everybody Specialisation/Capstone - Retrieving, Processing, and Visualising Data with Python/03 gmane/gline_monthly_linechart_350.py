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




#===========Count of (emails from each) DNS by month=================
counts = dict()
months = list()
# cur.execute('SELECT id, guid,sender_id,subject_id,sent_at FROM Messages')
for (message_id, message) in list(messages.items()):
    sender = message[1]
    pieces = senders[sender].split("@")
    if len(pieces) != 2 : continue
    dns = pieces[1]
    if dns not in orgs : continue

    # message[3] = sent_at
    month = message[3][:7]
    if month not in months : months.append(month)
    #key = (01, 'dns1') => used for viz later when retrieving the specific count combo for a particular month and dns
    key = (month, dns)
    counts[key] = counts.get(key,0) + 1


#list.sort() => sort based on the month#; used later to sort our dict
months.sort()
# print counts
# print months



#==========Prepare JavaScript file====================
fhand = open('gline.js','w')
#write the column headers
#x-axis
fhand.write("gline = [ ['Month'")
#y-axis
#orgs = list of ['dns1', ...]
for org in orgs:
    fhand.write(",'" + org + "'")
fhand.write("]")


#write the data values in the rows
#prep the data for visualisation
for month in months:
    fhand.write(",\n['" + month + "'")
    for org in orgs:
        #key = (01, 'dns1')
        key = (month, org)
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
Loaded messages= 350 senders= 87
Top 10 Organizations
['umich.edu', 'ucdavis.edu', 'ufp.pt', 'mac.com', 'berkeley.edu', 'uct.ac.za', 'columbia.edu', 'indiana.edu', 'unl.edu', 'mtu.edu']
Output written to gline.js
Open gline.htm to visualize the data



#from gline_monthly_linechart.py => get gline.js
gline = [ ['Month','umich.edu','ucdavis.edu','ufp.pt','mac.com','berkeley.edu','uct.ac.za','columbia.edu','indiana.edu','unl.edu','mtu.edu'],
['2005-12',57,11,10,12,12,14,13,12,12,11],
['2006-01',4,6,6,3,3,0,0,1,0,0]
];


'''
