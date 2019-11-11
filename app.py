import os
import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

# app.layout = html.Div([
#     html.H2('Hello World'),
#     dcc.Dropdown(
#         id='dropdown',
#         options=[{'label': i, 'value': i} for i in ['LA', 'NYC', 'MTL', 'Holyoke', 'Bangor']],
#         value='LA'
#     ),
#     html.Div(id='display-value'),

url = 'https://raw.githubusercontent.com/jon-aegis/meter-data/master/Fairingway2.csv'

df = pd.read_csv(url)
df['DT'] = pd.to_datetime(df.DT, infer_datetime_format=True)

app.layout = html.Div([html.H1("Energy Data", style={'textAlign': 'center'})])
#     dcc.Dropdown(id='my-dropdown',options=[{'label': 'Total Energy kWh', 'value': df['Total Energy kWh']},{'label': 'Cumulative BTUs', 'value': df['Cumulative BTUs']},{'label': 'Cumulative Gas Use', 'value': df['Cumulative Gas Use']}],
#         multi=True,value=['Total Energy kWh'],style={"display": "block","margin-left": "auto","margin-right": "auto","width": "60%"}),
#     dcc.Graph(id='my-graph')
# ], className="container")
#
# @app.callback(Output('my-graph', 'figure'),
#               [Input('my-dropdown', 'value')])
# def update_graph(selected_dropdown_value):
#     dropdown = {"Total Energy kWh": df['Total Energy kWh'], "Cumulative BTUs": df['Cumulative BTUs'], "Cumulative Gas Use": df['Cumulative Gas Use']}
# trace1 = []
# trace2 = []
# trace3 = []
trace1 = go.Scatter(
    x=df['DT'], y=df['Total Energy kWh'],  # Data
    mode='lines', name='Total Energy kWh'  # Additional options
)
trace2 = go.Scatter(x=df['DT'], y=df['Cumulative BTUs'], mode='lines', name='Cumulative BTUs')
trace3 = go.Scatter(x=df['DT'], y=df['Cumulative Gas Use'], mode='lines', name='Cumulative Gas Use')

layout = go.Layout(title='Simple Plot from csv data',
                   plot_bgcolor='rgb(230, 230,230)')

fig = go.Figure(data=[trace1, trace2, trace3], layout=layout)
traces = [trace1, trace2, trace3]
data = [val for sublist in traces for val in sublist]
figure = {'data': data,
          'layout': go.Layout(colorway=["#5E0DAC", '#FF4F00', '#375CB1', '#FF7400', '#FFF400', '#FF0056'],
                              height=600,
                              title="Energy Data",
                              xaxis={"title": "Date",
                                     'rangeselector': {'buttons': list(
                                         [{'count': 1, 'label': '1M', 'step': 'month', 'stepmode': 'backward'},
                                          {'count': 6, 'label': '6M', 'step': 'month', 'stepmode': 'backward'},
                                          {'step': 'all'}])},
                                     'rangeslider': {'visible': True}, 'type': 'date'},
                              yaxis={"title": "Price (USD)"})}
print(figure)
    # dcc.Graph(
    #     id='example-graph',
    #     figure={
    #         'data': [
    #             {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
    #             {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
    #         ],
    #         'layout': {
    #             'title': 'Dash Data Visualization'
#             }
#         }
#     )
# ])

# @app.callback(dash.dependencies.Output('display-value', 'children'),
#               [dash.dependencies.Input('dropdown', 'value')])
# def display_value(value):
#     return 'You have selected "{}"'.format(value)

if __name__ == '__main__':
    app.run_server(debug=True)
