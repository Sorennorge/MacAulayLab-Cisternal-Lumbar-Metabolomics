# -*- coding: utf-8 -*-

import os
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt 
import seaborn as sns
from matplotlib.colors import to_rgba
sns.set(style="white")
sns.set(style="ticks",font_scale=1)


## Folders ##

Folder1 = "Data/PCA data/Raw"
Folder2 = "Results/PCA/Raw"

os.makedirs(Folder2, exist_ok=True)

## Files ##

file_data = "PCA_data.xlsx"
file_targets = "PCA_targets.xlsx"



### Generate PCA plots (Supplementary for each group) ###

## Libraries ##

### Generate PCA plots (Supplementary for each group) ###


## Folders ##
Folder1 = "Data/Meta data"
Folder2 = "Data/PCA data/Raw"
Folder3 = "Data/Normalized data"
Folder4 = "Data/Enrichment data/Control group"

Folder5 = "Results/PCA/Individual groups"
os.makedirs(Folder5,exist_ok=True)

## Files ##

File1 = "Meta_data_groups.xlsx"
File2 = "PCA_targets.xlsx"
File3 = "Group Cisternal Normalized data.xlsx"
File3_2 = "Group Lumbar Normalized data.xlsx"
File4 = "Enrichement_data_all_group_Control.csv"

## Load data ##

df_groups = pd.read_excel(os.path.join(Folder1,File1))

df_metadata = pd.read_excel(os.path.join(Folder2,File2),header=None)
df_metadata = df_metadata.rename(columns={0:"Sample number",1:"Target"})

df_data1 = pd.read_excel(os.path.join(Folder3,File3))
df_data1 = df_data1.rename(columns={'Unnamed: 0':"Sample number"})
df_data2 = pd.read_excel(os.path.join(Folder3,File3_2))
df_data2 = df_data2.rename(columns={'Unnamed: 0':"Sample number"})
df_data = pd.concat([df_data1, df_data2], ignore_index=True)


df_data = df_data.set_index("Sample number")
df_data_T = df_data.T
sample_list = df_data_T.columns.tolist()
# Enrichment data
df_enrichment_data_all =  pd.read_csv(os.path.join(Folder4,File4),sep=";")
# Reduce groups to group with more than one count #
df_enrichment_data_all = df_enrichment_data_all.loc[df_enrichment_data_all['Count'] > 1]
# Create lists of groups for age plots #
Group_list_all = df_enrichment_data_all['Groups'].tolist()

## Add groups to data and reduce dataframe  ##
# Create mapping directory #
Group_mapping = dict(df_groups[['Compounds', 'Groups']].values)
# add groups to dataframe #
df_data_T['Groups'] = df_data_T.index.map(Group_mapping)

## Plot PCA for each group ##

popped_item = Group_list_all.pop(-1)
Group_list_all = sorted(Group_list_all)
Group_list_all.append(popped_item)

fig = plt.figure(figsize=(8.27,11.69))

gs = fig.add_gridspec(5,4,width_ratios=[1,1,1,1],height_ratios=[1,1,1,1,1],hspace=0.8,wspace=0.8)

ax0_1 = fig.add_subplot(gs[0, 0])
ax0_2 = fig.add_subplot(gs[0, 1])
ax0_3 = fig.add_subplot(gs[0, 2])
ax0_4 = fig.add_subplot(gs[0, 3])
ax1_1 = fig.add_subplot(gs[1, 0])
ax1_2 = fig.add_subplot(gs[1, 1])
ax1_3 = fig.add_subplot(gs[1, 2])
ax1_4 = fig.add_subplot(gs[1, 3])

ax2_1 = fig.add_subplot(gs[2, 0])
ax2_2 = fig.add_subplot(gs[2, 1])
ax2_3 = fig.add_subplot(gs[2, 2])
ax2_4 = fig.add_subplot(gs[2, 3])

ax3_1 = fig.add_subplot(gs[3, 0])
ax3_2 = fig.add_subplot(gs[3, 1])
ax3_3 = fig.add_subplot(gs[3, 2])
ax3_4 = fig.add_subplot(gs[3, 3])
ax4_1 = fig.add_subplot(gs[4, 0])


plot_list = [ax0_1,
             ax0_2, 
             ax0_3, 
             ax0_4, 
             ax1_1, 
             ax1_2, 
             ax1_3, 
             ax1_4, 
             ax2_1, 
             ax2_2, 
             ax2_3, 
             ax2_4, 
             ax3_1, 
             ax3_2, 
             ax3_3, 
             ax3_4, 
             ax4_1]

i = 0

for Group in Group_list_all:
    df_data_plot = df_data_T[df_data_T['Groups'] == Group]
    del df_data_plot['Groups']
    df_data_plot_T = df_data_plot.T
    pca_data = df_data_plot_T.values
    
    # data scaling
    x_scaled = StandardScaler().fit_transform(pca_data)
    
    pca = PCA(n_components=2)
    
    pca_features = pca.fit_transform(x_scaled)
    
    pca_df = pd.DataFrame(
        data=pca_features, 
        columns=['PC1','PC2'])
    
    Variance_PC_array = pca.explained_variance_ratio_
    
    PC_1_V = int(round(Variance_PC_array[0]*100,0))
    PC_2_V = int(round(Variance_PC_array[1]*100,0))
    
    pca_df['Groups'] = df_metadata['Target']
    pca_df['Values'] = df_metadata['Sample number']
    
    sns.regplot(
        x='PC1', 
        y='PC2', 
        data=pca_df[pca_df['Groups'] == 'Cisternal'], 
        fit_reg=False, 
        color=to_rgba("steelblue"),
        scatter_kws={'linewidths':0.5,'edgecolor':'k','s':15},ax=plot_list[i])

    sns.regplot(
        x='PC1', 
        y='PC2', 
        data=pca_df[pca_df['Groups'] == 'Lumbar'], 
        fit_reg=False,
        color=to_rgba("skyblue"),
        scatter_kws={'linewidths':0.5,'edgecolor':'k','s':15},ax=plot_list[i])
    plot_list[i].set_title("PCA {}".format(i+1))
    plot_list[i].set_xlabel( "PC 1 ({} %)".format(PC_1_V))
    plot_list[i].set_ylabel( "PC 2 ({} %)".format(PC_2_V))
    plot_list[i].locator_params(axis='both', nbins=6,integer=True)
    # change all spines
    for axis in ['top','bottom','left','right']:
        plot_list[i].spines[axis].set_linewidth(0.5)
    plot_list[i].tick_params(width=0.5)
    i += 1

save = True

All_in_one = 'Supplementary Lumbar vs Cisternal PCA plots.png'
if save == True:
    plt.savefig(os.path.join(Folder5,All_in_one),dpi=1200,bbox_inches='tight')
else:
    plt.show()