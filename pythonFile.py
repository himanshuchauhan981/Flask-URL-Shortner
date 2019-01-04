from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators
from wtforms.validators import DataRequired, Length
from flask_pymongo import PyMongo
import bitly_api

API_USER = "bitlyuser0018"
API_KEY = "R_bd9b0bff73df4a89a37780e38ed002ba"

app = Flask('__name__')
app.secret_key = 'development key'
app.jinja_env.filters['zip'] = zip

app.config['MONGO_DBNAME'] = 'url_registration'
app.config['MONGO_URI'] = 'mongodb://himanshuchauhan:himanshu0018@ds119024.mlab.com:19024/url_registration'
mongo = PyMongo(app)


class RegistrationForm(FlaskForm):
    username = StringField('Enter your Username ', validators=[DataRequired(), Length(min=4, max=25, message="Username must be between 4 to 25 characters")])
    mobNum = StringField('Enter your mobile number', validators=[DataRequired(), Length(min=10, max=10, message="Mobile Number must be of 10 digits")])
    pwd = PasswordField('Enter your Password', [validators.DataRequired(), validators.Length(min=6, max=120, message="Password must be of minimum 6 characters"), validators.EqualTo('confirmPassword', message='Passwords must match')])
    confirmPassword = PasswordField('Confirm your Password')
    submitForm = SubmitField('Create Account')


class LoginForm(FlaskForm):
    username = StringField(validators=[DataRequired(message="Username is Required")])
    pwd = PasswordField(validators=[DataRequired(message="Password is wrong")])
    submitLogin = SubmitField('Login')


@app.route('/registrationValidation/<username>/<mobNum>/<pwd>')
def registrationValidation(username, pwd, mobNum):
    form = RegistrationForm()
    userCount = mongo.db.urlRegisteration.find({'username': username}).count()
    mobileCount = mongo.db.urlRegisteration.find({'Mobile Number': mobNum}).count()
    if userCount is not 0 and mobileCount is not 0:
        flash(f'Username and Mobile Number already existed', 'danger')
    elif userCount is 0 and mobileCount is not 0:
        flash(f'Mobile Number already existed', 'danger')
    elif userCount is not 0 and mobileCount is 0:
        flash(f'Username already existed', 'danger')
    else:
        user = mongo.db.urlRegisteration
        user.insert({'username': username, 'password': pwd, 'Mobile Number': mobNum})
        flash(f'Account is successfully created', 'success')
        session['username'] = username
        return redirect(url_for('urlShortener'))
    return render_template('home.html', form=form, heading='Home - URLShortener')


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        mobNum = form.mobNum.data
        pwd = form.pwd.data
        return redirect(url_for('registrationValidation', username=username, mobNum=mobNum, pwd=pwd))
    else:
        return render_template('home.html', form=form, heading='Home - URLShortener')


@app.route('/loginUser', methods=['GET', 'POST'])
def loginUser():
    loginForm = LoginForm()
    if loginForm.validate_on_submit():
        username = loginForm.username.data
        pwd = loginForm.pwd.data
        return redirect(url_for('loginUserCheck', username=username, pwd=pwd))
    else:
        return render_template('login.html', loginForm=loginForm, heading='Login - URLShortener')


@app.route('/loginUserCheck/<username>/<pwd>')
def loginUserCheck(username, pwd):
    dataDict = {}
    loginForm = LoginForm()
    details = mongo.db.urlRegisteration.find({'username': username})
    for data in details:
        dataDict = data
    if dataDict:
        if dataDict['password'] == pwd:
            session['username'] = username
            return redirect(url_for('urlShortener', heading="URLShortener"))
    flash('Username or Password is Incorrect', 'danger')
    return render_template('login.html', loginForm=loginForm, heading='Login - URLShortener')


@app.route('/urlShort', methods=['GET', 'POST'])
def urlShort():
    if request.method == 'POST':
        urlText = request.form['textURL']
    else:
        urlText = request.args.get('textURL')

    session['show_url'] = 'show_url_on'

    bitly = bitly_api.Connection(API_USER, API_KEY)
    response = bitly.shorten(urlText)
    shorturl = response["url"]
    longurl = response["long_url"]
    user = mongo.db.urlData
    data = mongo.db.urlData.find_one({'Username': session['username'], 'Long URL': longurl})
    if not data:
        user.insert({'Username': session['username'], 'Short URL': shorturl, 'Long URL': longurl})
    return render_template('URL_Shortener.html', heading='URLShortener', shorturl=shorturl, longurl=longurl)


@app.route('/logoutUser')
def logoutUser():
    session.pop('username', None)
    session.pop('show_url', None)
    session.pop('savedURLs', None)
    return redirect(url_for('home'))


@app.route('/viewSavedURLs')
def viewSavedURLs():
    longURL = []
    shortURL = []
    session.pop('show_url', None)
    session['savedURLs'] = 'view'
    data = mongo.db.urlData.find()
    for items in data:
        if items['Username'] == session['username']:
            longURL.append(items['Short URL'])
            shortURL.append(items['Long URL'])
    tuplelongURL = tuple(longURL)
    tupleshortURL = tuple(shortURL)
    length = len(longURL)
    return render_template('URL_Shortener.html', heading='URLShortener', tuplelongURL=tuplelongURL, tupleshortURL=tupleshortURL, length=length)


@app.route('/login')
def login():
    loginForm = LoginForm()
    return render_template('login.html', loginForm=loginForm, heading='Login - URLShortener')


@app.route('/urlShortener')
def urlShortener():
    return render_template('URL_Shortener.html', heading='URLShortener')


@app.route('/home')
@app.route('/')
def home():
    form = RegistrationForm()
    return render_template('home.html', form=form, heading='Home - URLShortener')


if __name__ == '__main__':
    app.run(debug=True)
