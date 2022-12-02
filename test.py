from flask import Flask, render_template, request
from random import choice
import string

app = Flask(__name__)

spanish_list = []
with open('spanishdict.txt', 'r') as f:
    for line in f:
        try:
            line = line.strip('\n')
            spa,eng = line.split('-')
            if '/' in spa:
                spa1,spa2 = spa.split('/')
                spa1 = spa1.translate(str.maketrans('', '', string.punctuation)).lower().strip()
                spa2 = spa2.translate(str.maketrans('', '', string.punctuation)).lower().strip()
                l = [eng,spa1,spa2] 
            else:
                spa = spa.translate(str.maketrans('', '', string.punctuation)).lower().strip()
                l = [eng,spa] 
            spanish_list.append(l)       
        except:
            continue

loaded_q = []
with open('user_score.txt', 'w') as f:
    f.write(str(0))

@app.route('/', methods=['GET', 'POST'])
def basic():
    good = False
    with open('user_score.txt', 'r') as f:
        score = int(f.read())
    response = ""
    loaded_q.append(choice(spanish_list))
    eng = loaded_q[len(loaded_q)-1][0]
    q = f"Translate: {eng}"    

    if request.method == 'POST':
        if request.form['text']:
            t = request.form['text'].lower().translate(str.maketrans('', '', string.punctuation)).strip()
            # first check how many answers we have; if 2, check if answer is there
            # Note becauase Python is zero-indexed we are getting the previous index of our list with -2
            for i in loaded_q[len(loaded_q)-2][1:]:
                if t == i:
                    good = True
            if good:
                response = "Good!"
                with open('user_score.txt', 'r') as f:
                    score = int(f.read())
                score += 1
                with open('user_score.txt', 'w') as f:
                    f.write(str(score))
            else:
                response = f"Sorry, try: {loaded_q[len(loaded_q)-2][1]}"

                
    return render_template('index.html', q=q, response=response,score=score)

app.run(debug=True)

if __name__ == "__main__":
    app.run()