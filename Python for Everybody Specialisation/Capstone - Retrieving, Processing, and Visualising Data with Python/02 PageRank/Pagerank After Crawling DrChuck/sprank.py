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
prev_ranks
print(from_ids)
[1, 9, 11, 12, 16, 25, 47, 67, 85, 91, 98, 102, 123, 126, 138, 140, 143, 162, 164, 174, 186, 195, 197, 205, 228, 232, 242, 254, 257, 263, 268, 316, 322, 323, 329, 350, 363, 376, 378, 382, 388, 402, 406, 412, 437, 453, 455, 467, 489, 494, 513, 536, 557, 568, 571, 572, 614, 623, 643, 680, 690, 696, 709, 722, 728, 757, 759, 775, 867, 869, 889, 909, 942, 973, 1013, 1040, 1065, 1070, 1078, 1124, 1157, 1159, 1170, 1210, 1358, 1362, 1376, 1444, 1465, 1551, 1580, 1646, 1716, 1864, 1915]

print(to_ids)
[9, 11, 12, 16, 25, 1, 67, 85, 91, 98, 102, 123, 126, 138, 140, 143, 162, 164, 174, 186, 195, 197, 205, 228, 232, 680, 690, 47, 614, 623, 1376, 467, 1444, 1716, 316, 322, 323, 513, 942, 254, 257, 263, 268, 242, 889, 329, 350, 363, 376, 378, 382, 388, 402, 406, 453, 455, 412, 437, 536, 557, 568, 571, 572, 1915, 494, 489, 1580, 696, 1551, 643, 757, 759, 1040, 973, 709, 722, 728, 1013, 775, 867, 869, 1646, 909, 1070, 1078, 1124, 1157, 1159, 1170, 1210, 1358, 1362, 1065, 1465, 1864]

print(links)
[(1, 9), (1, 11), (1, 12), (1, 16), (1, 25), (9, 1), (11, 67), (11, 85), ..., (1915, 376), (1915, 378), (1915, 382), (1915, 388), (1915, 402), (1915, 406)]

print(many)
<depending on your 'How many iterations:' input> - e.g. 1 or 2, etc

print(prev_ranks)
{1: 1.0, 9: 1.0, 11: 1.0, 12: 1.0, 16: 1.0, 25: 1.0, 47: 1.0, 67: 1.0, 85: 1.0, 91: 1.0, 98: 1.0, 102: 1.0, 123: 1.0, 126: 1.0, 138: 1.0, 140: 1.0, 143: 1.0, 162: 1.0, 164: 1.0, 174: 1.0, 186: 1.0, 195: 1.0, 197: 1.0, 205: 1.0, 228: 1.0, 232: 1.0, 242: 1.0, 254: 1.0, 257: 1.0, 263: 1.0, 268: 1.0, 316: 1.0, 322: 1.0, 323: 1.0, 329: 1.0, 350: 1.0, 363: 1.0, 376: 1.0, 378: 1.0, 382: 1.0, 388: 1.0, 402: 1.0, 406: 1.0, 412: 1.0, 437: 1.0, 453: 1.0, 455: 1.0, 467: 1.0, 489: 1.0, 494: 1.0, 513: 1.0, 536: 1.0, 557: 1.0, 568: 1.0, 571: 1.0, 572: 1.0, 614: 1.0, 623: 1.0, 643: 1.0, 680: 1.0, 690: 1.0, 696: 1.0, 709: 1.0, 722: 1.0, 728: 1.0, 757: 1.0, 759: 1.0, 775: 1.0, 867: 1.0, 869: 1.0, 889: 1.0, 909: 1.0, 942: 1.0, 973: 1.0, 1013: 1.0, 1040: 1.0, 1065: 1.0, 1070: 1.0, 1078: 1.0, 1124: 1.0, 1157: 1.0, 1159: 1.0, 1170: 1.0, 1210: 1.0, 1358: 1.0, 1362: 1.0, 1376: 1.0, 1444: 1.0, 1465: 1.0, 1551: 1.0, 1580: 1.0, 1646: 1.0, 1716: 1.0, 1864: 1.0, 1915: 1.0}

