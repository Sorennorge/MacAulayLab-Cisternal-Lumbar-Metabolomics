# -*- coding: utf-8 -*-

### Create weigted data for enrichment analysis ###

## Need normalized data ## -> coming from a later script ##

import os
import pandas as pd


## Folders ##

Folder1 = "Data/Meta data"
Folder2 = "Data/Normalized data"
Folder3 = "Data/Enrichment data/Cisternal group"
Folder4 = "Data/Enrichment data/Cisternal group & Lumbar Weighted"
os.makedirs(Folder4,exist_ok=True)
## Files ##

File1 = "Meta_data_groups.xlsx"
File_norm_Cisternal = "Group Cisternal Normalized data.xlsx"
File_norm_Lumbar = "Group Lumbar Normalized data.xlsx"
File_norm_Cisternal_wo_outliers = "Group Cisternal Normalized data without outliers.xlsx"
File_norm_Lumbar_wo_outliers = "Group Lumbar Normalized data without outliers.xlsx"


File_out_1 = "Group Cisternal - Weighted data.xlsx"
File_out_2 = "Group Lumbar - Weighted data.xlsx"

File_out_3 = "Group Cisternal - Weighted data without outliers.xlsx"
File_out_4 = "Group Lumbar - Weighted data without outliers.xlsx"


## Load color scheme and create color mapping ##
Color_file = "Color_scheme_groups.csv"
df_color = pd.read_csv(os.path.join(Folder1,Color_file),sep=";")
Color_mapping = dict(df_color[['Groups', 'Colors']].values)

## Load meta data ##

df_meta = pd.read_excel(os.path.join(Folder1,File1))
df_meta = df_meta.loc[df_meta['LOI'] == "Yes"]
df_meta_mapping = df_meta[['Compounds','Groups']].set_index('Compounds')

### With outliers ###

## Load data ##

# Group Cisternal #
df_normalized_Cisternal = pd.read_excel(os.path.join(Folder2,File_norm_Cisternal)).rename(columns={"Unnamed: 0":"Samples"}).set_index('Samples')
df_normalized_Cisternal_T = df_normalized_Cisternal.T

# Group Lumbar #
df_normalized_Lumbar = pd.read_excel(os.path.join(Folder2,File_norm_Lumbar)).rename(columns={"Unnamed: 0":"Samples"}).set_index('Samples')
df_normalized_Lumbar_T = df_normalized_Lumbar.T

## Modify data ##
# Group Cisternal #
df_Cisternal_grouped = pd.concat([df_normalized_Cisternal_T,df_meta_mapping],join="inner",axis=1)
df_Cisternal_mean = df_Cisternal_grouped.groupby('Groups').mean()

# Group Lumbar #

df_Lumbar_grouped = pd.concat([df_normalized_Lumbar_T,df_meta_mapping],join="inner",axis=1)
df_Lumbar_mean = df_Lumbar_grouped.groupby('Groups').mean()

## mean data ##

# Group Cisternal #
df_Cisternal_mean['Mean'] = df_Cisternal_mean.mean(axis=1)
df_Cisternal_mean = df_Cisternal_mean.reset_index()

# Group Lumbar #
df_Lumbar_mean['Mean'] = df_Lumbar_mean.mean(axis=1)
df_Lumbar_mean = df_Lumbar_mean.reset_index()

### Cisternal Group ###
df_Cisternal_mean_sorted_mean = df_Cisternal_mean.sort_values(by=['Mean'],ascending=False,ignore_index=True)
idx_Cisternal = df_Cisternal_mean_sorted_mean.index.tolist()
pop_index_Cisternal = df_Cisternal_mean_sorted_mean.index[df_Cisternal_mean_sorted_mean['Groups']=='Small group collection'].tolist()[0]
idx_Cisternal.pop(pop_index_Cisternal)
df_Cisternal_mean_sorted_mean = df_Cisternal_mean_sorted_mean.reindex(idx_Cisternal+[pop_index_Cisternal]).reset_index(drop=True)
df_Cisternal_mean_sorted_mean.to_excel(os.path.join(Folder4,File_out_1),index=False)

