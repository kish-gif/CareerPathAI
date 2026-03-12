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



class CareerGuidanceSystem:
    def __init__(self):
        self.user_data = {}
        self.quiz_scores = {}
        self.ml_model = None
        self.load_or_create_sample_data()
    
    def load_or_create_sample_data(self):
        """Load existing data or create sample dataset for ML model"""
        try:
            self.df = pd.read_csv('career_quiz_data.csv')
        except FileNotFoundError:
            # Create sample dataset
            sample_data = []
            careers = list(CAREER_DATABASE.keys())
            
            for _ in range(100):  # Generate 100 sample records
                record = {}
                career = np.random.choice(careers)
                career_traits = CAREER_DATABASE[career]["required_traits"]
                
                # Generate scores based on career requirements with some noise
                for trait in ["math", "logical_thinking", "creativity", "tech_affinity", 
                             "empathy", "communication", "leadership", "analytical", 
                             "patience", "organization"]:
                    if trait in career_traits:
                        base_score = career_traits[trait]
                        record[trait] = max(1, min(5, np.random.normal(base_score * 5, 0.5)))
                    else:
                        record[trait] = np.random.uniform(1, 5)
                
                record['career'] = career
                sample_data.append(record)
            
            self.df = pd.DataFrame(sample_data)
            self.df.to_csv('career_quiz_data.csv', index=False)
    
    def train_ml_model(self):
        """Train a simple ML model for career prediction"""
        if len(self.df) > 0:
            features = ["math", "logical_thinking", "creativity", "tech_affinity", 
                       "empathy", "communication", "leadership", "analytical", 
                       "patience", "organization"]
            
            X = self.df[features]
            y = self.df['career']
            
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            
            self.ml_model = RandomForestClassifier(n_estimators=100, random_state=42)
            self.ml_model.fit(X_scaled, y)
            self.scaler = scaler
    
    def calculate_career_match(self, user_scores):
        """Calculate career match using rule-based logic"""
        career_scores = {}
        
        for career, info in CAREER_DATABASE.items():
            required_traits = info["required_traits"]
            total_score = 0
            trait_count = 0
            
            for trait, required_level in required_traits.items():
                if trait in user_scores:
                    user_score = user_scores[trait] / 5.0  # Normalize to 0-1
                    trait_score = 1 - abs(user_score - required_level)
                    total_score += trait_score
                    trait_count += 1
            
            if trait_count > 0:
                career_scores[career] = total_score / trait_count
            else:
                career_scores[career] = 0
        
        return career_scores
    
    def get_personality_tag(self, scores):
        """Generate personality tag based on dominant traits"""
        traits_mapping = {
            "creativity": "Creative Thinker",
            "logical_thinking": "Analytical Mind",
            "empathy": "People Person",
            "leadership": "Natural Leader",
            "tech_affinity": "Tech Enthusiast",
            "communication": "Great Communicator",
            "math": "Problem Solver"
        }
        
        # Find the highest scoring trait
        max_trait = max(scores.keys(), key=lambda x: scores[x])
        return traits_mapping.get(max_trait, "Versatile Professional")
    
    def save_results(self, user_info, career_result, scores):
        """Save results to CSV file"""
        result_data = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'name': user_info.get('name', ''),
            'age': user_info.get('age', ''),
            'education': user_info.get('education', ''),
            'stream': user_info.get('stream', ''),
            'recommended_career': career_result['top_career'],
            'confidence_score': career_result['confidence'],
            'personality_tag': career_result['personality_tag']
        }
        
        # Add scores
        result_data.update(scores)
        
        # Create or append to results file
        results_df = pd.DataFrame([result_data])
        
        if os.path.exists('C:/Users/Krishna/CareerPathAI/results.csv'):
            results_df.to_csv('C:/Users/Krishna/CareerPathAI/results.csv', mode='a', header=False, index=False)
        else:
            results_df.to_csv('results.csv', index=False)

# Initialize the system
if 'guidance_system' not in st.session_state:
    st.session_state.guidance_system = CareerGuidanceSystem()
    st.session_state.guidance_system.train_ml_model()

# Initialize session state variables
if 'current_step' not in st.session_state:
    st.session_state.current_step = 'info'
if 'user_info' not in st.session_state:
    st.session_state.user_info = {}
if 'quiz_scores' not in st.session_state:
    st.session_state.quiz_scores = {}


