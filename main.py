from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask.db'
db = SQLAlchemy(app)


class Post(db.Model):
    """
    Класс базы данных для постов
    id: возвращает id поста
    title: заголовок поста, nullable=False: проверка на пустой заголовок, string(300) максимальное кол_во символов
    text: текст пост, nullable=False: проверка на пустой текст поста
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)


@app.route("/index")
@app.route("/")
def index():
    """
    Декоратор и функция index.html (Главная страница)
    :return: index.html
    """
    return render_template('index.html')


@app.route("/posts")
def posts():
    """
    Декоратор и функция posts (Все записи)
    :return: Все записи из базы данных на страницу posts.html
    """
    post = Post.query.all()
    return render_template('posts.html', posts=post)


@app.route("/create", methods=['POST', 'GET'])
def create():
    """
    Запись поста в базу данных
    :return: В случае ошибки "При_добавление статьи произошла ошибка"
    :return:  Запись статьи в базу данных
    """
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']

        post = Post(title=title, text=text)

        try:
            db.session.add(post)
            db.session.commit()
            return redirect('/')  # Перенапровляет на главную страницу
        except:  # Отлавливаем ошибку в случае ее возникновения
            return "При добавление статьи произошла ошибка"
    else:
        return render_template('create.html')


@app.route("/about")
def about():
    """
    Декоратор и класс about.html (О нас)
    :return: about.html (О нас)
    """
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)  # Постоянно запускается сервер с обновлением базы данных
