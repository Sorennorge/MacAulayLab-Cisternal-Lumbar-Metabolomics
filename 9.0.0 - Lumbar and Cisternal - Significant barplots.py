# -*- coding: utf-8 -*-


### Barplots ###

import os
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns
custom_params = {"axes.spines.right": False, "axes.spines.top": False}
sns.set_theme(style="ticks", rc=custom_params)
sns.set(style="ticks",font_scale=3)

### Folders ###

Folder1 = "Results/Volcano/Data"
#Folder2 = "Results/Barplots"
Folder2 = "Results/Barplots/unlabeled"
os.makedirs(Folder2,exist_ok=True)

### Files ###

File1 = "Significant_pvalues.csv"
File2 = "Significant barplots.png"

### Load data ###

df = pd.read_csv(os.path.join(Folder1,File1),sep=";",decimal=",")

Groups_list = sorted(list(set(df['Groups'].tolist())))

# Labeled #
for group in Groups_list:
    Group_data = df[df['Groups'] == group].sort_values(by='Log2FC', ascending=False)
    number_of_cols = len(Group_data)
    fig = plt.figure(figsize=(number_of_cols,8))
    print(group)
    ax0_0 = sns.barplot(data=df[df['Groups'] == group].sort_values(by='Log2FC', ascending=False), x="Compounds", y="Log2FC",
                     hue="Expression",
                     palette=['steelblue','aliceblue'],
                     linewidth=1.2,
                     width=0.75,
                     dodge=False,
                     edgecolor="black")
    for axis in ['top','bottom','right']:
        ax0_0.spines[axis].set_visible(False)
    ax0_0.tick_params(axis='x', rotation=90,bottom=False)
    ax0_0.set_ylabel("$Log_{2}FC$")
    ax0_0.set_xlabel("")
    ax0_0.legend_.remove()
    ax0_0.spines['left'].set_position(('outward', 10))
    ax0_0.set_title('{}'.format(group))
    ax0_0.axhline(0, color='black', linestyle='-', linewidth=1.2)
    ax0_0.set_xlim(-0.5, len(df[df['Groups'] == group]) - 0.5)
    File = "Barplot - {}.png".format(group)
    plt.savefig(os.path.join(Folder2,File),dpi=1200,bbox_inches='tight')
    plt.show()

# Unlabeled #
for group in Groups_list:
    Group_data = df[df['Groups'] == group].sort_values(by='Log2FC', ascending=False)
    number_of_cols = len(Group_data)
    fig = plt.figure(figsize=(number_of_cols,8))
    print(group)
    ax0_0 = sns.barplot(data=df[df['Groups'] == group].sort_values(by='Log2FC', ascending=False), x="Compounds", y="Log2FC",
                     hue="Expression",
                     palette=['steelblue','aliceblue'],
                     linewidth=1.2,
                     width=0.75,
                     dodge=False,
                     edgecolor="black")
    for axis in ['top','bottom','right']:
        ax0_0.spines[axis].set_visible(False)
    ax0_0.set_xticks([])
    ax0_0.set_ylabel("")
    ax0_0.set_xlabel("")
    ax0_0.legend_.remove()
    ax0_0.spines['left'].set_position(('outward', 10))
    ax0_0.axhline(0, color='black', linestyle='-', linewidth=1.2)
    ax0_0.set_xlim(-0.5, len(df[df['Groups'] == group]) - 0.5)
    File = "Barplot - {} - Unlabeled.png".format(group)
    plt.savefig(os.path.join(Folder2,File),dpi=1200,bbox_inches='tight')
    plt.show()