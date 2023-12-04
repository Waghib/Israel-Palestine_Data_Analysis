import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tkinter as tk
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import warnings                    ## Filter warnings
warnings.filterwarnings('ignore')

try:
    df = pd.read_pickle('df_pickle.pkl')
except FileNotFoundError:
    df = pd.read_csv('fatalities_isr_pse_conflict_cleaned_dataset.csv')
    # Perform any necessary data processing here
    
    # Save the DataFrame to a pickle file for future use
    df.to_pickle('df_pickle.pkl')

    def set_color_palette(self):
        plt.rcParams["axes.prop_cycle"] = plt.cycler(
            color=["#4C2A85", "#BE96FF", "#957DAD", "red", "#A98CCC"]
        )

def ageDataHistogram():

    fig1, ax1 = plt.subplots()
    values_age = ['event_location_region']
    # sns.set(rc={'axes.facecolor': 'white', 'figure.facecolor': 'white'})
    
    for category in values_age:
        sns.histplot(data=df, x='age', hue=category, element='step', kde=True, ax=ax1)
        ax1.set_title(f'Age histogram with respect to: {category}')
        ax1.set_xlabel('Age')
        ax1.set_ylabel('Statistics')

    return fig1, ax1

        # Show the plot
        # plt.show()

def ageDataBoxPlot():
    fig2, ax2 = plt.subplots()
    # sns.set(style='darkgrid')
    data = [df[df['citizenship'] == citizenship]['age'] for citizenship in df['citizenship'].unique()]
    ax2.boxplot(data, labels=df['citizenship'].unique())

    ax2.set_title('Age Boxplot by Citizenship')
    ax2.set_xlabel('Citizenship')
    ax2.set_ylabel('Age')

    return fig2, ax2

def genderPlot():
        # Assuming 'x' is your DataFrame
    counts = df.groupby(['gender', 'citizenship']).size().reset_index(name='count')

    # Create a clustered bar plot using subplots
    fig3, ax3 = plt.subplots()
    sns.barplot(x='citizenship', y='count', hue='gender', data=counts, ax=ax3)

    # Add labels and title
    ax3.set_xlabel('Region')
    ax3.set_ylabel('Count')
    ax3.set_title('Clustered Bar Plot: Gender and Region')
    
    return fig3, ax3


def casualitiesYearWise():
    # Assuming 'x' is your DataFrame
    counts = df.groupby(['year_of_death', 'citizenship']).size().reset_index(name='count')

    # Create a bar plot using subplots
    fig4, ax4 = plt.subplots()
    sns.barplot(x='year_of_death', y='count', hue='citizenship', data=counts, ci=None, ax=ax4)

    # Add labels and title
    ax4.set_xlabel('Year')
    ax4.set_ylabel('Casualties')
    ax4.set_title('Casualties in Different Regions Over the Years')

    ax4.legend(title='Region', loc='upper right')
    return fig4, ax4

def groupResponsibleBarChart():
    counts = df.groupby(['killed_by']).size().reset_index(name='count')

    # Create a bar plot using subplots
    fig5, ax5 = plt.subplots()
    sns.barplot(x='killed_by', y='count', data=counts, ci=None, ax=ax5)

    # Add labels and title
    ax5.set_xlabel('Group Responsible')
    ax5.set_ylabel('Fatalities')
    ax5.set_title('Fatalities by Group Responsible')

    # Rotate x-axis labels for better visibility
    ax5.set_xticklabels(ax5.get_xticklabels(), rotation=10, ha='center')
    sns.despine()

    return fig5, ax5

def groupResponsiblePieChart():
    counts = df.groupby(['killed_by']).size().reset_index(name='count')

    # Create a pie chart using subplots
    fig6, ax6 = plt.subplots()
    ax6.pie(counts['count'], labels=counts['killed_by'], autopct='%1.1f%%', startangle=140)

    ax6.set_title('Distribution of Fatalities by Group Responsible')
    return fig6, ax6

# casualitiesYearWise()
# groupResponsibleBarChart()
# ageDataHistogram()
# genderPlot()
