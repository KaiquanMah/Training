Run differentials with .iterrows()
You've been hired by the San Francisco Giants as an analyst—congrats! The team's owner wants you to calculate a metric called the run differential for each season from the year 2008 to 2012. This metric is calculated by subtracting the total number of runs a team allowed in a season from the team's total number of runs scored in a season. 'RS' means runs scored and 'RA' means runs allowed.

The below function calculates this metric:

def calc_run_diff(runs_scored, runs_allowed):

    run_diff = runs_scored - runs_allowed

    return run_diff

A DataFrame has been loaded into your session as giants_df and printed into the console. Let's practice using .iterrows() to add a run differential column to this DataFrame.

  Team League  Year   RS   RA   W    G  Playoffs
0  SFG     NL  2012  718  649  94  162         1
1  SFG     NL  2011  570  578  86  162         0
2  SFG     NL  2010  697  583  92  162         1
3  SFG     NL  2009  657  611  88  162         0
4  SFG     NL  2008  640  759  72  162         0






Create an empty list called run_diffs that will be used to store the run differentials you will calculate.
# Create an empty list to store run differentials
run_diffs = []






Write a for loop that uses .iterrows() to loop over giants_df and collects each row's runs scored and runs allowed.
# Write a for loop and collect runs allowed and runs scored for each row
for i,row in giants_df.iterrows():
    runs_scored = row['RS']
    runs_allowed = row['RA']











Add a line to the for loop that uses the provided function to calculate each row's run differential.
# Create an empty list to store run differentials
run_diffs = []

# Write a for loop and collect runs allowed and runs scored for each row
for i,row in giants_df.iterrows():
    runs_scored = row['RS']
    runs_allowed = row['RA']
    
    # Use the provided function to calculate run_diff for each row
    run_diff = calc_run_diff(runs_scored, runs_allowed)









Add a line to the loop that appends each row's run differential to the run_diffs list.
# Create an empty list to store run differentials
run_diffs = []

# Write a for loop and collect runs allowed and runs scored for each row
for i,row in giants_df.iterrows():
    runs_scored = row['RS']
    runs_allowed = row['RA']
    
    #Use the provided function to calculate run_diff for each row
    run_diff = calc_run_diff(runs_scored, runs_allowed)
    
    # Append each run differential to the output list
    run_diffs.append(run_diff)

giants_df['RD'] = run_diffs
print(giants_df)


<script.py> output:
      Team League  Year   RS   RA   W    G  Playoffs   RD
    0  SFG     NL  2012  718  649  94  162         1   69
    1  SFG     NL  2011  570  578  86  162         0   -8
    2  SFG     NL  2010  697  583  92  162         1  114
    3  SFG     NL  2009  657  611  88  162         0   46
    4  SFG     NL  2008  640  759  72  162         0 -119
    
    
Great job! Take a look at the giants_df DataFrame with the new run differential column ('RD') you created (it has been printed in the console).

The 'Playoffs' column tells you if a team made the playoffs for a given season. A 1 means that the team made the playoffs in that season and a 0 means the team did not make the playoffs in that season.

Did you notice that in the seasons with the highest run differentials the Giants made the playoffs? In fact, in both of these seasons (2010 and 2012), the San Francisco Giants not only made the playoffs but also won the World Series! Cool!

    
