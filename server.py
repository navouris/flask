from flask import Flask
from flask import redirect, url_for
from flask import request, session, json
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import datetime
import pythonquiz as quiz
quiz.load_quiz() # φόρτωμα των ερωτημάτων του τεστ
app = Flask(__name__)
app.config['SECRET_KEY'] = "a-very-secret-key"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

class User(db.Model):
    username = db.Column(db.String(80), primary_key=True)
    password = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

class Game(db.Model):
    name = db.Column(db.String(80), db.ForeignKey('user.username'), primary_key=True)
    when = db.Column(db.String(80), primary_key=True)
    score = db.Column(db.Float(), nullable=False)

    def __repr__(self):
        return f'<Game {self.name}-{self.when}>'

@app.route ("/")
def root():
    return redirect(url_for("login"))

@app.route("/login", methods=['POST'])
def login():
    def send_quiz():
        questions = quiz.draw_questions()
        the_quiz = [quiz.show_question(q) for q in questions]
        session["username"] = name
        print("session is...", session)
        return json.jsonify(the_quiz)

    print("ROUTE /login")
    name = request.json["name"]
    password_hash = generate_password_hash(request.json["passw"])
    # πρώτα ελέγχουμε αν ο χρήστης υπάρχει με αυτό το όνομα
    user_existing = User.query.filter_by(username=name).first()
    if user_existing: # εφόσον υπάρχει ο χρήστης ... ελέγχουμε αν ο κωδικός είναι σωστός
        check_password = check_password_hash(user_existing.password, request.json["passw"])
        if check_password:
            return send_quiz() # στέλνουμε το τεστ στον χρήστη
        else:
            return json.jsonify({"error": "λάθος κωδικός"})
    else:
        password_hash = generate_password_hash(request.json["passw"])
        new_user = User(username=name, password=password_hash)
        db.session.add(new_user)
        db.session.commit()
        return send_quiz()

@app.route("/end", methods=["POST"])
def end():
    print("ROUTE /end", )
    print("session is...", session)
    name = session.get("username", None)
    score = request.json["score"]
    when =  datetime.datetime.now().strftime('%d-%m-%y %a %H:%M:%S')
    new_game = Game(name=name, when=when, score=score)
    try:
        db.session.add(new_game)
        db.session.commit()
        print(f'το τεστ του {name} αποθηκεύτηκε')
    except Exception as error:
        print(f'σφάλμα αποθήκευσης του τεστ του {name}: {error}')
    print(name, score)
    return json.jsonify({"ok": "saved game", "name": name})

@app.route("/newgame", methods=["POST"])
def newgame():
    print("ROUTE /newgame", )
    print("session is...", session)
    questions = quiz.draw_questions()
    the_quiz = [quiz.show_question(q) for q in questions]
    print(the_quiz)
    return json.jsonify(the_quiz)

if __name__ == "__main__":
    app.run(debug=True)