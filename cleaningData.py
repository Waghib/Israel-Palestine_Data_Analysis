import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
x = pd.read_csv("D:\\Users\\HP\\Documents\\5th semester\\STATS\\archive_2\\fatalities_isr_pse_conflict_2000_to_2023.csv")
j=[]
k=[]
#print(x[['name','age']].head())
# print(x.columns)
# print(x.iloc[0]['age'])
#print(x['age'][[1,2,3]])
# print(x['age'].value_counts())
# for i in range(0,113):
#     j.append(i)
#     k.append(len(x[x['age']==i]))

# plt.plot(j, k, label='Sample Line')

# # Add labels and title
# plt.xlabel('X-axis Label')
# plt.ylabel('Y-axis Label')
# plt.title('Simple Matplotlib Example')

# # Add a legend
# plt.legend()

# # Show the plot
# plt.show()
# print(x[(x['age'] <= 20) & (x['gender'] == 'F')])
# c=(x['age'] <= 20) & (x['gender'] == 'M')     # c represents rows which has given condition

#x.dropna(subset=['took_part_in_the_hostilities'], inplace=True)
#x.dropna(inplace=True)
# x.drop_duplicates(inplace=True)
#x.dropna(subset=x.columns.difference(['took_part_in_the_hostilities','ammunition']),inplace=True)
x.replace('NaN',np.nan,inplace=True)
x.replace('Missing',np.nan,inplace=True)
x=x.drop(columns=['took_part_in_the_hostilities','ammunition'])
x['age'].fillna(x['age'].mean(), inplace=True)
x.dropna(inplace=True)
x.drop_duplicates(inplace=True)
x['age'] = x['age'].astype(int)
x['name'] = x['name'].astype(str)

# Remove single quotes and leading/trailing whitespaces
x['name'] = x['name'].str.replace("'", "").str.strip()
x['name'] = x['name'].astype(str)
x['date_of_event'] = pd.to_datetime(x['date_of_event'])
x['year_of_event'] = x['date_of_event'].dt.year
x['month_of_event'] = x['date_of_event'].dt.month
x['day_of_event'] = x['date_of_event'].dt.day
# print(x['date_of_event'].dtypes)

x['date_of_death'] = pd.to_datetime(x['date_of_death'])
x['year_of_death'] = x['date_of_death'].dt.year
x['month_of_death'] = x['date_of_death'].dt.month
x['day_of_death'] = x['date_of_death'].dt.day
# print(x['date_of_death'].dtypes)
print(x[['date_of_death', 'year_of_death', 'month_of_death', 'day_of_death']].head())
print(x['age'].dtypes)
x.to_csv('fatalities_isr_pse_conflict_cleaned_dataset.csv', index=False)
