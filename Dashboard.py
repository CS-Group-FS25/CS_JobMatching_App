import streamlit as st

'''def show_job(page, job_titles_list):
    st.title(f"DASHBOARD FÜR {job_titles_list[page]}")'''

def main():
    st.title("DASHBOARD FÜR JOB MATCHER")
    # show_job(page, job_titles_list)
    st.write(f"Du hast job {st.session_state.clicked_job} angeklickt")