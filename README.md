# SAT Practice App 

This is an interactive SAT Math Practice application built using Streamlit.  
It loads questions from a CSV file, displays them one by one, tracks user progress, and shows final results at the end of the quiz.

---

## Features

### 1. Question-by-Question Quiz Flow
- Loads questions from `questions.csv`
- Displays one question at a time
- Four answer choices shown using radio buttons
- Shows detailed explanation after submitting an answer

### 2. Progress Saving (JSON)
The app automatically saves user progress in `progress.json`, including:
- Total questions attempted  
- Correct answers  
- Accuracy percentage  
- Data persists even after closing the app

### 3. Reset Progress
A **Start Fresh** button wipes all stored progress and restarts the quiz from the first question.

### 4. Quiz Completion Screen
Once all questions have been attempted, the app displays:
- Final score
- Accuracy percentage
- Completion message

### 5. Clean Interface
- Sidebar shows live metrics
- Separate Submit and Next buttons
- Proper handling of the final question

---

## Project Structure

