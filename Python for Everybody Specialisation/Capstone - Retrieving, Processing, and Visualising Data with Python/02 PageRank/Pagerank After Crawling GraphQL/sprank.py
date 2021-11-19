import sqlite3

conn = sqlite3.connect('spider.sqlite')
cur = conn.cursor()

#=================get 'from_ids'=======================
# Find the ids that send out page rank - we only are interested
# in pages in the SCC that have in and out links
cur.execute('''SELECT DISTINCT from_id FROM Links''')
from_ids = list()
for row in cur:
    from_ids.append(row[0])



#===========get 'links', NEW 'to_ids' in 'from_ids'==========
# Find the ids that receive page rank
to_ids = list()
links = list()
cur.execute('''SELECT DISTINCT from_id, to_id FROM Links''')
for row in cur:
    from_id = row[0]
    to_id = row[1]
    #we dont want the 'from page' to link back to itself as the 'to page'
    if from_id == to_id : continue
    #note the 'not in'; not sure when the following line would occur
    #i.e. DONT WANT from_id we have look at before?
    if from_id not in from_ids : continue
    #i.e. DONT WANT links that point to nowhere OR pages we havent retrieved yet (i.e. 'to' is not in 'from')
    if to_id not in from_ids : continue
    #List of links that point to another page (i.e. a to_id) we already retrieved (i.e. in the from_id)
    links.append(row)
    #List of NEW 'to_ids'
    #use lists and not hit the DB
    if to_id not in to_ids : to_ids.append(to_id)





#====Get existing 'new_rank' for each from_id => i.e. get our new 'prev_ranks'=========
# Get latest page ranks for strongly connected component (graph theory)
# every web page will be linked eventually
prev_ranks = dict()
for node in from_ids:
    cur.execute('SELECT new_rank FROM Pages WHERE id = ?', (node, ))
    row = cur.fetchone()
    prev_ranks[node] = row[0]

sval = input('How many iterations:')
#instantiate 'many' in case user input a 'sval' value <=0
many = 1
if ( len(sval) > 0 ) : many = int(sval)

# Sanity check
if len(prev_ranks) < 1 :
    print("Nothing to page rank.  Check data.")
    quit()




# Lets do Page Rank in memory so it is really fast
for i in range(many):
    # print prev_ranks.items()[:5]
    next_ranks = dict();
    total = 0.0

    #========1st SET OF 'next_ranks'========
    #instantiate the new 'next_ranks'
    for (node, old_rank) in list(prev_ranks.items()):
        total = total + old_rank
        next_ranks[node] = 0.0
    # print total


    # Find the number of outbound links and sent the page rank down each
    for (node, old_rank) in list(prev_ranks.items()):
        # print node, old_rank
        give_ids = list()
        for (from_id, to_id) in links:
            if from_id != node : continue
           #  print '   ',from_id,to_id

            if to_id not in to_ids: continue
            #so 'give_ids' contain the 'to_ids' we found, linked from the 'from_id'
            give_ids.append(to_id)
        if ( len(give_ids) < 1 ) : continue
        #and amount divides the old_rank by the number of 'to_ids' linked. WHY?
        #======================question on amount and total======================
        # give out a fractional amount of the 'from_id' node's current rank
        # to the 'to_ids'
        amount = old_rank / len(give_ids)
        # print node, old_rank,amount, give_ids


        #========2nd SET OF 'next_ranks' receiving fractional amount from 'from_id' current rank========
        #still within the same 'from_id'
        #next rank of these 'to_ids'
        for id in give_ids:
            next_ranks[id] = next_ranks[id] + amount



    # there are dysfunctional shapes where pagerank can be trapped
    # evaporation => takes a fraction from everyone, give it away to everybody else
    # so calculate the evap = total-newtotal
    newtot = 0
    for (node, next_rank) in list(next_ranks.items()):
        newtot = newtot + next_rank
    evap = (total - newtot) / len(next_ranks)

    #========3rd SET OF 'next_ranks' after adjusting for 'evap'========
    #adjust each next_rank by 'evap'
    # print newtot, evap
    for node in next_ranks:
        next_ranks[node] = next_ranks[node] + evap

    #calculate newtotal again => for what purpose?
    # we are not using 'newtotal' below
    # we are also instantiating 'newtotal' as 0 again above
    newtot = 0
    for (node, next_rank) in list(next_ranks.items()):
        newtot = newtot + next_rank


    # Compute the per-page average change from old rank to new rank
    # As indication of convergence/stability (i.e. changes/differences reduce over time) of the algorithm
    totdiff = 0
    for (node, old_rank) in list(prev_ranks.items()):
        new_rank = next_ranks[node]
        diff = abs(old_rank-new_rank)
        totdiff = totdiff + diff

    avediff = totdiff / len(prev_ranks)
    print(i+1, avediff)


    # rotate
    #continue in-memory calculations
    prev_ranks = next_ranks




#at the very end
# Put the final ranks back into the database
print(list(next_ranks.items())[:5])
#move the existing DB-level new_rank into the old_rank column
cur.execute('UPDATE Pages SET old_rank=new_rank')
#then insert our pagerank new_rank recomputation results into the DB
for (id, new_rank) in list(next_ranks.items()) :
    cur.execute('UPDATE Pages SET new_rank=? WHERE id=?', (new_rank, id))
conn.commit()
cur.close()


#low rank #s indicate those 'from_id' webpages point to somewhere
#but others dont point to them
#if these 'from_ids' care about people but people dont care about them, it is very sad!





'''
Visualise Outputs


Sprank.py on parity
# ==============E2E run of sprank.py========================
PS C:\...\Py4e> python .\sprank.py

#sval = input('How many iterations:')
How many iterations:10

# print(i+1, avediff)
#iteration #, average difference
1 0.0
2 0.0
3 0.0
4 0.0
5 0.0
6 0.0
7 0.0
8 0.0
9 0.0
10 0.0

#print(list(next_ranks.items())[:5])
[(1, 1.0), (2, 1.0), (3, 1.0), (4, 1.0), (5, 1.0)]
'''


'''
Sprank on GraphQL
#sval = input('How many iterations:')
How many iterations:10


# print(i+1, avediff)
#iteration #, average difference
1 0.6684823296740321
2 0.19797643024892284
3 0.10709283825765314
4 0.06071412774277475
5 0.035086020233825156
6 0.02063411413936657
7 0.012324382031826377
8 0.007463201972566078
9 0.004574984698928134
10 0.002837482534022427

#print(list(next_ranks.items())[:5])
[(2, 3.9070004012785313), (3, 4.018487891523265), (4, 3.924421117181356), (5, 3.924421117181356), (6, 4.018487891523265)]
'''
