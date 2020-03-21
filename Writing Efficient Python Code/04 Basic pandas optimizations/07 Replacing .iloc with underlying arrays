Replacing .iloc with underlying arrays
Now that you have a better grasp on a DataFrame's internals let's update one of your previous analyses to leverage a DataFrame's underlying arrays. You'll revisit the win percentage calculations you performed row by row with the .iloc method:

def calc_win_perc(wins, games_played):
    win_perc = wins / games_played
    return np.round(win_perc,2)

win_percs_list = []

for i in range(len(baseball_df)):
    row = baseball_df.iloc[i]

    wins = row['W']
    games_played = row['G']

    win_perc = calc_win_perc(wins, games_played)

    win_percs_list.append(win_perc)

baseball_df['WP'] = win_percs_list
Let's update this analysis to use arrays instead of the .iloc method. A DataFrame (baseball_df) has been loaded into your session.






In [1]: baseball_df
Out[1]: 
     Team League  Year   RS   RA    W    G  Playoffs
0     ARI     NL  2012  734  688   81  162         0
1     ATL     NL  2012  700  600   94  162         1
2     BAL     AL  2012  712  705   93  162         1
3     BOS     AL  2012  734  806   69  162         0
4     CHC     NL  2012  613  759   61  162         0
5     CHW     AL  2012  748  676   85  162         0
6     CIN     NL  2012  669  588   97  162         1
7     CLE     AL  2012  667  845   68  162         0
8     COL     NL  2012  758  890   64  162         0
9     DET     AL  2012  726  670   88  162         1
10    HOU     NL  2012  583  794   55  162         0
11    KCR     AL  2012  676  746   72  162         0
12    LAA     AL  2012  767  699   89  162         0
13    LAD     NL  2012  637  597   86  162         0
14    MIA     NL  2012  609  724   69  162         0
15    MIL     NL  2012  776  733   83  162         0
16    MIN     AL  2012  701  832   66  162         0
17    NYM     NL  2012  650  709   74  162         0
18    NYY     AL  2012  804  668   95  162         1
19    OAK     AL  2012  713  614   94  162         1
20    PHI     NL  2012  684  680   81  162         0
21    PIT     NL  2012  651  674   79  162         0
22    SDP     NL  2012  651  710   76  162         0
23    SEA     AL  2012  619  651   75  162         0
24    SFG     NL  2012  718  649   94  162         1
25    STL     NL  2012  765  648   88  162         1
26    TBR     AL  2012  697  577   90  162         0
27    TEX     AL  2012  808  707   93  162         1
28    TOR     AL  2012  716  784   73  162         0
29    WSN     NL  2012  731  594   98  162         1
...   ...    ...   ...  ...  ...  ...  ...       ...
1202  LAD     NL  1963  640  550   99  163         1
1203  MIN     AL  1963  767  602   91  161         0
1204  MLN     NL  1963  677  603   84  163         0
1205  NYM     NL  1963  501  774   51  162         0
1206  NYY     AL  1963  714  547  104  161         1
1207  PHI     NL  1963  642  578   87  162         0
1208  PIT     NL  1963  567  595   74  162         0
1209  SFG     NL  1963  725  641   88  162         0
1210  STL     NL  1963  747  628   93  162         0
1211  WSA     AL  1963  578  812   56  162         0
1212  BAL     AL  1962  652  680   77  162         0
1213  BOS     AL  1962  707  756   76  160         0
1214  CHC     NL  1962  632  827   59  162         0
1215  CHW     AL  1962  707  658   85  162         0
1216  CIN     NL  1962  802  685   98  162         0
1217  CLE     AL  1962  682  745   80  162         0
1218  DET     AL  1962  758  692   85  161         0
1219  HOU     NL  1962  592  717   64  162         0
1220  KCA     AL  1962  745  837   72  162         0
1221  LAA     AL  1962  718  706   86  162         0
1222  LAD     NL  1962  842  697  102  165         0
1223  MIN     AL  1962  798  713   91  163         0
1224  MLN     NL  1962  730  665   86  162         0
1225  NYM     NL  1962  617  948   40  161         0
1226  NYY     AL  1962  817  680   96  162         1
1227  PHI     NL  1962  705  759   81  161         0
1228  PIT     NL  1962  706  626   93  161         0
1229  SFG     NL  1962  878  690  103  165         1
1230  STL     NL  1962  774  664   84  163         0
1231  WSA     AL  1962  599  716   60  162         0

[1232 rows x 8 columns]







Use the right method to collect the underlying 'W' and 'G' arrays of baseball_df and pass them directly into the calc_win_perc() function. Store the result as a variable called win_percs_np.
# Use the W array and G array to calculate win percentages
win_percs_np = calc_win_perc(baseball_df['W'], baseball_df['G'])


In [3]: win_percs_np
Out[3]: 
0       0.50
1       0.58
2       0.57
3       0.43
...
1228    0.58
1229    0.62
1230    0.52
1231    0.37
Length: 1232, dtype: float64













Create a new column in baseball_df called 'WP' that contains the win percentages you just calculated.
# Use the W array and G array to calculate win percentages
win_percs_np = calc_win_perc(baseball_df['W'].values, baseball_df['G'].values)

In [5]: win_percs_np
Out[5]: array([0.5 , 0.58, 0.57, ..., 0.62, 0.52, 0.37])


# Append a new column to baseball_df that stores all win percentages
baseball_df['WP'] = win_percs_np

print(baseball_df.head())

<script.py> output:
      Team League  Year   RS   RA   W    G  Playoffs    WP
    0  ARI     NL  2012  734  688  81  162         0  0.50
    1  ATL     NL  2012  700  600  94  162         1  0.58
    2  BAL     AL  2012  712  705  93  162         1  0.57
    3  BOS     AL  2012  734  806  69  162         0  0.43
    4  CHC     NL  2012  613  759  61  162         0  0.38














Use timeit in cell magic mode within your IPython console to compare the runtimes between the old code block using .iloc and the new code you developed using NumPy arrays.
Don't include the code that defines the calc_win_perc() function or the print() statements or when timing.
You should include eight lines of code when timing the old code block and two lines of code when timing the new code you developed. You may need to press SHIFT+ENTER when using timeit in cell magic mode to get to a new line within your IPython console.

%%timeit
win_percs_list = []

for i in range(len(baseball_df)):
    row = baseball_df.iloc[i]

    wins = row['W']
    games_played = row['G']

    win_perc = calc_win_perc(wins, games_played)

    win_percs_list.append(win_perc)

baseball_df['WP'] = win_percs_list


2.17 s +- 572 ms per loop (mean +- std. dev. of 7 runs, 1 loop each)









%%timeit
win_percs_np = calc_win_perc(baseball_df['W'].values, baseball_df['G'].values)

# Append a new column to baseball_df that stores all win percentages
baseball_df['WP'] = win_percs_np

689 us +- 39.8 us per loop (mean +- std. dev. of 7 runs, 1000 loops each)



Which approach was the faster?

The original code with .iloc is much faster than using NumPy arrays
The old code block with .iloc and the new code with NumPy arrays have similar runtimes.

#YES - The NumPy array approach is faster than the .iloc approach.

Great job! You're knocking it out of the park! Using a DataFrame's underlying arrays to perform calculations can really speed up your code and yields some significant efficiency gains. Did you notice that the NumPy array approach was not just faster, but that it also used fewer lines of code and was easier to read?



