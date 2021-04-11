import os

import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output


MAPBOX_TOKEN = os.getenv('MAPBOX_TOKEN')
px.set_mapbox_access_token(MAPBOX_TOKEN)

df = pd.read_csv('data.csv')
fig = px.scatter_mapbox(
    df,
    lat="latitude",
    lon="longitude",
    color="SCORE",
    hover_data=['Place', 'location', 'SCORE'],
    color_continuous_scale=px.colors.sequential.Blues,
)


app = dash.Dash(
    __name__, 
    external_stylesheets=[
        'https://stackpath.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css'
    ]
)
server = app.server


app.layout = html.Div([

    html.H3(
        "Jimmy Papa's Ulitmate Philadelphia Cheesesteak Adventure, A Story", 
        style={
            'padding-left': '25px',
            'padding-bottom': '0px',
            'margin-bottom': '0px'
        }
    ),

    html.Div(id='map_div', children=[
        dcc.Graph(
            id = 'map',
            figure=fig
        )
    ]),
    html.Div(style={'padding-left': '50px','padding-right': '50px'}, children=[
        html.Div("Jimmy Papa's Note:", style={'font-weight': 'bold'}),
        html.Div(id='notes')
    ])

])

@app.callback(
    Output('notes', 'children'),
    [Input('map', 'hoverData')]
)
def display_notes(hover):
    note = df.loc[hover['points'][0]['pointIndex']]['Note']
    return html.Div(note)

if __name__ == '__main__':
    app.run_server(debug=False)
