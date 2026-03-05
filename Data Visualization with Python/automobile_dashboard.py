#!/usr/bin/env python
# coding: utf-8

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

# Load the data using pandas
data = pd.read_csv('automobile_sales.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Set the title of the dashboard
app.title = "Automobile Sales Statistics Dashboard"

# ─── Dropdown options ────────────────────────────────────────────────────────
dropdown_options = [
    {'label': 'Yearly Statistics',            'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics',  'value': 'Recession Period Statistics'},
]

# List of years
year_list = [i for i in range(1980, 2024, 1)]

# ─── TASK 2.1 + 2.2 + 2.3 – App Layout ──────────────────────────────────────
app.layout = html.Div([

    # TASK 2.1 – Title: centered, colour #503D36, font-size 24
    html.H1(
        "Automobile Sales Statistics Dashboard",
        style={
            'textAlign': 'center',
            'color':     '#503D36',
            'fontSize':  24,
        }
    ),

    # TASK 2.2 – Dropdown 1: Report type
    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=dropdown_options,
            value='Yearly Statistics',
            placeholder='Select a report type',
        )
    ]),

    # TASK 2.2 – Dropdown 2: Year (disabled by default)
    html.Div(
        dcc.Dropdown(
            id='select-year',
            options=[{'label': i, 'value': i} for i in year_list],
            value=2020,
            disabled=True,
            placeholder='Select a year',
        )
    ),

    # TASK 2.3 – Output display container
    html.Div([
        html.Div(
            id='output-container',
            className='chart-grid',
            style={'display': 'flex', 'flexWrap': 'wrap'},
        ),
    ])
])


# ─── TASK 2.4 – Callback: enable / disable the year dropdown ─────────────────
@app.callback(
    Output(component_id='select-year',        component_property='disabled'),
    Input(component_id='dropdown-statistics', component_property='value'),
)
def update_input_container(selected_statistics):
    if selected_statistics == 'Yearly Statistics':
        return False   # enabled
    else:
        return True    # disabled


# ─── Callback: render charts ──────────────────────────────────────────────────
@app.callback(
    Output(component_id='output-container',   component_property='children'),
    [Input(component_id='dropdown-statistics', component_property='value'),
     Input(component_id='select-year',         component_property='value')],
)
def update_output_container(selected_statistics, input_year):

    # ── TASK 2.5 – Recession Period Statistics ────────────────────────────────
    if selected_statistics == 'Recession Period Statistics':
        recession_data = data[data['Recession'] == 1]

        # Plot 1 – Avg automobile sales over recession years (line)
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure=px.line(
                yearly_rec,
                x='Year', y='Automobile_Sales',
                title='Average Automobile Sales fluctuation over Recession Period',
            )
        )

        # Plot 2 – Avg sales by vehicle type during recessions (bar)
        average_sales = (recession_data.groupby('Vehicle_Type')['Automobile_Sales']
                         .mean().reset_index())
        R_chart2 = dcc.Graph(
            figure=px.bar(
                average_sales,
                x='Vehicle_Type', y='Automobile_Sales',
                title='Average Number of Vehicles Sold by Vehicle Type during Recession',
            )
        )

        # Plot 3 – Ad expenditure share by vehicle type during recessions (pie)
        exp_rec = (recession_data.groupby('Vehicle_Type')['Advertising_Expenditure']
                   .sum().reset_index())
        R_chart3 = dcc.Graph(
            figure=px.pie(
                exp_rec,
                names='Vehicle_Type', values='Advertising_Expenditure',
                title='Total Advertising Expenditure Share by Vehicle Type during Recession',
            )
        )

        # Plot 4 – Unemployment rate effect on vehicle type & sales (bar)
        unemp_data = (recession_data
                      .groupby(['unemployment_rate', 'Vehicle_Type'])['Automobile_Sales']
                      .mean().reset_index())
        R_chart4 = dcc.Graph(
            figure=px.bar(
                unemp_data,
                x='unemployment_rate', y='Automobile_Sales', color='Vehicle_Type',
                labels={'unemployment_rate': 'Unemployment Rate',
                        'Automobile_Sales':  'Average Automobile Sales'},
                title='Effect of Unemployment Rate on Vehicle Type and Sales',
            )
        )

        return [
            html.Div(className='chart-item',
                     children=[html.Div(R_chart1), html.Div(R_chart2)],
                     style={'display': 'flex'}),
            html.Div(className='chart-item',
                     children=[html.Div(R_chart3), html.Div(R_chart4)],
                     style={'display': 'flex'}),
        ]

    # ── TASK 2.6 – Yearly Statistics ─────────────────────────────────────────
    elif input_year and selected_statistics == 'Yearly Statistics':
        yearly_data = data[data['Year'] == input_year]

        # Plot 1 – Yearly sales trend, full period (line)
        yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(
            figure=px.line(
                yas, x='Year', y='Automobile_Sales',
                title='Yearly Automobile Sales over the Whole Period',
            )
        )

        # Plot 2 – Total monthly sales for selected year (line)
        mas = yearly_data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        Y_chart2 = dcc.Graph(
            figure=px.line(
                mas, x='Month', y='Automobile_Sales',
                title='Total Monthly Automobile Sales in {}'.format(input_year),
            )
        )

        # Plot 3 – Avg vehicles sold by vehicle type in selected year (bar)
        avr_vdata = (yearly_data.groupby('Vehicle_Type')['Automobile_Sales']
                     .mean().reset_index())
        Y_chart3 = dcc.Graph(
            figure=px.bar(
                avr_vdata, x='Vehicle_Type', y='Automobile_Sales',
                title='Average Vehicles Sold by Vehicle Type in {}'.format(input_year),
            )
        )

        # Plot 4 – Total ad expenditure by vehicle type in selected year (pie)
        exp_data = (yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure']
                    .sum().reset_index())
        Y_chart4 = dcc.Graph(
            figure=px.pie(
                exp_data, names='Vehicle_Type', values='Advertising_Expenditure',
                title='Total Advertising Expenditure by Vehicle Type in {}'.format(input_year),
            )
        )

        return [
            html.Div(className='chart-item',
                     children=[html.Div(Y_chart1), html.Div(Y_chart2)],
                     style={'display': 'flex'}),
            html.Div(className='chart-item',
                     children=[html.Div(Y_chart3), html.Div(Y_chart4)],
                     style={'display': 'flex'}),
        ]

    else:
        return None


# Run the Dash app
if __name__ == '__main__':
    app.run(debug=True)
