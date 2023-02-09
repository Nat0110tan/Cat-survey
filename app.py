from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
  return "hi"

@app.route("/a")
def hello():
  return "haaaaaaaaa"