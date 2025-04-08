import streamlit as st
import pandas as pd
import numpy as np  




st.write("This is the Job Matcher page")
st.write("This app will help you find the best job for you")
st.write("Please enter your preferences below:")
age = st.number_input("What is your age?")
if age < 18:
    education_status = st.text_input("Are you still in education?")
else:
    current_job = st.text_input("What is your current job?")


st.text_input("What is your desired job?")