Settle a debate with .apply()
Word has gotten to the Arizona Diamondbacks about your awesome analytics skills. They'd like for you to help settle a debate amongst the managers. One manager claims that the team has made the playoffs every year they have had a win percentage of 0.50 or greater. Another manager says this is not true.

Let's use the below function and the .apply() method to see which manager is correct.

def calc_win_perc(wins, games_played):
    win_perc = wins / games_played
    return np.round(win_perc,2)
A DataFrame named dbacks_df has been loaded into your session.




Print the first five rows of the dbacks_df DataFrame to see what the data looks like.
# Display the first five rows of the DataFrame
print(dbacks_df.head())

<script.py> output:
      Team League  Year   RS   RA   W    G  Playoffs
    0  ARI     NL  2012  734  688  81  162         0
    1  ARI     NL  2011  731  662  94  162         1
    2  ARI     NL  2010  713  836  65  162         0
    3  ARI     NL  2009  720  782  70  162         0
    4  ARI     NL  2008  720  706  82  162         0






Create a pandas Series called win_percs by applying the calc_win_perc() function to each row of the DataFrame with a lambda function.
# Create a win percentage Series 
win_percs = dbacks_df.apply(lambda row: calc_win_perc(row['W'], row['G']), axis=1)
print(win_percs, '\n')

<script.py> output:
    0     0.50
    1     0.58
    2     0.40
    3     0.43
    4     0.51
    5     0.56
    6     0.47
    7     0.48
    8     0.31
    9     0.52
    10    0.60
    11    0.57
    12    0.52
    13    0.62
    14    0.40
    dtype: float64








Create a new column in dbacks_df called WP that contains the win percentages you calculated in the above step.
# Append a new column to dbacks_df
dbacks_df['WP'] = win_percs
print(dbacks_df, '\n')

# Display dbacks_df where WP is greater than 0.50
print(dbacks_df[dbacks_df['WP'] >= 0.50])

<script.py> output:
       Team League  Year   RS   RA    W    G  Playoffs    WP
    0   ARI     NL  2012  734  688   81  162         0  0.50
    1   ARI     NL  2011  731  662   94  162         1  0.58
    2   ARI     NL  2010  713  836   65  162         0  0.40
    3   ARI     NL  2009  720  782   70  162         0  0.43
    4   ARI     NL  2008  720  706   82  162         0  0.51
    5   ARI     NL  2007  712  732   90  162         1  0.56
    6   ARI     NL  2006  773  788   76  162         0  0.47
    7   ARI     NL  2005  696  856   77  162         0  0.48
    8   ARI     NL  2004  615  899   51  162         0  0.31
    9   ARI     NL  2003  717  685   84  162         0  0.52
    10  ARI     NL  2002  819  674   98  162         1  0.60
    11  ARI     NL  2001  818  677   92  162         1  0.57
    12  ARI     NL  2000  792  754   85  162         0  0.52
    13  ARI     NL  1999  908  676  100  162         1  0.62
    14  ARI     NL  1998  665  812   65  162         0  0.40 
    
       Team League  Year   RS   RA    W    G  Playoffs    WP
    0   ARI     NL  2012  734  688   81  162         0  0.50
    1   ARI     NL  2011  731  662   94  162         1  0.58
    4   ARI     NL  2008  720  706   82  162         0  0.51
    5   ARI     NL  2007  712  732   90  162         1  0.56
    9   ARI     NL  2003  717  685   84  162         0  0.52
    10  ARI     NL  2002  819  674   98  162         1  0.60
    11  ARI     NL  2001  818  677   92  162         1  0.57
    12  ARI     NL  2000  792  754   85  162         0  0.52
    13  ARI     NL  1999  908  676  100  162         1  0.62














Which manager was correct in their claim?

The manager who claimed the team made the playoffs every year they've had a win percentage of 0.50 or greater.
Both managers are crazy! The Arizona Diamondbacks have never made the playoffs.

#YES - The manager who claimed the team has not made the playoffs every year they've had a win percentage of 0.50 or greater.
Nicely done! Using the .apply() method with a lambda function allows you to apply a function to a DataFrame without the need to write a for loop.
Sadly, the second manager was correct. In the year 2012, 2008, 2003, and 2000 the Arizona Diamondbacks had a win percentage greater than or equal to 0.50, but still did not make the playoffs.

