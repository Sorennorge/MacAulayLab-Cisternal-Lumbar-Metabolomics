# -*- coding: utf-8 -*-

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
font_size = 8

## Function ##
def autopct_format(values):
    def my_format(pct):
        total = sum(values)
        val = pct*total/100.0
        return '{:.1f}% ({v:.2f})'.format(pct, v=val)
    return my_format

def draw_connection_line(placement_orientation,pie_chart_number, number_of_breaks, placement_number, length_start, length_orientation,explode_length,line_width):
    
    index_pie_chart_number = pie_chart_number-1
    
    length = length_start
    exploded_length = explode_length
    ang = numpy_array_list[index_pie_chart_number][0]

    x_start = numpy_array_list[index_pie_chart_number][1] + exploded_length * np.cos(np.deg2rad(ang))
    y_start = numpy_array_list[index_pie_chart_number][2] + exploded_length * np.sin(np.deg2rad(ang))

    x_end = x_start + length * np.cos(np.deg2rad(ang))
    y_end = y_start + length * np.sin(np.deg2rad(ang))
    
    # Placement_orientation needs to be right, or left
    if placement_orientation == 'right':
        length_right = length_orientation
        # number_of_breaks needs to be 1-3 #
        if number_of_breaks == 1:
            # Adjustment of meeting point of 2 lines with fixed placement point of text and second line #
            while_placement = placement_number
            while_placement_break_counter = 0  # ensures no infinity loops
            if while_placement < 0:
                while (y_end > while_placement+placement_correction_unit) or (y_end < while_placement-placement_correction_unit):
                    if y_end > while_placement:
                        length = length+placement_correction_unit
                        x_end = x_start + length * np.cos(np.deg2rad(ang))
                        y_end = y_start + length * np.sin(np.deg2rad(ang))
                    elif y_end < while_placement:
                        length = length-placement_correction_unit
                        x_end = x_start + length * np.cos(np.deg2rad(ang))
                        y_end = y_start + length * np.sin(np.deg2rad(ang))
                    else:
                        print(while_placement,y_end,length)
                    # ensures no infinity loops #
                    while_placement_break_counter += 1 
                    if while_placement_break_counter > 100000:
                        break
            else:
                while (y_end > while_placement+placement_correction_unit) or (y_end < while_placement-placement_correction_unit):
                    if y_end < while_placement:
                        length = length+placement_correction_unit
                        x_end = x_start + length * np.cos(np.deg2rad(ang))
                        y_end = y_start + length * np.sin(np.deg2rad(ang))
                    elif y_end > while_placement:
                        length = length-placement_correction_unit
                        x_end = x_start + length * np.cos(np.deg2rad(ang))
                        y_end = y_start + length * np.sin(np.deg2rad(ang))
                    else:
                        print(while_placement,y_end,length)
                    # ensures no infinity loops
                    while_placement_break_counter += 1 
                    if while_placement_break_counter > 100000:
                        break
            # Plot 2 lines (one break)
            plt.plot([x_start,x_end], [y_start,y_end], ls='dashed',color="grey", linewidth=line_width,clip_on = False)
            plt.plot([x_end,length_right-0.05], [placement_number,placement_number], ls='dashed',color="grey", linewidth=line_width,clip_on = False)
            
        elif number_of_breaks == 2:
            plt.plot([x_start,x_end], [y_start,y_end], ls='dashed',color="grey", linewidth=line_width,clip_on = False)
            plt.plot([x_end,length_right-0.125], [y_end,placement_number], ls='dashed',color="grey", linewidth=line_width,clip_on = False)
            plt.plot([length_right-0.125,length_right-0.05], [placement_number,placement_number], ls='dashed',color="grey", linewidth=line_width,clip_on = False)
        else:
            pass
    elif placement_orientation == 'left':
        length_left = length_orientation
        # Adjustment of meeting point of 2 lines with fixed placement point of text and second line #
        if number_of_breaks == 1:
            while_placement = placement_number
            if while_placement < 0:
                while (y_end > while_placement+placement_correction_unit) or (y_end < while_placement-placement_correction_unit):
                    if y_end > while_placement:
                        length = length+placement_correction_unit
                        x_end = x_start + length * np.cos(np.deg2rad(ang))
                        y_end = y_start + length * np.sin(np.deg2rad(ang))
                    elif y_end < while_placement:
                        length = length-placement_correction_unit
                        x_end = x_start + length * np.cos(np.deg2rad(ang))
                        y_end = y_start + length * np.sin(np.deg2rad(ang))
                    else:
                        print(while_placement,y_end,length)
            else:
                while (y_end > while_placement+placement_correction_unit) or (y_end < while_placement-placement_correction_unit):
                    if y_end < while_placement:
                        length = length+placement_correction_unit
                        x_end = x_start + length * np.cos(np.deg2rad(ang))
                        y_end = y_start + length * np.sin(np.deg2rad(ang))
                    elif y_end > while_placement:
                        length = length-placement_correction_unit
                        x_end = x_start + length * np.cos(np.deg2rad(ang))
                        y_end = y_start + length * np.sin(np.deg2rad(ang))
                    else:
                        print(while_placement,y_end,length)
            # Plot 2 lines (one break)
            plt.plot([x_start,x_end], [y_start,y_end], ls='dashed',color="grey", linewidth=line_width,clip_on = False)
            plt.plot([x_end,length_left+0.04], [placement_number,placement_number], ls='dashed',color="grey", linewidth=line_width,clip_on = False)
        elif number_of_breaks == 2:
            plt.plot([x_start,x_end], [y_start,y_end], ls='dashed',color="grey", linewidth=line_width,clip_on = False)
            plt.plot([x_end,length_left+0.2], [y_end,placement_number], ls='dashed',color="grey", linewidth=line_width,clip_on = False)
            plt.plot([length_left+0.2,length_left+0.04], [placement_number,placement_number], ls='dashed',color="grey", linewidth=line_width,clip_on = False)

        elif number_of_breaks == 3:
            # Four points
            plt.plot([x_start,x_end], [y_start,y_end], ls='dashed',color="grey", linewidth=line_width,clip_on = False)
            plt.plot([x_end,length_left+0.3], [y_end,y_end], ls='dashed',color="grey", linewidth=line_width,clip_on = False)
            plt.plot([length_left+0.3,length_left+0.2], [y_end,placement_number], ls='dashed',color="grey", linewidth=line_width,clip_on = False)
            plt.plot([length_left+0.2,length_left+0.04], [placement_number,placement_number], ls='dashed',color="grey", linewidth=line_width,clip_on = False)

        else:
            pass
    else:
        pass
    
