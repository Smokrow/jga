import pyttsx3
from flask_api import status
from flask import jsonify
import os, os.path
from flask import Flask
from flask_cors import CORS
app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})


@app.route("/number/<int:number>")
def read_number(number):
	engine = pyttsx3.init()
	engine.say(str(number))
	engine.runAndWait()
	return "ok",status.HTTP_200_OK

@app.route("/level/<int:level_num>")
def read_level(level_num):

    with open("levels/%i.txt" % level_num,"r") as f:
        text= f.read()

        engine = pyttsx3.init()
        engine.setProperty('voice', 10)
        engine.setProperty('rate', 150)
        engine.say(text)
        engine.runAndWait()
    return "ok",status.HTTP_200_OK

@app.route("/state")
def state():
    return jsonify(get_state()),status.HTTP_200_OK

def get_state():
    state={}
    with open("max_level.txt","r") as f:
        state["max_level"] = int(f.read())
        #num_levels = len([name for name in os.listdir('./levels/') if os.path.isfile(name)])
        current_dir=os.path.dirname(os.path.realpath(__file__))+"/levels"
        path, dirs, files = next(os.walk(current_dir))
        file_count = len(files)
        state["num_levels"] = file_count
    return state


@app.route("/solve/<int:level>/<int:solve>")
def solve(level, solve):

    if level >= get_state()["num_levels"] or level < 0:
        return "the provided level is not right",status.HTTP_400_BAD_REQUEST

    if level is get_state()["max_level"]:
        answer = get_answer(level)
        if answer == solve:
            save_max_level(level+1)
            return "success",status.HTTP_202_ACCEPTED
        else:
            return "wronganswer", status.HTTP_204_NO_CONTENT


    return "ok" ,status.HTTP_200_OK

@app.route("/reset")
def reset_max_level():
    save_max_level(0)
    return "Ok", status.HTTP_200_OK


def save_max_level(level):
    with open("max_level.txt","w") as f:
        f.write(str(level))
    return


def get_answer(level):
    with open("answers.txt","r") as f:
        for i in range(level+1):
            answer=int(f.readline())
        return answer
        

if __name__ =="__main__":
    app.run(host="0.0.0.0",port="5555")
