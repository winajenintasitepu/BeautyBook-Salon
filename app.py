from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/data')
def data():
    return render_template('data.html')

@app.route('/admin')
def admin():
    try:
        return render_template('admin.html')
    except:
        return "File admin.html belum diupload ke GitHub. Selesaikan halaman utama dulu yuk!"

if __name__ == '__main__':
    app.run(debug=True)
