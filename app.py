import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import numpy as np

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

url = 'https://raw.githubusercontent.com/jon-aegis/meter-data/master/Fairingway.csv'

df = pd.read_csv(url)
df['DT'] = pd.to_datetime(df.DT, infer_datetime_format=True)
df = df.replace(0, np.nan)
df = df.dropna(how='all', axis=0)

colors = {
    'background': '#000000',
    'text': '#0CDDD7'
}

app.layout = html.Div(children=[
    html.H1(children='Sample of Our Data', style={
            'textAlign': 'center',
            'color': colors['text']}),

    html.Div(children='''
        Data: Real Power, Gas Use, and BTU Output
    ''', style={'textAlign': 'center',
                'color': colors['text']}),
    dcc.Graph(
        id='Real Power',
        figure={
            'data': [
                go.Scatter(
                    x=df[df['location'] == i]['DT'],
                    y=df[df['location'] == i]['Real Power kW'],
                    text=df[df['location'] == i]['location'],
                    mode='lines',
                    opacity=0.7,
                    name=i
                ) for i in df.location.unique()
            ],
            'layout': go.Layout(
                title= '',
                xaxis={'title': 'Date'},
                yaxis={'title': 'Real Power kW'},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
        }
    ),
    dcc.Graph(
        id='Gas Use',
        figure={
            'data': [
                go.Scatter(
                    x=df[df['location'] == i]['DT'],
                    y=df[df['location'] == i]['Gas Use'],
                    text=df[df['location'] == i]['location'],
                    mode='lines',
                    opacity=0.7,
                    name=i
                ) for i in df.location.unique()
            ],
            'layout': go.Layout(
                xaxis={'title': 'Date'},
                yaxis={'title': 'Gas Use'},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
        }
    ),
    dcc.Graph(
        id='BTU Output',
        figure={
            'data': [
                go.Scatter(
                    x=df[df['location'] == i]['DT'],
                    y=df[df['location'] == i]['BTU Output'],
                    text=df[df['location'] == i]['location'],
                    mode='lines',
                    opacity=0.7,
                    name=i
                ) for i in df.location.unique()
            ],
            'layout': go.Layout(
                xaxis={'title': 'Date'},
                yaxis={'title': 'BTU Output'},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
