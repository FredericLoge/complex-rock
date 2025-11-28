# ## to run the app, in terminal:
# streamlit run src/example_streamlit.py

import streamlit as st
import pandas as pd
import numpy as np

st.title("Mon App Streamlit Super Simple")

# Widget pour choisir le nombre de points
nombre_points = st.slider("Choisissez le nombre de points", 10, 100, 50)

# Génération de données
data = pd.DataFrame({
    'x': np.random.randn(nombre_points),
    'y': np.random.randn(nombre_points),
})

# Affichage d'un graphique
st.line_chart(data)
