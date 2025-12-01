# panel serve scripts/example_geoviews.py --autoreload

import geoviews as gv
import holoviews as hv
import cartopy.crs as ccrs
import pandas as pd
import panel as pan

hv.extension('bokeh')  

# Example coordinates (latitude, longitude)
data = pd.DataFrame({
    "city": ["Paris", "London", "New York"],
    "lat":  [48.8566, 51.5074, 40.7128],
    "lon":  [ 2.3522, -0.1278, -74.0060]
})

# Base map (tiles)
tiles = gv.tile_sources.OSM.options(width=800, height=500)

# Points layer
points = gv.Points(
    data,
    kdims=["lon", "lat"],
    vdims=["city"]
).opts(
    color="red",
    size=10,
    tools=["hover"],
    marker="circle"
)

# Labels (optional)
labels = gv.Labels(data, kdims=["lon", "lat"], vdims=["city"]).opts(
    text_color="black",
    text_font_size="12pt",
    yoffset=6
)

# Combine map + markers
map_with_points = tiles * points * labels


bokeh_plot = hv.render(map_with_points, backend="bokeh")

# Show it in Panel
app = pan.Column(
    "# GeoViews Map with Markers (Panel)",
    map_with_points
)

app.servable()
