import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tkinter as tk
import ttkbootstrap as ttk
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from allPlots import ageDataHistogram, ageDataBoxPlot, genderPlot, casualitiesYearWise, groupResponsibleBarChart, groupResponsiblePieChart

class FatalitiesDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Israel-Palestine Fatalities Data")
        ctk.set_appearance_mode("dark")
        # ctk.set_default_color_theme("dark-blue")
        self.load_data()
        self.set_color_palette()
        self.create_charts()
        self.create_dashboard()

    def load_data(self):
        try:
            self.df = pd.read_pickle('df_pickle.pkl')
        except FileNotFoundError:
            self.df = pd.read_csv('fatalities_isr_pse_conflict_cleaned_dataset.csv')
            # Perform any necessary data processing here
            # Save the DataFrame to a pickle file for future use
            self.df.to_pickle('df_pickle.pkl')

    def set_color_palette(self):
        plt.rcParams["axes.prop_cycle"] = plt.cycler(
            color=["#4C2A85", "#BE96FF", "red", "#5E366E", "#A98CCC"]
        )

    def create_charts(self):

        self.fig1, self.ax1 = ageDataHistogram()
        self.fig2, self.ax2 = ageDataBoxPlot()

        # Number of deaths per day
        deaths_per_day = self.df['day_of_event'].value_counts().reset_index()
        deaths_per_day.columns = ['day_of_event', 'Number_of_Deaths']
        deaths_per_day = deaths_per_day.sort_values(by='day_of_event')

        self.fig3, self.ax3 = plt.subplots()
        self.ax3.bar(deaths_per_day['day_of_event'], deaths_per_day['Number_of_Deaths'])
        self.ax3.set_title('Number of Deaths per day')
        self.ax3.set_xlabel('Months')
        self.ax3.set_ylabel('Number of Deaths')

        # Clustered bar plot of Fatalities data by year & citizenship
        self.fig4, self.ax4 = plt.subplots()
        year_order = sorted(self.df['year_of_event'].unique())
        sns.countplot(x='year_of_event', hue='citizenship', data=self.df, order=year_order, ax=self.ax4)
        self.ax4.set_xlabel('Years')
        self.ax4.set_ylabel('Number of Fatalities')
        self.ax4.set_title('Fatalities by Year and Citizenship')

    def create_dashboard(self):
        dashboard_frame = ctk.CTkFrame(self.root, height=5, width=10)
        dashboard_frame.pack(side="top", expand=True, fill="both", padx=10, pady=10)

        # Label and dropdown for y variable
        y_label = ctk.CTkLabel(dashboard_frame, text="Choose Analysis")
        y_label.grid(row=2, column=0, padx=50, pady=10)

        self.y_dropdown = ctk.CTkComboBox(dashboard_frame, values=["age", "gender", "casualities yearwise","group responsible for fatalities"],button_hover_color="#4C2A85", dropdown_hover_color="#4C2A85")
        self.y_dropdown.grid(row=2, column=1, padx=10, pady=10)

        # Label and dropdown for x variable
        x_label = ctk.CTkLabel(dashboard_frame, text="Type of Analysis")
        x_label.grid(row=2, column=3, padx=50, pady=10)

        self.x_dropdown = ctk.CTkComboBox(dashboard_frame, values=["graphical","descriptive"], button_hover_color="#4C2A85", dropdown_hover_color="#4C2A85")
        self.x_dropdown.grid(row=2, column=4, padx=10, pady=10)

        # Submit button
        self.submitBtn = ctk.CTkButton(dashboard_frame, text="Do Analysis", command=self.get_selected_value, border_width=2, fg_color="#4C2A85") 
        self.submitBtn.grid(row=2, column=5, padx=70, pady=10)

        # charts_frame = tk.Frame(self.root)
        # charts_frame.pack()

        self.main_frame = ctk.CTkFrame(self.root, bg_color="#F0F0F0", fg_color="#F0F0F0", border_width=2, border_color="black")
        self.main_frame.pack(fill="both", expand=True)

        self.canvas1 = FigureCanvasTkAgg(self.fig1, self.main_frame)
        self.canvas1.draw()
        self.canvas1.get_tk_widget().pack(side="left", fill="both", expand=True)

        self.canvas2 = FigureCanvasTkAgg(self.fig2, self.main_frame)
        self.canvas2.draw()
        self.canvas2.get_tk_widget().pack(side="bottom", fill="both", expand=True)

        root.mainloop()
    
    def get_selected_value(self):

        # Destroy existing widgets in the main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        valueY = self.y_dropdown.get()
        valueX = self.x_dropdown.get()

        # print(valueY, "\t" , valueX)
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

            elif valueY == "gender":
                self.fig3, self.ax23= genderPlot()
                self.canvas1 = FigureCanvasTkAgg(self.fig3, self.main_frame)
                self.canvas1.draw()
                self.canvas1.get_tk_widget().pack(side="left", fill="both", expand=True)

            elif valueY == "casualities yearwise":
                self.fig4, self.ax4 = casualitiesYearWise()
                self.canvas1 = FigureCanvasTkAgg(self.fig4, self.main_frame)
                self.canvas1.draw()
                self.canvas1.get_tk_widget().pack(side="left", fill="both", expand=True)

            elif valueY == "group responsible for fatalities":
                self.fig5, self.ax5 = groupResponsibleBarChart()
                self.canvas1 = FigureCanvasTkAgg(self.fig5, self.main_frame)
                self.canvas1.draw()
                self.canvas1.get_tk_widget().pack(side="left", fill="both", expand=True)

                self.fig6, self.ax6 = groupResponsiblePieChart()
                self.canvas2 = FigureCanvasTkAgg(self.fig6, self.main_frame)
                self.canvas2.draw()
                self.canvas2.get_tk_widget().pack(side="bottom", fill="both", expand=True)
            else :
                print("Value not found")
        else:
            if valueY == "age":
                print(valueY)
            elif valueY == "gender":
                print(valueY)
            elif valueY == "casualities yearwise":
                print(valueY)
            elif valueY == "group responsible for fatalities":
                print(valueY)
            else :
                print("Value not found")



if __name__ == "__main__":
    root = ctk.CTk()
    fatalities_dashboard = FatalitiesDashboard(root)
    root.mainloop()