def draw_connection_line_small_group(placement_orientation,pie_chart_number_start,pie_chart_number_end, placement_number,length_start,collection_point,line_width):
    # set global #
    small_group_collection_point = collection_point
    length = length_start
    # for start end set collection point #
    for i in range(pie_chart_number_start,pie_chart_number_end+1,1):
        index_pie_chart_number = i-1
        
        ang = numpy_array_list[index_pie_chart_number][0]
    
        x_start = numpy_array_list[index_pie_chart_number][1]
        y_start = numpy_array_list[index_pie_chart_number][2]
    
        x_end = x_start + length * np.cos(np.deg2rad(ang))
        y_end = y_start + length * np.sin(np.deg2rad(ang))
        
        plt.plot([x_start,x_end], [y_start,y_end], ls='dashed',color="grey", linewidth=line_width,clip_on = False)
        plt.plot([x_end,length_left+small_group_collection_point], [y_end,placement_number], ls='dashed',color="grey", linewidth=line_width,clip_on = False)
    # Draw end line
    plt.plot([length_left+small_group_collection_point,length_left+0.04], [placement_number,placement_number], ls='dashed',color="grey", linewidth=line_width,clip_on = False)


## Folders ##

Folder_0 = "Data/Meta data"

Folder_1 = "Data/Enrichment data/Cisternal group & Lumbar Weighted"
Folder_2 = "Results/Enrichement Analysis/Abundance"
os.makedirs(Folder_2,exist_ok=True)

Color_file = "Color_scheme_groups.csv"

## Files ##


File_1 = "Group Cisternal - Weighted data without outliers.xlsx"

## Load data ##

## Load color scheme and create color mapping ##

df_color = pd.read_csv(os.path.join(Folder_0,Color_file),sep=";")
Color_mapping = dict(df_color[['Groups', 'Colors']].values)


