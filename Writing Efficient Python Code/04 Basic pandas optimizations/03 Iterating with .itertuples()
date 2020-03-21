Iterating with .itertuples()
Remember, .itertuples() returns each DataFrame row as a special data type called a namedtuple. You can look up an attribute within a namedtuple with a special syntax. Let's practice working with namedtuples.
A pandas DataFrame has been loaded into your session called rangers_df. This DataFrame contains the stats ('Team', 'League', 'Year', 'RS', 'RA', 'W', 'G', and 'Playoffs') for the Major League baseball team named the Texas Rangers (abbreviated as 'TEX').


Use .itertuples() to loop over rangers_df and print each row.
# Loop over the DataFrame and print each row
for row in rangers_df.itertuples():
  print(row)

<script.py> output:
    Pandas(Index=0, Team='TEX', League='AL', Year=2012, RS=808, RA=707, W=93, G=162, Playoffs=1)
    Pandas(Index=1, Team='TEX', League='AL', Year=2011, RS=855, RA=677, W=96, G=162, Playoffs=1)
    Pandas(Index=2, Team='TEX', League='AL', Year=2010, RS=787, RA=687, W=90, G=162, Playoffs=1)
    Pandas(Index=3, Team='TEX', League='AL', Year=2009, RS=784, RA=740, W=87, G=162, Playoffs=0)
    Pandas(Index=4, Team='TEX', League='AL', Year=2008, RS=901, RA=967, W=79, G=162, Playoffs=0)
    Pandas(Index=5, Team='TEX', League='AL', Year=2007, RS=816, RA=844, W=75, G=162, Playoffs=0)
    Pandas(Index=6, Team='TEX', League='AL', Year=2006, RS=835, RA=784, W=80, G=162, Playoffs=0)
    Pandas(Index=7, Team='TEX', League='AL', Year=2005, RS=865, RA=858, W=79, G=162, Playoffs=0)
    Pandas(Index=8, Team='TEX', League='AL', Year=2004, RS=860, RA=794, W=89, G=162, Playoffs=0)
    Pandas(Index=9, Team='TEX', League='AL', Year=2003, RS=826, RA=969, W=71, G=162, Playoffs=0)
    Pandas(Index=10, Team='TEX', League='AL', Year=2002, RS=843, RA=882, W=72, G=162, Playoffs=0)
    Pandas(Index=11, Team='TEX', League='AL', Year=2001, RS=890, RA=968, W=73, G=162, Playoffs=0)
    Pandas(Index=12, Team='TEX', League='AL', Year=2000, RS=848, RA=974, W=71, G=162, Playoffs=0)
    Pandas(Index=13, Team='TEX', League='AL', Year=1999, RS=945, RA=859, W=95, G=162, Playoffs=1)
    Pandas(Index=14, Team='TEX', League='AL', Year=1998, RS=940, RA=871, W=88, G=162, Playoffs=1)
    Pandas(Index=15, Team='TEX', League='AL', Year=1997, RS=807, RA=823, W=77, G=162, Playoffs=0)
    Pandas(Index=16, Team='TEX', League='AL', Year=1996, RS=928, RA=799, W=90, G=163, Playoffs=1)
    Pandas(Index=17, Team='TEX', League='AL', Year=1993, RS=835, RA=751, W=86, G=162, Playoffs=0)
    Pandas(Index=18, Team='TEX', League='AL', Year=1992, RS=682, RA=753, W=77, G=162, Playoffs=0)
    Pandas(Index=19, Team='TEX', League='AL', Year=1991, RS=829, RA=814, W=85, G=162, Playoffs=0)
    Pandas(Index=20, Team='TEX', League='AL', Year=1990, RS=676, RA=696, W=83, G=162, Playoffs=0)
    Pandas(Index=21, Team='TEX', League='AL', Year=1989, RS=695, RA=714, W=83, G=162, Playoffs=0)
    Pandas(Index=22, Team='TEX', League='AL', Year=1988, RS=637, RA=735, W=70, G=161, Playoffs=0)
    Pandas(Index=23, Team='TEX', League='AL', Year=1987, RS=823, RA=849, W=75, G=162, Playoffs=0)
    Pandas(Index=24, Team='TEX', League='AL', Year=1986, RS=771, RA=743, W=87, G=162, Playoffs=0)
    Pandas(Index=25, Team='TEX', League='AL', Year=1985, RS=617, RA=785, W=62, G=161, Playoffs=0)
    Pandas(Index=26, Team='TEX', League='AL', Year=1984, RS=656, RA=714, W=69, G=161, Playoffs=0)
    Pandas(Index=27, Team='TEX', League='AL', Year=1983, RS=639, RA=609, W=77, G=163, Playoffs=0)
    Pandas(Index=28, Team='TEX', League='AL', Year=1982, RS=590, RA=749, W=64, G=162, Playoffs=0)
    Pandas(Index=29, Team='TEX', League='AL', Year=1980, RS=756, RA=752, W=76, G=163, Playoffs=0)
    Pandas(Index=30, Team='TEX', League='AL', Year=1979, RS=750, RA=698, W=83, G=162, Playoffs=0)
    Pandas(Index=31, Team='TEX', League='AL', Year=1978, RS=692, RA=632, W=87, G=162, Playoffs=0)
    Pandas(Index=32, Team='TEX', League='AL', Year=1977, RS=767, RA=657, W=94, G=162, Playoffs=0)
    Pandas(Index=33, Team='TEX', League='AL', Year=1976, RS=616, RA=652, W=76, G=162, Playoffs=0)
    Pandas(Index=34, Team='TEX', League='AL', Year=1975, RS=714, RA=733, W=79, G=162, Playoffs=0)
    Pandas(Index=35, Team='TEX', League='AL', Year=1974, RS=690, RA=698, W=83, G=161, Playoffs=0)
    Pandas(Index=36, Team='TEX', League='AL', Year=1973, RS=619, RA=844, W=57, G=162, Playoffs=0)
    
    
    
    
    
    
    
    
    
    
    
    
