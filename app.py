from flask import *
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import json,os




app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
DATABASE_URL="postgresql://hw_user:TzaO8qnbLogp5M3XwsLwK0EpTz45Z9Mf@dpg-cfht36la499bfu2gfnng-a.oregon-postgres.render.com/hw"
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Response(db.Model):
    __tablename__ = "useraccount"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    gender = db.Column(db.String(10), nullable=True)
    color = db.Column(db.String(10), nullable=True)
    cats = db.Column(db.String(80), nullable=True)
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
        cats = ','.join(request.form.getlist('cats'))
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
def admin_summary():
    responses = Response.query.all()

    # process the responses to generate data for charts
    color_counts = {}
    gender_counts = {}
    cats_counts = {}
    reason_answers = []

    for response in responses:
        color = response.color
        gender = response.gender
        cats = response.cats.split(',')
        reason = response.reason

        if color:
            if color not in color_counts:
                color_counts[color] = 0
            color_counts[color] += 1

        if gender:
            if gender not in gender_counts:
                gender_counts[gender] = 0
            gender_counts[gender] += 1

        if cats:
            for cat in cats:
                if cat not in cats_counts:
                    cats_counts[cat] = 0
                cats_counts[cat] += 1

        if reason:
            reason_answers.append(reason)

    # generate data for charts
    color_data = {
        'labels': list(color_counts.keys()),
        'data': list(color_counts.values())
    }
    gender_data = {
        'labels': list(gender_counts.keys()),
        'data': list(gender_counts.values())
    }
    cats_data = {
        'labels': list(cats_counts.keys()),
        'data': list(cats_counts.values())
    }

    # pass the processed data to the template
    return render_template('admin/summary.html',responses=responses,color_data=color_data,gender_data=gender_data,cats_data=cats_data,reason_answers=reason_answers)

if __name__ == '__main__':
  app.run()