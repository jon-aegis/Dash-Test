import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import numpy as np
import plotly.figure_factory as ff
from scipy.stats import zscore

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

url = 'https://raw.githubusercontent.com/jon-aegis/meter-data/master/Fairingway.csv'

mapbox_access_token = open("Mapbox_Token.csv").read()

df = pd.read_csv(url)
df['DT'] = pd.to_datetime(df.DT, infer_datetime_format=True)
df = df.replace(0, np.nan)
df = df.dropna(how='all', axis=0)
df = df.replace(np.nan, 0)
df['Real_Power_N'] = zscore(df['Real Power kW'])
df['Gas_Use_N'] = zscore(df['Gas Use'])

df_site = pd.read_csv('Site_Lat_Lon.csv')

x1 = df['Real_Power_N']
x2 = df['Gas_Use_N']
hist_data = [x1, x2]
group_labels = ['Real Power kW Dist', 'Gas Use Dist']

fig = ff.create_distplot(hist_data, group_labels)

colors = {
    'background': '#0F0F10',
    'background2': '#FFFFFF',
    'text': '#57B8E3',
    'text2': '#000000'
}

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(children='Sample of Our Data', style={
            'textAlign': 'center',
            'color': colors['text']}),

    html.Div(children='''
        Data: Real Power, Gas Use, and BTU Output
    ''', style={'textAlign': 'center',
                'color': colors['text']}),
    html.Div([
        html.Div([
            html.H3(children='Real Power kW', style={'textAlign': 'center',
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
                    xaxis={'title': 'Date'},
                    yaxis={'title': 'Real Power kW'},
                    margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                    legend={'x': 0, 'y': 1},
                    hovermode='closest',
                    font={'color': colors['text']},
                    plot_bgcolor= colors['background'],
                    paper_bgcolor= colors['background']
                )
            }
        )], className="six columns"),
        html.Div([
            html.H3(children='Gas Use', style={'textAlign': 'center',
                    'color': colors['text']}),
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
                    margin={'l': 50, 'b': 40, 't': 10, 'r': 10},
                    legend={'x': 0, 'y': 1},
                    hovermode='closest',
                    font={'color': colors['text']},
                    plot_bgcolor= colors['background'],
                    paper_bgcolor= colors['background']
                )
            }
        )], className="six columns")
    ]),
    html.Div([
        html.H3(children='BTU Output', style={'textAlign': 'center',
                'color': colors['text']}),
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
                margin={'l': 50, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest',
                font={'color': colors['text']},
                plot_bgcolor= colors['background'],
                paper_bgcolor= colors['background']
            )
        }
    )
]),
    html.Div([
        html.H3(children='Aegis Site Map',
                 style={'backgroundColor': colors['background'],
                        'textAlign': 'center', 'color': colors['text']}),
        dcc.Graph(
            id='Aegis Site Map',
            style={
                'height': 1000,
                'width': 1850,
                'Display': "block"
                },
            figure={
                'data': [
                    go.Scattermapbox(
                        lat= df_site['Lat'],
                        lon= df_site['Lon'],
                        mode='markers',
                        marker=dict(
                            size=10,
                        ),
                        text=df_site['Site']
                    )
                ],
                'layout': go.Layout(
                    autosize=True,
                    hovermode= 'closest',
                    plot_bgcolor=colors['background'],
                    paper_bgcolor=colors['background'],
                    margin={'l': 50, 'b': 40, 't': 10, 'r': 10},
                    mapbox=dict(
                    accesstoken= mapbox_access_token,
                    center=dict(
                        lat=40.7128,
                        lon=-74.0060
                    ),
                    zoom=10
                )
            )
        })
    ]),
    html.H3([
        html.Div(children='Gas Use and Real Power Distribution',
                 style={'backgroundColor': colors['background2'],
                'textAlign': 'center', 'color': colors['text2']}),
        dcc.Graph(
        id='Gas and Power Distribution',
        figure=fig
    )]),
])

if __name__ == '__main__':
    app.run_server(debug=True)
