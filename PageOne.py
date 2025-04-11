import streamlit as st
import pandas as pd
import numpy as np  

class Nutzerinformation:
    def __init__(self, age, education_status, current_job, branch, worktime, salary):
        self.age = age
        self.education_status = education_status
        self.current_job = current_job
        self.branch = branch
        self.worktime = worktime
        self.salary = salary



st.write("This is the Job Matcher page")
st.write("This app will help you find the best job for you")
st.write("Please enter your informations below:")
age = st.number_input("What is your age?")
if age < 18:
    education_status = st.text_input("Are you still in education?")
else:
    current_job = st.text_input("What is your current job?")


st.text_input("What is your desired job?")