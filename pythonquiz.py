import re
import os
import random
import datetime

_dir = "./"

total_questions = 5

## class Quiz

class Quiz:
    allQuiz = {}
    def __init__(self, id, question, replies, correct):
        self.id = id
        self.question = question
        self.replies = replies
        self.correct = correct
        if not correct: print(id, replies); input() # error in input data
        Quiz.allQuiz[id] = self

    def calculate_score(self, reply):
        print(self.replies)
        if int(reply) == int(self.correct): return 1
        elif int(reply) == len(self.replies) + 1: return 0
        elif  0 < int(reply) < len(self.replies) + 1:
            return -1/len(self.replies)

    def __str__(self):
        out = "\n\nΕρώτηση ["+str(self.id)+"]\n"
        out += self.question.replace("<pre>", "----").replace("</pre>", "----")
        out += "Απαντήσεις:\n"
        for i,r in sorted(self.replies.items()):
            out += str(i)+"\t"+ r + "\n"
        # out += "Correct reply:" +str(self.correct)
        return out.strip("\n")

### interface to the server ################################

def load_quiz():
    ## φόρτωσε δεδομένα ερωτήσεων από εξωτερικό αρχείο
    id = None
    code = False
    replies = {}
    question = ""
    for line in open(os.path.join(_dir, "questions.txt"), "r", encoding="utf-8"):
        if not line.strip(): continue
        if line.startswith("Q"): 
            if id: Quiz(id, question, replies, correct)
            id = line.strip().strip(".")
            correct = None
            question = ""
            replies = {}
        elif re.findall("^[1-9]+?\.", line): # reply
            reply_number = int(line.split()[0].strip("."))
            if line.strip().endswith("***"):
                correct = reply_number
                line = line.strip().rstrip("***")
            reply_body = " ".join(line.split()[1:])
            replies[reply_number] = reply_body.strip()
        else:
            question += line

def draw_questions():
    all_quiz_keys = list(Quiz.allQuiz.keys())
    random.shuffle(all_quiz_keys)
    return all_quiz_keys[:total_questions]

def show_question(id):
    if id in Quiz.allQuiz.keys():
        q = Quiz.allQuiz[id]
        return {"id": q.id, \
            "question": q.question, \
            "replies": {**q.replies, **{len(q.replies)+1: "Δεν γνωρίζω"}}, \
            "correct": q.correct}

if __name__ == "__main__":
    load_quiz()
    print(draw_questions())