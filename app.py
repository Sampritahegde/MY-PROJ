from flask import Flask, render_template, request, redirect, flash, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, UserMixin, logout_user
from flask_bcrypt import Bcrypt
import pickle
import numpy as np

app = Flask(__name__)


model = pickle.load(open('ckd.pkl', 'rb'))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'
app.config['SECRET_KEY'] = 'thisissecret'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    fname = db.Column(db.String(80), nullable=False)
    lname = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    def __repr__(self):
        return '<User %r>' % self.username 
    
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()


@app.route("/", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        email = request.form.get('email')
        password = request.form.get('password')
        username = request.form.get('uname')
        user = User(fname=fname, lname=lname, email=email, password=password, username=username)
        db.session.add(user)
        db.session.commit()
        flash('user has been registered successfully','success')
        return redirect('/login')
    return render_template("Register.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and password == user.password:
            login_user(user)
            return redirect('/index')
        else:
            flash('Invalid Credentials', 'warning')
            return redirect('/login')
    return render_template("login.html")


@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/DataAnalytics')
def DataAnalytics():
    return render_template('DataAnalytics.html')

@app.route('/Dataset')
def Dataset():
    return render_template('Dataset.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/models')
def models():
    return render_template('models.html')

@app.route('/Accuracy')
def Accuracy():
    return render_template('Accuracy.html')


@app.route('/predict', methods = ['GET', 'POST'])
def predict():
    int_features = [  x for x in request.form.values()]
    final_features = [np.array(int_features)]
    prediction = model.predict(final_features)

    output = prediction[0]
    print (output)
    
    if output == 0:
        return render_template('notspecifying.html', prediction_text= 'You are not suffering from Kidney Disease')
    else:
        return render_template('specifying.html', prediction_text= 'Ouch! You are suffering from Kidney Disease')

@app.route('/notspecifying')
def notspecifying():
    return render_template('notspecifying.html')

@app.route('/specifying')
def specifying():
    return render_template('specifying.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/login')


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8081, debug=True)