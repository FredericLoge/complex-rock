# in terminal: python basic-app-example-dash.py
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

df = pd.read_csv("https://raw.githubusercontent.com/tidyverse/dplyr/master/data-raw/starwars.csv")

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(id="var", options=["mass", "height"],       # UI Input Element
      value="mass", clearable=False),                        
    dcc.Graph(id="hist")                                     # UI Output Element
])

@app.callback(                       # callback: update the var selected changes
    Output("hist", "figure"),
    Input("var", "value")
)
def update_hist(selected_var):
    return px.histogram(df, x=selected_var, title=f"Histogram of {selected_var}")

app.run(debug=True, use_reloader=False) # debugger is super useful!
