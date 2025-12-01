# https://codeshare.io/5QdvvQ

# https://shiny.posit.co/py/api/core/
# UI Inputs / Rendering outputs

# in terminal: shiny run --reload basic-app-example-shiny.py
from shiny import App, render, ui
import plotnine as pn
import pandas as pd

df = pd.read_csv("https://raw.githubusercontent.com/tidyverse/dplyr/master/data-raw/starwars.csv")

app_ui = ui.page_fluid(
    ui.panel_title(ui.h2("Model Dashboard")),
    ui.markdown("Using `ui.layout_columns()` for the layout."),
    ui.layout_columns(
        ui.card(
ui.input_select(id="eye_color", label="Select eye color", choices=list(df.eye_color.unique())),
        ),
ui.card(
    ui.card_header("Subsetted dataframe (sorted)"),
    ui.output_data_frame(id="data_frame"),
    full_screen=True,
),
        ui.card(
ui.card_header("Height Histogram"),
    ui.output_plot(id="height_histogram"),
    full_screen=True,
),
ui.card(
    ui.card_header("Distrib of Gender"),
    ui.output_plot(id="distrib_genre"),
    full_screen=True,
),
        col_widths={"sm": (3, 9, 6, 6)},
        # row_heights=(2, 3),
        height="800px",
    ),
)

def height_histogram_defini_ailleurs(df_subsetted):
        return (
          pn.ggplot(data=df_subsetted)+
          pn.aes(x='height')+
          pn.geom_histogram()
        )

def server(input):

    @reactive.effect
    def my_subsetted_df():
	print(f'NEW VaLUE::: {input.eye_color()}')
	dff = df[(df['eye_color']==input.eye_color())]

    @render.text
    def nb_characters():
        return f'{my_subsetted_df().shape[0]} characters filtered.'

    @render.data_frame
    def data_frame():
        return my_subsetted_df()

    @render.plot
    def height_histogram():
	  return height_histogram_defini_ailleurs(df_subsetted = my_subsetted_df())

    @render.plot
    def distrib_genre():
        return (
          pn.ggplot(data=my_subsetted_df())+
          pn.aes(x='gender')+
          pn.geom_bar()
        )

app = App(app_ui, server)