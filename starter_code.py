# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 19:22:46 2024

@author: Roberto


starter code
"""


#lets start out by looking at some basic player stats by season 
#we're going to start by looking at on base percentage - how often a batter gets on base per plate appearence
#lets see how this stat evolves with age
#We're going to do this by looking at season summaries


import pandas as pd
import matplotlib.pyplot as plt

# Load the data
file_path = r"batting_season_summary.csv"
data = pd.read_csv(file_path)

# Group by 'age' and calculate the mean for each group
average_stats_by_age = data.groupby('age').mean()

# Reset index to turn 'age' back into a column
average_stats_by_age.reset_index(inplace=True)


# Plotting H/PA vs age
plt.figure(figsize=(10,6))
plt.scatter(average_stats_by_age['age'], average_stats_by_age['OBP'])
plt.title('On Base Percentage vs Age')
plt.xlabel('Age')
plt.ylabel('Average OBP')
plt.grid(True)
plt.show()




#what about a new stat? I want to look at number of hits per plate appearence
import pandas as pd
import matplotlib.pyplot as plt

# Create a new column for H/PA
data['H/PA'] = data['H'] / data['PA']

# Group by 'age' and calculate the mean for each group
average_stats_by_age = data.groupby('age').mean()

# Reset index to turn 'age' back into a column
average_stats_by_age.reset_index(inplace=True)


# Plotting H/PA vs age
plt.figure(figsize=(10,6))
plt.scatter(average_stats_by_age['age'], average_stats_by_age['H/PA'])
plt.title('Hits per Plate Appearance (H/PA) vs Age')
plt.xlabel('Age')
plt.ylabel('Average H/PA')
plt.grid(True)
plt.show()



#That looks great. But now I want to build a forecast.
#lets build a simple EWMA model to predict the player's batting averages for the 2024 season - This could be a starting point for your submission!

# Assuming data is already loaded into a pandas DataFrame with the name 'data'
data.sort_values(by=['Name', 'Year'], inplace=True)

# Define the alpha value for EWMA calculation
alpha_value = 0.1  # Replace this with the desired alpha value

# Group by player name and calculate EWMA for hits
data['ewma_hits'] = data.groupby('Name')['H'].transform(lambda x: x.ewm(alpha=alpha_value).mean())

# Select the last EWMA value as the next year's forecast
data['Expected Number of Hits Next Season'] = data.groupby('Name')['ewma_hits'].transform('last')

# Now create the 'submission' DataFrame
submission = data[['Name', 'Expected Number of Hits Next Season']].drop_duplicates()


#Now lets get only the players we need to forecast. We'll need to load in the example submission to do this
player_submission_table = pd.read_csv(r"submission_example.csv")
name_list = player_submission_table['Name']

submission = submission[submission['Name'].isin(name_list)]

# Calculate the total of forecasted hits for normalization
total_forecasted_hits = submission['Expected Number of Hits Next Season'].sum()

#submission should be in format: Name	Expected Number of Hits Next Season	Bid Amount($)

#DONT ADD A $ IN YOUR BID COLUMN, IT SHOULD BE A FLOAT OR INT

# To make our bid - we'll start simple - just divide the forecasted hits over total hits - bid propotional to forecasted hits for the season.
submission['Bid Amount($)'] = (submission['Expected Number of Hits Next Season'] / total_forecasted_hits) * 200

# Ensure the DataFrame has the correct columns
submission = submission[['Name', 'Expected Number of Hits Next Season', 'Bid Amount($)']]

#save the result
submission.to_csv('submission.csv', index = False)