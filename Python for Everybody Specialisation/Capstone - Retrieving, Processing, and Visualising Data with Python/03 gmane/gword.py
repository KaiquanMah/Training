import sqlite3
import time
import zlib
import string

conn = sqlite3.connect('index.sqlite')
cur = conn.cursor()

cur.execute('SELECT id, subject FROM Subjects')
subjects = dict()
for message_row in cur :
    # {'subject_id' : 'subject string...'}
    subjects[message_row[0]] = message_row[1]


#=============Prepare 'emailSubject' words and word counts=================
# cur.execute('SELECT id, guid,sender_id,subject_id,headers,body FROM Messages')
cur.execute('SELECT subject_id FROM Messages')
counts = dict()
for message_row in cur :
    # [message_row[0] = 'subject_id'
    # subjects[message_row[0]] = 'subject string...'
    text = subjects[message_row[0]]

    #https://www.programiz.com/python-programming/methods/string/translate
    #translate => single input param 'table' => a translation table containing the mapping between two characters; usually created by maketrans()
    #so maketrans is mapping NULL to NULL (1st and 2nd 'string arguments'); and removing punctiations (3rd 'string argument')
    #therefore this essentially just removes punctuation
    text = text.translate(str.maketrans('','',string.punctuation))
    #remove numbers
    text = text.translate(str.maketrans('','','1234567890'))
    text = text.strip()
    text = text.lower()
    #split on spaces
    words = text.split()
    for word in words:
        if len(word) < 4 : continue
        counts[word] = counts.get(word,0) + 1


#=============Normalise word counts=================
# counts = {'word': #, ...}
#sort by descending wordCount
#then return a LIST of the sorted words
x = sorted(counts, key=counts.get, reverse=True)
highest = None
lowest = None
for k in x[:100]:
    #by right this 'highest' if-statement executes only once
    #since our 'counts' are already sorted in descending order
    if highest is None or highest < counts[k] :
        highest = counts[k]
    #this 'lowest' if-statement executes until we finish iterating over the 'counts' dictionary
    if lowest is None or lowest > counts[k] :
        lowest = counts[k]
print('Range of counts:',highest,lowest)

# Spread the font sizes across 20-100 based on the count
bigsize = 80
smallsize = 20



#==========Prepare JavaScript file====================
fhand = open('gword.js','w')
fhand.write("gword = [")
first = True
for k in x[:100]:
    # if not 'True' => if 'False' => execute
    #so during the 1st 'for loop' iteration => first=True => NOT FALSE => so dont execute
    #during subsequent iterations, first=False => FALSE => so execute
    # so the 'if not first' statement recognises the 'first' TRUE/FALSE assignment as its base logic to evaluate against
    if not first : fhand.write( ",\n")
    first = False
    size = counts[k]
    #normalise the count based on the max-min range
    size = (size - lowest) / float(highest - lowest)
    size = int((size * bigsize) + smallsize)
    #{text: 'word',
    # size: 56.15}
    fhand.write("{text: '" + k + "', size: " + str(size) + "}")
fhand.write( "\n];\n")
fhand.close()

print("Output written to gword.js")
print("Open gword.htm in a browser to see the vizualization")












'''
# https://www.programiz.com/python-programming/methods/string/maketrans
#maketrans

#Example 1 - use dictionary => 'alphabetical character' map to 'integer'
# example dictionary
dict = {"a": "123", "b": "456", "c": "789"}
string = "abc"
print(string.maketrans(dict))
{97: '123', 98: '456', 99: '789'}


#Example 2 - 2 input strings of EQUAL LENGTH => 'string 1 character 1 unicode' map to 'string 2 character 1 unicode', ... and so on...
firstString = "abc"
secondString = "def"
string = "abc"
print(string.maketrans(firstString, secondString))
{97: 100, 98: 101, 99: 102}


#Example 3 - Use 'translational table' created by maketrans()
firstString = "abc"
secondString = "def"
thirdString = "abd"
string = "abc"
print(string.maketrans(firstString, secondString, thirdString))
#step 1 - find character from first string in third string => a is found, so 'None'; b is found, so None; c is not found, so remain as c; d is not in the first string, but in the third string, so add 'd' but keep as None
#step 2 - then map to second string => a->d (but above was 'None'), b->e (but above was 'None'), c->f (mapped); d (newly added from third string)->None

#97a, 98b, 99c, 100d
{97: None, 98: None, 99: 102, 100: None}







#https://www.programiz.com/python-programming/methods/string/translate
#translate
# first string
firstString = "abc"
secondString = "ghi"
thirdString = "ab"

string = "abcdef"
print("Original string:", string)
Original string: abcdef


translation = string.maketrans(firstString, secondString, thirdString)
#within maketrans
#step 1 - find char from first string in third string - a->None, b->None, c->remain as c
#step 2 - a->remain None, b->remain None, c->i; no extra additional characters from third string
#then apply to the <string>
#step 3 - 'abcdef' => None None i d e f -> idef

# translate string
print("Translated string:", string.translate(translation))
Translated string: idef






#https://www.geeksforgeeks.org/string-punctuation-in-python/
#string.punctuation
#string.punctuation is a pre-initialized string used as string constant
#containing a set of punctuation
# !"#$%&'()*+, -./:;<=>?@[\]^_`{|}~
'''





