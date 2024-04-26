from flask import Flask, render_template, request, redirect, url_for, session
import bcrypt
import datetime

app = Flask(__name__)
app.secret_key = 'super_secret_key'  # Needed for session management

# Data produk
produk = {
    1: {"nama": "Indomie", "harga": 3500},
    2: {"nama": "Teh Botol", "harga": 5000},
    3: {"nama": "Kopi Kapal Api", "harga": 2000},
    4: {"nama": "Sari Roti", "harga": 6000},
    5: {"nama": "Biskuit Roma", "harga": 6000}
}

# User data with hashed passwords (using bcrypt)
user_data = {
    "admin": {"nama": "Luthfi", "password": bcrypt.hashpw('123'.encode('utf-8'), bcrypt.gensalt())},
    "kasir1": {"nama": "Kasir 1", "password": bcrypt.hashpw('kasir123'.encode('utf-8'), bcrypt.gensalt())}
}

# Function to verify login credentials
def verify_login(username, password):
    user = user_data.get(username)
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
        return True
    return False

# Route for home page
@app.route('/')
def index():
    return render_template('index.html')

# Route for login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if verify_login(username, password):
            session['username'] = username
            return redirect(url_for('kasir'))
        else:
            return "Login gagal. Silakan coba lagi."
    return render_template('login.html')

# Route for cashier page
@app.route('/kasir', methods=['GET', 'POST'])
def kasir():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        waktu = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        nama_kasir = user_data[session['username']]['nama']
        keranjang_belanja = {}
        total_belanja = 0

        # Calculate total purchase price based on selected products
        for key, value in request.form.items():
            if key.isdigit() and value.isdigit():
                produk_id = int(key)
                jumlah = int(value)
                if produk_id in produk:
                    keranjang_belanja[produk_id] = jumlah
                    total_belanja += produk[produk_id]['harga'] * jumlah
        if 'hitung_total' in request.form:
            return render_template('kasir.html', produk=produk, keranjang_belanja=keranjang_belanja, total_belanja=total_belanja)

        # If "Proses" button is pressed, perform payment process
        elif 'proses' in request.form:
            uang_diberikan = int(request.form['uang_diberikan'])
            kembalian = uang_diberikan - total_belanja
            return render_template('struk.html', waktu=waktu, nama_kasir=nama_kasir, keranjang_belanja=keranjang_belanja,
                                   total_belanja=total_belanja, uang_diberikan=uang_diberikan, kembalian=kembalian)

    return render_template('kasir.html', produk=produk)

# Route for receipt page
@app.route('/struk')
def struk():
    return render_template('struk.html') 

if __name__ == "__main__":
    app.run(debug=True)
