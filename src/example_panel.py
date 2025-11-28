# ## launch from terminal
# poetry run panel serve src/example_panel.py

import panel as pn
import plotly.express as px
import altair as alt
import matplotlib.pyplot as plt
import numpy as np

pn.extension('plotly')  # enable Plotly support

# -----------------------
# WIDGET
# -----------------------
slider = pn.widgets.IntSlider(name="Number of Points", start=10, end=200, value=50)

# -----------------------
# PLOTLY
# -----------------------
def plotly_fig(n):
  df = px.data.iris().head(n)
  return px.scatter(df, x="sepal_width", y="sepal_length")

plotly_pane = pn.bind(plotly_fig, slider)

# -----------------------
# ALTAIR
# -----------------------
def altair_fig(n):
  df = px.data.iris().head(n)
  chart = alt.Chart(df).mark_circle().encode(x="petal_width", y="petal_length")
  return chart

altair_pane = pn.bind(altair_fig, slider)

# -----------------------
# MATPLOTLIB
# -----------------------
def mpl_fig(n):
  x = np.linspace(0, 10, n)
  y = np.sin(x)
  fig, ax = plt.subplots()
  ax.plot(x, y)
  ax.set_title("Matplotlib Sine Wave")
  return fig

mpl_pane = pn.bind(mpl_fig, slider)

# -----------------------
# LAYOUT
# -----------------------
dashboard = pn.Column(
  "# Mixed Visualization Dashboard (Panel)",
  slider,
  pn.Row(
    pn.Column("## Plotly", plotly_pane),
    pn.Column("## Altair", altair_pane),
    pn.Column("## Matplotlib", mpl_pane),
  )
)

dashboard.servable()
