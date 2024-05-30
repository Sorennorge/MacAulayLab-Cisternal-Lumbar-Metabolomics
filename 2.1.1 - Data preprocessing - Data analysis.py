# -*- coding: utf-8 -*-

### Metabolomics data analysis ###

## Libraries ##

import os
import numpy as np
import pandas as pd
import math
import statsmodels.stats.multitest as smt
from scipy.stats import gmean
from scipy.stats import ttest_ind
from outliers import smirnov_grubbs as grubbs

## input ##

DP_cutoff = 0

## Functions ##

def log2FC_func(A,B):
    FC = B/A
    log2FC = round(math.log(FC,2),4)
    return log2FC

## Folders ##

Folder0= "Data/Meta data"
Folder1 = "Data/Data cleaning"
Folder2 = "Data/Raw data analysis"
os.makedirs(Folder2, exist_ok=True)
Folder3 = "Data/PCA data/Raw"
os.makedirs(Folder3, exist_ok=True)
Folder4 = "Data/Data analysis"
os.makedirs(Folder4,exist_ok=True)
Folder5 = "Data/Normalized data"
os.makedirs(Folder5,exist_ok=True)

## Files ##

File0 = "Meta_data_groups.xlsx"
File1 = "raw_data_QC_Lumbar_Cisternal.xlsx"
File2 = "Raw_data_DP.xlsx"
File3 = "PCA_data.xlsx"
File4 = "PCA_targets.xlsx"
File6 = "DP overview.xlsx"
File7 = "Data analysis overview.xlsx"

# Normalized #
File_normalized = "Normalized data for group Lumbar and Cisternal.xlsx"
File_normalized_Lumbar = "Group Lumbar Normalized data.xlsx"
File_normalized_Cisternal = "Group Cisternal Normalized data.xlsx"
# Normalized without outliers 
File_normalized_data_wo_outliers = "Normalized data for group Lumbar and Cisternal without outliers.xlsx"
File_normalized_Lumbar_wo_outliers = "Group Lumbar Normalized data without outliers.xlsx"
File_normalized_Cisternal_wo_outliers = "Group Cisternal Normalized data without outliers.xlsx"

### load data ###

# Meta data #

df_groups = pd.read_excel(os.path.join(Folder0,File0))
df_groups_LOI = df_groups.loc[df_groups['LOI'] == "Yes"]
LOI_metabolite_list = df_groups_LOI['Compounds'].tolist()

df = pd.read_excel(os.path.join(Folder1,File1)).rename(columns=({'Unnamed: 0':'Compounds'}))

Header = df.columns.values.tolist()
QC_list = list(filter(lambda x: x.startswith('QC_'), Header))
Group_Lumbar_list = list(filter(lambda x: x.startswith("Lumbar_"), Header))
Group_Cisternal_list = list(filter(lambda x: x.startswith("Cisternal_"), Header))

# Modulate data for dict conversion #

df = df.set_index('Compounds')
Info_dict_QC = dict(zip(df.index, df[QC_list].values))
Info_dict_Lumbar = dict(zip(df.index, df[Group_Lumbar_list].values))
Info_dict_Cisternal = dict(zip(df.index, df[Group_Cisternal_list].values))

Compounds = df.index.tolist()

## Calculate raw descriptive power (DP) ##
Raw_DP_dict = {}
RAW_STD_dict_QC = {}
RAW_STD_dict_Samples = {}
Raw_Significant_metabolite_list = []
# Find DP of raw data and list of significant Compounds -> #
for key in Compounds:
    Group_Lumbar_and_Cisternal_concatenated = np.concatenate((Info_dict_Lumbar[key], Info_dict_Cisternal[key]), axis=None)
    Raw_DP = np.std(Group_Lumbar_and_Cisternal_concatenated,ddof=1)/np.std(Info_dict_QC[key],ddof=1)
    Raw_DP_dict[key] = Raw_DP
    RAW_STD_dict_Samples[key] = np.std(Group_Lumbar_and_Cisternal_concatenated,ddof=1)/np.mean(Info_dict_QC[key])
    RAW_STD_dict_QC[key] = np.std(Info_dict_QC[key],ddof=1)/np.mean(Info_dict_QC[key])
    if Raw_DP > DP_cutoff:
        if key in LOI_metabolite_list:
            Raw_Significant_metabolite_list.append(key)
        else:
            pass
        #Raw_Significant_metabolite_list.append(key)
    else:
        pass
  
# create dataframe from DP values (raw) #
raw_df_DP = pd.DataFrame({'Compounds': list(Raw_DP_dict.keys()),'DP':list(Raw_DP_dict.values()),'std samples':list(RAW_STD_dict_Samples.values()),'std QC':list(RAW_STD_dict_QC.values())})

raw_df_DP['Significance'] = np.where(raw_df_DP['DP'] >= DP_cutoff, "Yes", "No")

raw_df_DP.to_excel(os.path.join(Folder2,File2),sheet_name='Raw DP calc',header=True,index=False)

## Create PCA plot tables ##

df_without_QC = df[Group_Lumbar_list+Group_Cisternal_list]
# transpose data for correct PCA annotation #
PCA_df_T = df_without_QC.T
# Only include Compounds with DP > 0 #
PCA_df = PCA_df_T.loc[:, PCA_df_T.columns.isin(Raw_Significant_metabolite_list)]

PCA_targets = pd.DataFrame(index=PCA_df.index.copy())
PCA_targets['Samples'] = PCA_targets.index
PCA_targets.loc[PCA_targets['Samples'].str.startswith('Lumbar_'), 'Target'] = 'Lumbar'
PCA_targets.loc[PCA_targets['Samples'].str.startswith('Cisternal_'), 'Target'] = 'Cisternal'


