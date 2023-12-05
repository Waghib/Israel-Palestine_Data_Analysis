import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tkinter as tk
import ttkbootstrap as ttk
import customtkinter as ctk
from tabulate import tabulate
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from allPlots import ageDataHistogram, ageDataBoxPlot, genderPlot, casualitiesYearWise, groupResponsibleBarChart, groupResponsiblePieChart

class FatalitiesDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Israel-Palestine Fatalities Data")
        ctk.set_appearance_mode("dark")
        self.load_data()
        self.set_color_palette()
        self.create_charts()
        self.create_dashboard()

    def load_data(self):
        try:
            self.df = pd.read_pickle('df_pickle.pkl')
        except FileNotFoundError:
            self.df = pd.read_csv('fatalities_isr_pse_conflict_cleaned_dataset.csv')
            # Save the DataFrame to a pickle file for future use
            self.df.to_pickle('df_pickle.pkl')

    def set_color_palette(self):
        plt.rcParams["axes.prop_cycle"] = plt.cycler(
            color=["#4C2A85", "#BE96FF", "red", "#5E366E", "#A98CCC"]
        )

    def create_charts(self):

        self.fig1, self.ax1 = ageDataHistogram()
        self.fig2, self.ax2 = ageDataBoxPlot()

    def create_dashboard(self):

        dashboard_frame = ctk.CTkFrame(self.root)
        dashboard_frame.pack(side="top", fill="both", padx=10, pady=10)

        # Label and dropdown for y variable
        y_label = ctk.CTkLabel(dashboard_frame, text="Choose Analysis")
        y_label.grid(row=2, column=0, padx=50, pady=10)

        self.y_dropdown = ctk.CTkComboBox(dashboard_frame, values=["age", "gender", "casualities yearwise","group responsible for fatalities"],button_hover_color="#4C2A85", dropdown_hover_color="#4C2A85")
        self.y_dropdown.grid(row=2, column=1, padx=10, pady=10)

        # Label and dropdown for x variable
        x_label = ctk.CTkLabel(dashboard_frame, text="Type of Analysis")
        x_label.grid(row=2, column=3, padx=50, pady=10)

        self.x_dropdown = ctk.CTkComboBox(dashboard_frame, values=["graphical"], button_hover_color="#4C2A85", dropdown_hover_color="#4C2A85")
        self.x_dropdown.grid(row=2, column=4, padx=10, pady=10)

        # Submit button
        self.submitBtn = ctk.CTkButton(dashboard_frame, text="Do Analysis", command=self.get_selected_value, border_width=2, fg_color="#4C2A85") 
        self.submitBtn.grid(row=2, column=5, padx=70, pady=10)

        self.main_frame = ctk.CTkFrame(self.root, bg_color="#F0F0F0", fg_color="#F0F0F0", border_width=2, border_color="black")
        self.main_frame.pack(side="top",fill="both", expand=True)

        # self.mainLabel = ctk.CTkLabel(self.main_frame, width=50, height=50, text="Data Analysis", justify="center", font="")
        # self.mainLabel.pack()

        self.bottomFrame = ctk.CTkFrame(self.root)
        self.bottomFrame.pack(side="bottom", fill="both", padx=10, pady=10, expand=True)

                # Add a Text widget for displaying additional information
        self.info_text = tk.Text(self.bottomFrame, wrap=tk.WORD, width=80, height=8, fg="#4C2A85")
        self.info_text.pack(side="bottom", fill="both", expand=True)

        root.mainloop()
    
    def get_selected_value(self):

        # Destroy existing widgets in the main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        valueY = self.y_dropdown.get()
        valueX = self.x_dropdown.get()

        # Display additional information below the plot
        self.info_text.delete(1.0, tk.END)  # Clear previous text

        if valueX == "graphical":
            if valueY == "age":
                self.fig1, self.ax1 = ageDataHistogram()
                self.fig2, self.ax2 = ageDataBoxPlot()

                self.canvas1 = FigureCanvasTkAgg(self.fig1, self.main_frame)
                self.canvas1.draw()
                self.canvas1.get_tk_widget().pack(side="left", fill="both", expand=True)

                self.canvas2 = FigureCanvasTkAgg(self.fig2, self.main_frame)
                self.canvas2.draw()
                self.canvas2.get_tk_widget().pack(side="bottom", fill="both", expand=True)

               # Display additional information below the plot
                self.info_text.insert(tk.END, "\t\t\t\t\tHENCE DATA IS RIGHT SKEWED SO APPROPRIATE COMPARISON IS MEDIAN AND IQR\n\n")
                self.info_text.insert(tk.END, "Palestine \t\t\t\t\t\t\t\t Israel\n")
                self.info_text.insert(tk.END, "Median= {} \t\t\t\t\t\t\t\t {}\n".format(
                    np.median(self.df[self.df['event_location_region'] != 'Israel']['age']),
                    np.median(self.df[self.df['event_location_region'] == 'Israel']['age']))
                )
                Q1 = np.percentile(self.df[self.df['event_location_region'] != 'Israel']['age'], 25)
                Q3 = np.percentile(self.df[self.df['event_location_region'] != 'Israel']['age'], 75)
                IQR1 = Q3 - Q1
                
                Q1 = np.percentile(self.df[self.df['event_location_region'] == 'Israel']['age'], 25)
                Q3 = np.percentile(self.df[self.df['event_location_region'] == 'Israel']['age'], 75)
                IQR2 = Q3 - Q1

                self.info_text.insert(tk.END, f"IQR= {IQR1} \t\t\t\t\t\t\t\t {IQR2}")

                self.info_text.insert(tk.END, "\nDispersion= {} +- {} \t\t\t\t\t\t\t\t ".format(
                    np.median(self.df[self.df['event_location_region'] != 'Israel']['age']), IQR1,
                    np.median(self.df[self.df['event_location_region'] == 'Israel']['age']))
                )
                self.info_text.insert(tk.END, "{} +- {}\n".format(
                    np.median(self.df[self.df['event_location_region'] == 'Israel']['age']), IQR2)
                )
                self.info_text.insert(tk.END, "...................EXTRA  STATISTIC ARE........................\n")
                self.info_text.insert(tk.END, "Since it's a right skewd so mean and standard deviation could NOT be its appropriate statistical methods")

            elif valueY == "gender":
                self.fig3, self.ax23= genderPlot()
                self.canvas1 = FigureCanvasTkAgg(self.fig3, self.main_frame)
                self.canvas1.draw()
                self.canvas1.get_tk_widget().pack(side="left", fill="both", expand=True)

                # Israel Data
                israel_data = self.df[self.df['event_location_region'] == 'Israel']

                # Palestine Data
                palestine_data = self.df[self.df['event_location_region'] != 'Israel']

                # Separate data by gender for Israel
                israel_men_data = israel_data[israel_data['gender'] == 'M']
                israel_women_data = israel_data[israel_data['gender'] == 'F']

                # Separate data by gender for Palestine
                palestine_men_data = palestine_data[palestine_data['gender'] == 'M']
                palestine_women_data = palestine_data[palestine_data['gender'] == 'F']

                # Descriptive Statistics for Men and Women in Israel
                israel_men_stats = israel_men_data['gender'].value_counts()
                israel_women_stats = israel_women_data['gender'].value_counts()

                # Descriptive Statistics for Men and Women in Palestine
                palestine_men_stats = palestine_men_data['gender'].value_counts()
                palestine_women_stats = palestine_women_data['gender'].value_counts()

                # Display data side by side
                self.info_text.insert(tk.END, "\nIsrael Gender Data\t\t\tPalestine Gender Data\n")
                self.info_text.insert(tk.END, "Men: {}\t\t\t\tMen: {}\n".format(israel_men_stats.values, palestine_men_stats.values))
                self.info_text.insert(tk.END, "Women: {}\t\t\t\tWomen: {}\n".format(israel_women_stats.values, palestine_women_stats.values))

            elif valueY == "casualities yearwise":
                self.fig4, self.ax4 = casualitiesYearWise()
                self.canvas1 = FigureCanvasTkAgg(self.fig4, self.main_frame)
                self.canvas1.draw()
                self.canvas1.get_tk_widget().pack(side="left", fill="both", expand=True)

                # Casualties in Palestine
                casualties_by_year_P = self.df[self.df['event_location_region'] != 'Israel']['year_of_death'].value_counts().reset_index()
                casualties_by_year_P.columns = ['year_of_death', 'casualties']

                # Descriptive Statistics for Palestine
                yearly_stats_P = casualties_by_year_P['casualties'].describe()

                # Casualties in Israel
                casualties_by_year_I = self.df[self.df['event_location_region'] == 'Israel']['year_of_death'].value_counts().reset_index()
                casualties_by_year_I.columns = ['year_of_death', 'casualties']

                # Descriptive Statistics for Israel
                yearly_stats_I = casualties_by_year_I['casualties'].describe()

                # Display information in self.info_text
                self.info_text.insert(tk.END, "{:<20}  {:<30}  {:<20}\n".format("Year", "Casualties in Palestine", "Casualties in Israel"))

                for year in set(casualties_by_year_P['year_of_death']).union(set(casualties_by_year_I['year_of_death'])):
                    p_casualties = casualties_by_year_P[casualties_by_year_P['year_of_death'] == year]['casualties'].values[0] if year in set(casualties_by_year_P['year_of_death']) else 0
                    i_casualties = casualties_by_year_I[casualties_by_year_I['year_of_death'] == year]['casualties'].values[0] if year in set(casualties_by_year_I['year_of_death']) else 0

                    self.info_text.insert(tk.END, "{:<20}  {:<30}  {:<20}\n".format(year, p_casualties, i_casualties))

                self.info_text.insert(tk.END, "\nDescriptive Statistics\n\n")
                self.info_text.insert(tk.END, "{:<30}  {:<30}\n".format("Palestine", "Israel"))
                self.info_text.insert(tk.END, "{:<30}  {:<30}\n".format(f"Count: {yearly_stats_P['count']}", f"Count: {yearly_stats_I['count']}"))
                self.info_text.insert(tk.END, "{:<30}  {:<30}\n".format(f"Mean: {yearly_stats_P['mean']}", f"Mean: {yearly_stats_I['mean']}"))
                self.info_text.insert(tk.END, "{:<30}  {:<30}\n".format(f"Std: {yearly_stats_P['std']}", f"Std: {yearly_stats_I['std']}"))
                self.info_text.insert(tk.END, "{:<30}  {:<30}\n".format(f"Min: {yearly_stats_P['min']}", f"Min: {yearly_stats_I['min']}"))
                self.info_text.insert(tk.END, "{:<30}  {:<30}\n".format(f"25%: {yearly_stats_P['25%']}", f"25%: {yearly_stats_I['25%']}"))
                self.info_text.insert(tk.END, "{:<30}  {:<30}\n".format(f"50%: {yearly_stats_P['50%']}", f"50%: {yearly_stats_I['50%']}"))
                self.info_text.insert(tk.END, "{:<30}  {:<30}\n".format(f"75%: {yearly_stats_P['75%']}", f"75%: {yearly_stats_I['75%']}"))
                self.info_text.insert(tk.END, "{:<30}  {:<30}\n".format(f"Max: {yearly_stats_P['max']}", f"Max: {yearly_stats_I['max']}"))
                self.info_text.insert(tk.END, "\n")

            elif valueY == "group responsible for fatalities":
                self.fig5, self.ax5 = groupResponsibleBarChart()
                self.canvas1 = FigureCanvasTkAgg(self.fig5, self.main_frame)
                self.canvas1.draw()
                self.canvas1.get_tk_widget().pack(side="left", fill="both", expand=True)

                self.fig6, self.ax6 = groupResponsiblePieChart()
                self.canvas2 = FigureCanvasTkAgg(self.fig6, self.main_frame)
                self.canvas2.draw()
                self.canvas2.get_tk_widget().pack(side="left", fill="both", expand=True)

                # Casualties by Group Responsible Stats
                killed_by_stats = self.df['killed_by'].value_counts()
                killed_by_descriptive = killed_by_stats.describe()

                # Display Casualties by Group Responsible and Descriptive Statistics
                self.info_text.insert(tk.END, "\nCasualties by Group Responsible:\n")
                self.info_text.insert(tk.END, str(killed_by_stats) + "\n\n")

                # Display Descriptive Statistics for Casualties by Group Responsible
                self.info_text.insert(tk.END, "Descriptive Statistics for Casualties by Group Responsible:\n")
                self.info_text.insert(tk.END, str(killed_by_descriptive) + "\n")

            else :
                print("Value not found")



if __name__ == "__main__":
    root = ctk.CTk()
    fatalities_dashboard = FatalitiesDashboard(root)
    root.mainloop()