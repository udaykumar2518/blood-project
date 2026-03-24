from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'secret123'


# Home
@app.route('/')
def home():
    return render_template('index.html')


# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        blood = request.form['blood']
        city = request.form['city']
        phone = request.form['phone']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute("INSERT INTO donors (name, blood, city, phone) VALUES (?, ?, ?, ?)",
                       (name, blood, city, phone))

        conn.commit()
        conn.close()

        return redirect('/')

    return render_template('register.html')


# Search
@app.route('/search', methods=['GET', 'POST'])
def search():
    results = []

    if request.method == 'POST':
        blood = request.form['blood']
        city = request.form['city']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM donors WHERE blood=? AND city=?", (blood, city))
        results = cursor.fetchall()

        conn.close()

    return render_template('search.html', results=results)


# Donors
@app.route('/donors')
def donors():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM donors")
    data = cursor.fetchall()

    conn.close()

    return render_template('donors.html', donors=data)


# Dashboard (NO login required)
@app.route('/dashboard')
def dashboard():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM donors")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(DISTINCT blood) FROM donors")
    blood_types = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(DISTINCT city) FROM donors")
    cities = cursor.fetchone()[0]

    cursor.execute("SELECT * FROM donors ORDER BY id DESC LIMIT 5")
    donors = cursor.fetchall()

    conn.close()

    return render_template('dashboard.html',
                           total=total,
                           blood_types=blood_types,
                           cities=cities,
                           donors=donors)


# Delete (ADMIN ONLY)
@app.route('/delete/<int:id>')
def delete(id):
    if 'admin' not in session:
        return "Access Denied"

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM donors WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect('/donors')


# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == 'admin' and password == '1234':
            session['admin'] = True
            return redirect('/dashboard')
        else:
            return "Invalid credentials"

    return render_template('login.html')
@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect('/')

# Run app
if __name__ == '__main__':
    app.run(debug=True)