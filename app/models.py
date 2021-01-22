import sqlite3
from app.conn_to_db import create_connection


class Books:
    def __init__(self):
        self.db_file = 'library.db'

    def create_table(self):
        create_books_sql = """
        -- books table
        CREATE TABLE IF NOT EXISTS books (
            id integer PRIMARY KEY,
            Title text NOT NULL,
            Author text,
            Year text,
            Genre text,
            Done TEXT
        );
        """
        conn = create_connection(self.db_file)
        cursor = conn.cursor()
        cursor.execute(create_books_sql)

    def add_book(self, book):
        """
       Add a book into the books table
       :param book:
       :return: book id
       """
        sql = '''INSERT INTO books(Title, Author, Year, Genre, Done)
                 VALUES(?,?,?,?,?)'''
        conn = create_connection(self.db_file)
        cur = conn.cursor()
        cur.execute(sql, book)
        conn.commit()
        return cur.lastrowid

    def select_all(self, table):
        """
       Query all rows in the table
       :return:
       """
        conn = create_connection(self.db_file)
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {table}")
        rows = cur.fetchall()

        return rows

    def select_book(self, table, **query):
        """
       Query tasks from table with data from **query dict
       :param conn: the Connection object
       :param table: table name
       :param query: dict of attributes and values
       :return:
       """
        conn = create_connection(self.db_file)
        cur = conn.cursor()
        qs = []
        values = ()
        for k, v in query.items():
            qs.append(f"{k}=?")
            values += (v,)
        q = " AND ".join(qs)
        cur.execute(f"SELECT * FROM {table} WHERE {q}", values)
        rows = cur.fetchall()
        return rows

    def update(self, table, id, data):
        """
        update status, begin_date, and end date of a task
        :param data: updated data
        :param table: table name
        :param id: row id
        :return:
        """
        parameters = [f"{k} = ?" for k in data]
        parameters = ", ".join(parameters)
        values = tuple(v for v in data.values())
        values += (id,)

        sql = f''' UPDATE {table}
                 SET {parameters}
                 WHERE id = ?'''
        try:
            conn = create_connection(self.db_file)
            cur = conn.cursor()
            cur.execute(sql, values)
            conn.commit()
        except sqlite3.OperationalError as e:
            print(e)

    def delete_book(self, table, **kwargs):
        """
       Delete from table where attributes from
       :param conn:  Connection to the SQLite database
       :param table: table name
       :param kwargs: dict of attributes and values
       :return:
       """
        qs = []
        values = tuple()
        for k, v in kwargs.items():
            qs.append(f"{k}=?")
            values += (v,)
        q = " AND ".join(qs)

        sql = f'DELETE FROM {table} WHERE {q}'
        conn = create_connection(self.db_file)
        cur = conn.cursor()
        cur.execute(sql, values)
        conn.commit()


books = Books()
