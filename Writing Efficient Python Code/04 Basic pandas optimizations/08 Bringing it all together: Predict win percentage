Bringing it all together: Predict win percentage
A pandas DataFrame (baseball_df) has been loaded into your session. For convenience, a dictionary describing each column within baseball_df has been printed into your console. You can reference these descriptions throughout the exercise.

You'd like to attempt to predict a team's win percentage for a given season by using the team's total runs scored in a season ('RS') and total runs allowed in a season ('RA') with the following function:

def predict_win_perc(RS, RA):
    prediction = RS ** 2 / (RS ** 2 + RA ** 2)
    return np.round(prediction, 2)
Let's compare the approaches you've learned to calculate a predicted win percentage for each season (or row) in your DataFrame.



OrderedDict([('Team', 'Abbreviated team name'),
             ('League', 'Specifies National League or American League'),
             ('Year', "Each season's year"),
             ('RS', 'Runs scored in a season'),
             ('RA', 'Runs allowed in a season'),
             ('W', 'Wins in a season'),
             ('G', 'Games played in a season'),
             ('Playoffs', '`1` if a team made the playoffs; `0` if they did not'),
             ('WP', 'True win percentage for a season')])








Use a for loop and .itertuples() to predict the win percentage for each row of baseball_df with the predict_win_perc() function. Save each row's predicted win percentage as win_perc_pred and append each to the win_perc_preds_loop list.
win_perc_preds_loop = []

# Use a loop and .itertuples() to collect each row's predicted win percentage
for row in baseball_df.itertuples():
    runs_scored = row.RS
    runs_allowed = row.RA
    win_perc_pred = predict_win_perc(runs_scored, runs_allowed)
    win_perc_preds_loop.append(win_perc_pred)






Apply predict_win_perc() to each row of the baseball_df DataFrame using a lambda function. Save the predicted win percentage as win_perc_preds_apply.
# Apply predict_win_perc to each row of the DataFrame
win_perc_preds_apply = baseball_df.apply(lambda row: predict_win_perc(row['RS'], row['RA']), axis=1)








Calculate the predicted win percentages by passing the underlying 'RS' and 'RA' arrays from baseball_df into predict_win_perc(). Save these predictions as win_perc_preds_np.
# Calculate the win percentage predictions using NumPy arrays
win_perc_preds_np = predict_win_perc(baseball_df['RS'].values, baseball_df['RA'].values)
baseball_df['WP_preds'] = win_perc_preds_np
print(baseball_df.head())










Compare runtimes within your IPython console between all three approaches used to calculate the predicted win percentages.
Use %%timeit (cell magic mode) to time the six lines of code (not including comment lines) for the .itertuples() approach. You may need to press SHIFT+ENTER after entering %%timeit to get to a new line within your IPython console.
Use %timeit (line magic mode) to time the .apply() approach and the NumPy array approach separately. Each has only one line of code (not including comment lines).

%%timeit 
win_perc_preds_loop = []

# Use a loop and .itertuples() to collect each row's predicted win percentage
for row in baseball_df.itertuples():
    runs_scored = row.RS
    runs_allowed = row.RA
    win_perc_pred = predict_win_perc(runs_scored, runs_allowed)
    win_perc_preds_loop.append(win_perc_pred)
    

97.1 ms +- 15.2 ms per loop (mean +- std. dev. of 7 runs, 10 loops each)
    





%timeit win_perc_preds_apply = baseball_df.apply(lambda row: predict_win_perc(row['RS'], row['RA']), axis=1)

249 ms +- 11 ms per loop (mean +- std. dev. of 7 runs, 1 loop each)




What is the order of approaches from fastest to slowest?

The .apply() with a lambda function was the fastest, followed by the .itertuples() approach, and the array approach was slowest.
The .itertuples() approach was fastest, followed by the array approach, and the .apply() approach was slowest.
All three approaches had comparable runtimes.

#YES - Using NumPy arrays was the fastest approach, followed by the .itertuples() approach, and the .apply() approach was slowest.
Great job! That's a home run! You practiced using three different approaches to iterate over a pandas DataFrame and perform calculations. Did you notice that the .itertuples() approach beat the .apply() approach? Even though both these implementations can be useful, you should default to using a DataFrame's underlying arrays to perform calculations.
Take a look at your win percentage predictions (column 'WP_preds') and compare them to the actual win percentages (column 'WP'). Not bad!
You've done a great job throughout the course! Now, you are well on your way to writing efficient Python and pandas code!


