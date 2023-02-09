from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
DATABASE_URL="postgresql://hw_user:TzaO8qnbLogp5M3XwsLwK0EpTz45Z9Mf@dpg-cfht36la499bfu2gfnng-a.oregon-postgres.render.com/hw"
db = SQLAlchemy(app)

class Cat(db.Model):
  __tablename__ = "cat"
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  #varchar, null=0
  name = db.Column(db.String(100), nullable=False)
  password = db.Column(db.String(100), nullable=False)

@app.route("/cat/update")
def update_user():
  catt = Cat.query.filter_by(name="meme").first()
  # 这里的first返回的是一个user对象而不是query类数组
  catt.password = "123456" #已经是在这个数据库里面操作了,不用add
  db.session.commit()
  return "Successfully changed"

with app.app_context():
  db.create_all()

@app.route("/")
def hello():
  return "hi"

@app.route("/add/<string:n>")
def helloo(n):
  cat = Cat(name=n,password="123")
  db.session.add(cat)
  db.session.commit()
  return "Successfully added a new cat!"


if __name__ == '__main__':
  app.run()