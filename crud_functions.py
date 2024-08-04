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

    Products = [
        ['Редуксин', 'Редуксин', 199, 'image/1.JPG'],
        ['Турбослим', 'Турбослим Ночь', 299, 'image/2.JPG'],
        ['Голдлайн', 'Голдлайн', 1999, 'image/3.JPG'],
        ['Линдакса', 'Линдакса', 2999, 'image/4.JPG'],
    ]

    cursor.execute('SELECT COUNT(*) FROM Products')
    product_count = cursor.fetchone()[0]

    if product_count == 0:
        for product in Products:
            cursor.execute('INSERT INTO Products (title, description, price, photo) VALUES (?, ?, ?, ?)',
                           (product[0], product[1], product[2], product[3]))
    else:
        print('База заполнена')
    return connection, cursor


def get_all_products():
    connection, cursor = initiate_db()
    cursor.execute('SELECT * FROM Products')
    result = cursor.fetchall()
    connection.commit()
    connection.close()
    return result
