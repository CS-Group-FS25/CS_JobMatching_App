import streamlit as st
import pandas as pd


st.write("This is the landing page")

    
    
st.title("Job Fit Application")
st.subheader("Welcome to your personal Job Matcher")
st.write("Find the best job for you based on your preferences!")
st.write("Please chose your prefered function on the left sidebar:")

menü = st.sidebar.radio("Menu", ("Startseite", "Job Matcher", "Job nach Region", "Gehaltsfinder", "About" ))

if menü == "Startseite":
    st.write("Du bist auf der Startseite")
elif menü == "Job Matcher":
    import PageOne
    PageOne.main()
elif menü == "Job nach Region":
    import PageTwo
    PageTwo.main()
elif menü == "Gehaltsfinder":
    import PageThree
    PageThree.main()
