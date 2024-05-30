# -*- coding: utf-8 -*-

### Supplementary table ###

import os
import pandas as pd

## Parameter settings ##

mean_decimals = 2
sem_decimals = 2
FC_decimals = 2

## Functions ##

def Pvalue_annotation(df):
    if df['Pvalue'] <= 0.001:
        return '< 0.001'
    elif df['Pvalue'] <= 0.01:
        return '< 0.01'
    elif df['Pvalue'] <= 0.05:
        return '< 0.05'
    else:
        pass
    
def Padj_annotation(df):
    if df['Padj'] <= 0.001:
        return '< 0.001'
    elif df['Padj'] <= 0.01:
        return '< 0.01'
    elif df['Padj'] <= 0.05:
        return '< 0.05'
    elif df['Padj'] <= 0.1:
        return '< 0.1'
    else:
        pass

## Folders ##

Folder1 = "Data/Meta data"
Folder2 = "Results/Volcano/Data"
Folder3 = "Data/Data analysis"

Folder4 = "Results/Supplementary tables"
os.makedirs(Folder4,exist_ok=True)

## Files ##

File1 = "Meta_data_groups.xlsx"
File2 = "Significant_pvalues.csv"
File3 = "Data analysis overview.xlsx"

File4 = "Supplementary table 1.xlsx"

## Load data ##

df_meta = pd.read_excel(os.path.join(Folder1,File1))

df_signififant = pd.read_csv(os.path.join(Folder2,File2),sep=";",decimal=",")
df_signififant = df_signififant.set_index("Compounds")


df_overview = pd.read_excel(os.path.join(Folder3,File3))
df_overview = df_overview.set_index("Compounds")
df_overview = df_overview[['Group Lumbar Mean','Group Lumbar SEM','Group Cisternal Mean','Group Cisternal SEM']]
df_overview = df_overview.rename(columns=({'Group Lumbar Mean':'Lumbar Mean',
                                           'Group Lumbar SEM':'Lumbar SEM',
                                           'Group Cisternal Mean':'Cisternal Mean',
                                           'Group Cisternal SEM':'Cisternal SEM'}))

Mean_SEM_list = ['Lumbar Mean','Lumbar SEM','Cisternal Mean','Cisternal SEM']

df_merged = pd.concat([df_signififant,df_overview],join='inner',axis=1)

df_merged = df_merged[['Groups']+Mean_SEM_list+['Log2FC','Pvalue','Padj']]

# Round mean values #
df_merged['Lumbar Mean'] = df_merged['Lumbar Mean'].round(mean_decimals).apply('{0:.2f}'.format)
df_merged['Cisternal Mean'] = df_merged['Cisternal Mean'].round(mean_decimals).apply('{0:.2f}'.format)

# Round SEM values #
df_merged['Lumbar SEM'] = df_merged['Lumbar SEM'].round(sem_decimals).apply('{0:.2f}'.format)
df_merged['Cisternal SEM'] = df_merged['Cisternal SEM'].round(sem_decimals).apply('{0:.2f}'.format)

df_merged['Log2FC'] = df_merged['Log2FC'].round(FC_decimals).apply('{0:.2f}'.format)

df_merged['Pvalue'] = df_merged.apply(Pvalue_annotation,axis=1)
df_merged['Padj'] = df_merged.apply(Padj_annotation,axis=1)

## Write to Excel file
with pd.ExcelWriter(os.path.join(Folder4, File4)) as writer:
    df_meta.to_excel(writer, sheet_name='Group overview', index=False)
    df_merged.to_excel(writer, sheet_name='Significant lipids', index=True)




