from flask import *
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import json,os



app = Flask(__name__)
# app.config.from_object(config)
app.config['SQLALCHEMY_DATABASE_URI']= os.environ.get("DATABASE_URL")
DATABASE_URL="postgresql://hw_user:TzaO8qnbLogp5M3XwsLwK0EpTz45Z9Mf@dpg-cfht36la499bfu2gfnng-a.oregon-postgres.render.com/hw"

db = SQLAlchemy(app)
migrate = Migrate(app, db)

with app.app_context():
 db.create_all()

class Response(db.Model):
    __tablename__ = "useraccount"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    color = db.Column(db.String(10), nullable=True)
    cats = db.Column(db.Boolean, nullable=True)
    reason = db.Column(db.String(500), nullable=True)
    join_time = db.Column(db.DateTime, default=datetime.now)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/survey', methods=['GET', 'POST'])
def survey():
    if request.method == 'POST':
        name = request.form['name']
        gender = request.form['gender']
        color = request.form['color']
        cats = 'no' in request.form
        reason = request.form.get('reason', '')
        join_time = request.form.get('join_time')
        response = Response(name=name, gender=gender, color=color, cats=cats, reason=reason, join_time=join_time)
        db.session.add(response)
        db.session.commit()
        return render_template('thanks.html')
    else:
        return render_template('survey.html')

@app.route('/decline')
def decline():
    return render_template('decline.html')

@app.route('/thanks', methods=['POST'])
def thanks():
    return render_template('thanks.html')

@app.route('/api/results')
def get_results():
    reverse = request.args.get('reverse')
    if reverse == 'true':
        responses = Response.query.order_by(Response.id.desc()).all()
    else:
        responses = Response.query.all()
    results = []
    for response in responses:
        results.append({
            'name': response.name,
            'gender': response.gender,
            'color': response.color,
            'cats': response.cats,
            'reason': response.reason,
            'join_time': response.join_time
        })
    return jsonify(results)


@app.route('/admin/summary')
def summary():
    return render_template('summary.html')

if __name__ == '__main__':
  app.run()