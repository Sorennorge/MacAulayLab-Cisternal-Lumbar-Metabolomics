# -*- coding: utf-8 -*-

### Generate data for volcano plot ##

import os
import pandas as pd

## Folders ##

Folder1 = "Data/Meta data"
Folder2 = "Data/Data analysis"
Folder3 = "Data/Plot data/Volcano"
os.makedirs(Folder3,exist_ok=True)

## Files ##

File1 = "Meta_data_groups.xlsx"
File2 = "Data analysis overview.xlsx"

File3 = "Overview table.csv"

## Load data ##
df_groups = pd.read_excel(os.path.join(Folder1,File1))
df_overview = pd.read_excel(os.path.join(Folder2,File2))

df_groups_LOI = df_groups.loc[df_groups['LOI'] == "Yes"]
# Create mapping directory #
Group_mapping = dict(df_groups[['Compounds', 'Groups']].values)

# Add groups to overview dataframe #
df_overview['Groups'] = df_overview.Compounds.map(Group_mapping)

# Save overview as csv for volcano plot (8.1.0 Volcano plot grouped)
df_overview.to_csv(os.path.join(Folder3,File3),sep=";",index=False)
