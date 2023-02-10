from flask import Flask, render_template, request
import config
from exts import db
from models import UserModel
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
migrate = Migrate(app, db)


from flask import Flask, request, render_template, jsonify
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/survey', methods=['GET', 'POST'])
def survey():
    if request.method == 'POST':
        response = {
            'text_input': request.form['text_input'],
            'radio_buttons': request.form['radio_buttons'],
            'select_box': request.form['select_box'],
            'checkbox': request.form['checkbox'],
            'textarea': request.form['textarea']
        }
  
        return render_template('thanks.html')
    return render_template('survey.html')

@app.route('/decline')
def decline():
    return render_template('decline.html')

@app.route('/thanks', methods=['POST'])
def thanks():
    return render_template('thanks.html')




# @app.route("/")
# def index():
#     return render_template("index.html")

# @app.route("/survey", methods=["GET", "POST"])
# def survey():
#     if request.method == "POST":
#         name = request.form["name"]
#         radio = request.form["radio"]
#         select = request.form["select"]
#         checkbox = "on" if "checkbox" in request.form else None
#         textarea = request.form["textarea"] if checkbox else None
#         return render_template("thanks.html", name=name, radio=radio, select=select, checkbox=checkbox, textarea=textarea)
#     return render_template("survey.html")

# @app.route("/decline")
# def decline():
#     return "Thanks anyway!"

# @app.route("/thanks")
# def thanks():
#     return render_template("thanks.html")



if __name__ == '__main__':
  app.run()