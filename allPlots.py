import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tkinter as tk
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import statsmodels.api as sm
from sklearn.preprocessing import LabelEncoder

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

def yearCasualities():
    label_encoder = LabelEncoder()
    df['encoded_location'] = label_encoder.fit_transform(df['event_location_region'])
    df['encoded_gender'] = label_encoder.fit_transform(df['gender'])

    # Count occurrences of each combination of 'year_of_death' and 'encoded_location'
    grouped_data = df.groupby(['year_of_death', 'encoded_location', 'encoded_gender']).size().reset_index(name='casualties')

    # Extract independent variables
    X = grouped_data[['year_of_death', 'encoded_location', 'encoded_gender']]
    m = sm.add_constant(X)

    # Extract dependent variable
    y = grouped_data['casualties']

    # Perform linear regression using statsmodels for p-values
    model = sm.OLS(y, m).fit()

    # Print summary
    # print(model.summary())

    predictions = model.predict(m)

    # Add the predictions to the grouped_data DataFrame
    grouped_data['predicted_casualties'] = predictions

    # Create scatter plots for each variable against y
    fig7, ax7 = plt.subplots()

    # Scatter plot
    sns.scatterplot(x=grouped_data['year_of_death'], y=y, label='Actual Casualties', ax=ax7)

    # Plot the best-fit line
    sns.lineplot(x=grouped_data['year_of_death'], y=predictions, color='red', label='Best-Fit Line', ax=ax7)

    ax7.set_xlabel('Year of Death')
    ax7.set_ylabel('Casualties')
    ax7.set_title('Scatter Plot with Best-Fit Line for Year of Death')
    ax7.legend()

    # plt.show()

    return fig7, ax7

def locationCasualities():
    label_encoder = LabelEncoder()
    df['encoded_location'] = label_encoder.fit_transform(df['event_location_region'])
    df['encoded_gender'] = label_encoder.fit_transform(df['gender'])

    # Count occurrences of each combination of 'year_of_death' and 'encoded_location'
    grouped_data = df.groupby(['year_of_death', 'encoded_location', 'encoded_gender']).size().reset_index(name='casualties')

    # Extract independent variables
    X = grouped_data[['year_of_death', 'encoded_location', 'encoded_gender']]
    m = sm.add_constant(X)

    # Extract dependent variable
    y = grouped_data['casualties']

    # Perform linear regression using statsmodels for p-values
    model = sm.OLS(y, m).fit()

    # Print summary
    # print(model.summary())

    predictions = model.predict(m)

    # Add the predictions to the grouped_data DataFrame
    grouped_data['predicted_casualties'] = predictions

    # Create scatter plots for each variable against y
    fig8, ax8 = plt.subplots()

    # Scatter plot
    sns.scatterplot(x=grouped_data['encoded_location'], y=y, label='Actual Casualties', ax=ax8)

    # Plot the best-fit line
    sns.lineplot(x=grouped_data['encoded_location'], y=predictions, color='red', label='Best-Fit Line', ax=ax8)

    ax8.set_xlabel('Encoded Location')
    ax8.set_ylabel('Casualties')
    ax8.set_title('Scatter Plot with Best-Fit Line for Location')
    ax8.legend()

    # plt.show()

    return fig8, ax8

def genderCasualities():
    label_encoder = LabelEncoder()
    df['encoded_location'] = label_encoder.fit_transform(df['event_location_region'])
    df['encoded_gender'] = label_encoder.fit_transform(df['gender'])

    # Count occurrences of each combination of 'year_of_death' and 'encoded_location'
    grouped_data = df.groupby(['year_of_death', 'encoded_location', 'encoded_gender']).size().reset_index(name='casualties')

    # Extract independent variables
    X = grouped_data[['year_of_death', 'encoded_location', 'encoded_gender']]
    m = sm.add_constant(X)

    # Extract dependent variable
    y = grouped_data['casualties']

    # Perform linear regression using statsmodels for p-values
    model = sm.OLS(y, m).fit()

    # Print summary
    # print(model.summary())

    predictions = model.predict(m)

    # Add the predictions to the grouped_data DataFrame
    grouped_data['predicted_casualties'] = predictions

    # Create scatter plots for each variable against y
    fig9, ax9 = plt.subplots()

    # Scatter plot
    sns.scatterplot(x=grouped_data['encoded_gender'], y=y, label='Actual Casualties', ax=ax9)

    # Plot the best-fit line
    sns.lineplot(x=grouped_data['encoded_gender'], y=predictions, color='red', label='Best-Fit Line', ax=ax9)

    ax9.set_xlabel('Encoded Gender')
    ax9.set_ylabel('Casualties')
    ax9.set_title('Scatter Plot with Best-Fit Line for Gender')
    ax9.legend()

    # plt.show()

    return fig9, ax9

