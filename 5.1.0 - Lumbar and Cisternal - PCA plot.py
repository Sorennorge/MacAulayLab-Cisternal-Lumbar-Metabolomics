# -*- coding: utf-8 -*-

import os
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt 
import seaborn as sns
sns.set(style="white")
sns.set(style="ticks",font_scale=1.70)

## Folders ##

Folder1 = "Data/PCA data/Raw"
Folder2 = "Results/PCA"
os.makedirs(Folder2, exist_ok=True)

## Files ##

file_data = "PCA_data.xlsx"
file_targets = "PCA_targets.xlsx"

## Load data ##
df_data = pd.read_excel(os.path.join(Folder1,file_data),header=None)

df_targets = pd.read_excel(os.path.join(Folder1,file_targets),header=None)

# data scaling
x_scaled = StandardScaler().fit_transform(df_data)

# set principal compnents #
n = 10
pca = PCA(n_components=n)

# transport data
pca_features = pca.fit_transform(x_scaled)

columns_n = []
for i in range(1,n+1,1):
    columns_n.append("PC{}".format(i))
# create dataframe with the n PC
pca_df = pd.DataFrame(
    data=pca_features, 
    columns=columns_n)

## Variance for plot 

Variance_PC_array = pca.explained_variance_ratio_

PC_1_V = int(round(Variance_PC_array[0]*100,0))
PC_2_V = int(round(Variance_PC_array[1]*100,0))
PC_3_V = int(round(Variance_PC_array[2]*100,0))
PC_4_V = int(round(Variance_PC_array[3]*100,0))

pc_list = [PC_1_V,PC_2_V,PC_3_V,PC_4_V]
# map target names to PCA features   

pca_df['Location'] = df_targets[1]

x_pc = 1
y_pc = 2

File_out = "PCA_plot_PC{}_PC{}_legended.png".format(x_pc,y_pc)
plt.figure(figsize=(10,10))
g = sns.lmplot(
    x='PC{}'.format(x_pc), 
    y='PC{}'.format(y_pc), 
    data=pca_df, 
    hue='Location', 
    fit_reg=False, 
    legend=True,
    palette=["aliceblue","steelblue"],
    scatter_kws={'linewidths':1,'edgecolor':'k','s':100}
    )
sns.despine(top=False, right=False, left=False, bottom=False)
plt.xticks([-20,-10,0,10,20,30])
plt.yticks([-10,-5,0,5,10,15,20])
plt.xlabel( "PC {} ({} %)".format(x_pc,pc_list[x_pc-1]))
plt.ylabel( "PC {} ({} %)".format(y_pc,pc_list[y_pc-1]))
plt.savefig(os.path.join(Folder2,File_out),dpi=600,bbox_inches='tight')
plt.show()


File_out = "PCA_plot_PC{}_PC{}.png".format(x_pc,y_pc)
plt.figure(figsize=(10,10))
g = sns.lmplot(
    x='PC{}'.format(x_pc), 
    y='PC{}'.format(y_pc), 
    data=pca_df, 
    hue='Location', 
    fit_reg=False, 
    legend=False,
    palette=["aliceblue","steelblue"],
    scatter_kws={'linewidths':1,'edgecolor':'k','s':100}
    )
sns.despine(top=False, right=False, left=False, bottom=False)
plt.xticks([-20,-10,0,10,20,30])
plt.yticks([-10,-5,0,5,10,15,20])
plt.xlabel( "PC {} ({} %)".format(x_pc,pc_list[x_pc-1]))
plt.ylabel( "PC {} ({} %)".format(y_pc,pc_list[y_pc-1]))
plt.text(-14,-6,"Lumbar")
plt.text(12,5,"Cisternal")
plt.savefig(os.path.join(Folder2,File_out),dpi=1200,bbox_inches='tight')
plt.show()
    