#========1st SET OF 'next_ranks'========
print(next_ranks)
{1: 0.0, 9: 0.0, 11: 0.0, 12: 0.0, 16: 0.0, 25: 0.0, 47: 0.0, 67: 0.0, 85: 0.0, 91: 0.0, 98: 0.0, 102: 0.0, 123: 0.0, 126: 0.0, 138: 0.0, 140: 0.0, 143: 0.0, 162: 0.0, 164: 0.0, 174: 0.0, 186: 0.0, 195: 0.0, 197: 0.0, 205: 0.0, 228: 0.0, 232: 0.0, 242: 0.0, 254: 0.0, 257: 0.0, 263: 0.0, 268: 0.0, 316: 0.0, 322: 0.0, 323: 0.0, 329: 0.0, 350: 0.0, 363: 0.0, 376: 0.0, 378: 0.0, 382: 0.0, 388: 0.0, 402: 0.0, 406: 0.0, 412: 0.0, 437: 0.0, 453: 0.0, 455: 0.0, 467: 0.0, 489: 0.0, 494: 0.0, 513: 0.0, 536: 0.0, 557: 0.0, 568: 0.0, 571: 0.0, 572: 0.0, 614: 0.0, 623: 0.0, 643: 0.0, 680: 0.0, 690: 0.0, 696: 0.0, 709: 0.0, 722: 0.0, 728: 0.0, 757: 0.0, 759: 0.0, 775: 0.0, 867: 0.0, 869: 0.0, 889: 0.0, 909: 0.0, 942: 0.0, 973: 0.0, 1013: 0.0, 1040: 0.0, 1065: 0.0, 1070: 0.0, 1078: 0.0, 1124: 0.0, 1157: 0.0, 1159: 0.0, 1170: 0.0, 1210: 0.0, 1358: 0.0, 1362: 0.0, 1376: 0.0, 1444: 0.0, 1465: 0.0, 1551: 0.0, 1580: 0.0, 1646: 0.0, 1716: 0.0, 1864: 0.0, 1915: 0.0}

print(give_ids)
[228, 376, 378, 382, 388, 402, 406]

print(amount)
0.14285714285714285

print(old_rank)
1.0


#========2nd SET OF 'next_ranks' receiving fractional amount from 'from_id' current rank========
print(next_ranks)
{1: 1.0, 9: 0.2, 11: 0.5523809523809523, 12: 0.2, 16: 0.2, 25: 0.2, 47: 3.0, 67: 2.8579770504693114, 85: 0.05263157894736842, 91: 0.05263157894736842, 98: 0.05263157894736842, 102: 0.05263157894736842, 123: 0.707519175011435, 126: 0.6264294314216915, 138: 2.520797563289824, 140: 2.8579770504693114, 143: 2.847720640212901, 162: 2.8532151457074066, 164: 2.8579770504693114, 174: 2.8621437171359783, 186: 4.563117743110003, 195: 5.223374153366411, 197: 5.2169638969561545, 205: 5.223374153366411, 228: 3.930596098088359, 232: 5.2169638969561545, 242: 0.07692307692307693, 254: 0.0625, 257: 0.1213235294117647, 263: 0.0625, 268: 0.0625, 316: 0.06666666666666667, 322: 0.2477124183006536, 323: 0.2, 329: 0.08333333333333333, 350: 0.7602564102564103, 363: 0.8214285714285714, 376: 0.9464285714285712, 378: 0.9464285714285712, 382: 0.9464285714285712, 388: 0.9464285714285712, 402: 1.089285714285714, 406: 1.089285714285714, 412: 0.05555555555555555, 437: 0.19130216189039717, 453: 0.13333333333333333, 455: 0.13333333333333333, 467: 0.06666666666666667, 489: 0.06666666666666667, 494: 1.0, 513: 0.07692307692307693, 536: 0.1, 557: 1.9312090687090693, 568: 2.284744422244423, 571: 2.284744422244423, 572: 2.298730436230437, 614: 0.5, 623: 0.5, 643: 0.1111111111111111, 680: 2.2333333333333334, 690: 2.483333333333334, 696: 0.058823529411764705, 709: 0.14835164835164835, 722: 0.07692307692307693, 728: 0.07692307692307693, 757: 1.1464868464868463, 759: 0.5669122544122545, 775: 0.25, 867: 0.8999999999999999, 869: 1.0333333333333332, 889: 0.15384615384615385, 909: 0.08333333333333333, 942: 0.06666666666666667, 973: 0.20202020202020202, 1013: 0.2, 1040: 0.22483766233766234, 1065: 0.1, 1070: 0.32765151515151514, 1078: 0.32837301587301587, 1124: 0.13942307692307693, 1157: 0.0625, 1159: 0.0625, 1170: 0.07692307692307693, 1210: 0.07692307692307693, 1358: 0.7, 1362: 0.4, 1376: 0.12916666666666665, 1444: 0.0625, 1465: 0.1111111111111111, 1551: 1.0, 1580: 0.06666666666666667, 1646: 1.0, 1716: 0.06666666666666667, 1864: 0.06666666666666667, 1915: 0.125}

