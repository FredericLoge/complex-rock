# in terminal: shiny run --reload basic-app-example-shiny.py
from shiny import App, render, ui
import plotnine as pn
import pandas as pd

df = pd.read_csv("https://raw.githubusercontent.com/tidyverse/dplyr/master/data-raw/starwars.csv")

## user interface (UI) definition
app_ui = ui.page_fixed(                               # HTML/CSS/JS content
    ui.input_select(                                  # UI Input Element
        id="var", label="Select variable", choices=["height", "mass"]
    ),
    ui.output_plot("hist")                            # UI Output Element
)

## server function provides access to client-side input values
def server(input):                          # python function
    @render.plot                            # indicate reactivity + output type
    def hist():
        return (
          pn.ggplot(data=df)+
          pn.aes(x=input.var())+ # accessing input.var() value
          pn.geom_histogram()
        )

app = App(app_ui, server)