def main():
    # Sidebar with navigation
    st.sidebar.markdown("---")
    st.sidebar.markdown("## AI BASED CAREER RECOMMENDATION SYSTEM")
    st.sidebar.markdown("### Instructions:")
    st.sidebar.markdown("""
    1. **Fill Personal Info** - Enter your basic details  
    2. **Take the Quiz** - Answer 10 questions honestly  
    3. **Get Recommendations** - View your career matches  
    4. **Explore Careers** - Learn about suggested paths  
    5. **View Analysis** - See your trait visualization  
    """)
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📚 Quick Learning Links")
    st.sidebar.markdown("- [Coursera](https://www.coursera.org/)")
    st.sidebar.markdown("- [Kaggle](https://www.kaggle.com/learn)")
    st.sidebar.markdown("- [FreeCodeCamp](https://www.freecodecamp.org/)")
    st.sidebar.markdown("- [Google Digital Garage](https://learndigital.withgoogle.com/digitalgarage)")
    st.sidebar.markdown("- [LinkedIn Learning](https://www.linkedin.com/learning/)")
    st.sidebar.markdown("---")
    if st.sidebar.button("🔄 Start Over"):
        st.session_state.current_step = 'landing'
        st.session_state.user_info = {}
        st.session_state.quiz_scores = {}
        st.rerun()
    # Main header
    st.markdown('<h1 class="main-header">WHAT CAREER PATH IS RIGHT FOR ME?</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.5rem; color: #000;">Discover your ideal Career with AI-Powered Recommendations</p>', unsafe_allow_html=True)
    # Progress bar
    steps = ['landing', 'info', 'quiz', 'results']
    current_step_index = steps.index(st.session_state.current_step)
    progress = (current_step_index + 1) / len(steps)
    st.progress(progress)
    if st.session_state.current_step == 'landing':
        show_landing_page()
    elif st.session_state.current_step == 'info':
        show_user_info_form()
    elif st.session_state.current_step == 'quiz':
        show_quiz()
    elif st.session_state.current_step == 'results':
        show_results()

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

  <ul style="font-size:1.2rem; color:#000; text-align:left; list-style-type:disc;">
        <li>20 multiple-choice questions</li>
        <li>Takes approximately 5-15 minutes</li>
        <li>Immediate results with career recommendations</li>
        <li>Custom learning paths based on results</li>
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
  padding: 0.5rem 0rem;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  margin-top: -150px;
  margin-left: 12.5rem;
  margin-right: -150px;
}


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
    /* Make selected radio option text black */
    div[data-testid="stRadio"] label span {
        color: black !important;
    }
    /* Optional: make unselected options gray for contrast */
    div[data-testid="stRadio"] label span {
        color: #333 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def show_quiz():
    st.markdown('<h2 class="sub-header">Career Test Assessment</h2>', unsafe_allow_html=True)
    scores = {}

    with st.form("career_recommendation"):
        for i, q in enumerate(QUIZ_QUESTIONS):
            # Question text styled
            st.markdown(
                f"""
                <div class='question-text' style='margin-bottom:10px; font-size:22px; font-weight:bold;'>
                    Question {i+1}: {q['question']}
                </div>
                """,
                unsafe_allow_html=True
            )

            if q['type'] == 'slider':
                score = st.slider(
                    "",
                    min_value=1,
                    max_value=5,
                    value=3,
                    key=f"q_{i}",
                    label_visibility="collapsed"
                )
            else:  # radio
                # Add hidden placeholder option
                options = ["Select an option..."] + q['options']
                selection = st.radio(
                    "",
                    options,
                    key=f"q_{i}",
                    label_visibility="collapsed",
                    index=0  # defaults to hidden placeholder
                )

                # Only score if user picked a real option
                if selection != "Select an option...":
                    score = q['options'].index(selection) + 1
                else:
                    score = None

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
    # Calculate career matches
    career_scores = st.session_state.guidance_system.calculate_career_match(st.session_state.quiz_scores)
    sorted_careers = sorted(career_scores.items(), key=lambda x: x[1], reverse=True)
    # Get top 3 recommendations
    top_career = sorted_careers[0][0]
    alternatives = [career[0] for career in sorted_careers[1:3]]
    # Calculate confidence score
    confidence = sorted_careers[0][1] * 100
    # Get personality tag
    personality_tag = st.session_state.guidance_system.get_personality_tag(st.session_state.quiz_scores)
    # Prepare result data
    career_result = {
        'top_career': top_career,
        'alternatives': alternatives,
        'confidence': confidence,
        'personality_tag': personality_tag
    }
    # Display results
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        badge = "badge-green" if confidence > 80 else "badge-orange" if confidence > 60 else "badge-red"
        st.markdown(f"### **{top_career}** <span class='badge {badge}'>{confidence:.1f}% match</span>", unsafe_allow_html=True)
    with col2:
        st.metric("Personality Type", personality_tag)
    with col3:
        if st.button("Save Results"):
            st.session_state.guidance_system.save_results(
                st.session_state.user_info, 
                career_result, 
                st.session_state.quiz_scores
            )
            st.success("Results saved!")
        csv = pd.DataFrame([st.session_state.user_info | st.session_state.quiz_scores | career_result]).to_csv(index=False).encode('utf-8')
    # Career details
    show_career_details(top_career, " Top Recommendation")
    st.markdown("### Alternative Career Paths")
    col1, col2 = st.columns(2)
    with col1:
        if len(alternatives) > 0:
            show_career_details(alternatives[0], " Second Choice", compact=True)
    with col2:
        if len(alternatives) > 1:
            show_career_details(alternatives[1], " Third Choice", compact=True)
    # Trait analysis
    show_trait_analysis(top_career)
  

def show_career_details(career_name, title, compact=False):
    career_info = CAREER_DATABASE[career_name]
    if not compact:
        st.markdown(f"#### {title}")
        with st.expander(f"Learn more about {career_name}", expanded=True):
            st.markdown(f"**Description:** {career_info['description']}")
            st.markdown(f"**Job Roles:** {', '.join(career_info['job_roles'])}")
            st.markdown(f"**Salary Range:** {career_info['salary_range']}")
            st.markdown(f"**Tools & Technologies:** {', '.join(career_info['tools'])}")
            st.markdown("**Learning Resources:**")
            for resource in career_info['learning_resources']:
                st.markdown(f"• {resource}")
    else:
        with st.expander(f"{career_name}"):
            st.markdown(f"{career_info['description'][:100]}...")
            st.markdown(f"**Salary:** {career_info['salary_range']}")

def show_career_roadmap(career_name):
    career_info = CAREER_DATABASE.get(career_name, None)
    if career_info and "roadmap" in career_info:
        roadmap = career_info["roadmap"]
        with st.expander(f"📘 Education & Learning Roadmap for {career_name}", expanded=False):
            st.write("**Required High School Subjects:**", ", ".join(roadmap["high_school_subjects"]))
            st.write("**Suggested College Majors:**", ", ".join(roadmap["college_majors"]))
            st.write("**Certification Options:**", ", ".join(roadmap["certifications"]))
            st.write("**Online Learning Platforms:**", ", ".join(roadmap["online_platforms"]))
            st.write("**Internships/Project Ideas:**", ", ".join(roadmap["internships_projects"]))



def show_trait_analysis(top_career=None):
    st.markdown("###  Your Trait Analysis")
    traits = list(st.session_state.quiz_scores.keys())
    scores = list(st.session_state.quiz_scores.values())
    # Radar chart using Plotly
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=scores + [scores[0]],  # Close the polygon
        theta=traits + [traits[0]],
        fill='toself',
        name='Your Scores',
        line_color='rgb(31, 119, 180)'
    ))
    # If top_career is provided, show average required traits for comparison
    if top_career:
        required = CAREER_DATABASE[top_career]["required_traits"]
        avg_required = [required.get(trait, 0.5) * 5 for trait in traits]
        fig.add_trace(go.Scatterpolar(
            r=avg_required + [avg_required[0]],
            theta=traits + [traits[0]],
            fill='toself',
            name=f"{top_career} Ideal",
            line_color='rgb(255, 127, 14)'
        ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5]
            )),
        showlegend=True,
        title="Your Trait Profile",
        height=500
    )
    col1, col2 = st.columns([2, 1])
    with col1:
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.markdown("#### Trait Breakdown")
        for trait, score in st.session_state.quiz_scores.items():
            trait_name = trait.replace('_', ' ').title()
            st.markdown(f'<div class="trait-score">{trait_name}: {score}/5</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()