import configparser
from datetime import datetime
from flask import Flask, render_template, request, redirect, session, flash, jsonify
import os

from modules.Mongo.mongo_manager import MongoManager
from modules.user_manager import UserManager

app = Flask(__name__)

cfg = configparser.ConfigParser()
cfg.read('./config.ini')
app.secret_key = cfg.get('app', 'secret_key')

mongo_manager = MongoManager()


@app.route("/")
def main_page():
    return render_template("main_page.html")


@app.route("/home")
def home():
    if session.get('logged_in'):

        books = mongo_manager.get_all_books()
        temp_img_path = cfg.get('app', 'temp_books_img_path')

        books_list = [
            {"book_id": book.book_id, "book_name": book.book_name, "book_img_name": book.book_img_name}
            for book in books
        ]

        if not os.path.exists(temp_img_path):
            os.makedirs(temp_img_path)

        return render_template('home.html', books=books_list,
                               temp_img_path=temp_img_path)
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
            operation = f"Pomyślnie zalogowano użytkownika o emailu {email} "
            add_operation('system', operation)
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
            operation = f"Pomyślnie zarejestrowano użytkownika o emailu {email} "
            add_operation('system', operation)
            return redirect('/login')
        else:
            flash('Użytkownik o podanym emailu lub peselu już istnieje! Spróbuj ponownie.')
            return redirect('/register')

    return render_template('register.html')


@app.route('/logout')
def logout():
    if session['logged_in']:
        operation = f"Pomyślnie wylogowano użytkownika {session['user_data']['login']}!"
        session.pop('logged_in', None)
        add_operation('system', operation)
        flash('Wylogowano!')

    return redirect('/')


@app.route('/operation_history')
def operation_history():
    if session['logged_in']:
        if session['user_data']['login'] == 'admin':

            operations = mongo_manager.get_all_users_operations()

            return render_template('operation_history.html', operations=operations)
        else:
            redirect('/home')
    else:
        redirect('/')


@app.route('/add_book', methods=['POST'])
def add_book():
    if request.method == 'POST':
        book_name = request.form['book_name']
        book_image = request.files['book_image']

        if book_name and book_image:
            is_book_added = mongo_manager.add_book(book_name, book_image.filename)

            temp_img_dir = f"./{cfg.get('app', 'temp_books_img_path')}"

            if not os.path.exists(temp_img_dir):
                os.makedirs(temp_img_dir)

            if is_book_added:
                image_path = os.path.join(temp_img_dir, book_image.filename)
                book_image.save(image_path)
                operation = f"Dodano książkę o nazwie {book_name} i zdjęciu {book_image.filename}"
                add_operation(session['user_data']['login'], operation)
                response = jsonify({'message': "Książka została dodana!", 'status': 'success'})
            else:
                response = jsonify({'message': "Książka nie została dodana, ponieważ już istnieje!", 'status': 'danger'})
        else:
            response = jsonify({'message': "Nie uzupełniono wszystkich informacji o dodawanej książce", 'status': 'danger'})

        return response


@app.route('/remove_book', methods=['POST'])
def remove_book():
    book_id = int(request.form.get('book_id'))
    book_name = request.form.get('book_name')
    book_img = request.form.get('book_img')

    mongo_manager.remove_book(book_id)

    operation = f"Usunięcie książki o _id: {book_id}, nazwie: {book_name}, zdjęciu: {book_img} z bazy danych"
    add_operation(session['user_data']['login'], operation)

    response = jsonify({'message': "Książka została usunięta!", 'status': 'warning'})

    return response


@app.route('/edit_book', methods=['POST'])
def edit_book():
    book_id = int(request.form['book_id'])
    new_book_name = request.form['new_book_name']
    new_book_img = request.files['new_book_img']

    new_book_data = {
        'name': new_book_name,
        'img_name': new_book_img.filename
    }
    mongo_manager.edit_book(book_id, new_book_data)

    operation = f"Edycja książki o _id: {book_id}. Zmiana nazwy na {new_book_name} i zdjęcia na {new_book_img.filename}"
    add_operation(session['user_data']['login'], operation)

    response = jsonify({'message': f"Dane ksiązki zostały zamienione!", 'status': 'success'})

    return response


def add_operation(user, operation) -> None:
    """
    Add new operation to UsersOperations collection.
    :param user: User to whom the operation applies
    :param operation: Completed operation
    """
    mongo_manager.add_user_operation(user, operation, datetime.timestamp(datetime.now()))


if __name__ == "__main__":
    app.run(port=cfg.getint('app', 'port'),
            host="0.0.0.0",
            debug=cfg.getboolean('app', 'debug_mode'))
