import configparser
from flask import Flask, render_template, request, redirect, session, flash

from modules.user_manager import UserManager

app = Flask(__name__)

cfg = configparser.ConfigParser()
cfg.read('./config.ini')
app.secret_key = cfg.get('app', 'secret_key')


@app.route("/")
def main_page():
    return render_template("main_page.html")


@app.route("/home")
def home():
    if session.get('logged_in'):
        return render_template('home.html')
    else:
        return redirect('/login')


@app.route("/login",  methods=['GET', 'POST'])
def login():
    if session.get('logged_in'):
        return redirect('/home')

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user_manager = UserManager()

        user_data = user_manager.check_if_user_exist_in_db(email, password)

        if user_data:
            session['logged_in'] = True
            session['user_id'] = user_data['_id']
            session['user_data'] = user_data
            flash('Zalogowano pomyślnie!')
            return redirect('/home')
        else:
            flash('Nieprawidłowy email lub hasło. Spróbuj ponownie.')
            return redirect('/login')

    return render_template('login.html')


@app.route("/register",  methods=['GET', 'POST'])
def register():
    if session.get('logged_in'):
        return redirect('/home')

    if request.method == 'POST':
        login = request.form['login']
        email = request.form['email']
        password = request.form['password']
        pesel = int(request.form['pesel'])

        user_manager = UserManager()

        user_data = user_manager.register_user(login, email, password, pesel)

        if user_data:
            flash('Zarejestrowano pomyślnie! Zaloguj się.')
            return redirect('/login')
        else:
            flash('Użytkownik o podanym emailu lub peselu już istnieje! Spróbuj ponownie.')
            return redirect('/register')

    return render_template('register.html')


@app.route('/logout')
def logout():
    if session['logged_in']:
        session.pop('logged_in', None)

    return redirect('/')


if __name__ == "__main__":
    app.run(port=8080, host="0.0.0.0", debug=True)
