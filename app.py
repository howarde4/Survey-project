from flask import Flask, render_template, redirect, session, request
import surveys
from flask_debugtoolbar import DebugToolbarExtension

RESPONSES_KEY = 'responses'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey!'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

@app.route('/')
def home():
    title= surveys.satisfaction_survey.title
    instruction= surveys.satisfaction_survey.instructions
    return render_template('home.html', title=title, instruction=instruction)

@app.route('/questions', methods=["POST"])
def questions():
    session[RESPONSES_KEY]=[]
    return redirect('/questions/0')

@app.route('/answer', methods=["POST"])
def answers():
    choice= request.form['answers']
    response = session[RESPONSES_KEY]
    response.append(choice)
    session[RESPONSES_KEY] = response

    if(len(response) == len(surveys.satisfaction_survey.questions)):
        return redirect("/complete")
    else:
        return redirect(f"/questions/{len(response)}")

@app.route("/questions/<int:id>")
def next_question(id):
    response = session.get(RESPONSES_KEY)

    if(response is None):
        return redirect('/')
    
    if(len(response) == len(surveys.satisfaction_survey.questions)):
        return redirect('/complete')

    if(len(response) != id):
        flash(f"Invalid question id: {id}.")
        return redirect(f"/questions/{len(response)}")

    question = surveys.satisfaction_survey.questions[id]
    return render_template("questions.html", question_num=id, question=question)

@app.route('/complete')
def complete():
    return render_template('complete.html')