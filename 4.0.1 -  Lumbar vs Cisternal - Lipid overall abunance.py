# -*- coding: utf-8 -*-

### Bar chart group C and D ###

## Libraries ##

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import scipy
from scipy import stats
sns.set(font_scale=2.3)
sns.set_style("white")

## Folders ##
Folder1 = "Data/Enrichment data/Cisternal group & Lumbar Weighted"
Folder2 = "Results/Abundance/Group barplot"
os.makedirs(Folder2,exist_ok=True)

## Files ##
File1 = "Group Cisternal - Weighted data without outliers.xlsx"
File2 = "Group Lumbar - Weighted data without outliers.xlsx"
bar_file = "Overall abundance bar plot Cisternal vs Lumbar.png"

## load data ##

df_cis = pd.read_excel(os.path.join(Folder1,File1))


df_cis = df_cis.drop(['Mean'], axis=1)
df_cis_T = df_cis.set_index('Groups').T
df_cis_T['Mean'] = df_cis_T.mean(axis=1)
df_cis_mean = df_cis_T['Mean'].to_frame()
df_cis_mean['Group'] = "Cisternal"

df_lum = pd.read_excel(os.path.join(Folder1,File2))

df_lum = df_lum.drop(['Mean'], axis=1)
df_lum_T = df_lum.set_index('Groups').T
df_lum_T['Mean'] = df_lum_T.mean(axis=1)
df_lum_mean = df_lum_T['Mean'].to_frame()
df_lum_mean['Group'] = "Lumbar"

df_data = pd.concat([df_cis_mean,df_lum_mean],ignore_index=True)



Cisternal_values = np.array(df_cis_mean['Mean'].to_list(),dtype=float)
Lumbar_values = np.array(df_lum_mean['Mean'].to_list(),dtype=float)
stat, pvalue = scipy.stats.ttest_ind(Lumbar_values,Cisternal_values,equal_var = False)


def convert_pvalue_to_asterisks(pvalue):
    if pvalue <= 0.0001:
        return "****"
    elif pvalue <= 0.001:
        return "***"
    elif pvalue <= 0.01:
        return "**"
    elif pvalue <= 0.05:
        return "*"
    return "ns"

# Calculate mean and confidence intervals
def mean_ci(data, confidence=0.68):
    mean = np.mean(data)
    n = len(data)
    sem = stats.sem(data)
    h = sem * stats.t.ppf((1 + confidence) / 2., n-1)
    return mean, mean-h, mean+h

summary_stats = df_data.groupby('Group')['Mean'].apply(mean_ci).apply(pd.Series)
summary_stats.columns = ['Mean', 'CI Lower', 'CI Upper']

print(summary_stats)

plt.figure(figsize=(3,8))
p1 = sns.barplot(data=df_data, x="Group", y="Mean",
                 palette = ['steelblue','aliceblue'],
                 estimator=np.mean,
                 errorbar=('ci', 68),
                 capsize=.1,
                 errcolor = 'black',
                 errwidth=2.1,
                 linewidth=2,
                 width=0.6,
                 edgecolor="black")
                 #) #bootstrap ci 68% is SEM
#plt.xticks(['Cisternal, Lumbar'])
plt.xticks(rotation=45,ha='right',rotation_mode='anchor')
plt.ylabel('Lipid concentration (a.u.)')
plt.xlabel('')
plt.ylim([0,1.5])
sns.despine(top=True, right=True, left=False, bottom=False)
p1.spines['left'].set_linewidth(2)
p1.spines['bottom'].set_linewidth(2)

p1.yaxis.set_ticks_position('left')
p1.yaxis.set_label_coords(-0.35,0.5)
plt.text(0.3,1.4,"{}".format(convert_pvalue_to_asterisks(pvalue)),fontsize = 50)
plt.plot([1.45,1.45],'black',linewidth=2)
plt.savefig(os.path.join(Folder2,bar_file),dpi=1200,bbox_inches='tight')
plt.show()