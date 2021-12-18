import math
from myapp import app, login
from flask import render_template, request, redirect, url_for
import utils
import cloudinary.uploader
from flask_login import login_user, logout_user
from myapp.models import UserRole


@app.route("/")
def home():
    book_cates = utils.load_book_category()
    book_cate_id = request.args.get('book_category_id')
    kw = request.args.get('keyword')
    page = request.args.get('page', 1)
    books = utils.load_books(book_cate_id=book_cate_id, kw=kw, page=int(page))
    counter = utils.count_books()
    return render_template('index.html', books=books, book_categories=book_cates,
                           pages=math.ceil(counter/app.config['PAGE_SIZE']))

@app.route('/register', methods =['get', 'post'])
def user_register():
    err_msg =""
    if request.method.__eq__('POST'):
        name = request.form.get('name')
        # xử lý tên unique
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        confirm = request.form.get('confirm')
        avatar_path = None

        try:
            if password.strip().__eq__(confirm.strip()):
                avatar = request.files.get('avatar')
                if avatar:
                    res = cloudinary.uploader.upload(avatar)
                    avatar_path = res['secure_url']
                utils.add_user(name=name, username=username, password=password, email=email, avatar=avatar_path)
                return redirect(url_for('home'))
            else:
                err_msg = 'Mat khau khong khop'
        except Exception as ex:
            err_msg='He thong dang co loi:' +str(ex)


    return render_template('register.html',err_msg=err_msg)

@app.route('/user_signin', methods=['get', 'post'])
def user_signin():
    err_msg = ''
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')

        user = utils.check_login(username=username, password=password)
        if user:
            login_user(user=user)
            return redirect(url_for('home'))
        else:
            err_msg = 'Username hoac password khong chinh xac!!!'

    return render_template('login.html', err_msg=err_msg)

@app.route('/admin-login', methods=['post'])
def signin_admin():
    username = request.form['username']
    password = request.form['password']

    user = utils.check_login(username=username,
                            password=password,
                            role=UserRole.ADMIN)
    if user:
        login_user(user=user)

    return redirect('/admin')


@app.context_processor
def common_response():
    return {
        'book_category': utils.load_book_category()
    }

@app.route("/books")
def book_list():
    pub_id = request.args.get("publisher_id")
    kw = request.args.get("keyword")
    from_price = request.args.get("from_price")
    to_price = request.args.get("to_price")
    books = utils.load_books(pub_id=pub_id, kw=kw, from_price=from_price, to_price=to_price)
    return render_template('books.html', books=books)

@app.route("/books/<int:book_id>")
def book_detail(book_id):
    book = utils.get_book_by_id(book_id)
    return render_template('book_detail.html', book=book)


@app.route('/user_signout')
def user_signout():
    logout_user()
    return redirect(url_for('user_signin'))

@login.user_loader
def load_user(user_id):
    return utils.get_user_by_id(user_id=user_id)

if __name__ == '__main__':
    from myapp.admin import *
    app.run(debug=True)