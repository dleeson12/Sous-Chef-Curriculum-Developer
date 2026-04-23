import streamlit as st
from groq import Groq

# 1. Setup Groq Client
# Replace 'YOUR_GROQ_API_KEY' with the key you just generated
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.set_page_config(page_title="Culinary Curriculum Co-Developer", page_icon="🍳")

# System Prompt (The Persona)
SYSTEM_PROMPT = """
You are the 'Pedagogical Sous-Chef,' an expert instructional designer for the Culinary Institute of America. 

Your goal is to help faculty bridge technical culinary mastery with active inquiry-based learning.

When providing lesson scaffolds:
1. FOCUS on the specific technical culinary science relevant to the topic (e.g., if the topic is sauces, focus on emulsions or starch gelatinization; if the topic is meat, focus on Maillard or protein denaturation). 
2. AVOID repeating 'Maillard reaction' unless it is scientifically central to the user's specific topic.
3. USE technical culinary terminology correctly.
4. DESIGN Quality Assessments: Suggest performance-based evaluations that measure technical precision and sensory consistency.
"""

st.title("🍳 Culinary Curriculum Co-Developer")
st.caption("Bridging Instructional Design & Culinary Expertise")

# Sidebar for inputs
with st.sidebar:
    st.header("Lesson Parameters")
    topic = st.text_input("Culinary Topic", placeholder="e.g., Mother Sauces, Fermentation")
    method = st.selectbox("Instructional Method", [
        "Active Learning",
        "Competency-Based Assessment",
        "Cooperative Learning",
        "Inquiry-Based Learning",
        "Role-play/Simulation",
        "Scaffolded Discovery",
    ])
    
    generate_btn = st.button("Generate Lesson Plan")

# Main Logic
if generate_btn:
    if topic:
        with st.spinner("Sous-Chef is thinking..."):
            try:
                # Call Groq API
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": f"Create a lesson scaffold and assessment for {topic} using {method}."}
                    ],
                )
                
                # Display Result
                st.markdown("### 📋 Lesson Draft")
                lesson_plan = completion.choices[0].message.content  # Define the variable here
                st.write(lesson_plan)
                
                # The Download Button must be indented inside the 'try' block
                st.download_button(
                    label="📥 Download Lesson Plan as Text",
                    data=lesson_plan,
                    file_name=f"{topic}_lesson_plan.txt",
                    mime="text/plain"
                )
                
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a culinary topic first.")

        # After st.write(completion.choices[0].message.content)

        lesson_plan = completion.choices[0].message.content

                