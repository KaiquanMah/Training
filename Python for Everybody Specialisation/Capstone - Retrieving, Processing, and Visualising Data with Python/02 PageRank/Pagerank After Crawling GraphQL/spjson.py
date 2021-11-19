'''
Provided OOTB by the lecture without interpretation
d3.v2.js
force.css
force.html
force.js

The other files were interpreted/annotated and results were output from the .py files
spider.py
spider.sqlite - output
sprank.py
spdump.py
spjson.py
spider.js - output
spreset.py - not used
'''
import sqlite3

conn = sqlite3.connect('spider.sqlite')
cur = conn.cursor()

print("Creating JSON output on spider.js...")
howmany = int(input("How many nodes? "))

#addition relative to spdump.py
#WHERE 'AND ERROR IS NULL'
#ORDER BY 'id' also; no longer by inbound DESC
cur.execute('''SELECT COUNT(from_id) AS inbound, old_rank, new_rank, id, url
    FROM Pages JOIN Links ON Pages.id = Links.to_id
    WHERE html IS NOT NULL AND ERROR IS NULL
    GROUP BY id ORDER BY id,inbound''')





#create a javascript file handle
fhand = open('spider.js','w')
nodes = list()
maxrank = None
minrank = None
for row in cur :
    nodes.append(row)
    #rank = the 'new_rank'
    rank = row[2]
    if ((maxrank is None) or (maxrank < rank)): maxrank = rank
    if ((minrank is None) or (minrank > rank)): minrank = rank
    if len(nodes) > howmany : break

if ((maxrank == minrank) or (maxrank is None) or (minrank is None)):
    print("Error - please run sprank.py to compute page rank")
    quit()




#nodes - nodeWeight, rank, id, url
fhand.write('spiderJson = {"nodes":[\n')
count = 0
map = dict()
ranks = dict()
for row in nodes :
    if count > 0 : fhand.write(',\n')
    # print row
    rank = row[2]
    #normalise the rank
    #by taking the 'rank difference' over the 'rank range'
    #why multiply by arbitrary number '19'?
    #use the 'normalised rank' as the weight/size of the 'node ball'
    rank = 19 * ( (rank - minrank) / (maxrank - minrank) )
    #recall <inbound, old_rank, new_rank, id, url> from the initial 'SELECT' statement
    #weight = row[0] = count of inbound links => how big the little circle is
    #rank = row[2] = new_rank
    #id = row[3]
    #url = row[4]
    fhand.write('{'+'"weight":'+str(row[0])+',"rank":'+str(rank)+',')
    fhand.write(' "id":'+str(row[3])+', "url":"'+row[4]+'"}')
    #count => the node # in the 'map'
    map[row[3]] = count
    ranks[row[3]] = rank
    count = count + 1
fhand.write('],\n')




#links - <from_id, to_id, thickness of the line>
cur.execute('SELECT DISTINCT from_id, to_id FROM Links')
fhand.write('"links":[\n')

count = 0
for row in cur :
    #source = row[0] = from_id
    #target = row[1] = to_id
    # print row
    # so only show on the map if the 'from_id' and 'to_id' are BOTH found in the 'map' variable
    if row[0] not in map or row[1] not in map : continue
    if count > 0 : fhand.write(',\n')
    #rank[row[0]] => rank at the 'to_id'
    rank = ranks[row[0]]
    srank = 19 * ( (rank - minrank) / (maxrank - minrank) )
    fhand.write('{"source":'+str(map[row[0]])+',"target":'+str(map[row[1]])+',"value":3}')
    count = count + 1
fhand.write(']};')
fhand.close()
cur.close()

print("Open force.html in a browser to view the visualization")





