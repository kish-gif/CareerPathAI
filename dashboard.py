import streamlit as st
import pandas as pd
import plotly.express as px
import os

# -------------------------------
# Guidance Dashboard
# -------------------------------
st.title("Guidance Dashboard")


# -------------------------------
# Load Results File
# -------------------------------
if os.path.exists("results.csv"):
    df = pd.read_csv("results.csv")

    if not df.empty:
        # Show all saved results
        st.subheader("📂 Saved Results")
        st.dataframe(df)
        

        # -------------------------------
        # Career Recommendation Frequency
        # -------------------------------
        if "recommended_career" in df.columns:
            st.subheader("📊 Career Recommendation Frequency")
            career_counts = df["recommended_career"].value_counts().reset_index()
            career_counts.columns = ["Career", "Count"]
            fig_career = px.bar(
                career_counts,
                x="Career",
                y="Count",
                color="Career",
                title="Which Careers Are Recommended Most Often?",
                text_auto=True
            )
            st.plotly_chart(fig_career, use_container_width=True)

        # -------------------------------
        # Confidence Score Trend
        # -------------------------------
        if "confidence_score" in df.columns:
            st.subheader("📈 Confidence Score Trend Over Time")
            fig_conf = px.line(
                df,
                y="confidence_score",
                title="Confidence Score Progression",
                markers=True
            )
            st.plotly_chart(fig_conf, use_container_width=True)

        
        # -------------------------------
        # Learning Resources
        # -------------------------------
        if "learning_resources" in df.columns and pd.notna(latest["learning_resources"]):
            st.subheader("📚 Learning Resources")
            resources = str(latest["learning_resources"]).split(";")
            for r in resources:
                st.markdown(f"- {r.strip()}")

    else:
        st.info("No saved results yet. Complete a career test to see your dashboard.")
else:
    st.info("No results file found. Complete a career test to generate results.")