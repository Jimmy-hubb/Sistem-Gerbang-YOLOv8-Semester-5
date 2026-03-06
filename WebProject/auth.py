import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

# Koneksi MySQL
def get_db():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",        # ganti jika MySQL pakai password
        password="",        # isi password MySQL jika ada
        database="dbproject"  # pastikan DB sudah dibuat
    )

# Membuat tabel users jika belum ada
def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) UNIQUE,
            password VARCHAR(255)
        ) ENGINE=InnoDB
        """
    )

    conn.commit()
    cursor.close()
    conn.close()

# Register user baru
def register_user(username, password):
    conn = get_db()
    cursor = conn.cursor()

    # cek duplikasi username
    cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
    if cursor.fetchone():
        cursor.close()
        conn.close()
        return False, "Username sudah digunakan"

    hashed = generate_password_hash(password)
    cursor.execute(
        "INSERT INTO users (username, password) VALUES (%s, %s)",
        (username, hashed)
    )

    conn.commit()
    cursor.close()
    conn.close()
    return True, "Registrasi berhasil"

# Login user
def login_user(username, password):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT id, password FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if not user:
        return False, "User tidak ditemukan"

    user_id, hashed_password = user

    if not check_password_hash(hashed_password, password):
        return False, "Password salah"

    return True, user_id