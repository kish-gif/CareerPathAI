import streamlit as st

def show_instructions():
    st.markdown("""
        <style>
        .instruction-box {
            background: #ffffff; /* white background */
            border: 2px solid #000000; /* solid black border */
            border-radius: 0.75rem; /* rounded-lg */
            padding: 2rem; /* p-8 */
            margin: 2rem auto;
            max-width: 900px;
            text-align: left;
            font-family: 'Poppins', arial, sans-serif;
        }
        @media (min-width: 768px) {
            .instruction-box {
                padding: 3rem; /* md:p-12 */
            }
        }
        .instruction-box h2 {
            color: #111827; /* dark heading */
            font-size: 2.75rem;  /* text-sm */
        font-weight: 700;     /* font-medium */
            margin: 1.5rem auto 0 auto;

        }
        .instruction-box p {
            font-size: 1.25rem;
                    font-weight: 600;     /* font-medium */
            color: #374151; /* gray text */
            margin-bottom: 1rem;
        }
        .continue-btn {
            margin: 1.5rem auto 0 auto;
            background: #000000; /* black button */
            color: white;
            padding: 0.8rem 1.5rem;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            border: none;
        }
        .continue-btn:hover {
            background: #333333; /* slightly lighter black on hover */
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="instruction-box">
            <h2>Instructions</h2>
            <p>Rank how much you agree with each of the following statements on a scale from 1 to 5.</p>
            <p> 1 – Strongly Disagree<br>
2 – Disagree<br>
3 – Neutral<br>
4 – Agree<br>
5 – Strongly Agree
</p>
            <button class="continue-btn">Continue</button>
        </div>
    """, unsafe_allow_html=True)