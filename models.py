import sqlite3


class Books:
    def __init__(self):
        pass

    def create_table(self, conn):
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
        cursor = conn.cursor()
        cursor.execute(create_books_sql)

    def create_connection(self, db_file):
        """ create a database connection to the SQLite database
           specified by db_file
       :param db_file: database file
       :return: Connection object or None
       """
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except sqlite3.Error as e:
            print(e)
        return conn

    def add_book(self, conn, book):
        """
       Add a book into the books table
       :param conn:
       :param book:
       :return: book id
       """
        sql = '''INSERT INTO books(Title, Author, Year, Genre, Done)
                 VALUES(?,?,?,?,?)'''
        cur = conn.cursor()
        cur.execute(sql, book)
        conn.commit()
        return cur.lastrowid

    def select_all(self, conn, table):
        """
       Query all rows in the table
       :param conn: the Connection object
       :return:
       """
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {table}")
        rows = cur.fetchall()

        return rows

    def select_book(self, conn, table, **query):
        """
       Query tasks from table with data from **query dict
       :param conn: the Connection object
       :param table: table name
       :param query: dict of attributes and values
       :return:
       """
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

    def update(self, conn, table, id, new_data):
        """
        update status, begin_date, and end date of a task
        :param conn:
        :param table: table name
        :param id: row id
        :return:
        """
        parameters = [f"{k} = ?" for k in new_data]
        parameters = ", ".join(parameters)
        values = tuple(v for v in new_data.values())
        values += (id,)

        sql = f''' UPDATE {table}
                 SET {parameters}
                 WHERE id = ?'''
        try:
            cur = conn.cursor()
            cur.execute(sql, values)
            conn.commit()
            print("OK")
        except sqlite3.OperationalError as e:
            print(e)

    def delete_book(self, conn, table, **kwargs):
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
        cur = conn.cursor()
        cur.execute(sql, values)
        conn.commit()
        print("Deleted")


books = Books()
