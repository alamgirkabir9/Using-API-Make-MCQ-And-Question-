import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("API key is missing. Please set it in the .env file.")
    st.stop()

genai.configure(api_key=api_key)

with st.sidebar:
    st.write("Contract Information")
    st.selectbox("Author Information", ["Email: alomgirkabir720@gmail.com", "Phone: 01316190188"])

def extract_text_from_file(text_file):
    return text_file.read().decode("utf-8")

def generate_questions_only(text, num_questions, language):
    prompt = (
        f"Please generate {num_questions} questions from the following text in {language}:\n"
        f"{text}\n"
    )
    st.write("Prompt sent to AI for questions:")
    st.code(prompt)

    response = genai.GenerativeModel(
        model_name="gemini-1.0-pro"
    ).start_chat().send_message(prompt)
    
    return response.text

def generate_mcq_quiz(text, num_questions, language):
    prompt = (
        f"Please generate {num_questions} multiple-choice questions with 4 options from the following text in {language}:\n"
        f"{text}\n"
        f"Indicate the correct answer after each question."
    )
    st.write("Prompt sent to AI for MCQ Quiz:")
    st.code(prompt)
    response = genai.GenerativeModel(
        model_name="gemini-1.0-pro"
    ).start_chat().send_message(prompt)
    
    return response.text

st.title("AI-Powered Question/MCQ Quiz Generator")

task_choice = st.selectbox("Select Task", ["Generate Only Questions", "Generate MCQ Quiz"])

language = st.selectbox("Select Language", ["English", "Spanish", "French", "German", "Bangla"])

text_file = st.file_uploader("Upload a Text File", type="txt")
if text_file:
    text_content = extract_text_from_file(text_file)
    st.write("Text File Extracted Successfully!")

    num_questions_input = st.text_input("Enter Number of Questions (1-30)", "5")

    if st.button("Generate"):
        try:
            num_questions = int(num_questions_input)
            if num_questions < 1 or num_questions > 30:
                st.error("Please enter a number between 1 and 30.")
            else:
                if task_choice == "Generate Only Questions":
                    with st.spinner("Generating Questions..."):
                        questions = generate_questions_only(text_content, num_questions, language)

                    if questions.strip():
                        st.write("Generated Questions:")
                        question_lines = questions.strip().split('\n')

                        for idx, question in enumerate(question_lines):
                            st.write(f"**Q{idx + 1}: {question.strip()}**")

                    else:
                        st.error("No questions generated. Please check the input text.")

                elif task_choice == "Generate MCQ Quiz":
                    with st.spinner("Generating MCQs..."):
                        mcq_quiz = generate_mcq_quiz(text_content, num_questions, language)

                    st.write("AI Response:")
                    st.code(mcq_quiz.strip())

                    if mcq_quiz.strip():
                        st.write("Generated MCQ Quiz:")
                        mcq_lines = mcq_quiz.strip().split('\n')
                        question_counter = 1

                        for line in mcq_lines:
                            if "Correct answer:" in line:
                                question_part, correct_answer_part = line.split("Correct answer:")
                                
                                st.write(f"**Q{question_counter}: {question_part.strip()}**")
                                question_counter += 1
                                options = ["Option A", "Option B", "Option C", "Option D"]
                                user_choice = st.radio(f"Select your answer for Q{question_counter - 1}:", options)
                                st.write(f"**Correct Answer: {correct_answer_part.strip()}**")

                    else:
                        st.error("No MCQs generated. Please check the input text.")
        
        except ValueError:
            st.error("Invalid input. Please enter a valid number.")

st.markdown(
    """
    <div style="background-color: #f0f8ff; padding: 10px; border-radius: 5px; margin: 20px 0; border-left: 4px solid #007bff;">
        <h4 style="color: #007bff; margin-bottom: 5px;">Note:</h4>
        <p style="color: #333; margin: 0;">This app generates questions and MCQ quizzes based on the contents of the uploaded text file.</p>
    </div>
    
    <div style="text-align: center; margin-top: 30px;">
        <p style="font-size: 12px; color: #666;">Powered by <strong style="color: #007bff;">Alamgir</strong></p>
    </div>
    """,
    unsafe_allow_html=True
)
