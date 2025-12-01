# panel serve basic-app-example-panel.py --dev
import panel as pan
import pandas as pd
import plotly.express as px
pan.extension('plotly')
df = pd.read_csv("https://raw.githubusercontent.com/tidyverse/dplyr/master/data-raw/starwars.csv")

var = pan.widgets.Select(                                     # UI Input element
    name="Select variable", options=["mass", "height"], value="mass"
)

def make_plot(selected_var):                  # python function to update output
    return px.histogram( 
      df, x=selected_var, title=f"Histogram of {selected_var}"
    )

interactive_plot = pan.bind(               # binding output function to an input
  make_plot, selected_var=var
)

app = pan.Column(                       # Layout
    var,                                # Input
    pan.pane.Plotly(interactive_plot)   # Output
)

app.servable()
