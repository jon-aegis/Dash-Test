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
df = df.replace(0, np.nan)
df = df.dropna(how='all', axis=0)
df = df.replace(np.nan, 0)
df['DT'] = pd.to_datetime(df.DT, infer_datetime_format=True)

app.layout = html.Div([
    dcc.Graph(
        id='Energy_Data',
        figure={
            'data': [
                go.Scatter(
                    x=df[df['location'] == i]['DT'],
                    y=df[df['location'] == i]['Total Energy kWh'],
                    text=df[df['location'] == i]['location'],
                    mode='lines',
                    opacity=0.7,
                    lines={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'blue'}
                    },
                    name=i
                ) for i in df.location.unique()
            ],
            'layout': go.Layout(
                xaxis={'title': 'Date'},
                yaxis={'title': 'Total Energy kWh'},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
