import pandas as pd
from pandasql import sqldf
sql = lambda q: sqldf(q, globals())
import numpy as np
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler


# Importing data
d = r'/Users/npbuckli/GitHub/gerryscore/gerryscore/Excel work.xlsx'
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
data = pd.pivot_table(data,values='candidatevotes',index=['state','district'],columns='party').reset_index()

# Sorting
data = data.sort_values(by=['state','district'])

# Summing votes
data = data.fillna(0)
data['totalvotes'] = data['democrat'] + data['republican']

# Calculating vote share pct
def share(var):
    temp = data.copy()
    temp['{}share'.format(var)] = temp['{}'.format(var)] / temp['totalvotes']
    return temp
data = share('democrat')
data = share('republican')


# Calculating statistics needed for 
def calc(v1,v2):
    temp = data.copy()
    temp = data.groupby('state').agg({"{}".format(v1):{"{}_mean".format(v2):np.mean,"{}_median".format(v2):np.median,"{}_std".format(v2):np.std,"{}_count".format(v2):np.size}})
    temp.columns = temp.columns.droplevel(0)
    temp['{}_meanmediandiff'.format(v2)] = temp['{}_mean'.format(v2)] - temp['{}_median'.format(v2)]
    temp['{}_ste'.format(v2)] = temp['{}_std'.format(v2)] / (np.sqrt(temp["{}_count".format(v2)]))
    temp['{}_zscore'.format(v2)] = temp['{}_meanmediandiff'.format(v2)] / temp['{}_ste'.format(v2)] + .5808 #<- Corretion factor
    return temp

data1 = calc('democratshare','d')
data2 = calc('republicanshare','r')

# Merging on republican z-scores
data_summary = pd.merge(data1,data2[['r_zscore']],left_index=True,right_index=True)
data_summary = data_summary.dropna(subset=['d_zscore','r_zscore'])


# If the democrats were disadvantaged by mean, median difference, we want to take the republican z-score.
# And vice-versa for the republicans. 

data_summary['final_z'] = data_summary['d_zscore']
mask = data_summary['d_meanmediandiff'] >0
data_summary['final_z'][mask] = data_summary['r_zscore']

# Identifying which party is advantaged
data_summary['swing'] = 'Dem'
mask = data_summary['d_meanmediandiff'] >0 
data_summary['swing'][mask] = 'GOP'

mask = data_summary['d_meanmediandiff'] == 0 
data_summary['swing'][mask] = 'Neither'

data_summary = data_summary.reset_index()

# Scaling z-scores so they are easier to understand

scaler = MinMaxScaler()
data_summary['Score'] = 1 - (scaler.fit_transform(data_summary[['final_z']]))

# Plotting
data_summary = data_summary.sort_values('Score',ascending=False)
ax = sns.barplot(x='Score',y='state',hue='swing',data=data_summary,dodge=False,orient="h")
ax.figure.set_figheight(10)



