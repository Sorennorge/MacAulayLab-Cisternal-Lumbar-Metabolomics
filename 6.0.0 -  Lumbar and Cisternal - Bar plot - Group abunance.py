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
sns.set(font_scale=2)
sns.set_style("white")
# create -5pt offset in x direction
from matplotlib.transforms import ScaledTranslation


## Folders ##
Folder1 = "Data/Enrichment data/Cisternal group & Lumbar Weighted"
Folder2 = "Results/Abundance/Group barplot"
os.makedirs(Folder2,exist_ok=True)

## Files ##
File1 = "Group Cisternal - Weighted data without outliers.xlsx"
File2 = "Group Lumbar - Weighted data without outliers.xlsx"
bar_file = "Abundance bar plot.png"
overview_file = "Bar chart overview - Cisternal vs lumbar.xlsx"

## load data ##

df_cis = pd.read_excel(os.path.join(Folder1,File1))
df_cis = df_cis.drop(['Mean'], axis=1)

df_lum = pd.read_excel(os.path.join(Folder1,File2))
df_lum = df_lum.drop(['Mean'], axis=1)


stacked_lum = df_lum.set_index('Groups').stack().reset_index()
stacked_lum = stacked_lum.drop(['level_1'], axis=1).rename(columns={0:"Values"})
stacked_lum['State'] = "Lumbar"

stacked_cis = df_cis.set_index('Groups').stack().reset_index()
stacked_cis = stacked_cis.drop(['level_1'], axis=1).rename(columns={0:"Values"})
stacked_cis['State'] = "Cisternal"
df_data = pd.concat([stacked_cis,stacked_lum],ignore_index=True)

## Calculate significance ##

df_lum_T = df_lum.set_index('Groups').T.reset_index(drop=True)
df_cis_T = df_cis.set_index('Groups').T.reset_index(drop=True)
df_cis_T['Group'] = "Cisternal"
df_lum_T['Group'] = "Lumbar"
df_data_combined = pd.concat([df_cis_T,df_lum_T],axis=0,ignore_index=True)

col_names = df_data_combined.columns.values.tolist()[:-1]

cis_df = df_data_combined[df_data_combined['Group'] == 'Cisternal']
Lumbar_df = df_data_combined[df_data_combined['Group'] == 'Lumbar']

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

P_value_dict = {}
mean_cis_dict = {}
SEM_cis_dict = {}
mean_lum_dict = {}
SEM_lum_dict = {}
P_value_dict_sig = {}
for metabolite_group in col_names:
    cis_values = np.array(cis_df[metabolite_group].to_list(),dtype=float)
    Lumbar_values = np.array(Lumbar_df[metabolite_group].to_list(),dtype=float)
    stat, pvalue = scipy.stats.ttest_ind(Lumbar_values,cis_values,equal_var = False)
    mean_cis = np.mean(cis_values)
    mean_Lumbar = np.mean(Lumbar_values)
    SEM_cis = stats.sem(cis_values,ddof=1)
    SEM_Lumbar = stats.sem(Lumbar_values,ddof=1)
    P_value_dict[metabolite_group] = pvalue
    P_value_dict_sig[metabolite_group] = convert_pvalue_to_asterisks(pvalue)
    mean_cis_dict[metabolite_group] = mean_cis
    SEM_cis_dict[metabolite_group] = SEM_cis
    mean_lum_dict[metabolite_group] = mean_Lumbar
    SEM_lum_dict[metabolite_group] = SEM_Lumbar

df_overview = df_cis[['Groups']].copy()
df_overview['Cisternal mean'] = df_overview.Groups.map(mean_cis_dict)
df_overview['Cisternal SEM'] = df_overview.Groups.map(SEM_cis_dict)
df_overview['Lumbar mean'] = df_overview.Groups.map(mean_lum_dict)
df_overview['Lumbar SEM'] = df_overview.Groups.map(SEM_lum_dict)
df_overview['Pvalue'] = df_overview.Groups.map(P_value_dict)
df_overview['Significance'] = df_overview.Groups.map(P_value_dict_sig)


plt.figure(figsize=(14,8))
p1 = sns.barplot(data=df_data, x="Groups", y="Values",
                 hue="State",
                 palette = ['steelblue','aliceblue'],
                 estimator=np.mean,
                 errorbar=('ci', 68),
                 capsize=.1,
                 errcolor = 'black',
                 errwidth=2.1,
                 linewidth=2,
                 width=0.75,
                 edgecolor="black") #bootstrap ci 68% is SEM
plt.xticks(rotation=45,ha='right',va='center',rotation_mode='anchor',)
plt.ylabel('Lipid concentration (a.u.)')
plt.xlabel('')
plt.legend(bbox_to_anchor=(0.95, 0.1), loc='center left')
p1.legend_.set_title(None)
p1.legend_.set_frame_on(False)
sns.despine(top=True, right=True, left=False, bottom=False)
p1.yaxis.set_ticks_position('left')

font_size = 30


