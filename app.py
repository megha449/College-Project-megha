from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import sqlite3
import json

app = Flask(__name__)

# ==========================================
# SECRET KEY
# ==========================================

app.secret_key = 'super_secret_canteen_key'

# ==========================================
# BUILD DATABASE FROM schema.sql
# ==========================================

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

print("Database successfully built from schema.sql!")

connection.close()

# ==========================================
# DATABASE CONNECTION
# ==========================================

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# ==========================================
# STUDENT LOGIN
# ==========================================

@app.route('/', methods=['GET', 'POST'])
def login():

    error = None

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()

        user = conn.execute(
            '''
            SELECT * FROM users 
            WHERE username = ? 
            AND password = ? 
            AND role = ?
            ''',
            (username, password, 'student')
        ).fetchone()

        conn.close()

        if user:

            session.clear()

            session['student_logged_in'] = True
            session['student_username'] = username

            return redirect(url_for('dashboard'))

        else:
            error = 'Invalid Credentials'

    return render_template('login.html', error=error)

# ==========================================
# STUDENT DASHBOARD
# ==========================================

@app.route('/dashboard')
def dashboard():

    if not session.get('student_logged_in'):
        return redirect(url_for('login'))

    return render_template('index.html')

# ==========================================
# LOGOUT
# ==========================================

@app.route('/logout')
def logout():

    session.clear()

    return redirect(url_for('login'))

# ==========================================
# GET MENU API
# ==========================================

@app.route('/api/menu')
def get_menu():

    conn = get_db_connection()

    items = conn.execute('SELECT * FROM menu').fetchall()

    conn.close()

    menu_list = []

    for item in items:

        menu_list.append({
            'id': item['id'],
            'name': item['name'],
            'category': item['category'],
            'price': item['price']
        })

    return jsonify(menu_list)

# ==========================================
# PLACE ORDER API
# ==========================================

@app.route('/api/place_order', methods=['POST'])
def place_order():

    data = request.get_json()

    cart_items = json.dumps(data['cart'])

    total = data['total']

    conn = get_db_connection()

    cursor = conn.cursor()

    cursor.execute(
        '''
        INSERT INTO orders (items, total, status)
        VALUES (?, ?, ?)
        ''',
        (
            cart_items,
            total,
            'Preparing in Kitchen 🍳'
        )
    )

    order_id = cursor.lastrowid

    conn.commit()

    conn.close()

    return jsonify({
        'order_id': order_id,
        'status': 'Preparing in Kitchen 🍳'
    })

# ==========================================
# ORDER STATUS API
# ==========================================

@app.route('/api/order_status/<int:order_id>')
def order_status(order_id):

    conn = get_db_connection()

    order = conn.execute(
        'SELECT status FROM orders WHERE id = ?',
        (order_id,)
    ).fetchone()

    conn.close()

    if order:

        return jsonify({
            'status': order['status']
        })

    return jsonify({
        'error': 'Order not found'
    }), 404

# ==========================================
# ADMIN LOGIN
# ==========================================

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():

    error = None

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()

        admin = conn.execute(
            '''
            SELECT * FROM users 
            WHERE username = ? 
            AND password = ? 
            AND role = ?
            ''',
            (username, password, 'admin')
        ).fetchone()

        conn.close()

        if admin:

            session.clear()

            session['admin_logged_in'] = True
            session['admin_username'] = username

            return redirect(url_for('admin_dashboard'))

        else:
            error = 'Invalid Admin Credentials'

    return render_template('admin_login.html', error=error)

# ==========================================
# ADMIN DASHBOARD
# ==========================================

@app.route('/admin')
def admin_dashboard():

    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    return render_template('admin.html')

# ==========================================
# GET ALL ORDERS API
# ==========================================

@app.route('/api/all_orders')
def get_all_orders():

    if not session.get('admin_logged_in'):

        return jsonify({
            'error': 'Unauthorized'
        }), 401

    conn = get_db_connection()

    orders = conn.execute(
        '''
        SELECT * FROM orders
        WHERE status != "Completed ✅"
        ORDER BY id DESC
        '''
    ).fetchall()

    conn.close()

    order_list = []

    for order in orders:

        order_list.append({
            'id': order['id'],
            'items': json.loads(order['items']),
            'total': order['total'],
            'status': order['status']
        })

    return jsonify(order_list)

# ==========================================
# UPDATE ORDER STATUS API
# ==========================================

@app.route('/api/update_order', methods=['POST'])
def update_order():

    if not session.get('admin_logged_in'):

        return jsonify({
            'error': 'Unauthorized'
        }), 401

    data = request.get_json()

    order_id = data['order_id']
    new_status = data['status']

    conn = get_db_connection()

    conn.execute(
        '''
        UPDATE orders
        SET status = ?
        WHERE id = ?
        ''',
        (new_status, order_id)
    )

    conn.commit()

    conn.close()

    return jsonify({
        'success': True
    })

# ==========================================
# START SERVER
# ==========================================

if __name__ == '__main__':
    app.run(debug=True)