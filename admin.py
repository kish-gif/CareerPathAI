import streamlit as st
import json
import os
import career_database   
import questions         

CAREER_DATABASE = career_database.CAREER_DATABASE
QUIZ_QUESTIONS = questions.QUIZ_QUESTIONS


# -------------------------------
# Simple Login System
# -------------------------------
def login():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        st.title("🔒 Admin Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            # Replace with your own credentials
            if username == "admin" and password == "secure123":
                st.session_state.authenticated = True
                st.success("✅ Login successful!")
                st.experimental_rerun()
            else:
                st.error("❌ Invalid username or password")
        return False
    return True




# -------------------------------
# Utility Functions
# -------------------------------
def save_json(path, data):
    """Save dictionary/list to JSON file."""
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

def load_json(path, default):
    """Load JSON file if exists, else return default."""
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return default

# -------------------------------
# Quiz Question Management
# -------------------------------
def quiz_section():
    st.header("📋 Quiz Questions")

    # Add new question
    with st.expander("➕ Add New Question"):
        question = st.text_area("Question")
        trait = st.text_input("Trait")
        q_type = st.selectbox("Type", ["radio", "checkbox", "text"])
        options = st.text_area("Options (comma separated)")
        tooltip = st.text_area("Tooltip")

        if st.button("Save Question"):
            new_q = {
                "question": question,
                "trait": trait,
                "type": q_type,
                "options": options.split(","),
                "tooltip": tooltip
            }
            QUIZ_QUESTIONS.append(new_q)
            save_json("quiz_questions.json", QUIZ_QUESTIONS)
            st.success("✅ Question added successfully!")

    # Manage existing questions
    for i, q in enumerate(QUIZ_QUESTIONS):
        with st.expander(f"Q{i+1}: {q['question']}"):
            new_question = st.text_area("Edit Question", q["question"], key=f"q_{i}")
            new_trait = st.text_input("Trait", q["trait"], key=f"trait_{i}")
            new_type = st.selectbox("Type", ["radio", "checkbox", "text"], 
                                    index=["radio","checkbox","text"].index(q["type"]), key=f"type_{i}")
            new_options = st.text_area("Options", ", ".join(q["options"]), key=f"opts_{i}")
            new_tooltip = st.text_area("Tooltip", q["tooltip"], key=f"tip_{i}")

            if st.button(f"Update {i+1}", key=f"update_{i}"):
                QUIZ_QUESTIONS[i] = {
                    "question": new_question,
                    "trait": new_trait,
                    "type": new_type,
                    "options": new_options.split(","),
                    "tooltip": new_tooltip
                }
                save_json("quiz_questions.json", QUIZ_QUESTIONS)
                st.success("✅ Updated successfully!")

            if st.button(f"Delete {i+1}", key=f"delete_{i}"):
                QUIZ_QUESTIONS.pop(i)
                save_json("quiz_questions.json", QUIZ_QUESTIONS)
                st.warning("❌ Deleted successfully!")
                st.experimental_rerun()

# -------------------------------
# Career Management
# -------------------------------
def career_section():
    st.header("💼 Career Details")

    career_names = list(CAREER_DATABASE.keys())
    selected_career = st.selectbox("Select Career", career_names)

    if selected_career:
        career = CAREER_DATABASE[selected_career]

        new_desc = st.text_area("Description", career.get("description", ""), key="desc")
        new_salary = st.text_input("Salary Range", career.get("salary_range", ""), key="salary")
        new_tools = st.text_area("Tools (comma separated)", ", ".join(career.get("tools", [])), key="tools")
        new_resources = st.text_area("Learning Resources (comma separated)", ", ".join(career.get("learning_resources", [])), key="resources")

        st.subheader("📚 Roadmap")
        new_highschool = st.text_area("High School Subjects", ", ".join(career["roadmap"].get("high_school_subjects", [])))
        new_college = st.text_area("College Majors", ", ".join(career["roadmap"].get("college_majors", [])))
        new_certs = st.text_area("Certifications", ", ".join(career["roadmap"].get("certifications", [])))
        new_platforms = st.text_area("Online Platforms", ", ".join(career["roadmap"].get("online_platforms", [])))
        new_internships = st.text_area("Internships/Projects", ", ".join(career["roadmap"].get("internships_projects", [])))

        if st.button("Update Career"):
            CAREER_DATABASE[selected_career]["description"] = new_desc
            CAREER_DATABASE[selected_career]["salary_range"] = new_salary
            CAREER_DATABASE[selected_career]["tools"] = new_tools.split(",")
            CAREER_DATABASE[selected_career]["learning_resources"] = new_resources.split(",")
            CAREER_DATABASE[selected_career]["roadmap"] = {
                "high_school_subjects": new_highschool.split(","),
                "college_majors": new_college.split(","),
                "certifications": new_certs.split(","),
                "online_platforms": new_platforms.split(","),
                "internships_projects": new_internships.split(",")
            }
            save_json("career_database.json", CAREER_DATABASE)
            st.success(f"✅ {selected_career} updated successfully!")

        if st.button("Delete Career"):
            del CAREER_DATABASE[selected_career]
            save_json("career_database.json", CAREER_DATABASE)
            st.warning(f"❌ {selected_career} deleted successfully!")
            st.experimental_rerun()

    with st.expander("➕ Add New Career"):
        new_name = st.text_input("Career Name")
        new_desc = st.text_area("Description")
        new_salary = st.text_input("Salary Range")
        new_tools = st.text_area("Tools (comma separated)")
        new_resources = st.text_area("Learning Resources (comma separated)")
        new_highschool = st.text_area("High School Subjects (comma separated)")
        new_college = st.text_area("College Majors (comma separated)")
        new_certs = st.text_area("Certifications (comma separated)")
        new_platforms = st.text_area("Online Platforms (comma separated)")
        new_internships = st.text_area("Internships/Projects (comma separated)")

        if st.button("Save Career"):
            CAREER_DATABASE[new_name] = {
                "description": new_desc,
                "salary_range": new_salary,
                "tools": new_tools.split(","),
                "learning_resources": new_resources.split(","),
                "roadmap": {
                    "high_school_subjects": new_highschool.split(","),
                    "college_majors": new_college.split(","),
                    "certifications": new_certs.split(","),
                    "online_platforms": new_platforms.split(","),
                    "internships_projects": new_internships.split(",")
                }
            }
            save_json("career_database.json", CAREER_DATABASE)
            st.success(f"✅ {new_name} added successfully!")

# -------------------------------
# Main App
# -------------------------------
def main():
    st.sidebar.title("Navigation")
    choice = st.sidebar.radio("Go to:", ["Quiz Questions", "Career Details"])

    if choice == "Quiz Questions":
        quiz_section()
    elif choice == "Career Details":
        career_section()

if __name__ == "__main__":
    main()