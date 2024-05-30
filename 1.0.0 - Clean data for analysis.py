# -*- coding: utf-8 -*-

### Clean raw data for analysis ###

import os
import pandas as pd

## Global variable ##

Sample_counter = 0
QC_counter = 0

## Function ##

def Sample_anno(df):
    global Sample_counter
    global QC_counter
    if df['Group'] == 'QC':
        QC_counter += 1
        return 'QC_{}'.format(QC_counter)
    else:
        Sample_counter += 1
        return 'Sample_{}'.format(Sample_counter)
        
def Sample_anno_meta(df):
    sample = 'Sample_{}'.format(df['Sample number'])
    return sample
## Folders ##

Folder1 = "Data/Raw data"
Folder2 = "Data/Meta data"

## Files ##

file1_input = "Viime 2_v2.csv"
file_meta = "Patient_meta_data_lumbar_vs_cisternal.xlsx"

# Output #

File_out_1 = "Raw_data_full.xlsx"
File_out_2 = "Raw_data.xlsx"
File_out_3 = "Raw_data_transposed.xlsx"

## Load data ##

df_raw = pd.read_csv(os.path.join(Folder1,file1_input),sep=";")
df_raw_control = df_raw[(df_raw['Group'] == 'QC') | (df_raw['Group'] == 'Gruppe B') | (df_raw['Group'] == 'Gruppe C')].copy()

# Load meta data #

df_meta_data = pd.read_excel(os.path.join(Folder2,file_meta))

## add samples to Control ##

df_raw_control['Samples'] = df_raw_control.apply(Sample_anno,axis=1)

# Rearrange columns #

Control_cols = list(df_raw_control.columns.values)
list_rearangement = ['Name','Group','Samples']
for key in list_rearangement:
    Control_cols.pop(Control_cols.index(key))

df_raw_control = df_raw_control[list_rearangement+Control_cols]

df_QC =  df_raw_control[(df_raw_control['Group'] == 'QC')]

df_QC_meta = df_QC[['Samples']].copy()
df_QC_meta['Label'] = 'QC'

# add samples column to meta data #

#df_meta_data['Samples'] = df_meta_data.apply(Sample_anno_meta,axis=1)

df_meta_data_apply = df_meta_data[['Samples','Label']].copy()

df_meta_data_apply_merged = pd.concat([df_QC_meta,df_meta_data_apply],axis=0)

## Correct annotation for samples ##

df_raw_control.loc[df_raw_control['Group'] == 'QC', 'Name'] = df_raw_control['Samples']

df_Control_full = pd.concat([df_meta_data_apply_merged.set_index('Samples'),df_raw_control.set_index('Name')],join='inner',axis=1)

# Rearrange columns #

Control_cols_full = list(df_Control_full.columns.values)

list_rearangement_full = ['Samples','Group','Label']

for key in list_rearangement_full:
    Control_cols_full.pop(Control_cols_full.index(key))

df_Control_full = df_Control_full[list_rearangement_full+Control_cols_full]
df_Control_full = df_Control_full.reset_index().set_index("Samples").rename(columns={'index':"Sample_name"})
## Save raw Control dataframe to file ##

df_Control_full.to_excel(os.path.join(Folder1,File_out_1))

df_Control = df_Control_full.copy()

df_Control = df_Control.drop(['Sample_name', 'Group'], axis=1)
df_Control = df_Control.reset_index()

## Save Control dataframe ##

df_Control.to_excel(os.path.join(Folder1,File_out_2),index=False)

## Transpose and save ##

df_Control_T = df_Control.T
df_Control_T.to_excel(os.path.join(Folder1,File_out_3),header=False)