'''
Visualise Outputs

print(nodes)
/[(1, 1.0421052631578942, 0.01580406503022213, 1, 'http://dr-chuck.com'), (1, 0.2421052631578943, 0.009152115236365346, 9, 'http://dr-chuck.com/dr-chuck/resume/index.htm'), (6, 0.5944862155388466, 0.0114942624460394, 11, 'https://www.coursera.org/instructor/drchuck'), (1, 0.2421052631578943, 0.009152115236365346, 12, 'http://afs.dr-chuck.com/papers'), (1, 0.2421052631578943, 0.009152115236365346, 16, 'https://www.youtube.com/user/csev'), (1, 0.2421052631578943, 0.009152115236365346, 25, 'https://www.sakaiproject.org'), (4, 3.0421052631578944, 3.6287280067837773, 47, 'https://www.sakailms.org/sakai-news'), (41, 2.900082313627206, 5.240727888148923, 67, 'https://www.coursera.org'), (2, 0.0947368421052627, 0.0063850487790983205, 85, 'https://www.coursera.org/learn/intermediate-postgresql'), (2, 0.0947368421052627, 0.0063850487790983205, 91, 'https://www.coursera.org/learn/python-network-data-ru'), (2, 0.0947368421052627, 0.0063850487790983205, 98, 'https://www.coursera.org/learn/python-network-data-es'), (2, 0.0947368421052627, 0.0063850487790983205, 102, 'https://www.coursera.org/learn/introcss'), (11, 0.7496244381693293, 1.5806321248303277, 123, 'https://www.coursera.org/browse/information-technology'), (10, 0.6685346945795858, 1.2324524475794438, 126, 'https://www.coursera.org/browse/personal-development'), (37, 2.5629028264477185, 4.746215206962574, 138, 'https://www.coursera.org/professional-certificates/ibm-data-engineer'), (41, 2.900082313627206, 5.240727888148923, 140, 'https://www.coursera.org/professional-certificates/facebook-social-media-marketing'), (41, 2.8898259033707956, 5.190854517613607, 143, 'https://www.coursera.org/professional-certificates/salesforce-sales-operations'), (41, 2.895320408865301, 5.217453854552131, 162, 'https://www.coursera.org/courses?query=english%20speaking'), (41, 2.900082313627206, 5.240727888148923, 164, 'https://www.coursera.org/courses?query=full%20stack%20web%20development'), (41, 2.9042489802938727, 5.261263497195856, 174, 'https://www.coursera.org/collections/marketing-skills'), (59, 4.605223006267897, 4.870635211990323, 186, 'https://www.coursera.org/articles/web-developer'), (66, 5.265479416524305, 5.317862831712241, 195, 'https://www.coursera.org/degrees/data-analytics'), (66, 5.2590691601140485, 5.286376799848499, 197, 'https://www.coursera.org/degrees/social-sciences'), (66, 5.265479416524305, 5.317862831712241, 205, 'https://www.coursera.org/articles/how-long-does-a-masters-degree-take'), (49, 3.9727013612462536, 5.379773808584641, 228, 'https://www.coursera.org/about/privacy'), (66, 5.2590691601140485, 5.286376799848498, 232, 'https://www.coursera.org/articles')]

print(fhand)
<_io.TextIOWrapper name='spider.js' mode='w' encoding='cp1252'>



#at the end of the code
with open('spider.js','r') as jsFile:
    lines = jsFile.readlines()
    print(lines)

['spiderJson = {"nodes":[\n', '{"weight":1,"rank":0.033305110940424265, "id":1, "url":"http://dr-chuck.com"},\n', '{"weight":1,"rank":0.009784191138624426, "id":9, "url":"http://dr-chuck.com/dr-chuck/resume/index.htm"},\n', '{"weight":6,"rank":0.0180658917512221, "id":11, "url":"https://www.coursera.org/instructor/drchuck"},\n', '{"weight":1,"rank":0.009784191138624426, "id":12, "url":"http://afs.dr-chuck.com/papers"},\n', '{"weight":1,"rank":0.009784191138624426, "id":16, "url":"https://www.youtube.com/user/csev"},\n', '{"weight":1,"rank":0.009784191138624426, "id":25, "url":"https://www.sakaiproject.org"},\n', '{"weight":4,"rank":12.808400672014578, "id":47, "url":"https://www.sakailms.org/sakai-news"},\n', '{"weight":41,"rank":18.50834145706326, "id":67, "url":"https://www.coursera.org"},\n', '{"weight":2,"rank":0.0, "id":85, "url":"https://www.coursera.org/learn/intermediate-postgresql"},\n', '{"weight":2,"rank":0.0, "id":91, "url":"https://www.coursera.org/learn/python-network-data-ru"},\n', '{"weight":2,"rank":0.0, "id":98, "url":"https://www.coursera.org/learn/python-network-data-es"},\n', '{"weight":2,"rank":0.0, "id":102, "url":"https://www.coursera.org/learn/introcss"},\n', '{"weight":11,"rank":5.566448991875248, "id":123, "url":"https://www.coursera.org/browse/information-technology"},\n', '{"weight":10,"rank":4.335305264242521, "id":126, "url":"https://www.coursera.org/browse/personal-development"},\n', '{"weight":37,"rank":16.7597724696817, "id":138, "url":"https://www.coursera.org/professional-certificates/ibm-data-engineer"},\n', '{"weight":41,"rank":18.50834145706326, "id":140, "url":"https://www.coursera.org/professional-certificates/facebook-social-media-marketing"},\n', '{"weight":41,"rank":18.331992027954527, "id":143, "url":"https://www.coursera.org/professional-certificates/salesforce-sales-operations"},\n', '{"weight":41,"rank":18.426045785168668, "id":162, "url":"https://www.coursera.org/courses?query=english%20speaking"},\n', '{"weight":41,"rank":18.50834145706326, "id":164, "url":"https://www.coursera.org/courses?query=full%20stack%20web%20development"},\n', '{"weight":41,"rank":18.580954213990573, "id":174, "url":"https://www.coursera.org/collections/marketing-skills"},\n', '{"weight":59,"rank":17.199714599536602, "id":186, "url":"https://www.coursera.org/articles/web-developer"},\n', '{"weight":66,"rank":18.781086272898264, "id":195, "url":"https://www.coursera.org/degrees/data-analytics"},\n', '{"weight":66,"rank":18.669753437670327, "id":197, "url":"https://www.coursera.org/degrees/social-sciences"},\n', '{"weight":66,"rank":18.781086272898264, "id":205, "url":"https://www.coursera.org/articles/how-long-does-a-masters-degree-take"},\n', '{"weight":49,"rank":19.0, "id":228, "url":"https://www.coursera.org/about/privacy"},\n', '{"weight":66,"rank":18.669753437670323, "id":232, "url":"https://www.coursera.org/articles"}],\n', '"links":[\n', '{"source":0,"target":1,"value":3},\n', '{"source":0,"target":2,"value":3},\n', '{"source":0,"target":3,"value":3},\n', '{"source":0,"target":4,"value":3},\n', '{"source":0,"target":5,"value":3},\n', '{"source":1,"target":0,"value":3},\n', '{"source":2,"target":7,"value":3},\n', '{"source":2,"target":8,"value":3},\n', '{"source":2,"target":9,"value":3},\n', '{"source":2,"target":10,"value":3},\n', '{"source":2,"target":11,"value":3},\n', '{"source":2,"target":12,"value":3},\n', '{"source":2,"target":13,"value":3},\n', '{"source":2,"target":14,"value":3},\n', '{"source":2,"target":15,"value":3},\n', '{"source":2,"target":16,"value":3},\n', '{"source":2,"target":17,"value":3},\n', '{"source":2,"target":18,"value":3},\n', '{"source":2,"target":19,"value":3},\n', '{"source":2,"target":20,"value":3},\n', '{"source":2,"target":21,"value":3},\n', '{"source":2,"target":22,"value":3},\n', '{"source":2,"target":23,"value":3},\n', '{"source":2,"target":24,"value":3},\n', '{"source":2,"target":25,"value":3},\n', '{"source":5,"target":6,"value":3},\n', '{"source":6,"target":6,"value":3},\n', '{"source":7,"target":7,"value":3},\n', '{"source":7,"target":12,"value":3},\n', '{"source":7,"target":13,"value":3},\n', '{"source":7,"target":14,"value":3},\n', '{"source":7,"target":15,"value":3},\n', '{"source":7,"target":16,"value":3},\n', '{"source":7,"target":17,"value":3},\n', '{"source":7,"target":18,"value":3},\n', '{"source":7,"target":19,"value":3},\n', '{"source":7,"target":20,"value":3},\n', '{"source":7,"target":21,"value":3},\n', '{"source":7,"target":22,"value":3},\n', '{"source":7,"target":23,"value":3},\n', '{"source":7,"target":24,"value":3},\n', '{"source":7,"target":25,"value":3},\n', '{"source":8,"target":2,"value":3},\n', '{"source":8,"target":7,"value":3},\n', '{"source":8,"target":8,"value":3},\n', '{"source":8,"target":14,"value":3},\n', '{"source":8,"target":15,"value":3},\n', '{"source":8,"target":16,"value":3},\n', '{"source":8,"target":17,"value":3},\n', '{"source":8,"target":18,"value":3},\n', '{"source":8,"target":19,"value":3},\n', '{"source":8,"target":20,"value":3},\n', '{"source":8,"target":21,"value":3},\n', '{"source":8,"target":22,"value":3},\n', '{"source":8,"target":23,"value":3},\n', '{"source":8,"target":24,"value":3},\n', '{"source":8,"target":25,"value":3},\n', '{"source":9,"target":2,"value":3},\n', '{"source":9,"target":7,"value":3},\n', '{"source":9,"target":9,"value":3},\n', '{"source":9,"target":14,"value":3},\n', '{"source":9,"target":15,"value":3},\n', '{"source":9,"target":16,"value":3},\n', '{"source":9,"target":17,"value":3},\n', '{"source":9,"target":18,"value":3},\n', '{"source":9,"target":19,"value":3},\n', '{"source":9,"target":20,"value":3},\n', '{"source":9,"target":21,"value":3},\n', '{"source":9,"target":22,"value":3},\n', '{"source":9,"target":23,"value":3},\n', '{"source":9,"target":24,"value":3},\n', '{"source":9,"target":25,"value":3},\n', '{"source":10,"target":2,"value":3},\n', '{"source":10,"target":7,"value":3},\n', '{"source":10,"target":10,"value":3},\n', '{"source":10,"target":14,"value":3},\n', '{"source":10,"target":15,"value":3},\n', '{"source":10,"target":16,"value":3},\n', '{"source":10,"target":17,"value":3},\n', '{"source":10,"target":18,"value":3},\n', '{"source":10,"target":19,"value":3},\n', '{"source":10,"target":20,"value":3},\n', '{"source":10,"target":21,"value":3},\n', '{"source":10,"target":22,"value":3},\n', '{"source":10,"target":23,"value":3},\n', '{"source":10,"target":24,"value":3},\n', '{"source":10,"target":25,"value":3},\n', '{"source":11,"target":2,"value":3},\n', '{"source":11,"target":7,"value":3},\n', '{"source":11,"target":11,"value":3},\n', '{"source":11,"target":14,"value":3},\n', '{"source":11,"target":15,"value":3},\n', '{"source":11,"target":16,"value":3},\n', '{"source":11,"target":17,"value":3},\n', '{"source":11,"target":18,"value":3},\n', '{"source":11,"target":19,"value":3},\n', '{"source":11,"target":20,"value":3},\n', '{"source":11,"target":21,"value":3},\n', '{"source":11,"target":22,"value":3},\n', '{"source":11,"target":23,"value":3},\n', '{"source":11,"target":24,"value":3},\n', '{"source":11,"target":25,"value":3},\n', '{"source":12,"target":7,"value":3},\n', '{"source":12,"target":13,"value":3},\n', '{"source":12,"target":14,"value":3},\n', '{"source":12,"target":15,"value":3},\n', '{"source":12,"target":16,"value":3},\n', '{"source":12,"target":17,"value":3},\n', '{"source":12,"target":18,"value":3},\n', '{"source":12,"target":19,"value":3},\n', '{"source":12,"target":20,"value":3},\n', '{"source":12,"target":21,"value":3},\n', '{"source":12,"target":22,"value":3},\n', '{"source":12,"target":23,"value":3},\n', '{"source":12,"target":24,"value":3},\n', '{"source":12,"target":25,"value":3},\n', '{"source":13,"target":7,"value":3},\n', '{"source":13,"target":12,"value":3},\n', '{"source":13,"target":14,"value":3},\n', '{"source":13,"target":15,"value":3},\n', '{"source":13,"target":16,"value":3},\n', '{"source":13,"target":17,"value":3},\n', '{"source":13,"target":18,"value":3},\n', '{"source":13,"target":19,"value":3},\n', '{"source":13,"target":20,"value":3},\n', '{"source":13,"target":21,"value":3},\n', '{"source":13,"target":22,"value":3},\n', '{"source":13,"target":23,"value":3},\n', '{"source":13,"target":24,"value":3},\n', '{"source":13,"target":25,"value":3},\n', '{"source":14,"target":7,"value":3},\n', '{"source":14,"target":12,"value":3},\n', '{"source":14,"target":14,"value":3},\n', '{"source":14,"target":15,"value":3},\n', '{"source":14,"target":16,"value":3},\n', '{"source":14,"target":17,"value":3},\n', '{"source":14,"target":18,"value":3},\n', '{"source":14,"target":19,"value":3},\n', '{"source":14,"target":20,"value":3},\n', '{"source":14,"target":21,"value":3},\n', '{"source":14,"target":22,"value":3},\n', '{"source":14,"target":23,"value":3},\n', '{"source":14,"target":24,"value":3},\n', '{"source":14,"target":25,"value":3},\n', '{"source":15,"target":7,"value":3},\n', '{"source":15,"target":14,"value":3},\n', '{"source":15,"target":15,"value":3},\n', '{"source":15,"target":16,"value":3},\n', '{"source":15,"target":17,"value":3},\n', '{"source":15,"target":18,"value":3},\n', '{"source":15,"target":19,"value":3},\n', '{"source":15,"target":20,"value":3},\n', '{"source":15,"target":21,"value":3},\n', '{"source":15,"target":22,"value":3},\n', '{"source":15,"target":23,"value":3},\n', '{"source":15,"target":24,"value":3},\n', '{"source":15,"target":25,"value":3},\n', '{"source":16,"target":7,"value":3},\n', '{"source":16,"target":14,"value":3},\n', '{"source":16,"target":15,"value":3},\n', '{"source":16,"target":16,"value":3},\n', '{"source":16,"target":17,"value":3},\n', '{"source":16,"target":18,"value":3},\n', '{"source":16,"target":19,"value":3},\n', '{"source":16,"target":20,"value":3},\n', '{"source":16,"target":21,"value":3},\n', '{"source":16,"target":22,"value":3},\n', '{"source":16,"target":23,"value":3},\n', '{"source":16,"target":24,"value":3},\n', '{"source":16,"target":25,"value":3},\n', '{"source":17,"target":7,"value":3},\n', '{"source":17,"target":12,"value":3},\n', '{"source":17,"target":13,"value":3},\n', '{"source":17,"target":14,"value":3},\n', '{"source":17,"target":15,"value":3},\n', '{"source":17,"target":16,"value":3},\n', '{"source":17,"target":17,"value":3},\n', '{"source":17,"target":18,"value":3},\n', '{"source":17,"target":19,"value":3},\n', '{"source":17,"target":20,"value":3},\n', '{"source":17,"target":21,"value":3},\n', '{"source":17,"target":22,"value":3},\n', '{"source":17,"target":23,"value":3},\n', '{"source":17,"target":24,"value":3},\n', '{"source":17,"target":25,"value":3},\n', '{"source":18,"target":7,"value":3},\n', '{"source":18,"target":12,"value":3},\n', '{"source":18,"target":13,"value":3},\n', '{"source":18,"target":14,"value":3},\n', '{"source":18,"target":15,"value":3},\n', '{"source":18,"target":16,"value":3},\n', '{"source":18,"target":17,"value":3},\n', '{"source":18,"target":18,"value":3},\n', '{"source":18,"target":19,"value":3},\n', '{"source":18,"target":20,"value":3},\n', '{"source":18,"target":21,"value":3},\n', '{"source":18,"target":22,"value":3},\n', '{"source":18,"target":23,"value":3},\n', '{"source":18,"target":24,"value":3},\n', '{"source":18,"target":25,"value":3},\n', '{"source":19,"target":7,"value":3},\n', '{"source":19,"target":14,"value":3},\n', '{"source":19,"target":15,"value":3},\n', '{"source":19,"target":16,"value":3},\n', '{"source":19,"target":17,"value":3},\n', '{"source":19,"target":18,"value":3},\n', '{"source":19,"target":19,"value":3},\n', '{"source":19,"target":20,"value":3},\n', '{"source":19,"target":21,"value":3},\n', '{"source":19,"target":22,"value":3},\n', '{"source":19,"target":23,"value":3},\n', '{"source":19,"target":24,"value":3},\n', '{"source":19,"target":25,"value":3},\n', '{"source":20,"target":7,"value":3},\n', '{"source":20,"target":14,"value":3},\n', '{"source":20,"target":15,"value":3},\n', '{"source":20,"target":16,"value":3},\n', '{"source":20,"target":17,"value":3},\n', '{"source":20,"target":18,"value":3},\n', '{"source":20,"target":19,"value":3},\n', '{"source":20,"target":20,"value":3},\n', '{"source":20,"target":21,"value":3},\n', '{"source":20,"target":22,"value":3},\n', '{"source":20,"target":23,"value":3},\n', '{"source":20,"target":24,"value":3},\n', '{"source":20,"target":25,"value":3},\n', '{"source":21,"target":7,"value":3},\n', '{"source":21,"target":14,"value":3},\n', '{"source":21,"target":15,"value":3},\n', '{"source":21,"target":16,"value":3},\n', '{"source":21,"target":17,"value":3},\n', '{"source":21,"target":18,"value":3},\n', '{"source":21,"target":19,"value":3},\n', '{"source":21,"target":20,"value":3},\n', '{"source":21,"target":21,"value":3},\n', '{"source":21,"target":22,"value":3},\n', '{"source":21,"target":23,"value":3},\n', '{"source":21,"target":24,"value":3},\n', '{"source":21,"target":25,"value":3},\n', '{"source":22,"target":7,"value":3},\n', '{"source":22,"target":14,"value":3},\n', '{"source":22,"target":15,"value":3},\n', '{"source":22,"target":16,"value":3},\n', '{"source":22,"target":17,"value":3},\n', '{"source":22,"target":18,"value":3},\n', '{"source":22,"target":19,"value":3},\n', '{"source":22,"target":20,"value":3},\n', '{"source":22,"target":21,"value":3},\n', '{"source":22,"target":22,"value":3},\n', '{"source":22,"target":23,"value":3},\n', '{"source":22,"target":24,"value":3},\n', '{"source":22,"target":25,"value":3},\n', '{"source":23,"target":7,"value":3},\n', '{"source":23,"target":14,"value":3},\n', '{"source":23,"target":15,"value":3},\n', '{"source":23,"target":16,"value":3},\n', '{"source":23,"target":17,"value":3},\n', '{"source":23,"target":18,"value":3},\n', '{"source":23,"target":19,"value":3},\n', '{"source":23,"target":20,"value":3},\n', '{"source":23,"target":21,"value":3},\n', '{"source":23,"target":22,"value":3},\n', '{"source":23,"target":23,"value":3},\n', '{"source":23,"target":24,"value":3},\n', '{"source":23,"target":25,"value":3},\n', '{"source":24,"target":7,"value":3},\n', '{"source":24,"target":15,"value":3},\n', '{"source":24,"target":16,"value":3},\n', '{"source":24,"target":17,"value":3},\n', '{"source":24,"target":18,"value":3},\n', '{"source":24,"target":19,"value":3},\n', '{"source":24,"target":21,"value":3},\n', '{"source":24,"target":22,"value":3},\n', '{"source":24,"target":23,"value":3},\n', '{"source":24,"target":24,"value":3},\n', '{"source":24,"target":25,"value":3},\n', '{"source":25,"target":7,"value":3},\n', '{"source":25,"target":14,"value":3},\n', '{"source":25,"target":15,"value":3},\n', '{"source":25,"target":16,"value":3},\n', '{"source":25,"target":17,"value":3},\n', '{"source":25,"target":18,"value":3},\n', '{"source":25,"target":19,"value":3},\n', '{"source":25,"target":20,"value":3},\n', '{"source":25,"target":21,"value":3},\n', '{"source":25,"target":22,"value":3},\n', '{"source":25,"target":23,"value":3},\n', '{"source":25,"target":24,"value":3},\n', '{"source":25,"target":25,"value":3}]};']
'''
