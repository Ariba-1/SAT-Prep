# --- IMPORTS AND DATA SETUP ---
import streamlit as st
import pandas as pd
import json 
import os # NEW: Needed to delete the progress file.

# --- Global Settings ---
PROGRESS_FILE = "progress.json"

@st.cache_data
def load_data():
    """Loads the questions from the CSV file."""
    try:
        df = pd.read_csv("questions.csv")
        return df
    except FileNotFoundError:
        st.error("Error: questions.csv file not found! Please check your file path.")
        return pd.DataFrame()

# --- PERSISTENCE FUNCTIONS (Saving and Loading Progress) ---

def load_progress():
    """Loads saved progress from the JSON file."""
    try:
        with open(PROGRESS_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Initial score tracking dictionary (Time Spent tracking omitted for now, see next steps)
        return {"questions_answered": 0, "correct_answers": 0, "time_spent": 0}

def save_progress(progress_data):
    """Saves the current progress to the JSON file."""
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(progress_data, f)
        
# --- ACTION FUNCTIONS (Quiz Logic) ---

def reset_progress():
    """Resets all progress by deleting the progress.json file."""
    # 1. Delete the physical progress file
    if os.path.exists(PROGRESS_FILE):
        os.remove(PROGRESS_FILE)
        
    # 2. Reset the session state variables immediately
    st.session_state.q_index = 0
    st.session_state.submitted = False
    st.session_state.progress = load_progress() # Loads the now-empty default stats
    
    st.rerun() # Forces the entire script to restart cleanly

def submit_answer(selected_letter, correct_answer):
    """Marks the question as submitted, updates the score, and saves progress."""
    st.session_state.submitted = True
    
    # 1. Update Score Tracking
    st.session_state.progress['questions_answered'] += 1
    if selected_letter == correct_answer:
        st.session_state.progress['correct_answers'] += 1
        
    # 2. Save the updated score (The Persistence requirement)
    save_progress(st.session_state.progress)


def next_question():
    """Moves to the next question if available."""
    st.session_state.submitted = False
    
    # Only increment if we haven't reached the end
    if st.session_state.q_index < total_questions - 1:
        st.session_state.q_index += 1
    # Note: If we are at the end, the main logic will handle the "Quiz Over" screen.


# --- INITIALIZATION (Runs once per session/reset) ---
df = load_data()
total_questions = len(df)

if "q_index" not in st.session_state:
    st.session_state.q_index = 0
    st.session_state.submitted = False
    st.session_state.progress = load_progress() # Load previous session's progress

# --- MAIN APP DISPLAY ---

st.title("SAT Exam Practice")
st.sidebar.header("Overall Progress")

# Calculate and display accuracy metrics
attempted = st.session_state.progress['questions_answered']
correct = st.session_state.progress['correct_answers']
accuracy = (correct / attempted) * 100 if attempted > 0 else 0

st.sidebar.metric("Attempted", attempted)
st.sidebar.metric("Correct", correct)
st.sidebar.metric("Accuracy", f"{accuracy:.1f}%")

# Add the reset button to the sidebar
st.sidebar.button(
    "Start Fresh (Clear Saved Progress)", 
    on_click=reset_progress,
    help="Warning: This clears all your past scores and restarts the index."
)

def next_question():
    """Moves to the next question if available."""
    st.session_state.submitted = False
    
    # Check if we are moving from the last question (index 9) to the "End" state (index 10)
    if st.session_state.q_index == total_questions - 1:
        st.session_state.q_index += 1
        st.rerun() # Force a clean rerun to hit the Quiz End Screen block immediately
    
    # Only increment if we haven't reached the end
    elif st.session_state.q_index < total_questions - 1:
        st.session_state.q_index += 1

# --- QUIZ END SCREEN ---

if st.session_state.q_index >= total_questions:
    st.success("Congratulations! You have completed the practice module.")
    
    # The custom message you requested
    st.subheader("Your final result is:") 
    
    st.subheader(f"Final Score: {correct} / {attempted} ({accuracy:.1f}%)")
    st.stop() 

# --- QUESTION DISPLAY LOOP ---

q_index = st.session_state.q_index
q = df.iloc[q_index]

st.subheader(f"Question {q_index + 1} of {total_questions}")
st.markdown(q['question_text']) # Uses markdown for correct math notation display

# Display image if exists
if pd.notna(q["image_filename"]) and q["image_filename"] != "":
    # Placeholder for actual image
    st.warning(f"Image placeholder: '{q['image_filename']}' would be displayed here.")


# Options Setup
options = {
    "A": q["option_a"],
    "B": q["option_b"],
    "C": q["option_c"],
    "D": q["option_d"]
}
option_labels = [f"{letter}: {text}" for letter, text in options.items()]

selected_label = st.radio("Choose an answer:", option_labels, key=f"radio_{q_index}", index=None, disabled=st.session_state.submitted)

# Map selected text to letter
selected_letter = None
if selected_label:
    selected_letter = selected_label.split(':')[0]

# --- SUBMIT/NEXT BUTTONS ---
col1, col2 = st.columns(2)

if not st.session_state.submitted:
    # Only allow submission if an option is selected
    if selected_label:
        col1.button("Submit Answer", 
                    on_click=submit_answer, 
                    args=(selected_letter, q["correct_answer"]))
else:
    # Show result only after submission
    if selected_letter == q["correct_answer"]:
        st.success("Correct! That was a great answer.")
    else:
        st.error(f"Incorrect. You chose {selected_letter}. The correct answer is {q['correct_answer']}.")
    
    st.info(f"**Explanation:** {q['explanation']}")
    
    # Show next button after submission
    col2.button("Next Question", on_click=next_question)