import streamlit as st
from LandingPage import landing_page
from PageOne import page_one
from PageTwo import page_two
from PageThree import page_three
from PageFour import page_four


# Menu Sidebar wird definiert. Der Standartwert ist wird auf LandingPage gesetzt
st.sidebar.title("TITEL SIDEBAR")
menu = st.sidebar.selectbox(
    "Choose a page",
    ["Landing Page",
     "Seite 1",
     "Seite 2",
     "Seite 3",
     "Seite 4"],
    index=0             # Definition des Standartwertes (LandingPage)
)

# Page Routing basierend auf Sidebar Auswahl
if menu == "Landing Page":
    landing_page()
elif menu == "Seite 1":
    page_one()
elif menu == "Seite 2":
    page_two()
elif menu == "Seite 3":
    page_three()
elif menu == "Seite 4":
    page_four()