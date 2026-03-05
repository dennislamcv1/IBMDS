"""
DV0101EN - Final Assignment Part 1
Automobile Sales Data Visualization
Using real automobile_sales.csv dataset
Tasks: 1.1 – 1.9 (Matplotlib & Seaborn)
"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import os, warnings
warnings.filterwarnings('ignore')

OUTPUT_DIR = '/mnt/user-data/outputs'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ─────────────────────────────────────────
# LOAD DATASET
# ─────────────────────────────────────────
df = pd.read_csv('/mnt/user-data/uploads/automobile_sales.csv')
df.rename(columns={'unemployment_rate': 'Unemployment_Rate'}, inplace=True)

print(f"Dataset shape: {df.shape}")
print(df.head())
print(df.describe())
print(df.columns.tolist())


# ─────────────────────────────────────────
# TASK 1.1 – Line chart: Average automobile sales per year
# ─────────────────────────────────────────
df_line = df.groupby('Year')['Automobile_Sales'].mean()

plt.figure(figsize=(14, 6))
df_line.plot(kind='line', color='steelblue', marker='o', markersize=4, linewidth=1.8)
plt.xticks(range(1980, 2024), rotation=75, fontsize=8)
plt.xlabel('Year')
plt.ylabel('Average Automobile Sales')
plt.title('Automobile Sales during Recession')

annotations = {
    1980: '1980\nRecession',
    1982: '1981-82\nRecession',
    1991: '1991\nRecession',
    2001: '2000-01\nRecession',
    2008: '2008-09\nRecession',
    2020: '2020 COVID',
}
for yr, label in annotations.items():
    if yr in df_line.index:
        plt.annotate(label, xy=(yr, df_line[yr]),
                     xytext=(yr + 0.4, df_line[yr] + 12),
                     fontsize=7, color='red',
                     arrowprops=dict(arrowstyle='->', color='red', lw=0.8))

plt.legend(['Avg Automobile Sales'])
plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/task1_1_line_avg_sales.png', dpi=150)
plt.close()
print("Task 1.1 saved.")


# ─────────────────────────────────────────
# TASK 1.2 – Ad Expenditure vs Sales trend (non-recession, Seaborn)
# ─────────────────────────────────────────
df_non_rec = df[df['Recession'] == 0]
df_trends = df_non_rec.groupby('Year', as_index=False).agg(
    Avg_Sales=('Automobile_Sales', 'mean'),
    Avg_Ad_Spend=('Advertising_Expenditure', 'mean')
)

fig, ax1 = plt.subplots(figsize=(13, 6))
sns.lineplot(data=df_trends, x='Year', y='Avg_Sales',
             marker='o', linestyle='-', color='green', label='Avg Automobile Sales', ax=ax1)
ax1.set_xlabel('Year')
ax1.set_ylabel('Avg Automobile Sales', color='green')
ax1.tick_params(axis='y', labelcolor='green')

ax2 = ax1.twinx()
sns.lineplot(data=df_trends, x='Year', y='Avg_Ad_Spend',
             marker='s', linestyle='--', color='blue', label='Avg Ad Expenditure', ax=ax2)
ax2.set_ylabel('Avg Advertising Expenditure ($)', color='blue')
ax2.tick_params(axis='y', labelcolor='blue')

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
ax2.get_legend().remove()

plt.title('Advertising Expenditure vs Automobile Sales during Non-Recession Periods')
ax1.grid(axis='y', linestyle='--', alpha=0.4)
plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/task1_2_ad_vs_sales.png', dpi=150)
plt.close()
print("Task 1.2 saved.")


# ─────────────────────────────────────────
# TASK 1.3 – Bar charts: Sales by recession period & vehicle type
# ─────────────────────────────────────────
# Part A – overall average
new_df = df.groupby('Recession')['Automobile_Sales'].mean().reset_index()
plt.figure(figsize=(7, 5))
sns.barplot(x='Recession', y='Automobile_Sales', hue='Recession',
            data=new_df, palette=['steelblue', 'tomato'], legend=False)
plt.xlabel('Period')
plt.ylabel('Average Automobile Sales')
plt.title('Average Automobile Sales during Recession and Non-Recession')
plt.xticks(ticks=[0, 1], labels=['Non-Recession', 'Recession'])
plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/task1_3a_sales_recession_overall.png', dpi=150)
plt.close()

# Part B – by vehicle type
grouped_df = df.groupby(['Recession', 'Vehicle_Type'])['Automobile_Sales'].mean().reset_index()
plt.figure(figsize=(12, 6))
sns.barplot(x='Recession', y='Automobile_Sales', hue='Vehicle_Type', data=grouped_df)
plt.xticks(ticks=[0, 1], labels=['Non-Recession', 'Recession'])
plt.xlabel('Period')
plt.ylabel('Average Automobile Sales')
plt.title('Vehicle-Wise Sales during Recession and Non-Recession Period')
plt.legend(title='Vehicle Type', bbox_to_anchor=(1.01, 1), loc='upper left')
plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/task1_3b_sales_by_vehicle.png', dpi=150)
plt.close()
print("Task 1.3 saved.")


# ─────────────────────────────────────────
# TASK 1.4 – Subplots: GDP during recession vs non-recession
# ─────────────────────────────────────────
rec_data     = df[df['Recession'] == 1]
non_rec_data = df[df['Recession'] == 0]

fig = plt.figure(figsize=(14, 6))
ax0 = fig.add_subplot(1, 2, 1)
ax1 = fig.add_subplot(1, 2, 2)

sns.lineplot(x='Year', y='GDP', data=rec_data, label='Recession', color='tomato', ax=ax0)
ax0.set_xlabel('Year'); ax0.set_ylabel('GDP')
ax0.set_title('GDP Variation during Recession Period'); ax0.legend()

sns.lineplot(x='Year', y='GDP', data=non_rec_data, label='Non-Recession', color='steelblue', ax=ax1)
ax1.set_xlabel('Year'); ax1.set_ylabel('GDP')
ax1.set_title('GDP Variation during Non-Recession Period'); ax1.legend()

plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/task1_4_gdp_subplots.png', dpi=150)
plt.close()
print("Task 1.4 saved.")


# ─────────────────────────────────────────
# TASK 1.5 – Bubble plot: Seasonality impact (non-recession)
# ─────────────────────────────────────────
non_rec_data = df[df['Recession'] == 0].copy()

month_order = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
non_rec_data['Month_Num'] = pd.Categorical(
    non_rec_data['Month'], categories=month_order, ordered=True).codes + 1

plt.figure(figsize=(12, 6))
sns.scatterplot(data=non_rec_data, x='Month_Num', y='Automobile_Sales',
                size='Seasonality_Weight', hue='Seasonality_Weight',
                sizes=(20, 400), palette='viridis', legend='brief', alpha=0.6)
plt.xticks(range(1, 13), month_order)
plt.xlabel('Month')
plt.ylabel('Automobile Sales')
plt.title('Seasonality Impact on Automobile Sales')
plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/task1_5_seasonality_bubble.png', dpi=150)
plt.close()
print("Task 1.5 saved.")


# ─────────────────────────────────────────
# TASK 1.6 – Scatter: Consumer Confidence & Price vs Sales (recession)
# ─────────────────────────────────────────
rec_data = df[df['Recession'] == 1]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

ax1.scatter(rec_data['Consumer_Confidence'], rec_data['Automobile_Sales'],
            alpha=0.5, color='steelblue', edgecolors='none')
ax1.set_xlabel('Consumer Confidence'); ax1.set_ylabel('Automobile Sales')
ax1.set_title('Consumer Confidence and Automobile Sales during Recessions')
ax1.grid(True, linestyle='--', alpha=0.4)

ax2.scatter(rec_data['Price'], rec_data['Automobile_Sales'],
            alpha=0.5, color='tomato', edgecolors='none')
ax2.set_xlabel('Vehicle Price ($)'); ax2.set_ylabel('Automobile Sales')
ax2.set_title('Relationship between Vehicle Price and Sales during Recessions')
ax2.grid(True, linestyle='--', alpha=0.4)

plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/task1_6_scatter_recession.png', dpi=150)
plt.close()
print("Task 1.6 saved.")


# ─────────────────────────────────────────
# TASK 1.7 – Pie: Ad expenditure – recession vs non-recession
# ─────────────────────────────────────────
Rdata  = df[df['Recession'] == 1]
NRdata = df[df['Recession'] == 0]
RAtotal  = Rdata['Advertising_Expenditure'].sum()
NRAtotal = NRdata['Advertising_Expenditure'].sum()

plt.figure(figsize=(7, 7))
plt.pie([RAtotal, NRAtotal], labels=['Recession', 'Non-Recession'],
        autopct='%1.1f%%', startangle=90,
        colors=['#ff6b6b', '#4ecdc4'], wedgeprops=dict(edgecolor='white'))
plt.title('Advertising Expenditure during Recession and Non-Recession Periods')
plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/task1_7_pie_ad_exp.png', dpi=150)
plt.close()
print("Task 1.7 saved.")


# ─────────────────────────────────────────
# TASK 1.8 – Pie: Ad expenditure by vehicle type during recession
# ─────────────────────────────────────────
VTexpenditure = Rdata.groupby('Vehicle_Type')['Advertising_Expenditure'].sum()

plt.figure(figsize=(8, 8))
plt.pie(VTexpenditure.values, labels=VTexpenditure.index,
        autopct='%1.1f%%', startangle=90, wedgeprops=dict(edgecolor='white'))
plt.title('Share of Each Vehicle Type in Total Ad Expenditure during Recessions')
plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/task1_8_pie_vehicle_ad.png', dpi=150)
plt.close()
print("Task 1.8 saved.")


# ─────────────────────────────────────────
# TASK 1.9 – Line plot: Unemployment rate vs vehicle-type sales (recession)
# ─────────────────────────────────────────
df_rec = df[df['Recession'] == 1]

plt.figure(figsize=(16, 6))
sns.lineplot(data=df_rec, x='Unemployment_Rate', y='Automobile_Sales',
             hue='Vehicle_Type', marker='o', palette='tab10', linewidth=1.8)
plt.title('Effect of Unemployment Rate on Vehicle Type and Sales')
plt.xlabel('Unemployment Rate (%)')
plt.ylabel('Automobile Sales')
plt.legend(title='Vehicle Type', bbox_to_anchor=(1.01, 1), loc='upper left')
plt.grid(axis='both', linestyle='--', alpha=0.4)
plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/task1_9_unemployment_lineplot.png', dpi=150)
plt.close()
print("Task 1.9 saved.")

print("\n All 9 charts saved to /mnt/user-data/outputs/")
