from flask import Flask, render_template
from flask_pymongo import PyMongo
from random import randint


RANDOM_START = 1
RANDOM_END = 999999999999999999

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://mongo:27017/dev" # раскомментировать при сборке в образ docker
#app.config["MONGO_URI"] = "mongodb://172.17.0.4:27017/dev" # раскомментировать при локальной работе приложения
mongo = PyMongo(app)
db = mongo.db

def get_randoms_from_db():
    randoms_db = db.random.find()
    randoms_for_template: list[int] = []
    for random_db in randoms_db:
        randoms_for_template.append(random_db["random"])
    return randoms_for_template

@app.route("/")
def index():
    randoms_for_template = get_randoms_from_db()
    return render_template('index.html',  randoms=randoms_for_template)

@app.route("/randoms/delete", methods=["GET"])
def delete_randoms():
    db.random.drop()
    randoms_for_template = get_randoms_from_db()
    return render_template('index.html',  randoms=randoms_for_template)

@app.route("/randoms/add", methods=["GET"])
def add_random():
    db.random.insert_one({"random": randint(RANDOM_START, RANDOM_END)})
    randoms_for_template = get_randoms_from_db()
    return render_template('index.html',  randoms=randoms_for_template)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