# Data #
df_Cisternal = pd.read_excel(os.path.join(Folder_1,File_1))


## Create variables for plots ##

df_Cisternal['Percentage'] = (df_Cisternal['Mean'] / df_Cisternal['Mean'].sum() * 100)

data_all_Cisternal = df_Cisternal['Percentage']
labels_all_Cisternal = df_Cisternal['Groups']

## Create color palettes for plots #

color_all_Cisternal = labels_all_Cisternal.to_frame().replace({"Groups": Color_mapping})['Groups'].tolist()

# Create the Seaborn palette
#palette = sns.color_palette("blend:steelblue,white", len(labels_all_Cisternal))

# Use the palette directly in RGB format
#color_all_Cisternal = palette


explode_set_all_Cisternal = [0.15]*len(labels_all_Cisternal)


fig = plt.figure(figsize=(12,10))

wedges, texts = plt.pie(data_all_Cisternal,
        #labels = labels_all_Cisternal,
        colors = color_all_Cisternal,
        explode=explode_set_all_Cisternal,
        #autopct=autopct_format(data_all_Cisternal),
        textprops={'fontsize': font_size},
        wedgeprops = {"edgecolor":"black",'linewidth': 2,"alpha": 0.65},
        counterclock=False,
        startangle=90,
        pctdistance=1.2,
        labeldistance=1.4)

hole = plt.Circle((0, 0), 0.6, facecolor='white',edgecolor="black", linewidth=0.8)
plt.gcf().gca().add_artist(hole)
plt.text(0,0,"Cisternal",fontsize=40,ha='center',va='center',fontweight="bold")


# fontsize for labels
font_size_text = 34

# Length of left #
length_right = 1.5
length_left = -1.5

placement_correction_unit = 0.0001


Placement_right_1 = float(1.425)
Placement_right_2 = float(1.0)
Placement_right_3 = float(0.35)
Placement_right_4 = float(-0.25)
Placement_right_5 = float(-0.7)
Placement_right_6 = float(-1.1)
Placement_right_7 = float(-1.5)

Placement_left_1 = float(-1.5)
Placement_left_2 = float(-1.15)
Placement_left_3 = float(-0.7)
Placement_left_4 = float(-0.3)
Placement_left_5 = float(0.1)
Placement_left_6 = float(0.5)
Placement_left_7 = float(0.75)
Placement_left_8 = float(0.975)
Placement_left_9 = float(1.2)
Placement_left_10 = float(1.425)

# Labels #
# right #
plt.text(length_right,Placement_right_1,"{} ({}%)".format(labels_all_Cisternal[0],round(data_all_Cisternal[0],1)),fontsize=font_size_text,ha='left',va='center')
plt.text(length_right,Placement_right_2,"{} ({}%)".format(labels_all_Cisternal[1],round(data_all_Cisternal[1],1)),fontsize=font_size_text,ha='left',va='center')
plt.text(length_right,Placement_right_3,"{} ({}%)".format(labels_all_Cisternal[2],round(data_all_Cisternal[2],1)),fontsize=font_size_text,ha='left',va='center')
plt.text(length_right,Placement_right_4,"{} ({}%)".format(labels_all_Cisternal[3],round(data_all_Cisternal[3],1)),fontsize=font_size_text,ha='left',va='center')
plt.text(length_right,Placement_right_5,"{} ({}%)".format(labels_all_Cisternal[4],round(data_all_Cisternal[4],1)),fontsize=font_size_text,ha='left',va='center')
plt.text(length_right,Placement_right_6,"{} ({}%)".format(labels_all_Cisternal[5],round(data_all_Cisternal[5],1)),fontsize=font_size_text,ha='left',va='center')
plt.text(length_right,Placement_right_7,"{} ({}%)".format(labels_all_Cisternal[6],round(data_all_Cisternal[6],1)),fontsize=font_size_text,ha='left',va='center')

