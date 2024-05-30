# -*- coding: utf-8 -*-

### Data analysis - Outlier test for whole samples ###

## Requirements ##
# Raw data - Metabolomics #

## Libraries ##

import os
import pandas as pd
from outliers import smirnov_grubbs as grubbs
from natsort import natsort_keygen

## Global counter variable ##

Lumbar_counter = 0
Cisternal_counter = 0

## functions ##

def rewrite_samples(df):
    global Lumbar_counter
    global Cisternal_counter
    condition = df['Label']
    if condition == 'Lumbar':
        Lumbar_counter += 1
        return "{}_{}".format(condition,Lumbar_counter)
    elif condition == 'Cisternal':
        Cisternal_counter += 1
        return "{}_{}".format(condition,Cisternal_counter)
    else:
        return df['Samples']

## Folders ##
# input #
Folder1 = "Data/Raw data"

# output #

Folder2 = "Data/Lookup data"
Folder3 = "Data/Data cleaning"

os.makedirs(Folder2,exist_ok=True)
os.makedirs(Folder3,exist_ok=True)

##  Files ##

# Input #
file1_input = "Raw_data.xlsx"

# output #

file2_init_sample_lookup_file = "Initial_Sample_lookup_table.xlsx"
file3_init_outliers_overview = 'Outliers overview.xlsx'

file4_raw_data_without_outliers = "raw_data_QC_Lumbar_Cisternal.xlsx"

# Load data #

df_init = pd.read_excel(os.path.join(Folder1,file1_input))


df_init['Sample number'] = df_init.apply(rewrite_samples,axis=1)

df_correct_anno = df_init[['Samples','Label','Sample number']]

# Save initial lookup sample number #

df_correct_anno.to_excel(os.path.join(Folder2,file2_init_sample_lookup_file),index=False)

## Set sample number to index and remove Samples and diagnosis ##

df_init = df_init.set_index('Sample number').drop('Samples',axis=1).drop('Label',axis=1)

## Transpose dataframe ##

df_init_T = df_init.T

## Sample lists ##

QC_list = df_init_T.columns[df_init_T.columns.str.startswith("QC")].to_list()
Lumbar_list = df_init_T.columns[df_init_T.columns.str.startswith("Lumbar")].to_list()
Cisternal_list = df_init_T.columns[df_init_T.columns.str.startswith("Cisternal")].to_list()


## init variables ##

# initial data variables for data cleaning #

init_Name_list = df_init_T.index.tolist()

# create dictionaries with numpy arrays #
init_QC_dict = dict(zip(df_init_T.index, df_init_T[QC_list].values))
init_Group_Lumbar_dict = dict(zip(df_init_T.index, df_init_T[Lumbar_list].values))
init_Group_Cisternal_dict = dict(zip(df_init_T.index, df_init_T[Cisternal_list].values))

# Outlier calculations #

Group_Lumbar_without_outliers = {}
Group_Cisternal_without_outliers = {}


## create dictionaries with numpy arrays ##

## run grubbs test for outliers in initial raw data ##

outlier_overview_Lumbar = {}
outlier_overview_Cisternal = {}

for key in init_Name_list:
    ## remove outliers ##
    Group_Lumbar_without_outliers[key] = grubbs.test(init_Group_Lumbar_dict[key], alpha=.05)
    Group_Cisternal_without_outliers[key] = grubbs.test(init_Group_Cisternal_dict[key], alpha=.05)
    
    ## Get outlier index and and create overview of which samples have outliers ##
    outlier_index_Lumbar = grubbs.two_sided_test_indices(init_Group_Lumbar_dict[key], alpha=.05)
    outlier_index_Cisternal = grubbs.two_sided_test_indices(init_Group_Cisternal_dict[key], alpha=.05)
    ## Lumbar outliers overview ##
    for i in outlier_index_Lumbar:
        outlier_sample_Lumbar = "Lumbar_{}".format(i+1)
        if outlier_sample_Lumbar in outlier_overview_Lumbar:
            outlier_overview_Lumbar[outlier_sample_Lumbar] += 1
        else:
            outlier_overview_Lumbar[outlier_sample_Lumbar] = 1
    ## Cisternal outliers overview ##
    for i in outlier_index_Cisternal:
        outlier_sample_Cisternal = "Cisternal_{}".format(i+1)
        if outlier_sample_Cisternal in outlier_overview_Cisternal:
            outlier_overview_Cisternal[outlier_sample_Cisternal] += 1
        else:
            outlier_overview_Cisternal[outlier_sample_Cisternal] = 1
## Percentage calculateion ##
outlier_overview_percentage = {}
for key in outlier_overview_Lumbar:
    outlier_overview_percentage[key] = round(outlier_overview_Lumbar[key]/len(init_Name_list)*100,2)
for key in outlier_overview_Cisternal:
    outlier_overview_percentage[key] = round(outlier_overview_Cisternal[key]/len(init_Name_list)*100,2)   

## Create overview dataframe of outliers ##
# Lumbar #
df_outlier_overview_Lumbar = pd.DataFrame.from_dict(outlier_overview_Lumbar,orient='index',columns=['Outliers'])
df_outlier_overview_Lumbar['Percentage'] = df_outlier_overview_Lumbar.index.map(outlier_overview_percentage)
df_outlier_overview_Lumbar = df_outlier_overview_Lumbar.reset_index().rename(columns=({"index":"Samples"}))
df_outlier_overview_Lumbar = df_outlier_overview_Lumbar.sort_values(by="Samples",key=natsort_keygen()).reset_index(drop=True)

# Cisternal #
df_outlier_overview_Cisternal = pd.DataFrame.from_dict(outlier_overview_Cisternal,orient='index',columns=['Outliers'])
df_outlier_overview_Cisternal['Percentage'] = df_outlier_overview_Cisternal.index.map(outlier_overview_percentage)
df_outlier_overview_Cisternal = df_outlier_overview_Cisternal.reset_index().rename(columns=({"index":"Samples"}))
df_outlier_overview_Cisternal = df_outlier_overview_Cisternal.sort_values(by="Samples",key=natsort_keygen()).reset_index(drop=True)

df_outlier_overview = pd.concat([df_outlier_overview_Lumbar,df_outlier_overview_Cisternal],axis=0,ignore_index=True)                                                                               

df_outlier_overview.to_excel(os.path.join(Folder3,file3_init_outliers_overview),index=False)


# Exclusion of samples based on percentage of outliers within the sample #
Sample_exclusion_list = []
for key in outlier_overview_percentage:
    if outlier_overview_percentage[key] > 20:
        Sample_exclusion_list.append(key)

df_raw_without_outliers = df_init_T[df_init_T.columns[~df_init_T.columns.isin(Sample_exclusion_list)]]

## Save dataframe without outlier samples to file ##

df_raw_without_outliers.to_excel(os.path.join(Folder3,file4_raw_data_without_outliers))
