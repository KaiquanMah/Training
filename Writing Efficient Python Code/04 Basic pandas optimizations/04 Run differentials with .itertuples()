Run differentials with .itertuples()
The New York Yankees have made a trade with the San Francisco Giants for your analyst contract— you're a hot commodity! Your new boss has seen your work with the Giants and now wants you to do something similar with the Yankees data. He'd like you to calculate run differentials for the Yankees from the year 1962 to the year 2012 and find which season they had the best run differential.

You've remembered the function you used when working with the Giants and quickly write it down:

def calc_run_diff(runs_scored, runs_allowed):

    run_diff = runs_scored - runs_allowed

    return run_diff
Let's use .itertuples() to loop over the yankees_df DataFrame (which has been loaded into your session) and calculate run differentials.




        # Loop over the DataFrame and calculate each row's run differential
        for row in yankees_df.itertuples():
            print(row)
Pandas(Index=0, Team='NYY', League='AL', Year=2012, RS=804, RA=668, W=95, G=162, Playoffs=1)
Pandas(Index=1, Team='NYY', League='AL', Year=2011, RS=867, RA=657, W=97, G=162, Playoffs=1)
Pandas(Index=2, Team='NYY', League='AL', Year=2010, RS=859, RA=693, W=95, G=162, Playoffs=1)
Pandas(Index=3, Team='NYY', League='AL', Year=2009, RS=915, RA=753, W=103, G=162, Playoffs=1)
Pandas(Index=4, Team='NYY', League='AL', Year=2008, RS=789, RA=727, W=89, G=162, Playoffs=0)
Pandas(Index=5, Team='NYY', League='AL', Year=2007, RS=968, RA=777, W=94, G=162, Playoffs=1)
Pandas(Index=6, Team='NYY', League='AL', Year=2006, RS=930, RA=767, W=97, G=162, Playoffs=1)
Pandas(Index=7, Team='NYY', League='AL', Year=2005, RS=886, RA=789, W=95, G=162, Playoffs=1)
Pandas(Index=8, Team='NYY', League='AL', Year=2004, RS=897, RA=808, W=101, G=162, Playoffs=1)
Pandas(Index=9, Team='NYY', League='AL', Year=2003, RS=877, RA=716, W=101, G=163, Playoffs=1)
Pandas(Index=10, Team='NYY', League='AL', Year=2002, RS=897, RA=697, W=103, G=161, Playoffs=1)
Pandas(Index=11, Team='NYY', League='AL', Year=2001, RS=804, RA=713, W=95, G=161, Playoffs=1)
Pandas(Index=12, Team='NYY', League='AL', Year=2000, RS=871, RA=814, W=87, G=161, Playoffs=1)
Pandas(Index=13, Team='NYY', League='AL', Year=1999, RS=900, RA=731, W=98, G=162, Playoffs=1)
Pandas(Index=14, Team='NYY', League='AL', Year=1998, RS=965, RA=656, W=114, G=162, Playoffs=1)
Pandas(Index=15, Team='NYY', League='AL', Year=1997, RS=891, RA=688, W=96, G=162, Playoffs=1)
Pandas(Index=16, Team='NYY', League='AL', Year=1996, RS=871, RA=787, W=92, G=162, Playoffs=1)
Pandas(Index=17, Team='NYY', League='AL', Year=1993, RS=821, RA=761, W=88, G=162, Playoffs=0)
Pandas(Index=18, Team='NYY', League='AL', Year=1992, RS=733, RA=746, W=76, G=162, Playoffs=0)
Pandas(Index=19, Team='NYY', League='AL', Year=1991, RS=674, RA=777, W=71, G=162, Playoffs=0)
Pandas(Index=20, Team='NYY', League='AL', Year=1990, RS=603, RA=749, W=67, G=162, Playoffs=0)
Pandas(Index=21, Team='NYY', League='AL', Year=1989, RS=698, RA=792, W=74, G=161, Playoffs=0)
Pandas(Index=22, Team='NYY', League='AL', Year=1988, RS=772, RA=748, W=85, G=161, Playoffs=0)
Pandas(Index=23, Team='NYY', League='AL', Year=1987, RS=788, RA=758, W=89, G=162, Playoffs=0)
Pandas(Index=24, Team='NYY', League='AL', Year=1986, RS=797, RA=738, W=90, G=162, Playoffs=0)
Pandas(Index=25, Team='NYY', League='AL', Year=1985, RS=839, RA=660, W=97, G=161, Playoffs=0)
Pandas(Index=26, Team='NYY', League='AL', Year=1984, RS=758, RA=679, W=87, G=162, Playoffs=0)
Pandas(Index=27, Team='NYY', League='AL', Year=1983, RS=770, RA=703, W=91, G=162, Playoffs=0)
Pandas(Index=28, Team='NYY', League='AL', Year=1982, RS=709, RA=716, W=79, G=162, Playoffs=0)
Pandas(Index=29, Team='NYY', League='AL', Year=1980, RS=820, RA=662, W=103, G=162, Playoffs=1)
Pandas(Index=30, Team='NYY', League='AL', Year=1979, RS=734, RA=672, W=89, G=160, Playoffs=0)
Pandas(Index=31, Team='NYY', League='AL', Year=1978, RS=735, RA=582, W=100, G=163, Playoffs=1)
Pandas(Index=32, Team='NYY', League='AL', Year=1977, RS=831, RA=651, W=100, G=162, Playoffs=1)
Pandas(Index=33, Team='NYY', League='AL', Year=1976, RS=730, RA=575, W=97, G=159, Playoffs=1)
Pandas(Index=34, Team='NYY', League='AL', Year=1975, RS=681, RA=588, W=83, G=160, Playoffs=0)
Pandas(Index=35, Team='NYY', League='AL', Year=1974, RS=671, RA=623, W=89, G=162, Playoffs=0)
Pandas(Index=36, Team='NYY', League='AL', Year=1973, RS=641, RA=610, W=80, G=162, Playoffs=0)
Pandas(Index=37, Team='NYY', League='AL', Year=1971, RS=648, RA=641, W=81, G=162, Playoffs=0)
Pandas(Index=38, Team='NYY', League='AL', Year=1970, RS=680, RA=612, W=93, G=163, Playoffs=0)
Pandas(Index=39, Team='NYY', League='AL', Year=1969, RS=562, RA=587, W=80, G=162, Playoffs=0)
Pandas(Index=40, Team='NYY', League='AL', Year=1968, RS=536, RA=531, W=83, G=164, Playoffs=0)
Pandas(Index=41, Team='NYY', League='AL', Year=1967, RS=522, RA=621, W=72, G=163, Playoffs=0)
Pandas(Index=42, Team='NYY', League='AL', Year=1966, RS=611, RA=612, W=70, G=160, Playoffs=0)
Pandas(Index=43, Team='NYY', League='AL', Year=1965, RS=611, RA=604, W=77, G=162, Playoffs=0)
Pandas(Index=44, Team='NYY', League='AL', Year=1964, RS=730, RA=577, W=99, G=164, Playoffs=1)
Pandas(Index=45, Team='NYY', League='AL', Year=1963, RS=714, RA=547, W=104, G=161, Playoffs=1)
Pandas(Index=46, Team='NYY', League='AL', Year=1962, RS=817, RA=680, W=96, G=162, Playoffs=1)





