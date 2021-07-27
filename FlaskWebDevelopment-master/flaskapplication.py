from flask import Flask, render_template, session,  request, redirect, Response, url_for, flash
from werkzeug.wrappers import Request, Response
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask_sqlalchemy import SQLAlchemy


class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')


app = Flask(__name__, template_folder='templates')
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = '7cwtzhl0tkg9obj9'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cgpa.sqlite3'

db = SQLAlchemy(app)


class cgpa(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    Course_Code = db.Column(db.String(100), nullable=False)
    Course_Title = db.Column(db.String(50), nullable=False)
    Credit_Attemped = db.Column(db.Integer, nullable=False)
    Letter_Grade = db.Column(db.String(20), nullable=False)
    Grade_Points = db.Column(db.Integer, nullable=False)
    Points_Secured = db.Column(db.Integer, nullable=False)


def __init__(self, Course_Code, Course_Title, Credit_Attemped, Letter_Grade, Grade_Points, Points_Secured):
    self.Course_Code = Course_Code
    self.Course_Title = Course_Title
    self.Credit_Attemped = Credit_Attemped
    self.Letter_Grade = Letter_Grade
    self.Grade_Points = Grade_Points
    self.Points_Secured = Points_Secured


@app.route('/')
def show_all():
    return render_template('Cgpa.html', cgpa=cgpa.query.all())


db.create_all()


@app.route('/gpa', methods=['GET', 'POST'])
def gpa():
    if request.method == 'POST':
        if not request.form['Course_Code'] or not request.form['Course_Title'] or not request.form['Credit_Attemped'] or not request.form['Letter_Grade'] or not request.form['Grade_Points'] or not request.form['Points_Secured']:
            flash('Please enter all the fields', 'error')
    else:
        cgpas = cgpa(request.form['Course_Code'], request.form['Course_Title'], request.form['Credit_Attemped'],
                     request.form['Letter_Grade'], request.form['Grade_Points'], request.form['Points_Secured'])

        db.session.add(cgpas)
        db.session.commit()
        flash('Record was successfully added')
        return redirect(url_for('show_all'))

    return render_template('Cgpa.html')


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html',
                           form=form, name=session.get('name'))


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