print(total)
95.0

print(newtot)
91.00000000000004

print(evap)
0.042105263157894285


#========3rd SET OF 'next_ranks' after adjusting for 'evap'========
print(next_ranks)
{1: 1.0421052631578942, 9: 0.2421052631578943, 11: 0.5944862155388466, 12: 0.2421052631578943, 16: 0.2421052631578943, 25: 0.2421052631578943, 47: 3.0421052631578944, 67: 2.900082313627206, 85: 0.0947368421052627, 91: 0.0947368421052627, 98: 0.0947368421052627, 102: 0.0947368421052627, 123: 0.7496244381693293, 126: 0.6685346945795858, 138: 2.5629028264477185, 140: 2.900082313627206, 143: 2.8898259033707956, 162: 2.895320408865301, 164: 2.900082313627206, 174: 2.9042489802938727, 186: 4.605223006267897, 195: 5.265479416524305, 197: 5.2590691601140485, 205: 5.265479416524305, 228: 3.9727013612462536, 232: 5.2590691601140485, 242: 0.11902834008097121, 254: 0.10460526315789428, 257: 0.16342879256965898, 263: 0.10460526315789428, 268: 0.10460526315789428, 316: 0.10877192982456095, 322: 0.2898176814585479, 323: 0.2421052631578943, 329: 0.12543859649122763, 350: 0.8023616734143046, 363: 0.8635338345864657, 376: 0.9885338345864655, 378: 0.9885338345864655, 382: 0.9885338345864655, 388: 0.9885338345864655, 402: 1.1313909774436082, 406: 1.1313909774436082, 412: 0.09766081871344984, 437: 0.23340742504829146, 453: 0.17543859649122762, 455: 0.17543859649122762, 467: 0.10877192982456095, 489: 0.10877192982456095, 494: 1.0421052631578942, 513: 0.11902834008097121, 536: 0.1421052631578943, 557: 1.9733143318669635, 568: 2.3268496854023173, 571: 2.3268496854023173, 572: 2.3408356993883315, 614: 0.5421052631578943, 623: 0.5421052631578943, 643: 0.1532163742690054, 680: 2.275438596491228, 690: 2.5254385964912283, 696: 0.10092879256965899, 709: 0.19045691150954264, 722: 0.11902834008097121, 728: 0.11902834008097121, 757: 1.1885921096447405, 759: 0.6090175175701488, 775: 0.2921052631578943, 867: 0.9421052631578942, 869: 1.0754385964912274, 889: 0.19595141700404814, 909: 0.12543859649122763, 942: 0.10877192982456095, 973: 0.2441254651780963, 1013: 0.2421052631578943, 1040: 0.26694292549555665, 1065: 0.1421052631578943, 1070: 0.36975677830940945, 1078: 0.37047827903091013, 1124: 0.1815283400809712, 1157: 0.10460526315789428, 1159: 0.10460526315789428, 1170: 0.11902834008097121, 1210: 0.11902834008097121, 1358: 0.7421052631578943, 1362: 0.44210526315789433, 1376: 0.17127192982456094, 1444: 0.10460526315789428, 1465: 0.1532163742690054, 1551: 1.0421052631578942, 1580: 0.10877192982456095, 1646: 1.0421052631578942, 1716: 0.10877192982456095, 1864: 0.10877192982456095, 1915: 0.16710526315789428}

print(newtot)
94.99999999999993

print(totdiff)
94.17126430501047

print(avediff)
0.9912764663685313

print(i+1, avediff)
#iteration #, average difference
#1 0.9912764663685313







# ==============E2E run of sprank.py========================
PS C:\...\Py4e> python .\sprank.py

#sval = input('How many iterations:')
How many iterations:10

# print(i+1, avediff)
#iteration #, average difference
1 0.30855125680999534
2 0.17748201584136528
3 0.11823348747349391
4 0.08918726634882701
5 0.06930730437779122
6 0.057930372297655575
7 0.05119766932567704
8 0.04726500998789554
9 0.04502180886291953
10 0.04367525141126639

#print(list(next_ranks.items())[:5])
[(1, 0.01580406503022213), (9, 0.009152115236365346), (11, 0.0114942624460394), (12, 0.009152115236365346), (16, 0.009152115236365346)]
'''
