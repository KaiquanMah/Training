Analyzing baseball stats with .apply()
The Tampa Bay Rays want you to analyze their data.

They'd like the following metrics:

The sum of each column in the data
The total amount of runs scored in a year ('RS' + 'RA' for each year)
The 'Playoffs' column in text format rather than using 1's and 0's
The below function can be used to convert the 'Playoffs' column to text:

def text_playoffs(num_playoffs): 
    if num_playoffs == 1:
        return 'Yes'
    else:
        return 'No' 
Use .apply() to get these metrics. A DataFrame (rays_df) has been loaded and printed to the console. This DataFrame is indexed on the 'Year' column.



       RS   RA   W  Playoffs
2012  697  577  90         0
2011  707  614  91         1
2010  802  649  96         1
2009  803  754  84         0
2008  774  671  97         1






Apply sum() to each column of rays_df to collect the sum of each column. Be sure to specify the correct axis.
# Gather sum of all columns
stat_totals = rays_df.apply(sum, axis=0)
print(stat_totals)

<script.py> output:
    RS          3783
    RA          3265
    W            458
    Playoffs       3
    dtype: int64
    
    
    
    
    
    
    
    
Apply sum() to each row of rays_df, only looking at the 'RS' and 'RA' columns, and specify the correct axis.
# Gather total runs scored in all games per year
total_runs_scored = rays_df[['RS', 'RA']].apply(sum, axis=1)
print(total_runs_scored)

<script.py> output:
    2012    1274
    2011    1321
    2010    1451
    2009    1557
    2008    1445
    dtype: int64
    
    
    
    
    
    
    
    
Use .apply() and a lambda function to apply text_playoffs() to each row's 'Playoffs' value of the rays_df DataFrame.
# Convert numeric playoffs to text
textual_playoffs = rays_df.apply(lambda row: text_playoffs(row['Playoffs']), axis=1)
print(textual_playoffs)

<script.py> output:
    2012     No
    2011    Yes
    2010    Yes
    2009     No
    2008    Yes
    dtype: object
    

Great work! The .apply() method let's you apply functions to all rows or columns of a DataFrame by specifying an axis.

If you've been using pandas for some time, you may have noticed that a better way to find these stats would use the pandas built-in .sum() method.

You could have used rays_df.sum(axis=0) to get columnar sums and rays_df[['RS', 'RA']].sum(axis=1) to get row sums.

You could have also used .apply() directly on a Series (or column) of the DataFrame. For example, you could use rays_df['Playoffs'].apply(text_playoffs) to convert the 'Playoffs' column to text.

