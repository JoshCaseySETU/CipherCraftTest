from database import databaseConnect
import random
from flask import session

def questions(module_number):
    query = f"SELECT Question, Option1, Option2, Option3, Option4, Correct FROM Quiz WHERE Module = '{module_number}'"
    result = databaseConnect(query)
    
    quiz_data = []
    correct_answers = []  # Initialize list to store correct answers
    
    for row in result:
        question_data = {
            'Question': row[0],
            'Option1': row[1],
            'Option2': row[2],
            'Option3': row[3],
            'Option4': row[4],
        }
        correct_answer = row[5]
        correct_answers.append(correct_answer)  # Store correct answer
        quiz_data.append(question_data)
        
        random.shuffle(quiz_data)
        
    session['correct_answers'] = correct_answers  # Store correct answers in session
    
    return quiz_data


def store_selected_option(question_index, selected_option):
    print("Storing selected option:", selected_option, "for question index:", question_index)
    # Retrieve or initialize the dictionary of selected options in the session
    selected_options = session.get('selected_options', {})
    # Store the selected option for the current question index in the dictionary
    selected_options[str(question_index)] = selected_option  # Convert to string
    session['selected_options'] = selected_options



def get_selected_option(question_index):
    # Retrieve the dictionary of selected options from the session
    selected_options = session.get('selected_options', {})
    # Retrieve the selected option for the current question index from the dictionary
    return selected_options.get(question_index, '')

def generate_new_quiz_data():
    module_number = session.get('module_num')
    return questions(module_number)


        