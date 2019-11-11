import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

url = 'https://raw.githubusercontent.com/jon-aegis/meter-data/master/Fairingway.csv'

df = pd.read_csv(url)
df['DT'] = pd.to_datetime(df.DT, infer_datetime_format=True)

app.layout = html.Div([
    dcc.Graph(
        id='Energy_Data',
        figure={
            'data': [
                go.Scatter(
                    x=df[df['loaction'] == i]['DT'],
                    y=df[df['loaction'] == i]['Total Energy kWh'],
                    text=df[df['loaction'] == i]['location'],
                    mode='lines',
                    opacity=0.7,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name=i
                ) for i in df.loaction.unique()
            ],
            'layout': go.Layout(
                xaxis={'type': 'log', 'title': 'Date'},
                yaxis={'title': 'Total Energy kWh'},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
        }
    )
])
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