# Cholesteryl esters (0) #
i = 0
y = 2.1
Sig = df_overview.loc[df_overview['Groups'] == col_names[0], 'Significance'].values[0]
plt.plot([i-0.35,i+0.35],[y,y],'black',linewidth=2)
plt.text(i,y,"{}".format(Sig),fontsize = font_size,ha='center', va='center')
# Platelet-activating factors (1) #
i = 1
y = 2.05
Sig = df_overview.loc[df_overview['Groups'] == col_names[1], 'Significance'].values[0]
plt.plot([i-0.35,i+0.35],[y,y],'black',linewidth=2)
plt.text(i,y,"{}".format(Sig),fontsize = font_size,ha='center', va='center')
i = 2
y = 2.05
# Plasmenylphosphatidylcholines (2) #
Sig = df_overview.loc[df_overview['Groups'] == col_names[2], 'Significance'].values[0]
plt.plot([i-0.35,i+0.35],[y,y],'black',linewidth=2)
plt.text(i,y,"{}".format(Sig),fontsize = font_size,ha='center', va='center')
# Sphingomyelines (3) #
i = 3
y = 1.9
Sig = df_overview.loc[df_overview['Groups'] == col_names[i], 'Significance'].values[0]
plt.plot([i-0.35,i+0.35],[y,y],'black',linewidth=2)
plt.text(i,y,"{}".format(Sig),fontsize = font_size,ha='center', va='center')
# Ceramides (4) #
i = 4
y = 1.7
Sig = df_overview.loc[df_overview['Groups'] == col_names[i], 'Significance'].values[0]
plt.plot([i-0.35,i+0.35],[y,y],'black',linewidth=2)
plt.text(i,y,"{}".format(Sig),fontsize = font_size,ha='center', va='center')
# Phosphocholines (5) #
i = 5
y = 1.7
Sig = df_overview.loc[df_overview['Groups'] == col_names[i], 'Significance'].values[0]
plt.plot([i-0.35,i+0.35],[y,y],'black',linewidth=2)
plt.text(i,y,"{}".format(Sig),fontsize = font_size,ha='center', va='center')
# Amides (6) #
i = 6
y = 1.7
Sig = df_overview.loc[df_overview['Groups'] == col_names[i], 'Significance'].values[0]
plt.plot([i-0.35,i+0.35],[y,y],'black',linewidth=2)
plt.text(i,y,"{}".format(Sig),fontsize = font_size,ha='center', va='center')
# Phosphatidylcholines (7) #
i = 7
y = 1.7
Sig = df_overview.loc[df_overview['Groups'] == col_names[i], 'Significance'].values[0]
plt.plot([i-0.35,i+0.35],[y,y],'black',linewidth=2)
plt.text(i,y,"{}".format(Sig),fontsize = font_size,ha='center', va='center')
# Phosphatidylserines (8) #
i = 8
y = 1.6
Sig = df_overview.loc[df_overview['Groups'] == col_names[i], 'Significance'].values[0]
plt.plot([i-0.35,i+0.35],[y,y],'black',linewidth=2)
plt.text(i,y,"{}".format(Sig),fontsize = font_size,ha='center', va='center')
# Phosphatidylethanolamines (9) #
i = 9
y = 1.6
Sig = df_overview.loc[df_overview['Groups'] == col_names[i], 'Significance'].values[0]
plt.plot([i-0.35,i+0.35],[y,y],'black',linewidth=2)
plt.text(i,y,"{}".format(Sig),fontsize = font_size,ha='center', va='center')
# Lysophosphatidylcholines (10) #
i = 10
y = 1.6
Sig = df_overview.loc[df_overview['Groups'] == col_names[i], 'Significance'].values[0]
plt.plot([i-0.35,i+0.35],[y,y],'black',linewidth=2)
plt.text(i,y,"{}".format(Sig),fontsize = font_size,ha='center', va='center')
# Plasmenylphosphatidylethaolamines (11) #
i = 11
y = 1.3
Sig = df_overview.loc[df_overview['Groups'] == col_names[i], 'Significance'].values[0]
plt.plot([i-0.35,i+0.35],[y,y],'black',linewidth=2)
plt.text(i,y+0.05,"{}".format(Sig),fontsize = font_size-10,ha='center', va='center')
# Triacylglycerols (12) #
i = 12
y = 1.3
Sig = df_overview.loc[df_overview['Groups'] == col_names[i], 'Significance'].values[0]
plt.plot([i-0.35,i+0.35],[y,y],'black',linewidth=2)
plt.text(i,y,"{}".format(Sig),fontsize = font_size,ha='center', va='center')
# Fatty acids (13) #
i = 13
y = 1.1
Sig = df_overview.loc[df_overview['Groups'] == col_names[i], 'Significance'].values[0]
plt.plot([i-0.35,i+0.35],[y,y],'black',linewidth=2)
plt.text(i,y,"{}".format(Sig),fontsize = font_size,ha='center', va='center')
# Phosphatidic acids (14) #
i = 14
y = 1.0
Sig = df_overview.loc[df_overview['Groups'] == col_names[i], 'Significance'].values[0]
plt.plot([i-0.35,i+0.35],[y,y],'black',linewidth=2)
plt.text(i,y,"{}".format(Sig),fontsize = font_size,ha='center', va='center')
# Monoacrylglycerols (15) #
i = 15
y = 0.9
Sig = df_overview.loc[df_overview['Groups'] == col_names[i], 'Significance'].values[0]
plt.plot([i-0.35,i+0.35],[y,y],'black',linewidth=2)
plt.text(i,y+0.05,"{}".format(Sig),fontsize = font_size-10,ha='center', va='center')
# Small group collection (16) #
i = 16
y = 1.4
Sig = df_overview.loc[df_overview['Groups'] == col_names[i], 'Significance'].values[0]
plt.plot([i-0.35,i+0.35],[y,y],'black',linewidth=2)
plt.text(i,y,"{}".format(Sig),fontsize = font_size,ha='center', va='center')

plt.savefig(os.path.join(Folder2,bar_file),dpi=1200,bbox_inches='tight')
plt.show()

df_overview.to_excel(os.path.join(Folder2,overview_file),index=False)