Loop over rangers_df with .itertuples() and save each row's Index, Year, and Wins (W) attribute as i, year, and wins.
# Loop over the DataFrame and print each row's Index, Year and Wins (W)
for row in rangers_df.itertuples():
  i = row.Index
  year = row.Year
  wins = row.W
  print(i, year, wins)

<script.py> output:
    0 2012 93
    1 2011 96
    2 2010 90
    3 2009 87
    4 2008 79
    5 2007 75
    6 2006 80
    7 2005 79
    8 2004 89
    9 2003 71
    10 2002 72
    11 2001 73
    12 2000 71
    13 1999 95
    14 1998 88
    15 1997 77
    16 1996 90
    17 1993 86
    18 1992 77
    19 1991 85
    20 1990 83
    21 1989 83
    22 1988 70
    23 1987 75
    24 1986 87
    25 1985 62
    26 1984 69
    27 1983 77
    28 1982 64
    29 1980 76
    30 1979 83
    31 1978 87
    32 1977 94
    33 1976 76
    34 1975 79
    35 1974 83
    36 1973 57













Now, loop over rangers_df and print these values only for those rows where the Rangers made the playoffs.
# Loop over the DataFrame and print each row's Index, Year and Wins (W)
for row in rangers_df.itertuples():
  i = row.Index
  year = row.Year
  wins = row.W
  
  # Check if rangers made Playoffs (1 means yes; 0 means no)
  if row.Playoffs == 1:
    print(i, year, wins)


<script.py> output:
    0 2012 93
    1 2011 96
    2 2010 90
    13 1999 95
    14 1998 88
    16 1996 90

Awesome! You're getting the hang of using .itertuples(). Remember, you need to use the dot syntax for referencing an attribute in a namedtuple.

You can create a new variable using a row's dot reference (as you did when storing row.Index as the variable i). Or you can use the row's dot reference directly to perform calculations and checks. Notice that you did not have to save row.Playoffs to a new variable in your check statement (you were able to use row.Playoffs directly in your check).

Did you notice the pattern in the Texas Rangers playoff appearances? Only six appearances and two distinct sets of groupings (one from 2010 - 2012 and one from 1996 - 1999).

