import pandas as pd
import datetime as dt
import streamlit as st
import plotly.express as px


st.title(':blue[Automobile Statistics Dashboard]')

st.divider()

df = pd.read_csv('historical_automobile_sales.csv')

st.dataframe(data=df, width=800, height=200)

st.divider()

st.selectbox(
    'Select Statistics',
    ('Yearly Statistics', 'Recession Period Statistics'))

st.selectbox( 'Select Year', options=set(df.Year) )

st.divider()

recession_data = df[df["Recession"] == 1]

#Plot 1 Automobile sales fluctuate over Recession Period (year wise) using line chart

# grouping data for plotting
yearly_rec=recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()

st.line_chart(data=yearly_rec, x="Year", y="Automobile_Sales")

st.divider()

#Plot 2 Calculate the average number of vehicles sold by vehicle type and represent as a Bar chart

df2 = df.groupby(['Vehicle_Type'])['Automobile_Sales'].mean().reset_index()
df2

st.divider()


st.bar_chart(data=df2, x='Vehicle_Type', y='Automobile_Sales', width=0, height=0, use_container_width=True)



st.divider()

# Plot 3 : Pie chart for total expenditure share by vehicle type during recessions

# grouping data for plotting

df3 = recession_data.groupby(['Vehicle_Type'])['Advertising_Expenditure'].sum().reset_index()
df3

fig1 = px.pie(data_frame=df3, names='Vehicle_Type', values='Advertising_Expenditure', color_discrete_sequence=px.colors.qualitative.Plotly)

st.plotly_chart(fig1, use_container_width=True)

st.divider()