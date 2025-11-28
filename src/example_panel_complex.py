# ## launch from terminal
# poetry run panel serve src/example_panel_complex.py

import panel as pn
import plotly.express as px
import altair as alt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Enable extensions
pn.extension("plotly")

# ----------------------------------------------------------
# DATA
# ----------------------------------------------------------
df = px.data.gapminder()

# ----------------------------------------------------------
# WIDGETS (User inputs)
# ----------------------------------------------------------
continent_select = pn.widgets.Select(
    name="Continent",
    options=sorted(df["continent"].unique()),
    value="Europe"
)

year_slider = pn.widgets.Select(
    name="Year", 
    options=sorted(df["year"].unique()), 
    value=2002
)

n_points_slider = pn.widgets.IntSlider(
    name="Number of Points (for Matplotlib)", start=50, end=500, value=200
)

# ----------------------------------------------------------
# FILTER DATA - IMPROVEMENT
# ----------------------------------------------------------

@pn.cache(200)
def get_filtered(continent, year):
    return df[(df["continent"] == continent) & (df["year"] == year)]

# ----------------------------------------------------------
# VISUALIZATIONS (reactive, depend on widgets)
# ----------------------------------------------------------

# ---- Plotly: bubble chart by continent & year ----
def plotly_bubble(continent, year):
    dff = get_filtered(continent, year)
    fig = px.scatter(
        dff,
        x="gdpPercap",
        y="lifeExp",
        size="pop",
        color="country",
        title=f"Life Expectancy vs GDP — {continent} ({year})",
        hover_name="country",
        log_x=True,
    )
    return fig

plotly_pane = pn.bind(plotly_bubble, continent_select, year_slider)


# ---- Altair: bar chart of life expectancy by country ----
def altair_bar(continent, year):
    dff = get_filtered(continent, year)
    chart = (
        alt.Chart(dff)
        .mark_bar()
        .encode(
            x=alt.X("country:N", sort="-y"),
            y="lifeExp:Q",
            color="country:N",
        )
        .properties(title=f"Life Expectancy — {continent} ({year})")
        .interactive()  # enable panning, zooming
    )
    return chart

altair_pane = pn.bind(altair_bar, continent_select, year_slider)


# ---- Matplotlib: sine wave with adjustable points ----
def mpl_plot(n_points):
    x = np.linspace(0, 10, n_points)
    y = np.sin(x)

    fig, ax = plt.subplots(figsize=(5, 3))
    ax.plot(x, y)
    ax.set_title(f"Sine Wave with {n_points} points")
    ax.grid(True)

    return fig

mpl_pane = pn.bind(mpl_plot, n_points_slider)


# ---- Data Table (filtered) ----
def table_view(continent, year):
    dff = get_filtered(continent, year)
    return dff[["country", "lifeExp", "pop", "gdpPercap"]]

table_pane = pn.bind(table_view, continent_select, year_slider)


# ----------------------------------------------------------
# LAYOUT WITH TABS
# ----------------------------------------------------------

tabs = pn.Tabs(
    ("Plotly Bubble Chart", pn.Column(plotly_pane)),
    ("Altair Bar Chart", pn.Column(altair_pane)),
    ("Matplotlib Plot", pn.Column(mpl_pane)),
    ("Data Table", pn.Column(pn.pane.DataFrame(table_pane))),
)


# ----------------------------------------------------------
# TEMPLATE FOR NICE UI
# ----------------------------------------------------------

template = pn.template.FastListTemplate(
    title="Complex Mixed Visualization Dashboard (Panel)",
    sidebar=[
        "### Global Controls",
        continent_select,
        year_slider,
        "### Matplotlib Settings",
        n_points_slider,
    ],
    main=tabs,
    theme="dark"  # can be "default", "dark", "fast", etc
)

template.servable()
