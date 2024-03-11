import os
from flask import Flask, session, redirect, url_for, render_template, request, jsonify, make_response
from flask_bcrypt import Bcrypt
from auth import signUp, Login 
from content import fetch_content, next_page_func, prev_page_func, is_module_completed, fetch_pages_topic
from quiz import questions, get_selected_option, store_selected_option, generate_new_quiz_data
from progress import store_session_in_database, fetch_user_progress
    
app = Flask(__name__)
app.secret_key = os.environ.get('sessionKey')
bcrypt = Bcrypt(app)
    
# Home page route 
@app.route('/')
def home():
    return render_template("home.html")

# Sign Up Route
@app.route('/signUp', methods=['GET', 'POST'])
def signUpPage():
    
    # Extract sign up form information 
    if request.method == 'POST':

        username = request.form['username']
        email = request.form['email']
        confirmEmail = request.form['confirmEmail']
        password = request.form['password']
        confirmPassword = request.form['confirmPassword']
        
        # Calls the sign up function 
        return signUp(username, email, confirmEmail, password, confirmPassword, bcrypt)

    return render_template("signUp.html")

# Login page route 
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        
        # Extracts login form information 
        username = request.form['username']
        password = request.form['password']
        
        # Calls Login function 
        return Login(username, password, bcrypt)

    return render_template("login.html")

@app.route('/content')
def content():
    
    print(fetch_user_progress())
    
    if session.get('module_num') is None: 
        session.setdefault('module_num', 1)
        session.setdefault('topic_num', 1)
        session.setdefault('page_num', 1)
    
    module_num = session['module_num']
    topic_num = session['topic_num']
    page_num = session['page_num']
    
    print("Session variables in content route:", module_num, topic_num, page_num)
    
    total_pages = fetch_pages_topic(module_num, topic_num)
    if total_pages == 0:
        return "Error: Total pages is zero"
    
    content_progress = (page_num / total_pages) * 100
    
    if content_progress == 100 and session['topic_num'] >= 4:
        session['topic_num'] += 1
        session['page_num'] = 1

    
    content_data = fetch_content(module_num, topic_num, page_num)
    completed_module = is_module_completed(module_num, topic_num, page_num)

    return render_template("contentPage.html", content_data=content_data, completed_module=completed_module)

@app.route('/update_session/<module_number>/<topic_number>')
def update_session(module_number, topic_number):
    session['module_num'] = module_number
    session['topic_num'] = topic_number
    session['page_num'] = 1
    store_session_in_database()
    return redirect(url_for('content'))

   
@app.route('/prev_page')
def prev_page_route():
    module_num = session['module_num']
    topic_num = session['topic_num']
    page_num = session['page_num']
    
    module_num, topic_num, page_num = prev_page_func(module_num, topic_num, page_num)
    session['module_num'] = module_num
    session['topic_num'] = topic_num
    session['page_num'] = page_num
    
    store_session_in_database()
    return redirect(url_for('content'))

@app.route('/next_page')  # Update the route to use underscore notation
def next_page_route():
    module_num = session['module_num']
    topic_num = session['topic_num']
    page_num = session['page_num']
    
    module_num, topic_num, page_num = next_page_func(module_num, topic_num, page_num)
    session['module_num'] = module_num
    session['topic_num'] = topic_num
    session['page_num'] = page_num
    
    store_session_in_database()
    return redirect(url_for('content'))
 
@app.route('/authStatus')
def authStatus():
    if 'username' in session:
        return jsonify({'authenticated': True, 'username': session['username']})
    else:
        return jsonify({'authenticated': False})

# Logout route 
@app.route('/logout', methods=['POST'])
def logout():

    store_session_in_database() 
    session.clear()
    return jsonify({'success': True})

@app.route('/quiz/<module_number>/<int:question_index>', methods=['GET', 'POST'])
def quiz(module_number, question_index):
    
    if not session.get('in_quiz'):
        return redirect(url_for('home'))
    
    # Grabs the questions based on the module
    quiz_data = session.get('quiz_data')  # Retrieve quiz data from session

    if not quiz_data:  # If quiz data is not stored in session, generate and store it
        quiz_data = questions(module_number)
        session['quiz_data'] = quiz_data

    num_questions = len(quiz_data)
    current_question = quiz_data[int(question_index) - 1]  # Convert to integer
    prev_question = int(question_index) - 1 if int(question_index) > 1 else None  # Convert to integer
    next_question = int(question_index) + 1 if int(question_index) < num_questions else None  # Convert to integer

    if request.method == 'POST':
        # Retrieve the selected option and question index from the form submission
        selected_option = request.form.get('selected_option')
        question_index = int(request.form.get('question_index'))  # Convert to integer
        # Store the selected option for the current question
        store_selected_option(question_index, selected_option)

    quiz_progress = (int(question_index) / num_questions) * 100
    # Retrieve the selected option for the current question
    selected_option = get_selected_option(question_index)
    
    

    return render_template("quiz.html", current_question=current_question, prev_question=prev_question,
                           next_question=next_question, module_number=module_number, selected_option=selected_option, current_question_index=question_index, progress=quiz_progress)
    
@app.route('/quiz', methods=['GET', 'POST'])
def default_quiz():
    
    if 'in_quiz' in session and session['in_quiz']:
        # Redirect to the homepage
        return redirect(url_for('home'))
    else:
        # If 'in_quiz' session does not exist, set it and redirect to the quiz
        session['in_quiz'] = True
        # Redirect to the first question of the first module
        return redirect(url_for('quiz', module_number='1', question_index=1))


@app.route('/results')
def results():
    
    session.pop('in_quiz', None)
    
    session['quiz_data'] = generate_new_quiz_data()
    # Retrieve the selected options and correct answers from the session
    selected_options = session.get('selected_options', {})
    correct_answers = session.get('correct_answers', [])  # Retrieve correct answers from session

    print("Selected options:", selected_options)
    print("Correct answers:", correct_answers)

    # Calculate the user's score
    num_correct = sum(1 for index, selected_option in selected_options.items() if selected_option == correct_answers[int(index) - 1])

    # Get the total number of questions
    total_questions = len(correct_answers)

    # Calculate the percentage score
    score_percentage = (num_correct / total_questions) * 100 if total_questions > 0 else 0

    return render_template("results.html", num_correct=num_correct, total_questions=total_questions, score_percentage=score_percentage)

@app.route('/retake_quiz', methods=['POST', 'GET'])
def retake_quiz():
    if 'in_quiz' in session and session['in_quiz']:
        session.pop('quiz_data', None)  # Clear the quiz data session variable
        session.pop('selected_options', None)  # Clear selected options session variable
        session.pop('correct_answers', None)  # Clear correct answers session variable
        session['in_quiz'] = False  # Set in_quiz session variable to False to indicate quiz is not in progress
    return redirect(url_for('default_quiz'))

@app.after_request
def add_cache_control(response):
    if session.get('in_quiz'):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
    return response

if __name__ == "__main__":
    app.run()