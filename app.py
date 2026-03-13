import streamlit as st
import career_database   # your career_database.py
import questions         # your questions.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

import json

def load_data():
    with open("career_database.json", "r") as f:
        careers = json.load(f)
    with open("quiz_questions.json", "r") as f:
        questions = json.load(f)
    return careers, questions

CAREER_DATABASE, QUIZ_QUESTIONS = load_data()




# Set page configuration
st.set_page_config(
    page_title="Career Path Finder",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(
    """
    <style>
    /* Remove radio button container box */
    div[data-testid="stRadio"] {
        background: none !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
    }

    /* Remove slider container box */
    div[data-testid="stSlider"] {
        background: none !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

hide_sidebar_css = """
<style>
[data-testid="stSidebar"] {
    display: none;
}
[data-testid="stSidebarNav"] {
    display: none;
}
</style>
"""
st.markdown(hide_sidebar_css, unsafe_allow_html=True)

 # Enhanced Custom CSS for better styling and user experience
light_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

body {
font-family: 'Inter', sans-serif;
    background-color: #f9fafb !important; /* gray-50 */
    color: #111827; /* gray-900 */

}
.main-container {
    background: #fff;
    border-radius: 18px;
    box-shadow: 0 8px 32px 0 rgba(31, 119, 180, 0.15);
    padding: 2.5rem 2rem 2rem 2rem;
    margin: 2rem auto 2rem auto;
    max-width: 900px;
    animation: fadeIn 1.2s;
}
.block-container {
  overflow: auto;              /* allow scrolling */
  scrollbar-width: none;       /* Firefox */
  -ms-overflow-style: none;    /* IE/Edge */
}

.block-container::-webkit-scrollbar {
  display: none;               /* Chrome, Safari, Opera */
}


@keyframes fadeIn {
    0% { opacity: 0; transform: translateY(30px); }
    100% { opacity: 1; transform: translateY(0); }
}
.main-header {
    font-size: 2.7rem;
    color: #3a3a7c;
    text-align: center;
    margin-bottom: 1.5rem;
    font-weight: 800;
    letter-spacing: 1px;
    text-shadow: 1px 2px 8px rgba(31,119,180,0.08);
}
.sub-header {
    font-size: 1.3rem;
    color: #2c3e50;
    margin: 1.2rem 0 0.7rem 0;
    font-weight: 600;
}
.career-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 1.5rem;
    border-radius: 12px;
    color: white;
    margin: 1rem 0;
    box-shadow: 0 4px 16px rgba(0,0,0,0.10);
    font-size: 1.8rem;
}
.trait-score {
    background: #f8f9fa;
    padding: 0.5rem 1rem;
    border-radius: 7px;
    margin: 0.3rem 0;
    border-left: 5px solid #1f77b4;
    font-size: 1.05rem;
}

.instruction-box {
            background: #ffffff;
            border: 1.2px solid #000000;
            border-radius: 0.75rem;
            padding: 2rem;
            margin: 1rem auto;
            max-width: 1400px;
            text-align: left;
                        border: none;'            

        }
    
        .instruction-box h2 {
            color: #111827;
            margin: 1rem auto 0 auto;
        }
        .instruction-box p {
            font-size: 1.25rem;
            color: #374151;
            margin-bottom: 1rem;
        }


.confidence-high { color: #27ae60; font-weight: bold; }
.confidence-medium { color: #f39c12; font-weight: bold; }
.confidence-low { color: #e74c3c; font-weight: bold; }
.badge {
    display: inline-block;
    padding: 0.25em 0.7em;
    font-size: 1em;
    font-weight: 700;
    border-radius: 0.5em;
    margin-left: 0.5em;
    box-shadow: 0 2px 8px rgba(31,119,180,0.08);
}
.badge-green { background: #27ae60; color: white; }
.badge-orange { background: #f39c12; color: white; }
.badge-red { background: #e74c3c; color: white; }
.testimonial {
    background: #f1f8ff;
    border-left: 5px solid #1f77b4;
    margin: 1em 0;
    padding: 1em;
    border-radius: 8px;
    font-style: italic;
    font-size: 1.05rem;
}
.footer {
    text-align: center;
    color: #888;
    font-size: 1rem;
    margin-top: 2.5rem;
    margin-bottom: 0.5rem;
    letter-spacing: 0.5px;
}

</style>
"""
st.markdown(light_css, unsafe_allow_html=True)



import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import json

# ---------------- DATA LOADING ----------------
def load_data():
    with open("career_database.json", "r") as f:
        careers = json.load(f)
    with open("quiz_questions.json", "r") as f:
        questions = json.load(f)
    return careers, questions

CAREER_DATABASE, QUIZ_QUESTIONS = load_data()

# ---------------- CAREER DETAILS ----------------
def show_career_details(career_name, title, compact=False):
    career_info = CAREER_DATABASE.get(career_name, None)
    if not career_info:
        st.warning(f"No data found for {career_name}")
        return

    if not compact:
        st.markdown(f"#### {title}")
        with st.expander(f"Learn more about {career_name}", expanded=True):
            st.markdown(f"**Description:** {career_info.get('description','')}")
            st.markdown(f"**Job Roles:** {', '.join(career_info.get('job_roles', []))}")
            st.markdown(f"**Salary Range:** {career_info.get('salary_range','')}")
            st.markdown(f"**Tools & Technologies:** {', '.join(career_info.get('tools', []))}")
            st.markdown("**Learning Resources:**")
            for resource in career_info.get('learning_resources', []):
                st.markdown(f"• {resource}")
    else:
        with st.expander(f"{career_name}"):
            st.markdown(f"{career_info.get('description','')[:100]}...")
            st.markdown(f"**Salary:** {career_info.get('salary_range','')}")



# ---------------- MAIN FLOW ----------------
def main():
    # Main header
    st.markdown('<h1 class="main-header">WHAT CAREER PATH IS RIGHT FOR ME?</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.5rem; color: #000;">Discover your ideal Career with AI-Powered Recommendations</p>', unsafe_allow_html=True)

    # Progress bar
    steps = ['info', 'quiz', 'results']
    if "current_step" not in st.session_state:
        st.session_state.current_step = "info"   # ✅ start directly at instruction/info page
    elif st.session_state.current_step not in steps:
        st.session_state.current_step = "info"   # ✅ reset if invalid

    current_step_index = steps.index(st.session_state.current_step)
    progress = (current_step_index + 1) / len(steps)
    st.progress(progress)

    # Flow control
    if st.session_state.current_step == 'info':
        show_user_info_form()
    elif st.session_state.current_step == 'quiz':
        show_quiz()
    elif st.session_state.current_step == 'results':
        show_results()


# ---------------- INFO / INSTRUCTIONS ----------------
def show_user_info_form():
    st.markdown("""
        <div class="instruction-box">
            <h2>Your Journey Starts Here</h2>
             <p style="text-align: left; font-size: 1.2rem; color: #000;">
        Choosing the right career path can feel overwhelming, 
        but understanding your strengths, interests, and values is the first step toward building a fulfilling future. That’s why we created this free career test, a tool designed to help you identify the best career options 
        based on your unique profile. This test evaluates your interests, skills, and working style to match you with potential careers across 
        business, technology, creative, healthcare, education, and analytical domains. When answering, try to select the option that most closely reflects your natural preferences.
    </p>
    <p style="text-align: left; font-size: 1.5rem; color: #000;">Career Test Instructions</p>

    <ul style="font-size:40px; color:#000; text-align:left; list-style-type:disc;">        
        <li li style="font-size:19px;">20 multiple-choice questions</li>
        <li li style="font-size:19px;">Takes approximately 5-15 minutes</li>
        <li li style="font-size:19px;">Immediate results with career recommendations</li>
        <li li style="font-size:19px;">Custom learning paths based on results</li>
    </ul>
            <p style="text-align: left; font-size: 1.2rem; color: #000;">Answer the following skill-based questions and click Get Career Recommendation to calculate your score.<br> Use your score to find recommendations aligning with your skill level and interests.</p>

    </div>

    """, unsafe_allow_html=True)

    st.markdown(
    """
    <style>
   div.stButton > button:first-child {
      background-color: #000000;
      color: white;
      font-size: 1.2rem;
      border-radius: 8px;
      cursor: pointer;
      margin-top: -150px;
      margin-left: 12.5rem;
      margin-right: -150px;
    }
    div.stButton > button:first-child:hover {
        background-color: #333333;
    }
    </style>
    """,
    unsafe_allow_html=True
    )

    if st.button("Start Career Test"):
        st.session_state.current_step = 'quiz'
        st.rerun()

# 🔹 CSS injection to hide the placeholder option
st.markdown(
    """
    <style>
    div[data-testid="stRadio"] label:first-child {
        display: none !important;
    }
    div[data-testid="stRadio"] label span {
        color: black !important;
    }
    div[data-testid="stRadio"] label span {
        color: #333 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- QUIZ ----------------
def show_quiz():
    st.markdown('<h2 class="sub-header">Career Test Assessment</h2>', unsafe_allow_html=True)
    scores = {}

    with st.form("career_recommendation"):
        for i, q in enumerate(QUIZ_QUESTIONS):
            st.markdown(
                f"""
                <div class='question-text' style='margin-bottom:10px; font-size:22px; font-weight:bold;'>
                    Question {i+1}: {q['question']}
                </div>
                """,
                unsafe_allow_html=True
            )

            if q['type'] == 'slider':
                score = st.slider("", min_value=1, max_value=5, value=3, key=f"q_{i}", label_visibility="collapsed")
            else:  # radio
                options = ["Select an option..."] + q['options']
                selection = st.radio("", options, key=f"q_{i}", label_visibility="collapsed", index=0)
                score = q['options'].index(selection) + 1 if selection != "Select an option..." else 0  # ✅ default to 0

            scores[q['trait']] = score
            st.markdown("---")

        submitted = st.form_submit_button("Get My Career Recommendations", type="primary")
        if submitted:
            st.session_state.quiz_scores = scores
            st.session_state.current_step = 'results'
            st.toast("Quiz completed! Generating your personalized career recommendations...", icon="🎉")
            st.balloons()
            st.rerun()

def show_results():
    st.markdown('<h2 class="sub-header">Your Career Recommendations</h2>', unsafe_allow_html=True)

    # ✅ Fixed data from your record
    top_career = "UX/UI Designer"
    confidence = 89.88888888888889
    personality_tag = "People Person"
    trait_scores = {
        "Organization": 3,
        "Patience": 3,
        "Communication": 4,
        "Logical Thinking": 3,
        "Math": 5,
        "Tech Affinity": 3,
        "Analytical": 4,
        "Creativity": 3,
        "Empathy": 5,
        "Leadership": 2
    }
 

    # Header layout
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        badge = "badge-green" if confidence > 80 else "badge-orange" if confidence > 60 else "badge-red"
        st.markdown(f"### **{top_career}** <span class='badge {badge}'>{confidence:.1f}% match</span>", unsafe_allow_html=True)
    with col2:
        st.metric("Personality Type", " People Person")
    with col3:
        if st.button("Save Results"):
            st.success("Results saved!")

    # Career details
    show_career_details(top_career, " Top Recommendation")

    # Alternative careers (hard-coded for now, like your screenshot)
    st.markdown("### Alternative Career Paths")
    col1, col2 = st.columns(2)
    with col1:
        show_career_details("Counselor/Therapist", " Second Choice", compact=True)
    with col2:
        show_career_details("UX/UI Designer", " Third Choice", compact=True)

    # ✅ Call trait analysis here
    show_trait_analysis(top_career, trait_scores)
2026-03-14 03:07:21,,,,,UX/UI Designer,89.99999999999999,Analytical Mind,3,1,4,5,3,2,1,4,4,1


def show_trait_analysis(top_career="UX/UI Designer", trait_scores=None):
    st.markdown("### Your Trait Analysis")

    # ✅ Trait scores from your record if none passed
    if trait_scores is None:
        trait_scores = {
            "Organization": 3,
            "Patience": 1,
            "Communication": 4,
            "Logical Thinking": 5,
            "Math": 3,
            "Tech Affinity": 2,
            "Analytical": 1,
            "Creativity": 4,
            "Empathy": 4,
            "Leadership": 1
        }

    traits = list(trait_scores.keys())
    scores = list(trait_scores.values())

    # Radar chart
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=scores + [scores[0]],  # close polygon
        theta=traits + [traits[0]],
        fill='toself',
        name='Your Scores',
        line_color='rgb(31, 119, 180)'  # Blue
    ))

    if top_career and top_career in CAREER_DATABASE:
        required = CAREER_DATABASE[top_career]["required_traits"]
        avg_required = [required.get(trait, 0.5) * 5 for trait in traits]
        fig.add_trace(go.Scatterpolar(
            r=avg_required + [avg_required[0]],
            theta=traits + [traits[0]],
            fill='toself',
            name=f"{top_career} Ideal",
            line_color='rgb(255, 127, 14)'  # Orange
        ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5]
            )
        ),
        showlegend=True,
        title="Your Trait Profile",
        height=500
    )

    # Layout: chart left, trait breakdown right
    col1, col2 = st.columns([2, 1])
    with col1:
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.markdown("#### Trait Breakdown")

        # ✅ Box style for each trait
        for trait, score in trait_scores.items():
            trait_name = trait.replace('_', ' ').title()
            st.markdown(
                f"""
                <div style="
                    background-color:#ffffff;
                    border:1px solid #ddd;
                    border-radius:8px;
                    padding:12px;
                    margin-bottom:10px;
                    font-size:1rem;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                ">
                    <b>{trait_name}</b>
                    {score}/5
                </div>
                """,
                unsafe_allow_html=True
            )

# ---------------- ENTRY POINT ----------------
if __name__ == "__main__":
    main()