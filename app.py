from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "beautybook123"

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="beautybook_db"
)

# =========================
# HALAMAN BOOKING PELANGGAN
# =========================
@app.route('/', methods=['GET', 'POST'])
def home():

    if request.method == 'POST':

        nama = request.form['nama']
        telepon = request.form['telepon']
        layanan = request.form['layanan']
        tanggal = request.form['tanggal']
        jam = request.form['jam']
        catatan = request.form['catatan']

        cursor = db.cursor()

        cursor.execute("""
        INSERT INTO reservasi
        (nama, telepon, layanan, tanggal, jam, catatan)
        VALUES (%s,%s,%s,%s,%s,%s)
        """, (nama, telepon, layanan, tanggal, jam, catatan))

        db.commit()

        return redirect('/')

    return render_template('index.html')


# =========================
# LOGIN ADMIN
# =========================
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        cursor = db.cursor()

        cursor.execute(
            "SELECT * FROM admin WHERE username=%s AND password=%s",
            (username, password)
        )

        admin = cursor.fetchone()

        if admin:
            session['login'] = True
            return redirect('/admin')

    return render_template('login.html')


# =========================
# DASHBOARD ADMIN
# =========================
@app.route('/admin')
def admin():

    if 'login' not in session:
        return redirect('/login')

    cursor = db.cursor()

    cursor.execute("SELECT COUNT(*) FROM reservasi")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT * FROM reservasi ORDER BY id DESC")
    data = cursor.fetchall()

    return render_template(
        'admin.html',
        total=total,
        data=data
    )


# =========================
# HAPUS DATA
# =========================
@app.route('/hapus/<int:id>')
def hapus(id):

    if 'login' not in session:
        return redirect('/login')

    cursor = db.cursor()

    cursor.execute(
        "DELETE FROM reservasi WHERE id=%s",
        (id,)
    )

    db.commit()

    return redirect('/admin')


# =========================
# LOGOUT
# =========================
@app.route('/logout')
def logout():

    session.clear()

    return redirect('/login')


if __name__ == '__main__':
    # Ditambahkan host='0.0.0.0' agar bisa diakses dari HP lewat Wi-Fi
    app.run(host='0.0.0.0', port=5000, debug=True)