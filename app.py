from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import sqlite3
import json

app = Flask(__name__)
# Secret key is required to use sessions for secure login
app.secret_key = 'super_secret_canteen_key' 

# --- DATABASE HELPER ---
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# ==========================================
# STUDENT ROUTES
# ==========================================

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
        conn.close()
        
        if user:
            session['student_logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            error = 'Invalid Credentials. Please try again.'
            
    return render_template('login.html', error=error)

@app.route('/dashboard')
def dashboard():
    # Optional: protect dashboard so only logged-in students can see it
    if not session.get('student_logged_in'):
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/api/menu')
def get_menu():
    conn = get_db_connection()
    items = conn.execute('SELECT * FROM menu').fetchall()
    conn.close()
    
    menu_list = [{'id': item['id'], 'name': item['name'], 'category': item['category'], 'price': item['price']} for item in items]
    return jsonify(menu_list)

@app.route('/api/place_order', methods=['POST'])
def place_order():
    data = request.get_json()
    cart_items = json.dumps(data['cart']) # Save the list of items as text
    total = data['total']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO orders (items, total, status) VALUES (?, ?, ?)', (cart_items, total, 'Preparing in Kitchen 🍳'))
    order_id = cursor.lastrowid # Get the new Order ID
    conn.commit()
    conn.close()
    
    return jsonify({'order_id': order_id, 'status': 'Preparing in Kitchen 🍳'})

@app.route('/api/order_status/<int:order_id>')
def order_status(order_id):
    conn = get_db_connection()
    order = conn.execute('SELECT status FROM orders WHERE id = ?', (order_id,)).fetchone()
    conn.close()
    
    if order:
        return jsonify({'status': order['status']})
    return jsonify({'error': 'Order not found'}), 404


# ==========================================
# KITCHEN ADMIN ROUTES
# ==========================================

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    error = None
    if request.method == 'POST':
        # Hardcoded admin credentials for the kitchen staff
        if request.form['username'] == 'admin' and request.form['password'] == 'kitchen123':
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            error = 'Invalid Admin Credentials'
    return render_template('admin_login.html', error=error)

@app.route('/admin')
def admin_dashboard():
    # Check if admin is actually logged in
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    return render_template('admin.html')

@app.route('/api/all_orders')
def get_all_orders():
    conn = get_db_connection()
    orders = conn.execute('SELECT * FROM orders WHERE status != "Completed ✅" ORDER BY id DESC').fetchall()
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

@app.route('/api/update_order', methods=['POST'])
def update_order():
    data = request.get_json()
    order_id = data['order_id']
    new_status = data['status']
    
    conn = get_db_connection()
    conn.execute('UPDATE orders SET status = ? WHERE id = ?', (new_status, order_id))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

# --- START SERVER ---
if __name__ == '__main__':
    app.run(debug=True)