import sqlite3
def initiate_db():
    connection = sqlite3.connect('initiate.db ')
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL,
    photo TEXT)
    ''')
    # connection.commit()
    # connection.close()
    return connection, cursor

def get_all_products():
    connection, cursor = initiate_db()
    cursor.execute('SELECT * FROM Products')
    result = cursor.fetchall()
    connection.commit()
    connection.close()
    return result


# products = get_all_products()
# print(products)