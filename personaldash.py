import os
import pandas as pd
import streamlit as st
import plotly.express as px
from fpdf import FPDF
from career_database import CAREER_DATABASE

# ✅ Inject CSS to hide scrollbars
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    body {
        font-family: 'Inter', sans-serif;
        background-color: #f9fafb !important; /* gray-50 */
        color: #111827; /* gray-900 */
    }

    /* Streamlit uses .block-container for the main content area */
    .block-container {
        overflow: auto;
        scrollbar-width: none;       /* Firefox */
        -ms-overflow-style: none;    /* IE/Edge */
    }
    .block-container::-webkit-scrollbar {
        display: none;               /* Chrome, Safari, Opera */
    }

    
    </style>
    """,
    unsafe_allow_html=True
)



def show_career_details(career_name, title, compact=False):
    career_info = CAREER_DATABASE[career_name]
    if not compact:
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
  

def show_roadmap(career_name):
    career_info = CAREER_DATABASE.get(career_name, None)
    if career_info and "roadmap" in career_info:
        roadmap = career_info["roadmap"]
        with st.expander(f"Roadmap for {career_name}", expanded=False):
            st.write("**Required High School Subjects:**", ", ".join(roadmap["high_school_subjects"]))
            st.write("**Suggested College Majors:**", ", ".join(roadmap["college_majors"]))
            st.write("**Certification Options:**", ", ".join(roadmap["certifications"]))
            st.write("**Online Learning Platforms:**", ", ".join(roadmap["online_platforms"]))
            st.write("**Internships/Project Ideas:**", ", ".join(roadmap["internships_projects"]))


# -------------------------------
# Load Results File
# -------------------------------
if os.path.exists("results.csv"):
    df = pd.read_csv("results.csv")

    if not df.empty:

        latest_result = df.tail(1)
        latest = df.iloc[-1]

        st.title("Your Career Recommendations")

        st.markdown(
            f"""
            <div style="font-size:25px; font-weight:bold;">
                {latest.get('recommended_career', 'Not available')}
            </div>
            <div style="background-color:#4CAF50; color:white; 
                        display:inline-block; padding:6px 12px; 
                        border-radius:6px; font-weight:bold; margin-top:8px;">
                {latest.get('confidence_score', 'Not available')}% match
            </div>
            <div style="font-size:25px; font-weight:bold; margin-top:12px;">
                Personality Type
            </div>
            <div style="font-size:25px; color:#333;">
                {latest.get('personality_tag', 'Not available')}
            </div>
            """,
            unsafe_allow_html=True
        )

        # Prepare top career and alternatives
        top_career = {
            "career": latest.get("recommended_career", "Not available"),
            "description": latest.get("description", "Create intuitive and visually appealing user interfaces and experiences for digital products."),
            "job_roles": latest.get("job_roles", "Product Designer, Visual Designer, Interaction Designer, Design Researcher"),
            "salary_range": latest.get("salary_range", "60,000 – 120,000"),
            "tools": latest.get("tools", "Figma, Adobe Creative Suite, Sketch, InVision, Principle"),
            "learning_resources": latest.get("learning_resources", "Google UX Design Certificate; Coursera - UI/UX Design Specialization; Adobe Design University")
        }

       # Example alternatives (replace with your actual data source)
        alternatives = [
            {"career": "Marketing Manager", "confidence_score": 70},
            {"career": "Data Scientist", "confidence_score": 65}
        ]

        # Prepare the career name from latest
        career_name = latest.get("recommended_career", "Not available")


        # Top Recommendation Dropdown
        st.subheader("Top Career Recommendation")
        show_career_details(career_name, "Tailored Just for You")



        # ✅ Alternative Career Paths Dropdowns
        alt_name = alternatives[0].get("career", "Not available")
        st.subheader("Alternative Career Paths")
        show_career_details(alt_name, "Second Choice", compact=True)

        # Alternative Career Paths Dropdowns
        st.markdown("### Education & Learning Roadmap")
        show_roadmap(top_career["career"]) 

        # Understanding Your Results
        st.subheader("Understanding Your Career Test Results")
        st.write("""
        The career test evaluates your personal traits and compares them against ideal role profiles to identify both your core strengths and supporting skills.
        By plotting your scores against these ideal profiles, the Career Path Finder highlights where you align strongly, identifies minor gaps, and generates a confidence score with a personality tag, ensuring that recommendations are balanced, personalized, and directly connected to your unique mix of abilities.
        """)

        # Trait Profile Chart (BEFORE interpretation)
        trait_columns = [
            "math", "logical_thinking", "creativity", "tech_affinity",
            "empathy", "communication", "leadership", "analytical",
            "patience", "organization"
        ]
        scores = [latest[col] for col in trait_columns if col in latest]

        career_ideal_profiles = {
            "UX/UI Designer": {
                "math": 3, "logical_thinking": 4, "creativity": 5, "tech_affinity": 4,
                "empathy": 4, "communication": 4, "leadership": 3, "analytical": 4,
                "patience": 3, "organization": 4
            }
        }
        recommended_career = latest.get("recommended_career", "UX/UI Designer")
        ideal_traits = career_ideal_profiles.get(recommended_career, {})
        ideal_scores = [ideal_traits.get(trait, 3) for trait in trait_columns]

        data = {
            "Trait": trait_columns,
            "Your Scores": scores,
            f"{recommended_career} Ideal": ideal_scores
        }
        df_scores = pd.DataFrame(data)

        df_melted = df_scores.melt(
            id_vars="Trait",
            value_vars=["Your Scores", f"{recommended_career} Ideal"],
            var_name="Profile",
            value_name="Score"
        )

        fig = px.bar(
            df_melted,
            x="Trait",
            y="Score",
            color="Profile",
            barmode="group",
            title=f"Trait Profile vs {recommended_career} Ideal",
            color_discrete_map={
                "Your Scores": "rgb(31, 119, 180)",   # Blue
                f"{recommended_career} Ideal": "rgb(255, 150, 66)"  # Orange
            }
        )

        # ✅ Make trait labels vertical (top-to-bottom)
        fig.update_layout(
            xaxis=dict(title="Traits", tickangle=90),  # rotate labels vertically
            yaxis=dict(title="Score", range=[0, 5]),
            showlegend=True
        )

        st.plotly_chart(fig, use_container_width=True)

       # ✅ Interpreting Trait Profile (AFTER chart)
        st.subheader("Interpreting Your Bar Display")
        st.markdown(
            "<div style='font-size:16px; font-weight:bold; color:#000000;'>Blue bars (Your Scores) = Represent your personal strengths and current aptitude levels.</div>",
            unsafe_allow_html=True
        )
        st.markdown(
            "<div style='font-size:16px; font-weight:bold; color:#000000;'>Orange bars (Ideal Profile) = Show the target career’s required traits.</div>",
            unsafe_allow_html=True
        )
        st.write("""
        When the blue bars closely match the orange bars, it indicates a strong fit with the career’s ideal traits. Larger differences highlight areas for improvement, pointing to traits you may want to develop further to strengthen your fit.
        """)

    else:
        st.info("No saved results yet. Complete a career test to see your dashboard.")
else:
    st.info("No results file found. Complete a career test to generate results.")

from fpdf import FPDF
import os
import pandas as pd
import streamlit as st

# -------------------------------
# Add Download Button (Realtime + Safe Encoding)
# -------------------------------
if os.path.exists("results.csv"):
    df = pd.read_csv("results.csv")
    if not df.empty:
        latest = df.iloc[-1]

        # ✅ Pull top career from JSON database
        recommended = latest.get("recommended_career", "Not available")
        top_career = CAREER_DATABASE.get(recommended, {
            "description": "No description available",
            "job_roles": [],
            "salary_range": "N/A",
            "tools": [],
            "learning_resources": [],
            "roadmap": {}
        })

        def safe_text(value):
            if isinstance(value, str):
                return value.replace("₱", "PHP")
            return value

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, "Career Recommendation Report", ln=True, align="C")
        pdf.ln(10)

        pdf.set_font("Arial", 'B', 14)
        pdf.cell(200, 10, f"Top Recommendation: {recommended}", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, f"Confidence Score: {latest.get('confidence_score', 'N/A')}%", ln=True)
        pdf.cell(200, 10, f"Personality Type: {latest.get('personality_tag', 'Not available')}", ln=True)
        pdf.ln(8)

        # ✅ Career Details Section
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, "Career Details", ln=True)

        pdf.set_font("Arial", 'B', 12); pdf.cell(200, 10, "Description:", ln=True)
        pdf.set_font("Arial", size=12); pdf.multi_cell(0, 10, safe_text(top_career.get('description', 'N/A')))

        pdf.set_font("Arial", 'B', 12); pdf.cell(200, 10, "Job Roles:", ln=True)
        pdf.set_font("Arial", size=12); pdf.multi_cell(0, 10, ", ".join(top_career.get('job_roles', [])))

        pdf.set_font("Arial", 'B', 12); pdf.cell(200, 10, "Salary Range:", ln=True)
        pdf.set_font("Arial", size=12); pdf.multi_cell(0, 10, safe_text(top_career.get('salary_range', 'N/A')))

        pdf.set_font("Arial", 'B', 12); pdf.cell(200, 10, "Tools & Technologies:", ln=True)
        pdf.set_font("Arial", size=12); pdf.multi_cell(0, 10, ", ".join(top_career.get('tools', [])))

        pdf.set_font("Arial", 'B', 12); pdf.cell(200, 10, "Learning Resources:", ln=True)
        pdf.set_font("Arial", size=12); pdf.multi_cell(0, 10, ", ".join(top_career.get('learning_resources', [])))
        pdf.ln(8)

        # ✅ Career Roadmap Section
        roadmap = top_career.get("roadmap", {})
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, "Career Roadmap", ln=True)

        pdf.set_font("Arial", 'B', 12); pdf.cell(200, 10, "High School Subjects:", ln=True)
        pdf.set_font("Arial", size=12); pdf.multi_cell(0, 10, ", ".join(roadmap.get('high_school_subjects', [])))

        pdf.set_font("Arial", 'B', 12); pdf.cell(200, 10, "College Majors:", ln=True)
        pdf.set_font("Arial", size=12); pdf.multi_cell(0, 10, ", ".join(roadmap.get('college_majors', [])))

        pdf.set_font("Arial", 'B', 12); pdf.cell(200, 10, "Certifications:", ln=True)
        pdf.set_font("Arial", size=12); pdf.multi_cell(0, 10, ", ".join(roadmap.get('certifications', [])))

        pdf.set_font("Arial", 'B', 12); pdf.cell(200, 10, "Online Platforms:", ln=True)
        pdf.set_font("Arial", size=12); pdf.multi_cell(0, 10, ", ".join(roadmap.get('online_platforms', [])))

        pdf.set_font("Arial", 'B', 12); pdf.cell(200, 10, "Internships/Projects:", ln=True)
        pdf.set_font("Arial", size=12); pdf.multi_cell(0, 10, ", ".join(roadmap.get('internships_projects', [])))
        pdf.ln(8)

        # ✅ Get PDF bytes safely
        pdf_bytes = pdf.output(dest="S").encode("latin-1", "replace")

        st.download_button(
            label="Download Results",
            data=pdf_bytes,
            file_name="career_results.pdf",
            mime="application/pdf"
        )