'''
E2E run

PS C:\...\Py4e\gmane> python .\gword.py
Range of counts: 127 4
Output written to gword.js
Open gword.htm in a browser to see the vizualization






# gword.js
gword = [{text: 'sakai', size: 100},
{text: 'with', size: 41},
{text: 'error', size: 37},
{text: 'problem', size: 31},
{text: 'password', size: 29},
{text: 'forgotten', size: 29},
{text: 'feature', size: 29},
{text: 'message', size: 29},
{text: 'tool', size: 28},
{text: 'mysql', size: 26},
{text: 'resources', size: 26},
{text: 'site', size: 25},
{text: 'version', size: 25},
{text: 'desktop', size: 25},
{text: 'samigo', size: 25},
{text: 'update', size: 25},
{text: 'webdav', size: 25},
{text: 'maven', size: 25},
{text: 'center', size: 25},
{text: 'portal', size: 25},
{text: 'visual', size: 25},
{text: 'basic', size: 25},
{text: 'course', size: 25},
{text: 'oracle', size: 24},
{text: 'file', size: 23},
{text: 'apis', size: 23},
{text: 'creating', size: 23},
{text: 'profile', size: 23},
{text: 'collab', size: 22},
{text: 'section', size: 22},
{text: 'sakaiperson', size: 22},
{text: 'different', size: 22},
{text: 'documentation', size: 21},
{text: 'memory', size: 21},
{text: 'cannot', size: 21},
{text: 'again', size: 21},
{text: 'assigning', size: 21},
{text: 'workspace', size: 21},
{text: 'quota', size: 21},
{text: 'forums', size: 21},
{text: 'status', size: 21},
{text: 'austin', size: 21},
{text: 'worksite', size: 21},
{text: 'taxonomy', size: 21},
{text: 'email', size: 21},
{text: 'import', size: 21},
{text: 'eclipse', size: 21},
{text: 'system', size: 21},
{text: 'sakaiscript', size: 21},
{text: 'services', size: 21},
{text: 'delegates', size: 21},
{text: 'sakais', size: 21},
{text: 'melete', size: 21},
{text: 'provider', size: 20},
{text: 'schedule', size: 20},
{text: 'high', size: 20},
{text: 'level', size: 20},
{text: 'sectionmanager', size: 20},
{text: 'nosuchbeandefinitionexception', size: 20},
{text: 'address', size: 20},
{text: 'username', size: 20},
{text: 'question', size: 20},
{text: 'dynamic', size: 20},
{text: 'language', size: 20},
{text: 'preferences', size: 20},
{text: 'test', size: 20},
{text: 'project', size: 20},
{text: 'default', size: 20},
{text: 'template', size: 20},
{text: 'instructor', size: 20},
{text: 'from', size: 20},
{text: 'into', size: 20},
{text: 'sakaiportallogin', size: 20},
{text: 'presense', size: 20},
{text: 'sepp', size: 20},
{text: 'code', size: 20},
{text: 'regarding', size: 20},
{text: 'manager', size: 20},
{text: 'other', size: 20},
{text: 'related', size: 20},
{text: 'development', size: 20},
{text: 'available', size: 20},
{text: 'firefox', size: 20},
{text: 'wiki', size: 20},
{text: 'permission', size: 20},
{text: 'denied', size: 20},
{text: 'requires', size: 20},
{text: 'returns', size: 20},
{text: 'getting', size: 20},
{text: 'started', size: 20},
{text: 'permissionexception', size: 20},
{text: 'when', size: 20},
{text: 'sites', size: 20},
{text: 'scheduler', size: 20},
{text: 'casifying', size: 20},
{text: 'upload', size: 20},
{text: 'files', size: 20},
{text: 'restrict', size: 20},
{text: 'creation', size: 20},
{text: 'manner', size: 20}
];


'''
