import plotly.express as px
import pandas as pd
import numpy as np
import dash 
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output


px.set_mapbox_access_token(TOKEN)


def stars_to_rating(score):
    try:
        if set(score) == set("*"):
            return len(score) * 10
        return score
    except:
        return score


def strings_to_nan(score):
    try:
        return int(score)
    except ValueError:
        return np.nan


def preprocess(df):
    df = df[~df["latitude"].isna()]
    df["SCORE"] = df["SCORE"].apply(lambda x: stars_to_rating(x))
    df["SCORE"] = df["SCORE"].apply(lambda x: strings_to_nan(x))
    df["SCORE"] = df["SCORE"].fillna(0)
    df["SCORE"] = df["SCORE"].apply(lambda x: int(x))

    df.columns = [c.strip() for c in df.columns]
    return df


df = pd.read_csv("data.csv")
df = preprocess(df)



fig = px.scatter_mapbox(
    df,
    lat="latitude",
    lon="longitude",
    color="SCORE",
    hover_data=['Place', 'location', 'SCORE'],
    color_continuous_scale=px.colors.sequential.Blues,
)


app = dash.Dash(__name__, external_stylesheets=['https://stackpath.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css'])
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