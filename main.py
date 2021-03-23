from flask import Flask, render_template, request, redirect
import csv
from flask_sqlalchemy import SQLAlchemy
# from email_users import send_letter


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:3337@localhost/database_name'
db = SQLAlchemy(app)


class MyDB(db.Model):
    __tablename__ = 'table_name'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200), nullable=False)


    def __init__(self, email, subject):
        self.email = email
        self.subject = subject


db.create_all()




@app.route('/')
def home():
    return render_template('index.html')


@app.route('/<string:page_name>')
def page_name(page_name):
    return render_template(page_name)


@app.route("/submit_form", methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        data = request.form.to_dict()
        write_to_csv(data)
        print('after csv')
        email = request.form['email']
        subject = request.form['subject']
        db_data = MyDB(email, subject)
        db.session.add(db_data)
        db.session.commit()
        # send_letter()
        print('add to db')
        return redirect('/thanks.html')



def write_to_csv(mess):
    with open('database.csv', mode='a') as database:
        fieldnames = ['email', 'subject', 'text_message']
        writer = csv.DictWriter(database, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(mess)
        print('add to csv')


count = db.session.query(MyDB.email).count()

if __name__ == '__main__':
    app.run(debug=True)