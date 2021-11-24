import sqlite3
import time
import zlib

howmany = int(input("How many to dump? "))


conn = sqlite3.connect('index.sqlite')
cur = conn.cursor()

cur.execute('SELECT id, sender FROM Senders')
senders = dict()
for message_row in cur :
    senders[message_row[0]] = message_row[1]


cur.execute('SELECT id, subject FROM Subjects')
subjects = dict()
for message_row in cur :
    subjects[message_row[0]] = message_row[1]


# cur.execute('SELECT id, guid,sender_id,subject_id,headers,body FROM Messages')
cur.execute('SELECT id, guid,sender_id,subject_id,sent_at FROM Messages')
messages = dict()
for message_row in cur :
    messages[message_row[0]] = (message_row[1],message_row[2],message_row[3],message_row[4])

#connected to the DB tables and extracted the records
#record 'id' in each table is the 'key'
#other col values become the record's 'value'
print("Loaded messages=",len(messages),"subjects=",len(subjects),"senders=",len(senders))



sendcounts = dict()
sendorgs = dict()
for (message_id, message) in list(messages.items()):
    #message = guid,sender_id,subject_id,sent_at
    #message[1] = sender_id
    sender = message[1]
    sendcounts[sender] = sendcounts.get(sender,0) + 1
    #senders dictionary {'sender_id': 'senderEmail', ...}
    pieces = senders[sender].split("@")
    #e.g. senders[sender] = abcdef@iupui.edu
    # pieces = ['abcdef', 'iupui.edu']
    if len(pieces) != 2 : continue
    # pieces[1] = iupui.edu
    dns = pieces[1]
    sendorgs[dns] = sendorgs.get(dns,0) + 1




print('')
print('Top',howmany,'Email list participants')

#sendcounts dictionary
#https://stackoverflow.com/questions/39496096/understanding-dictionary-get-in-python
#key = sendcounts.get => i.e. sort the values in the dictionary
#reverse=True => in descending order
x = sorted(sendcounts, key=sendcounts.get, reverse=True)
#'x' is now a sorted list of 'keys', from the highest to the lowest corresponding dict value
for k in x[:howmany]:
    # so use the sender_id to print the senderEmail and sendCount
    print(senders[k], sendcounts[k])
    #the moment the printed count above is <10, break
    if sendcounts[k] < 10 : break

# print('x')
# print(x)
# print('sendcounts')
# print(sendcounts)








print('')
print('Top',howmany,'Email list organizations')

x = sorted(sendorgs, key=sendorgs.get, reverse=True)
for k in x[:howmany]:
    print(k, sendorgs[k])
    #the moment the printed count above is <10, break
    if sendorgs[k] < 10 : break




'''
# Previous understanding that sendcounts is a dictionary; 
# before understanding that by running 'sorted' on the dictionary and specifying the dictionary keys => we would get a list of the 'sorted ids' based on the ascending/descending order

sendcounts = {'abc': 'abcdef', 'dee': 'defg', 'ghi': 'ghss'}
print(sendcounts[:2])

Traceback (most recent call last):
  File "<string>", line 2, in <module>
TypeError: unhashable type: 'slice'


# print('sendcounts')
# print(sendcounts)
sendcounts
{1: 2, 2: 3, 3: 1, 4: 1, 5: 2, 6: 2, 7: 4, 8: 2, 9: 1, 10: 1, 11: 1, 12: 1, 13: 1, 14: 4, 15: 1, 16: 1, 17: 2, 18: 1, 19: 1, 20: 1, 21: 2, 22: 1, 23: 1, 24: 2, 25: 1, 26: 1, 27: 1, 28: 1, 29: 1, 30: 2, 31: 1, 32: 2, 33: 1}

# print('x')
# print(x)
x
[7, 14, 2, 1, 5, 6, 8, 17, 21, 24, 30, 32, 3, 4, 9, 10, 11, 12, 13, 15, 16, 18, 19, 20, 22, 23, 25, 26, 27, 28, 29, 31, 33]

'''



'''
E2E run

How many to dump? 20
Loaded messages= 350 subjects= 205 senders= 87

Top 20 Email list participants
csev@umich.edu 33
ggolden22@mac.com 15
slt@columbia.edu 13
gwang3@unl.edu 12
swgithen@mtu.edu 11
nuno@ufp.pt 11
dgcotton@ucdavis.edu 10
jleasia@umich.edu 10
marquard@uct.ac.za 10
ys2n@virginia.edu 9

Top 20 Email list organizations
umich.edu 61
ucdavis.edu 17
ufp.pt 16
mac.com 15
berkeley.edu 15
uct.ac.za 14
columbia.edu 13
indiana.edu 13
unl.edu 12
mtu.edu 11
gmail.com 11
virginia.edu 9
'''
