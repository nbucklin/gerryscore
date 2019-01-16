import pandas as pd

# Importing data
d = r'/Users/npbuckli/GitHub/gerryscore/Excel work.xlsx'
data_raw = pd.read_excel(d,sheet='data')

# Filtering out stuff we don't need
data = data_raw[(data_raw['year'] == 2016) & (data_raw['special'] == False) & (data_raw['writein'] == False)]

# Seeing the frequency of political parties
pd.crosstab(data['state'],data['party'],margins=True)
data['party'].value_counts()

# We only really need R or D so keepign that
data = data[(data['party'] == 'democrat') | (data['party'] == 'republican')]

# Cleaning up the dataset because it's got a bunch of variables we don't need
data = data[['state','district','party','candidatevotes']]

# Transposing D/R 
test = pd.pivot_table(data,values='candidatevotes',index=['state','district'],columns='party')

