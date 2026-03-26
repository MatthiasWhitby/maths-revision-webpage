from flask import Flask, render_template, session, redirect, url_for, request
import random
from fractions import Fraction
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "local_dev_key")

def differentiation_question():
    a = random.randint(2, 9)
    n = random.randint(2, 6)
    question = "Differentiate: {}x<sup>{}</sup>".format(a, n)
    answer = "{}x<sup>{}</sup>".format(a*n, n-1)
    wrong1 = "{}x<sup>{}</sup>".format(a, n-1)
    wrong2 = "{}x<sup>{}</sup>".format(a*n, n)
    wrong3 = "{}x<sup>{}</sup> + c".format(Fraction(a, n+1), n+1)
    return question, answer, wrong1, wrong2, wrong3

def integration_question():
    a = random.randint(2, 9)
    n = random.randint(2, 6)
    question = "Integrate: {}x<sup>{}</sup>".format(a, n)
    answer = "{}x<sup>{}</sup> + c".format(Fraction(a, n+1), n+1)
    wrong1 = "{}x<sup>{}</sup> + c".format(Fraction(a, n), n+1)
    wrong2 = "{}x<sup>{}</sup> + c".format(a, n+1)
    wrong3 = "{}x<sup>{}</sup> + c".format(Fraction(a, n+1), n)
    return question, answer, wrong1, wrong2, wrong3

def sequence_question():
    a = random.randint(1, 10)
    d = random.randint(2, 9)
    question = "Find the nth term of the sequence: {}, {}, {}, {}, {}".format(a, a+d, a+2*d, a+3*d, a+4*d)
    if a - d == 0:
        answer = "{}n".format(d)
        wrong1 = "{}n + {}".format(d, a) 
    elif a - d > 0:
        answer = "{}n + {}".format(d, a-d)
        wrong1 = "{}n".format(d)
    else:
        answer = "{}n - {}".format(d, abs(a-d))
        wrong1 = "{}n".format(d)
    wrong2 = "{}(n-1) + {}".format(d, a)
    wrong3 = "{}n + {}".format(d, a)
    return question, answer, wrong1, wrong2, wrong3

def generate_question(topic):
    if topic == "1":
        return differentiation_question()
    elif topic == "2":
        return integration_question()
    elif topic == "3":
        return sequence_question()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/quiz", methods=["POST", "GET"])
def quiz():
    if request.method == "POST":
        session["topic"] = request.form["topic"]
        session["score"] = 0
        session["questions"] = 0

    topic = session.get("topic")
    if topic is None:
        return redirect(url_for("home"))
    question, answer, wrong1, wrong2, wrong3 = generate_question(topic)
    session["answer"] = answer

    options = [answer, wrong1, wrong2, wrong3]
    random.shuffle(options)
    return render_template("quiz.html", question=question, options=options)

@app.route("/result", methods=["POST"])
def result():
    user_answer = request.form["chosen"]
    if user_answer == session["answer"]:
        session["score"] += 1
        correct = True
    else:
        correct = False
    session["questions"] += 1
    session.modified = True
    return render_template("result.html", correct=correct, answer=session["answer"], score=session["score"], questions=session["questions"])

if __name__ == "__main__":
    app.run(debug=True)