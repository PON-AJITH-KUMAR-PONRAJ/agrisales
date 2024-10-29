from db_config import get_db_connection

def create_user(username, password, role):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (username, password, role) VALUES (%s, %s, %s)', (username, password, role))
    conn.commit()
    cursor.close()
    conn.close()

def get_user_by_username(username):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

def create_product(name, price, description, farmer_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO products (name, price, description, farmer_id) VALUES (%s, %s, %s, %s)', (name, price, description, farmer_id))
    conn.commit()
    cursor.close()
    conn.close()

def get_products_by_farmer(farmer_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM products WHERE farmer_id = %s', (farmer_id,))
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return products

def get_all_products():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return products

def get_all_users():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return users

def delete_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Delete related products first
    cursor.execute('DELETE FROM products WHERE farmer_id = %s', (user_id,))

    # Then delete the user
    cursor.execute('DELETE FROM users WHERE id = %s', (user_id,))
    
    conn.commit()
    cursor.close()
    conn.close()


def delete_product(product_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM products WHERE id = %s', (product_id,))
    conn.commit()
    cursor.close()
    conn.close()
