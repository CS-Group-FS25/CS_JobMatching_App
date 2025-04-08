import streamlit as st

def page_one():
    st.write("PAGE ONE")
import pandas as pd
import numpy as np  

class NutzerInfo:
    def __init__(age, education_status, current_job, desired_job):
        self.age = age
        self.education_status = education_status
        self.current_job = current_job
        self.desired_job = desired_job

    def __str__(self):
        return f"Age: {self.age}, Education Status: {self.education_status}, Current Job: {self.current_job}, Desired Job: {self.desired_job}"

if "nutzer" not in st.session_state:
    st.session_state.nutzer = NutzerInfo()

st.write("This is the Job Matcher page")
st.write("This app will help you find the best job for you")
st.write("Please enter your preferences below:")
age = st.number_input("What is your age?")
if age < 18:
    education_status = st.text_input("Are you still in education?")
else:
    current_job = st.text_input("What is your current job?")


st.text_input("What is your desired job?")