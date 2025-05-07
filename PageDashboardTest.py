import streamlit as st
import streamlit.components.v1 as components
import matplotlib.pyplot as plt
import numpy as np

def __init__():
    st.set_page_config(layout="wide", page_title="Job Dashboard")

def main():
    # --- Layout with 2 columns ---
    col1, col2 = st.columns([2.5, 1.5])

    # --- Left Column: Map and Job List ---
    with col1:
        st.markdown("### Job Opportunities on Map")
        # Placeholder for the map (replace with actual map later)
        st.empty()
        components.html("""
            <div style='width:100%; height:450px; background-color:#ddd; display:flex; align-items:center; justify-content:center;'>
                [Map Placeholder]
            </div>
        """, height=450)

        with st.expander("### Job Listings", expanded=True):
            sort_option = st.selectbox("Sort by:", ["Closest", "Best Paid", "Most Relevant"])
            for i in range(1, 6):
                st.markdown(f"**Job Listing {i}** - [Placeholder data]")

    # --- Right Column: Tabs for Salary, Skill Match and Top 5 Jobs ---
    with col2:
        tab1, tab2, tab3 = st.tabs(["Salary Range", "Skill Match", "Top 5 Jobs"])

        with tab1:
            st.markdown("### Salary Range")
            components.html("""
                <div style='width:100%; height:300px; background-color:#f2f2f2; display:flex; align-items:center; justify-content:center;'>
                    [Salary Chart Placeholder]
                </div>
            """, height=300)
            st.markdown("Some insights into the salary range for this role...")

        with tab2:
            st.markdown("### Skill Match by Category")
            skills = [f"Skill {i}" for i in range(1, 11)]
            match_scores = np.random.randint(40, 100, size=10)

            fig, ax = plt.subplots(figsize=(4, 4))
            ax.bar(skills, match_scores, color="#4CAF50")
            ax.set_ylabel("Match %")
            ax.set_ylim(0, 100)
            ax.set_xticklabels(skills, rotation=90)
            ax.set_title("Skill Match by Category")
            st.pyplot(fig)

        with tab3:
            st.markdown("### Your Top 5 Jobs (Clickable)")
            for i in range(1, 6):
                st.button(f"Switch to Job {i}")