### D Group ###
df_Lumbar_mean_sorted_mean = df_Lumbar_mean.sort_values(by=['Mean'],ascending=False,ignore_index=True)
idx_Lumbar = df_Lumbar_mean_sorted_mean.index.tolist()
pop_index_Lumbar = df_Lumbar_mean_sorted_mean.index[df_Lumbar_mean_sorted_mean['Groups']=='Small group collection'].tolist()[0]
idx_Lumbar.pop(pop_index_Lumbar)
df_Lumbar_mean_sorted_mean = df_Lumbar_mean_sorted_mean.reindex(idx_Lumbar+[pop_index_Lumbar]).reset_index(drop=True)
df_Lumbar_mean_sorted_mean.to_excel(os.path.join(Folder4,File_out_2),index=False)

### Without outliers ###

## Load data ##

# Group Cisternal #
df_normalized_Cisternal_wo = pd.read_excel(os.path.join(Folder2,File_norm_Cisternal_wo_outliers)).rename(columns={"Sample number":"Samples"}).set_index('Samples')
df_normalized_Cisternal_T_wo = df_normalized_Cisternal_wo.T

# Group D #
df_normalized_Lumbar_wo = pd.read_excel(os.path.join(Folder2,File_norm_Lumbar_wo_outliers)).rename(columns={"Sample number":"Samples"}).set_index('Samples')
df_normalized_Lumbar_T_wo = df_normalized_Lumbar_wo.T
## Modify data ##


# Group C #
df_Cisternal_grouped_wo = pd.concat([df_normalized_Cisternal_T_wo,df_meta_mapping],join="inner",axis=1)
df_Cisternal_mean_wo = df_Cisternal_grouped_wo.groupby('Groups').mean()

# Group Lumbar #

df_Lumbar_grouped_wo = pd.concat([df_normalized_Lumbar_T_wo,df_meta_mapping],join="inner",axis=1)
df_Lumbar_mean_wo = df_Lumbar_grouped_wo.groupby('Groups').mean()

## mean data ##

# Group Cisternal #
df_Cisternal_mean_wo['Mean'] = df_Cisternal_mean_wo.mean(axis=1)
df_Cisternal_mean_wo = df_Cisternal_mean_wo.reset_index()

# Group Lumbar #
df_Lumbar_mean_wo['Mean'] = df_Lumbar_mean_wo.mean(axis=1)
df_Lumbar_mean_wo = df_Lumbar_mean_wo.reset_index()

### Cisternal Group ###
df_Cisternal_mean_sorted_mean_wo = df_Cisternal_mean_wo.sort_values(by=['Mean'],ascending=False,ignore_index=True)
idx_Cisternal_wo = df_Cisternal_mean_sorted_mean_wo.index.tolist()
pop_index_Cisternal_wo = df_Cisternal_mean_sorted_mean_wo.index[df_Cisternal_mean_sorted_mean_wo['Groups']=='Small group collection'].tolist()[0]
idx_Cisternal_wo.pop(pop_index_Cisternal_wo)
df_Cisternal_mean_sorted_mean_wo = df_Cisternal_mean_sorted_mean_wo.reindex(idx_Cisternal_wo+[pop_index_Cisternal_wo]).reset_index(drop=True)
df_Cisternal_mean_sorted_mean_wo.to_excel(os.path.join(Folder4,File_out_3),index=False)

### Lumbar Group ###
df_Lumbar_mean_sorted_mean_wo = df_Lumbar_mean_wo.sort_values(by=['Mean'],ascending=False,ignore_index=True)
idx_Lumbar_wo = df_Lumbar_mean_sorted_mean_wo.index.tolist()
pop_index_Lumbar_wo = df_Lumbar_mean_sorted_mean_wo.index[df_Lumbar_mean_sorted_mean_wo['Groups']=='Small group collection'].tolist()[0]
idx_Lumbar_wo.pop(pop_index_Lumbar_wo)
df_Lumbar_mean_sorted_mean_wo = df_Lumbar_mean_sorted_mean_wo.reindex(idx_Lumbar_wo+[pop_index_Lumbar_wo]).reset_index(drop=True)
df_Lumbar_mean_sorted_mean_wo.to_excel(os.path.join(Folder4,File_out_4),index=False)
