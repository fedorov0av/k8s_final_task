from flask import Flask, render_template
from flask_pymongo import PyMongo
from random import randint

app = Flask(__name__)
#app.config["MONGO_URI"] = "mongodb://mongo:27017/dev" # раскомментировать при сборке в образ docker
app.config["MONGO_URI"] = "mongodb://172.17.0.4:27017/dev" 
mongo = PyMongo(app)
db = mongo.db

@app.route("/")
def index():
    randoms_db = db.random.find()
    randoms_for_template = []
    for random_db in randoms_db:
        randoms_for_template.append(random_db["random"])
    return render_template('index.html',  randoms=randoms_for_template)

@app.route("/randoms/delete", methods=["GET"])
def delete_randoms():
    db.random.drop()
    randoms_db = db.random.find()
    randoms_for_template = []
    for random_db in randoms_db:
        randoms_for_template.append(random_db["random"])
    return render_template('index.html',  randoms=randoms_for_template)

@app.route("/randoms/add", methods=["GET"])
def add_random():
    db.random.insert_one({"random": randint(1,900000000000000000)})
    randoms_db = db.random.find()
    randoms_for_template = []
    for random_db in randoms_db:
        randoms_for_template.append(random_db["random"])
    return render_template('index.html',  randoms=randoms_for_template)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)