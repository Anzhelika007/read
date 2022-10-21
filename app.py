from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'hard to guess'
db = SQLAlchemy(app)


def create_app():
    app = Flask(__name__)
    db.init_app(app)
    return app


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    author = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(20), nullable=False)
    rating = db.Column(db.Integer)
    cover = db.Column(db.String(50), nullable=False, default='default.jpg')
    description = db.Column(db.Text)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)

    def __repr__(self):
        return f'<Book {self.title}>'


@app.route('/')
def index():
    books = Book.query.all()
    return render_template('index.html', books=books)


@app.route('/static/books/<filename>')
def send_file(filename):
    return filename


@app.route('/<int:book_id>/')
def book(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template('book.html', book=book)


if __name__ == '__main__':
    app.run(debug=True)