def yearConfidenceInterval():
    label_encoder = LabelEncoder()
    df['encoded_location'] = label_encoder.fit_transform(df['event_location_region'])
    df['encoded_gender'] = label_encoder.fit_transform(df['gender'])

    # Count occurrences of each combination of 'year_of_death' and 'encoded_location'
    grouped_data = df.groupby(['year_of_death', 'encoded_location', 'encoded_gender']).size().reset_index(name='casualties')

    # Extract independent variables
    X = grouped_data[['year_of_death', 'encoded_location', 'encoded_gender']]
    X = sm.add_constant(X)

    # Extract dependent variable
    y = grouped_data['casualties']

    # Perform linear regression using statsmodels for p-values
    model = sm.OLS(y, X).fit()

    # Get predictions and confidence intervals
    predictions = model.get_prediction(X)
    predictions_summary = predictions.summary_frame()

    # Add the predicted values and confidence intervals to the grouped_data DataFrame
    grouped_data['predicted_casualties'] = predictions_summary['mean']
    grouped_data['lower_ci'] = predictions_summary['obs_ci_lower']
    grouped_data['upper_ci'] = predictions_summary['obs_ci_upper']

    # Create scatter plots for each variable against y
    fig, ax = plt.subplots()
    # Scatter plot
    sns.scatterplot(x=grouped_data['year_of_death'], y=y, label='Actual Casualties', ax=ax)
    # Plot the best-fit line
    sns.lineplot(x=grouped_data['year_of_death'], y=grouped_data['predicted_casualties'], color='red', label='Best-Fit Line', ax=ax)
    # Plot confidence intervals
    plt.fill_between(grouped_data['year_of_death'], grouped_data['lower_ci'], grouped_data['upper_ci'], color='red', alpha=0.2, label='95% Confidence Interval')

    ax.set_xlabel('year_of_death')
    ax.set_ylabel('Casualties')
    ax.set_title(f'Best-Fit Line and Confidence Intervals for year of death')
    ax.legend()
    # plt.show()
    return fig, ax

def locationConfidenceInterval():
    label_encoder = LabelEncoder()
    df['encoded_location'] = label_encoder.fit_transform(df['event_location_region'])
    df['encoded_gender'] = label_encoder.fit_transform(df['gender'])

    # Count occurrences of each combination of 'year_of_death' and 'encoded_location'
    grouped_data = df.groupby(['year_of_death', 'encoded_location', 'encoded_gender']).size().reset_index(name='casualties')

    # Extract independent variables
    X = grouped_data[['year_of_death', 'encoded_location', 'encoded_gender']]
    X = sm.add_constant(X)

    # Extract dependent variable
    y = grouped_data['casualties']

    # Perform linear regression using statsmodels for p-values
    model = sm.OLS(y, X).fit()

    # Get predictions and confidence intervals
    predictions = model.get_prediction(X)
    predictions_summary = predictions.summary_frame()

    # Add the predicted values and confidence intervals to the grouped_data DataFrame
    grouped_data['predicted_casualties'] = predictions_summary['mean']
    grouped_data['lower_ci'] = predictions_summary['obs_ci_lower']
    grouped_data['upper_ci'] = predictions_summary['obs_ci_upper']

    # Create scatter plots for each variable against y
    fig, ax = plt.subplots()
    # Scatter plot
    sns.scatterplot(x=grouped_data['encoded_location'], y=y, label='Actual Casualties', ax=ax)
    # Plot the best-fit line
    sns.lineplot(x=grouped_data['encoded_location'], y=grouped_data['predicted_casualties'], color='red', label='Best-Fit Line', ax=ax)
    # Plot confidence intervals
    plt.fill_between(grouped_data['encoded_location'], grouped_data['lower_ci'], grouped_data['upper_ci'], color='red', alpha=0.2, label='95% Confidence Interval', )

    ax.set_xlabel('encoded_location')
    ax.set_ylabel('Casualties')
    ax.set_title(f'Best-Fit Line and Confidence Intervals for location')
    ax.legend()
    # plt.show()
    return fig, ax

def genderConfidenceInterval():
    label_encoder = LabelEncoder()
    df['encoded_location'] = label_encoder.fit_transform(df['event_location_region'])
    df['encoded_gender'] = label_encoder.fit_transform(df['gender'])

    # Count occurrences of each combination of 'year_of_death' and 'encoded_location'
    grouped_data = df.groupby(['year_of_death', 'encoded_location', 'encoded_gender']).size().reset_index(name='casualties')

    # Extract independent variables
    X = grouped_data[['year_of_death', 'encoded_location', 'encoded_gender']]
    X = sm.add_constant(X)

    # Extract dependent variable
    y = grouped_data['casualties']

    # Perform linear regression using statsmodels for p-values
    model = sm.OLS(y, X).fit()

    # Get predictions and confidence intervals
    predictions = model.get_prediction(X)
    predictions_summary = predictions.summary_frame()

    # Add the predicted values and confidence intervals to the grouped_data DataFrame
    grouped_data['predicted_casualties'] = predictions_summary['mean']
    grouped_data['lower_ci'] = predictions_summary['obs_ci_lower']
    grouped_data['upper_ci'] = predictions_summary['obs_ci_upper']

    # Create scatter plots for each variable against y
    fig, ax = plt.subplots()
    
    # Scatter plot
    sns.scatterplot(x=grouped_data['encoded_gender'], y=y, label='Actual Casualties', ax=ax)
    # Plot the best-fit line
    sns.lineplot(x=grouped_data['encoded_gender'], y=grouped_data['predicted_casualties'], color='red', label='Best-Fit Line', ax=ax)
    # Plot confidence intervals
    plt.fill_between(grouped_data['encoded_gender'], grouped_data['lower_ci'], grouped_data['upper_ci'], color='red', alpha=0.2, label='95% Confidence Interval')

    ax.set_xlabel('encoded_gender')
    ax.set_ylabel('Casualties')
    ax.set_title(f'Best-Fit Line and Confidence Intervals for gender')
    ax.legend()

    # plt.show()
    return fig, ax

def probabiltyForChildren():
    for i in df['citizenship'].drop_duplicates():
        total_count = len(df[df['age'] <= 18])
        count_below_18 = len(df[(df['citizenship'] == i) & (df['age'] <= 18)])
        
        probability = count_below_18 / total_count if total_count > 0 else 0
        print(i, " = ", probability)

def probabiltyForWomen():
    print("For women")
    for i in df['citizenship'].drop_duplicates():
        total_count = len(df[df['gender'] == 'F'])
        count_For_F = len(df[(df['citizenship'] == i) & (df['gender'] == 'F')])
        probability = count_For_F / total_count if total_count > 0 else 0
        print(i, " = ", probability)
