import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from PIL import Image
import seaborn as sns
import tkinter as tk
from tkinter import scrolledtext
import customtkinter as ctk
from tabulate import tabulate
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import statsmodels.api as sm
from sklearn.preprocessing import LabelEncoder
from allPlots import (
    ageDataHistogram,
    ageDataBoxPlot,
    genderPlot,
    casualitiesYearWise,
    groupResponsibleBarChart,
    groupResponsiblePieChart,
    yearCasualities,
    locationCasualities,
    genderCasualities,
    yearConfidenceInterval,
    locationConfidenceInterval,
    genderConfidenceInterval,
)


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
            self.df = pd.read_pickle("df_pickle.pkl")
        except FileNotFoundError:
            self.df = pd.read_csv("fatalities_isr_pse_conflict_cleaned_dataset.csv")
            # Save the DataFrame to a pickle file for future use
            self.df.to_pickle("df_pickle.pkl")

    def set_color_palette(self):
        plt.rcParams["axes.prop_cycle"] = plt.cycler(
            color=["#4C2A85", "#BE96FF", "red", "#5E366E", "#A98CCC"]
        )

    def create_charts(self):
        self.fig1, self.ax1 = ageDataHistogram()
        self.fig2, self.ax2 = ageDataBoxPlot()

    def clearDashboard(self):
        for widget in root.winfo_children():
            widget.destroy()
        self.create_dashboard()

    def create_dashboard(self):
        # creating dashboard frame
        dashboard_frame = ctk.CTkFrame(self.root)
        dashboard_frame.pack(side="top", fill="both", padx=10, pady=10)

        image_path = os.path.join(os.path.dirname(__file__), "images/homeImage.png")
        image = ctk.CTkImage(light_image=Image.open(image_path), size=(40, 40))

        self.HomeBtn = ctk.CTkButton(
            dashboard_frame,
            image=image,
            text="",
            command=self.clearDashboard,
            fg_color="transparent",
            width=40,
            height=30,
        )
        self.HomeBtn.grid(row=2, column=0, padx=10, pady=10)

        # Label and dropdown for analysis
        y_label = ctk.CTkLabel(dashboard_frame, text="Choose Analysis")
        y_label.grid(row=2, column=1, padx=50, pady=10)

        self.y_dropdown = ctk.CTkComboBox(
            dashboard_frame,
            values=[
                "age",
                "gender",
                "casualities yearwise",
                "group responsible for fatalities",
            ],
            button_hover_color="#4C2A85",
            dropdown_hover_color="#4C2A85",
        )
        self.y_dropdown.grid(row=2, column=2, padx=10, pady=10)

        # Submit button
        self.submitBtn = ctk.CTkButton(
            dashboard_frame,
            text="Do Analysis",
            command=self.get_selected_value,
            border_width=2,
            fg_color="#4C2A85",
        )
        self.submitBtn.grid(row=2, column=4, padx=40, pady=10)

        # Regression Model button
        self.regBtn = ctk.CTkButton(
            dashboard_frame,
            text="Regression Model",
            command=self.regressionModel,
            border_width=2,
            fg_color="#4C2A85",
        )
        self.regBtn.grid(row=2, column=6, padx=40, pady=10)

        # Visual Confidencs Interval button
        self.confidenceIntervalBtn = ctk.CTkButton(
            dashboard_frame,
            text="Confidence Interval",
            command=self.confidenceInterval,
            border_width=2,
            fg_color="#4C2A85",
        )
        self.confidenceIntervalBtn.grid(row=2, column=7, padx=40, pady=10)

        # Probability Model button
        self.ProbBtn = ctk.CTkButton(
            dashboard_frame,
            text="Probabilty Method",
            command=self.probabilityMethod,
            border_width=2,
            fg_color="#4C2A85",
        )
        self.ProbBtn.grid(row=2, column=8, padx=40, pady=10)

        self.main_frame = ctk.CTkFrame(
            self.root,
            bg_color="#F0F0F0",
            fg_color="#F0F0F0",
            border_width=2,
            border_color="black",
        )
        self.main_frame.pack(side="top", fill="both", expand=True)

        self.bottomFrame = ctk.CTkFrame(self.root)
        self.bottomFrame.pack(side="bottom", fill="both", padx=10, pady=10, expand=True)

        image_path = os.path.join(
            os.path.dirname(__file__), "images/Purple Modern Software Company Logo.png"
        )
        image = ctk.CTkImage(light_image=Image.open(image_path), size=(500, 500))
        image_label = ctk.CTkLabel(self.main_frame, image=image, text="")
        image_label.place(x=10, y=15)

        image_path1 = os.path.join(
            os.path.dirname(__file__), "images/data.png"
        )

        image1 = ctk.CTkImage(light_image=Image.open(image_path1), size=(600, 1000))
        image_label1 = ctk.CTkLabel(self.main_frame, image=image1, text="")
        image_label1.place(x=750, y=20)

        self.bottomFrame.pack_forget()
        # Add a Text widget for displaying additional information
        self.info_text = tk.Text(
            self.bottomFrame, wrap=tk.WORD, width=80, height=8, fg="#4C2A85"
        )
        self.info_text.pack(side="bottom", fill="both", expand=True)

        root.mainloop()

    def get_selected_value(self):
        self.bottomFrame.pack(side="bottom", fill="both", padx=10, pady=10, expand=True)
        # Destroy existing widgets in the main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        valueY = self.y_dropdown.get()

        # Display additional information below the plot
        self.info_text.delete(1.0, tk.END)  # Clear previous text

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
            self.info_text.insert(
                tk.END,
                "\t\t\t\t\tHENCE DATA IS RIGHT SKEWED SO APPROPRIATE COMPARISON IS MEDIAN AND IQR\n\n",
            )
            self.info_text.insert(tk.END, "Palestine \t\t\t\t\t\t\t\t Israel\n")
            self.info_text.insert(
                tk.END,
                "Median= {} \t\t\t\t\t\t\t\t {}\n".format(
                    np.median(
                        self.df[self.df["event_location_region"] != "Israel"]["age"]
                    ),
                    np.median(
                        self.df[self.df["event_location_region"] == "Israel"]["age"]
                    ),
                ),
            )
            Q1 = np.percentile(
                self.df[self.df["event_location_region"] != "Israel"]["age"], 25
            )
            Q3 = np.percentile(
                self.df[self.df["event_location_region"] != "Israel"]["age"], 75
            )
            IQR1 = Q3 - Q1

            Q1 = np.percentile(
                self.df[self.df["event_location_region"] == "Israel"]["age"], 25
            )
            Q3 = np.percentile(
                self.df[self.df["event_location_region"] == "Israel"]["age"], 75
            )
            IQR2 = Q3 - Q1

            self.info_text.insert(tk.END, f"IQR= {IQR1} \t\t\t\t\t\t\t\t {IQR2}")

            self.info_text.insert(
                tk.END,
                "\nDispersion= {} +- {} \t\t\t\t\t\t\t\t ".format(
                    np.median(
                        self.df[self.df["event_location_region"] != "Israel"]["age"]
                    ),
                    IQR1,
                    np.median(
                        self.df[self.df["event_location_region"] == "Israel"]["age"]
                    ),
                ),
            )
            self.info_text.insert(
                tk.END,
                "{} +- {}\n".format(
                    np.median(
                        self.df[self.df["event_location_region"] == "Israel"]["age"]
                    ),
                    IQR2,
                ),
            )
            self.info_text.insert(
                tk.END,
                "...................EXTRA  STATISTIC ARE........................\n",
            )
            self.info_text.insert(
                tk.END,
                "Since it's a right skewd so mean and standard deviation could NOT be its appropriate statistical methods",
            )

        elif valueY == "gender":
            self.fig3, self.ax23 = genderPlot()
            self.canvas1 = FigureCanvasTkAgg(self.fig3, self.main_frame)
            self.canvas1.draw()
            self.canvas1.get_tk_widget().pack(side="left", fill="both", expand=True)

            # Israel Data
            israel_data = self.df[self.df["event_location_region"] == "Israel"]

            # Palestine Data
            palestine_data = self.df[self.df["event_location_region"] != "Israel"]

            # Separate data by gender for Israel
            israel_men_data = israel_data[israel_data["gender"] == "M"]
            israel_women_data = israel_data[israel_data["gender"] == "F"]

            # Separate data by gender for Palestine
            palestine_men_data = palestine_data[palestine_data["gender"] == "M"]
            palestine_women_data = palestine_data[palestine_data["gender"] == "F"]

            # Descriptive Statistics for Men and Women in Israel
            israel_men_stats = israel_men_data["gender"].value_counts()
            israel_women_stats = israel_women_data["gender"].value_counts()

            # Descriptive Statistics for Men and Women in Palestine
            palestine_men_stats = palestine_men_data["gender"].value_counts()
            palestine_women_stats = palestine_women_data["gender"].value_counts()

            # Display data side by side
            self.info_text.insert(
                tk.END, "\nIsrael Gender Data\t\t\tPalestine Gender Data\n"
            )
            self.info_text.insert(
                tk.END,
                "Men: {}\t\t\t\tMen: {}\n".format(
                    israel_men_stats.values, palestine_men_stats.values
                ),
            )
            self.info_text.insert(
                tk.END,
                "Women: {}\t\t\t\tWomen: {}\n".format(
                    israel_women_stats.values, palestine_women_stats.values
                ),
            )

        elif valueY == "casualities yearwise":
            self.fig4, self.ax4 = casualitiesYearWise()
            self.canvas1 = FigureCanvasTkAgg(self.fig4, self.main_frame)
            self.canvas1.draw()
            self.canvas1.get_tk_widget().pack(side="left", fill="both", expand=True)

            # Casualties in Palestine
            casualties_by_year_P = (
                self.df[self.df["event_location_region"] != "Israel"]["year_of_death"]
                .value_counts()
                .reset_index()
            )
            casualties_by_year_P.columns = ["year_of_death", "casualties"]

            # Descriptive Statistics for Palestine
            yearly_stats_P = casualties_by_year_P["casualties"].describe()

            # Casualties in Israel
            casualties_by_year_I = (
                self.df[self.df["event_location_region"] == "Israel"]["year_of_death"]
                .value_counts()
                .reset_index()
            )
            casualties_by_year_I.columns = ["year_of_death", "casualties"]

            # Descriptive Statistics for Israel
            yearly_stats_I = casualties_by_year_I["casualties"].describe()

            # Display information in self.info_text
            self.info_text.insert(
                tk.END,
                "{:<20}  {:<30}  {:<20}\n".format(
                    "Year", "Casualties in Palestine", "Casualties in Israel"
                ),
            )

            for year in set(casualties_by_year_P["year_of_death"]).union(
                set(casualties_by_year_I["year_of_death"])
            ):
                p_casualties = (
                    casualties_by_year_P[casualties_by_year_P["year_of_death"] == year][
                        "casualties"
                    ].values[0]
                    if year in set(casualties_by_year_P["year_of_death"])
                    else 0
                )
                i_casualties = (
                    casualties_by_year_I[casualties_by_year_I["year_of_death"] == year][
                        "casualties"
                    ].values[0]
                    if year in set(casualties_by_year_I["year_of_death"])
                    else 0
                )

                self.info_text.insert(
                    tk.END,
                    "{:<20}  {:<30}  {:<20}\n".format(year, p_casualties, i_casualties),
                )

            self.info_text.insert(tk.END, "\nDescriptive Statistics\n\n")
            self.info_text.insert(
                tk.END, "{:<30}  {:<30}\n".format("Palestine", "Israel")
            )
            self.info_text.insert(
                tk.END,
                "{:<30}  {:<30}\n".format(
                    f"Count: {yearly_stats_P['count']}",
                    f"Count: {yearly_stats_I['count']}",
                ),
            )
            self.info_text.insert(
                tk.END,
                "{:<30}  {:<30}\n".format(
                    f"Mean: {yearly_stats_P['mean']}", f"Mean: {yearly_stats_I['mean']}"
                ),
            )
            self.info_text.insert(
                tk.END,
                "{:<30}  {:<30}\n".format(
                    f"Std: {yearly_stats_P['std']}", f"Std: {yearly_stats_I['std']}"
                ),
            )
            self.info_text.insert(
                tk.END,
                "{:<30}  {:<30}\n".format(
                    f"Min: {yearly_stats_P['min']}", f"Min: {yearly_stats_I['min']}"
                ),
            )
            self.info_text.insert(
                tk.END,
                "{:<30}  {:<30}\n".format(
                    f"25%: {yearly_stats_P['25%']}", f"25%: {yearly_stats_I['25%']}"
                ),
            )
            self.info_text.insert(
                tk.END,
                "{:<30}  {:<30}\n".format(
                    f"50%: {yearly_stats_P['50%']}", f"50%: {yearly_stats_I['50%']}"
                ),
            )
            self.info_text.insert(
                tk.END,
                "{:<30}  {:<30}\n".format(
                    f"75%: {yearly_stats_P['75%']}", f"75%: {yearly_stats_I['75%']}"
                ),
            )
            self.info_text.insert(
                tk.END,
                "{:<30}  {:<30}\n".format(
                    f"Max: {yearly_stats_P['max']}", f"Max: {yearly_stats_I['max']}"
                ),
            )
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
            killed_by_stats = self.df["killed_by"].value_counts()
            killed_by_descriptive = killed_by_stats.describe()

            # Display Casualties by Group Responsible and Descriptive Statistics
            self.info_text.insert(tk.END, "\nCasualties by Group Responsible:\n")
            self.info_text.insert(tk.END, str(killed_by_stats) + "\n\n")

            # Display Descriptive Statistics for Casualties by Group Responsible
            self.info_text.insert(
                tk.END, "Descriptive Statistics for Casualties by Group Responsible:\n"
            )
            self.info_text.insert(tk.END, str(killed_by_descriptive) + "\n")
        else:
            print("Incorrect value")

    def regressionModel(self):
        self.bottomFrame.pack(side="bottom", fill="both", padx=10, pady=10, expand=True)

        for widget in self.main_frame.winfo_children():
            widget.destroy()

        self.info_text.delete(1.0, tk.END)  # Clear previous text

        # Create frames for each canvas
        frame1 = tk.Frame(self.main_frame)
        frame1.grid(row=0, column=0, sticky="nsew")

        frame2 = tk.Frame(self.main_frame)
        frame2.grid(row=0, column=1, sticky="nsew")

        frame3 = tk.Frame(self.main_frame)
        frame3.grid(row=0, column=2, sticky="nsew")

        small_figsize = (4, 3)

        self.fig6, self.ax6 = yearCasualities()
        self.canvas1 = FigureCanvasTkAgg(self.fig6, master=frame1)
        self.canvas1.draw()
        self.canvas1.get_tk_widget().pack(side="top", fill="both", expand=True)

        self.fig7, self.ax7 = locationCasualities()
        self.canvas2 = FigureCanvasTkAgg(self.fig7, master=frame2)
        self.canvas2.draw()
        self.canvas2.get_tk_widget().pack(side="top", fill="both", expand=True)

        self.fig8, self.ax8 = genderCasualities()
        self.canvas3 = FigureCanvasTkAgg(self.fig8, master=frame3)
        self.canvas3.draw()
        self.canvas3.get_tk_widget().pack(side="top", fill="both", expand=True)

        # Configure row and column weights to make the columns resizable
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(2, weight=1)

        label_encoder = LabelEncoder()
        self.df["encoded_location"] = label_encoder.fit_transform(
            self.df["event_location_region"]
        )
        self.df["encoded_gender"] = label_encoder.fit_transform(self.df["gender"])

        # Count occurrences of each combination of 'year_of_death' and 'encoded_location'
        grouped_data = (
            self.df.groupby(["year_of_death", "encoded_location", "encoded_gender"])
            .size()
            .reset_index(name="casualties")
        )

        # Extract independent variables
        X = grouped_data[["year_of_death", "encoded_location", "encoded_gender"]]
        m = sm.add_constant(X)

        # Extract dependent variable
        y = grouped_data["casualties"]

        # Perform linear regression using statsmodels for p-values
        model = sm.OLS(y, m).fit()

        # Print summary
        summary_text = model.summary()
        self.info_text.insert(tk.END, summary_text)

    def confidenceInterval(self):
        # Hide the bottom frame
        self.bottomFrame.pack_forget()
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        self.info_text.delete(1.0, tk.END)  # Clear previous text
        # Create frames for each canvas
        frame1 = tk.Frame(self.main_frame)
        frame1.grid(row=0, column=0, sticky="nsew")

        frame2 = tk.Frame(self.main_frame)
        frame2.grid(row=0, column=1, sticky="nsew")

        frame3 = tk.Frame(self.main_frame)
        frame3.grid(row=0, column=2, sticky="nsew")

        small_figsize = (4, 3)

        self.fig6, self.ax6 = yearConfidenceInterval()
        self.canvas1 = FigureCanvasTkAgg(self.fig6, master=frame1)
        self.canvas1.draw()
        self.canvas1.get_tk_widget().pack(side="top", fill="both", expand=True)

        self.fig7, self.ax7 = locationConfidenceInterval()
        self.canvas2 = FigureCanvasTkAgg(self.fig7, master=frame2)
        self.canvas2.draw()
        self.canvas2.get_tk_widget().pack(side="top", fill="both", expand=True)

        self.fig8, self.ax8 = genderConfidenceInterval()
        self.canvas3 = FigureCanvasTkAgg(self.fig8, master=frame3)
        self.canvas3.draw()
        self.canvas3.get_tk_widget().pack(side="top", fill="both", expand=True)

        # Configure row and column weights to make the columns resizable
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(2, weight=1)

    def probabilityMethod(self):
        # Hide the bottom frame
        self.bottomFrame.pack_forget()
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        # Create scrolled text widgets for displaying results
        women_result_text = scrolledtext.ScrolledText(
            self.main_frame, wrap=tk.WORD, width=40, height=8, fg="#4C2A85"
        )
        women_result_text.pack(side="left", fill="both", expand=True)

        children_result_text = scrolledtext.ScrolledText(
            self.main_frame, wrap=tk.WORD, width=40, height=8, fg="#4C2A85"
        )
        children_result_text.pack(side="right", fill="both", expand=True)

        # Configure tags for formatting
        women_result_text.tag_configure("header", font=("Helvetica", 12, "bold"))
        women_result_text.tag_configure("normal", font=("Helvetica", 10))

        children_result_text.tag_configure("header", font=("Helvetica", 12, "bold"))
        children_result_text.tag_configure("normal", font=("Helvetica", 10))

        # Display results for women
        women_result_text.insert(tk.END, "Probability Results for Women\n", "header")
        women_result_text.insert(
            tk.END,
            "If people who died are women then probilities of them being in following regions are\n\n",
            "normal",
        )

        for i in self.df["citizenship"].drop_duplicates():
            total_count = len(self.df[self.df["gender"] == "F"])
            count_for_F = len(
                self.df[(self.df["citizenship"] == i) & (self.df["gender"] == "F")]
            )
            probability = count_for_F / total_count if total_count > 0 else 0
            women_result_text.insert(tk.END, f"\n{i} = {probability:.2%}\n", "normal")

        # Scroll to the bottom to show the latest results
        women_result_text.yview(tk.END)

        # Display results for children
        children_result_text.insert(
            tk.END, "Probability Results for Children\n", "header"
        )
        children_result_text.insert(
            tk.END,
            "If people who died are under 18 then probilities of them being in following regions are.\n\n",
            "normal",
        )

        for i in self.df["citizenship"].drop_duplicates():
            total_count = len(self.df[self.df["age"] <= 18])
            count_below_18 = len(
                self.df[(self.df["citizenship"] == i) & (self.df["age"] <= 18)]
            )
            probability = count_below_18 / total_count if total_count > 0 else 0
            children_result_text.insert(
                tk.END, f"\n{i} = {probability:.2%}\n", "normal"
            )

        # Scroll to the bottom to show the latest results
        children_result_text.yview(tk.END)

if __name__ == "__main__":
    root = ctk.CTk()
    fatalities_dashboard = FatalitiesDashboard(root)
    root.mainloop()
