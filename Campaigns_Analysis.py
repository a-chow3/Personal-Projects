import pandas as pd
import numpy as np
from pathlib import Path


df = pd.read_csv("campaigns.csv")


### Sort Weekday by the Open Rate where the total recipients are greater than 10


# Create a column thaat converts the Open Rate percentages to decimals
df['Open Rate Value'] = df['Open Rate'].str.rstrip('%').astype('float') / 100

# Create a column thaat converts the Click Rate percentages to decimals
df['Click Rate Value'] = df['Click Rate'].str.rstrip('%').astype('float') / 100

# Create a DF for only emails that have at least 10 recipients
df_tr_10 = df[df['Total Recipients'] > 10]

# Series that Sorts the mean Open Rate for each Weekday
weekday_by_or = df_tr_10.groupby('Send Weekday')['Open Rate Value'].mean().sort_values(ascending=False)

'''
Thursday, Friday, Monday, Tuesday, Wednesday -> these are the weekdays' open rate in descending order

As we can see, generally having email on the bookend of the week tend to be more effective, 
as this is the time where most people check their emails because they are either just starting their week and need to check their emails, 
or they are just finishing their week and have time to check their email before their week starts back up again

This is also slightly misleading because the two highest days: Thursday and Friday have only one value, where every other weekday has multiple values.

'''

### Sort Weekday by the Click Rate where the total recipients are greater than 10

# Series that Sorts the mean Click Rate for each Weekday
weekday_by_cr = df_tr_10.groupby('Send Weekday')['Click Rate Value'].mean().sort_values(ascending=False)

'''
extremely similar to the Open Rate Data
'''



### Does Time of Day matter at all?

# Convert to Datetime variable
df['DateTime'] = pd.to_datetime(df['Send Date'], format='%b %d, %Y %I:%M %p')

## Open/Click Rates based on time of day

# 1am-Noon
morning_or = df[(df['DateTime'].dt.hour >= 1) & (df['DateTime'].dt.hour < 12)]['Open Rate Value'].mean()
morning_cr = df[(df['DateTime'].dt.hour >= 1) & (df['DateTime'].dt.hour < 12)]['Click Rate Value'].mean()


# Noon-5pm
afternoon_or = df[(df['DateTime'].dt.hour >= 12) & (df['DateTime'].dt.hour < 17)]['Open Rate Value'].mean()
afternoon_cr = df[(df['DateTime'].dt.hour >= 12) & (df['DateTime'].dt.hour < 17)]['Click Rate Value'].mean()


# 5-9pm
evening_or = df[(df['DateTime'].dt.hour >= 17) & (df['DateTime'].dt.hour < 21)]['Open Rate Value'].mean()
evening_cr = df[(df['DateTime'].dt.hour >= 17) & (df['DateTime'].dt.hour < 21)]['Click Rate Value'].mean()

# 9-1am
night_or = df[(df['DateTime'].dt.hour >= 21) | (df['DateTime'].dt.hour <= 1)]['Open Rate Value'].mean()
night_cr = df[(df['DateTime'].dt.hour >= 21) | (df['DateTime'].dt.hour <= 1)]['Click Rate Value'].mean()



### What students (emails/computing ids) check their email the most

data_dir = Path.cwd() / "granular_activity opens"

dfs = []

for i in data_dir.iterdir():
    df_opens = pd.read_csv(i)  
    #df["Date"] = pd.to_datetime(df["Date"])
    #df.set_index("dt", inplace=True)
    
    ticker = i.stem 
    df_opens["ticker"] = ticker
    
    dfs.append(df_opens)

df_opens = pd.concat(dfs)

df_opens.columns = df_opens.columns.str.lower()

# Subset data to only include UVA student emails
uva_emails = df_opens[df_opens['email'].str.endswith('@virginia.edu')]

# Add "Computing ID" column to exclude the full email
uva_emails['computing id'] = uva_emails['email'].str.replace('@virginia.edu', '')

# Number of Opens per UVA Computing ID over the course of the year
uva_cid_opens = uva_emails['computing id'].value_counts()


### Which recipients almost never open emails (> 10 opens)
less_than_10_opens = uva_cid_opens[uva_cid_opens < 10]



### Over the Year, which events got the most clicks (ranked)

data_dir = Path.cwd() / "granular_activity clicks"

dfs = []

for i in data_dir.iterdir():
    df_clicks = pd.read_csv(i)  
    #df["Date"] = pd.to_datetime(df["Date"])
    #df.set_index("dt", inplace=True)
    
    ticker = i.stem 
    df_clicks["ticker"] = ticker
    
    dfs.append(df_clicks)

df_clicks = pd.concat(dfs)

df_clicks.columns = df_clicks.columns.str.lower()


event_clicks = df_clicks["ticker"].value_counts()