plt.text(length_left,Placement_left_1,"{} ({}%)".format(labels_all_Cisternal[7],round(data_all_Cisternal[7],1)),fontsize=font_size_text,ha='right',va='center')
plt.text(length_left,Placement_left_2,"{} ({}%)".format(labels_all_Cisternal[8],round(data_all_Cisternal[8],1)),fontsize=font_size_text,ha='right',va='center')
plt.text(length_left,Placement_left_3,"{} ({}%)".format(labels_all_Cisternal[9],round(data_all_Cisternal[9],1)),fontsize=font_size_text,ha='right',va='center')
plt.text(length_left,Placement_left_4,"{} ({}%)".format(labels_all_Cisternal[10],round(data_all_Cisternal[10],1)),fontsize=font_size_text,ha='right',va='center')
plt.text(length_left,Placement_left_5,"{} ({}%)".format(labels_all_Cisternal[11].replace("dylethao","dyl-\nethao"),round(data_all_Cisternal[11],1)),fontsize=font_size_text,ha='right',va='center')
plt.text(length_left,Placement_left_6,"{} ({}%)".format(labels_all_Cisternal[12],round(data_all_Cisternal[12],1)),fontsize=font_size_text,ha='right',va='center')
plt.text(length_left,Placement_left_7,"{} ({}%)".format(labels_all_Cisternal[13],round(data_all_Cisternal[13],1)),fontsize=font_size_text,ha='right',va='center')
plt.text(length_left,Placement_left_8,"{} ({}%)".format(labels_all_Cisternal[14],round(data_all_Cisternal[14],1)),fontsize=font_size_text,ha='right',va='center')
plt.text(length_left,Placement_left_9,"{} ({}%)".format(labels_all_Cisternal[15],round(data_all_Cisternal[15],1)),fontsize=font_size_text,ha='right',va='center')
plt.text(length_left,Placement_left_10,"{} ({}%)".format(labels_all_Cisternal[16],round(data_all_Cisternal[16],1)),fontsize=font_size_text,ha='right',va='center')


numpy_array_list = []
for i, p in enumerate(wedges):
    if i == 23:
        ang = (p.theta2 - p.theta1)/1.25 + p.theta1
        y = np.sin(np.deg2rad(ang))
        x = np.cos(np.deg2rad(ang))
        numpy_array_list.append([ang,x,y]) 
    else:
        ang = (p.theta2 - p.theta1)/2. + p.theta1
        y = np.sin(np.deg2rad(ang))
        x = np.cos(np.deg2rad(ang))
        numpy_array_list.append([ang,x,y])

line_widthy = 2        
draw_connection_line("right",1, 1, Placement_right_1, 0.1, length_right,0.15,line_widthy)
draw_connection_line("right",2, 1, Placement_right_2, 0.1, length_right,0.15,line_widthy)
draw_connection_line("right",3, 1, Placement_right_3, 0.1, length_right,0.15,line_widthy)
draw_connection_line("right",4, 1, Placement_right_4, 0.1, length_right,0.15,line_widthy)
draw_connection_line("right",5, 1, Placement_right_5, 0.1, length_right,0.15,line_widthy)
draw_connection_line("right",6, 1, Placement_right_6, 0.1, length_right,0.15,line_widthy)
draw_connection_line("right",7, 1, Placement_right_7, 0.1, length_right,0.15,line_widthy)

draw_connection_line("left",8, 1, Placement_left_1, 0.2, length_left,0.15,line_widthy)
draw_connection_line("left",9, 1, Placement_left_2, 0.2, length_left,0.15,line_widthy)
draw_connection_line("left",10, 1, Placement_left_3, 0.2, length_left,0.15,line_widthy)
draw_connection_line("left",11, 1, Placement_left_4, 0.2, length_left,0.15,line_widthy)
draw_connection_line("left",12, 1, Placement_left_5, 0.2, length_left,0.15,line_widthy)
draw_connection_line("left",13, 1, Placement_left_6, 0.2, length_left,0.15,line_widthy)
draw_connection_line("left",14, 1, Placement_left_7, 0.2, length_left,0.15,line_widthy)
draw_connection_line("left",15, 1, Placement_left_8, 0.2, length_left,0.15,line_widthy)
draw_connection_line("left",16, 1, Placement_left_9, 0.2, length_left,0.15,line_widthy)
draw_connection_line("left",17, 1, Placement_left_10, 0.2, length_left,0.15,line_widthy)

File_out = "Abundance_piechart_Cisternal_old_color_new_middel.png"
plt.savefig(os.path.join(Folder_2,File_out),dpi=1200,bbox_inches='tight')