Use .itertuples() to loop over yankees_df and grab each row's runs scored and runs allowed values.
run_diffs = []

# Loop over the DataFrame and calculate each row's run differential
for row in yankees_df.itertuples():
    
    runs_scored = row.RS
    runs_allowed = row.RA





Now, calculate each row's run differential using calc_run_diff(). Be sure to append each row's run differential to run_diffs.
run_diffs = []

# Loop over the DataFrame and calculate each row's run differential
for row in yankees_df.itertuples():
    
    runs_scored = row.RS
    runs_allowed = row.RA

    run_diff = calc_run_diff(runs_scored , runs_allowed)
    
    run_diffs.append(run_diff)















Append a new column called 'RD' to the yankees_df DataFrame that contains the run differentials you calculated.
run_diffs = []

# Loop over the DataFrame and calculate each row's run differential
for row in yankees_df.itertuples():
    
    runs_scored = row.RS
    runs_allowed = row.RA

    run_diff = calc_run_diff(runs_scored, runs_allowed)
    
    run_diffs.append(run_diff)

# Append new column
yankees_df['RD'] = run_diffs
print(yankees_df)



<script.py> output:
       Team League  Year   RS   RA    W    G  Playoffs   RD
    0   NYY     AL  2012  804  668   95  162         1  136
    1   NYY     AL  2011  867  657   97  162         1  210
    2   NYY     AL  2010  859  693   95  162         1  166
    3   NYY     AL  2009  915  753  103  162         1  162
    4   NYY     AL  2008  789  727   89  162         0   62
    5   NYY     AL  2007  968  777   94  162         1  191
    6   NYY     AL  2006  930  767   97  162         1  163
    7   NYY     AL  2005  886  789   95  162         1   97
    8   NYY     AL  2004  897  808  101  162         1   89
    9   NYY     AL  2003  877  716  101  163         1  161
    10  NYY     AL  2002  897  697  103  161         1  200
    11  NYY     AL  2001  804  713   95  161         1   91
    12  NYY     AL  2000  871  814   87  161         1   57
    13  NYY     AL  1999  900  731   98  162         1  169
    14  NYY     AL  1998  965  656  114  162         1  309
    15  NYY     AL  1997  891  688   96  162         1  203
    16  NYY     AL  1996  871  787   92  162         1   84
    17  NYY     AL  1993  821  761   88  162         0   60
    18  NYY     AL  1992  733  746   76  162         0  -13
    19  NYY     AL  1991  674  777   71  162         0 -103
    20  NYY     AL  1990  603  749   67  162         0 -146
    21  NYY     AL  1989  698  792   74  161         0  -94
    22  NYY     AL  1988  772  748   85  161         0   24
    23  NYY     AL  1987  788  758   89  162         0   30
    24  NYY     AL  1986  797  738   90  162         0   59
    25  NYY     AL  1985  839  660   97  161         0  179
    26  NYY     AL  1984  758  679   87  162         0   79
    27  NYY     AL  1983  770  703   91  162         0   67
    28  NYY     AL  1982  709  716   79  162         0   -7
    29  NYY     AL  1980  820  662  103  162         1  158
    30  NYY     AL  1979  734  672   89  160         0   62
    31  NYY     AL  1978  735  582  100  163         1  153
    32  NYY     AL  1977  831  651  100  162         1  180
    33  NYY     AL  1976  730  575   97  159         1  155
    34  NYY     AL  1975  681  588   83  160         0   93
    35  NYY     AL  1974  671  623   89  162         0   48
    36  NYY     AL  1973  641  610   80  162         0   31
    37  NYY     AL  1971  648  641   81  162         0    7
    38  NYY     AL  1970  680  612   93  163         0   68
    39  NYY     AL  1969  562  587   80  162         0  -25
    40  NYY     AL  1968  536  531   83  164         0    5
    41  NYY     AL  1967  522  621   72  163         0  -99
    42  NYY     AL  1966  611  612   70  160         0   -1
    43  NYY     AL  1965  611  604   77  162         0    7
    44  NYY     AL  1964  730  577   99  164         1  153
    45  NYY     AL  1963  714  547  104  161         1  167
    46  NYY     AL  1962  817  680   96  162         1  137












In what year within your DataFrame did the New York Yankees have the highest run differential?
You'll need to rerun the code that creates the 'RD' column if you'd like to analyze the DataFrame with code rather than looking at the console output.

yankees_df[yankees_df.RD == max(yankees_df.RD)]

In [4]: yankees_df[yankees_df.RD == max(yankees_df.RD)]
Out[4]: 
   Team League  Year   RS   RA    W    G  Playoffs   RD
14  NYY     AL  1998  965  656  114  162         1  309


In 2011 (with a Run Differential of 210)
In 1962 (with a Run Differential of 503)
In 1985 (with a Run Differential of 315)

#YES - In 1998 (with a Run Differential of 309)
Great job! You used .itertuples() to help the Yankees calculate run differentials. Remember, using .itertuples() is just like using .iterrows() except it tends to be faster. You also have to use a dot reference when looking up attributes with .itertuples().

You found that the Yankees' highest run differential was in 1998. Did you know they actually hold the record for the highest run differential in an MLB season (411 in the year 1939 where they scored 967 runs and allowed 556)? Wow!

