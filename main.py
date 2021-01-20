from flask import Flask, request, render_template, redirect, url_for
from forms import BooksForm
from models import books

app = Flask(__name__)
app.config["SECRET_KEY"] = "ilovereading"


@app.route("/books/", methods=["GET", "POST"])
def books_list():
    form = BooksForm()
    data = list(form.data.values())
    data = data[0:5]
    db_file = 'library.db'
    conn = books.create_connection(db_file)
    book_list = books.select_all(conn, 'books')
    error = ""

    if request.method == "POST":
        if form.validate_on_submit():
            books.add_book(conn, data)
        return redirect(url_for("books_list"))

    return render_template("books.html", form=form, books=book_list, error=error)


@app.route("/books/<int:book_id>/", methods=["GET", "POST"])
def book_details(book_id):
    db_file = 'library.db'
    conn = books.create_connection(db_file)
    book = books.select_book(conn, 'books', id=book_id)
    table_headers = ['Title', 'Author', 'Year', 'Genre', 'Done']
    book_dict = dict(zip(table_headers, book[0][1:]))
    form = BooksForm(data=book_dict)

    if request.method == "POST":
        form = BooksForm()
        data = list(form.data.values())
        data_dict = dict(zip(table_headers, data))
#        if form.validate_on_submit():
        if request.form['btn'] == 'Zapisz':
            books.update(conn, 'books', book_id, data_dict)
        if request.form['btn'] == 'Usuń':
            books.delete_book(conn, 'books', id=book_id)

        return redirect(url_for("books_list"))

    return render_template("book.html", form=form, book_id=book_id)


if __name__ == "__main__":
    app.run(debug=False)
