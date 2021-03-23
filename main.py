from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from email_users import send_letter

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:3337@localhost/w_index'
db = SQLAlchemy(app)


class MyDB(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email_ = db.Column(db.String(120), unique=True, nullable=False)
    weight_ = db.Column(db.Integer, nullable=False)
    height_ = db.Column(db.Integer, nullable=False)
    index_ = db.Column(db.Integer, nullable=False)

    def __init__(self, email, weight, height, index):
        self.email_ = email
        self.weight_ = weight
        self.height_ = height
        self.index_ = index


db.create_all()


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/info", methods=['POST'])
def info():
    if request.method == 'POST':
        email = request.form['email_addr']
        weight = request.form['weight']
        height = request.form['height']
        w_index = int(int(weight) / ((int(height) / 100) ** 2))
        if db.session.query(MyDB).filter(MyDB.email_ == email).count() == 0:
            db_data = MyDB(email, weight, height, w_index)
            db.session.add(db_data)
            db.session.commit()
            avr_index = db.session.query(func.avg(MyDB.index_)).scalar()
            avr_index = int(avr_index)
            count = db.session.query(MyDB.email_).count()
            send_letter(email, w_index, avr_index, count)
            print(avr_index)
        else:
            return render_template('index.html', text='This email is already in use!')
        return render_template('info.html')


if __name__ == '__main__':
    app.debug = True
    app.run()