PCA_df.to_excel(os.path.join(Folder3,File3),sheet_name='PCA data',header=False,index=False)
PCA_targets.to_excel(os.path.join(Folder3,File4),sheet_name='PCA Targets',header=False,index=False)

## For PCA plot ##
# Run script 3.1.2 - PCA plots for raw data #

## Normalize data for Compounds DP > 2.5 ##
# Reduce dataframe to only Compounds with DP > 2.5 #
df_significant = df[df.index.isin(Raw_Significant_metabolite_list)]
# Calculate geomean for Compounds
df_geomean = pd.DataFrame(index=df_significant.index.copy())
df_geomean['geomean'] = gmean(df_significant.iloc[:, df_significant.columns.get_indexer(QC_list)], axis=1)

# Normalize data based on geomean #
DF_normalized = df_significant.loc[:,Group_Lumbar_list+Group_Cisternal_list].div(df_geomean["geomean"], axis=0)
## Remove outliers
DF_normalized_without_outliers =  DF_normalized.copy()

## Save normalized data to files ##

DF_normalized_all_T = DF_normalized.reset_index().rename(columns=({"Compounds":"Samples"})).set_index('Samples').T
DF_normalized_all_T.to_excel(os.path.join(Folder5,File_normalized),sheet_name='Normalized data',index=False)

# Divide normalized data into two seperate files #

DF_normalized_all_T_Lumbar = DF_normalized_all_T.T[Group_Lumbar_list].T
DF_normalized_all_T_Cisternal = DF_normalized_all_T.T[Group_Cisternal_list].T

DF_normalized_all_T_Lumbar.to_excel(os.path.join(Folder5,File_normalized_Lumbar),sheet_name='Normalized data Lumbar')
DF_normalized_all_T_Cisternal.to_excel(os.path.join(Folder5,File_normalized_Cisternal),sheet_name='Normalized data Cisternal')


index_list = DF_normalized.index
column_list = np.array(DF_normalized.columns.tolist())
counter = 0
for i in DF_normalized.index:
    # Get array for Cisternal (C) and Disease (D)
    numpy_array_Lumbar = np.array(DF_normalized.loc[i,Group_Lumbar_list])
    numpy_array_Cisternal = np.array(DF_normalized.loc[i,Group_Cisternal_list])
    # Get outlier index #
    outlier_index_Lumbar =  grubbs.two_sided_test_indices(numpy_array_Lumbar, alpha=.05)
    outlier_index_Lumbar = np.array(outlier_index_Lumbar,dtype=int)
    outlier_index_Cisternal =  grubbs.two_sided_test_indices(numpy_array_Cisternal, alpha=.05)
    outlier_index_Cisternal = np.array(outlier_index_Cisternal,dtype=int)
    outlier_index_Cisternal = (outlier_index_Cisternal + len(Group_Lumbar_list))
    all_entries = np.concatenate((outlier_index_Lumbar,outlier_index_Cisternal), axis=0)
    if len(all_entries) > 0:
        #print(all_entries)
        cols = column_list[all_entries].tolist()
        #print(cols)
        for loc_col in cols:
            DF_normalized_without_outliers.at[i,loc_col] = np.nan
        #print(i)


# Transpose normalized data #
# Here without outliers #!!! 
DF_normalized_T = DF_normalized_without_outliers.T.copy()
DF_normalized_T = DF_normalized_T.reset_index().rename(columns=({'index':"Sample number"}))
# Save normalized - transposed data to file #
DF_normalized_T.to_excel(os.path.join(Folder5,File_normalized_data_wo_outliers),sheet_name='Normalized data',index=False)

## Divide normalized data into two seperate files ##

DF_normalized_T_Lumbar = DF_normalized_T.set_index('Sample number').T[Group_Lumbar_list].T
DF_normalized_T_Cisternal = DF_normalized_T.set_index('Sample number').T[Group_Cisternal_list].T

DF_normalized_T_Lumbar.to_excel(os.path.join(Folder5,File_normalized_Lumbar_wo_outliers),sheet_name='Normalized data Lumbar')
DF_normalized_T_Cisternal.to_excel(os.path.join(Folder5,File_normalized_Cisternal_wo_outliers),sheet_name='Normalized data Cisternal')
                          

## Create overview table - without outliers ##

df_overview = DF_normalized_without_outliers.reset_index()[['Compounds']].copy()
df_overview = df_overview.set_index('Compounds')
## Add Mean and SD to overview ##
# Group Lumbar #
df_overview["Group Lumbar Mean"] = DF_normalized_without_outliers[Group_Lumbar_list].mean(axis=1)
df_overview["Group Lumbar SEM"] = DF_normalized_without_outliers[Group_Lumbar_list].sem(axis=1,ddof=1)
# Group Cisternal #
df_overview["Group Cisternal Mean"] = DF_normalized_without_outliers[Group_Cisternal_list].mean(axis=1)
df_overview["Group Cisternal SEM"] = DF_normalized_without_outliers[Group_Cisternal_list].sem(axis=1,ddof=1)


# Add Log2FC #
df_overview["Log2FC"] = np.log2(df_overview["Group Cisternal Mean"]/df_overview["Group Lumbar Mean"])
## add p-value of welch t test #
df_overview['Pvalue'] = ttest_ind(DF_normalized_without_outliers[Group_Cisternal_list], DF_normalized_without_outliers[Group_Lumbar_list],nan_policy='omit',equal_var = False, axis=1)[1]
df_overview['Padj'] = smt.fdrcorrection(df_overview['Pvalue'],alpha=0.05,method="indep")[1]

## Save overview table to file ###
df_overview = df_overview.reset_index()
df_overview.to_excel(os.path.join(Folder4,File7),sheet_name='Overview',header=True,index=False)
