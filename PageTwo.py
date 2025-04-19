import streamlit as st
import pandas as pd
import pydeck as pdk

def page_two():
    st.write("Diese Jobs gibt es in deiner Region")

# Streamlit UI
st.title("Aktuelle Jobs in deiner Nähe")

address = st.text_input("Ort eingeben", "Zürich")
radius = st.slider("Umkreis in km", 5, 10, 25, 50, 100)

