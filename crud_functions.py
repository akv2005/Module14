import sqlite3
def initiate_db():
    connection = sqlite3.connect('initiate.db')
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users(
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    age INTEGER NOT NULL,
    balance INTEGER NOT NULL)
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL,
    photo TEXT)
    ''')

    Products = [
        ['Редуксин', 'Редуксин', 199, './image/1.jpg'],
        ['Турбослим', 'Турбослим Ночь', 299, './image/2.jpg'],
        ['Голдлайн', 'Голдлайн', 1999, './image/3.jpg'],
        ['Линдакса', 'Линдакса', 2999, './image/4.jpg'],
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

def add_user(username, email, age, balance = 1000):
    connection, cursor = initiate_db()
    check_users = cursor.execute(f'SELECT * FROM Users WHERE username = "{username}"')
    if not check_users.fetchone():
        cursor.execute(f'INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)',
                       (username, email, age, balance))
        connection.commit()
        connection.close()
    else:
        raise (f'Пользователь {username} уже есть в базе данных.')

def is_included(username):
    connection, cursor = initiate_db()
    check_user = cursor.execute(f'SELECT * FROM Users WHERE username = "{username}"')
    result = check_user.fetchone() != None
    connection.commit()
    connection.close()
    return result

# products = get_all_products()
# print(products)
#users = add_user()