import os
import base64
from datetime import datetime
from flask import (
    Flask, render_template, request, redirect,
    url_for, session, send_from_directory, jsonify
)
import mysql.connector
from mqtt import publish_message, run_mqtt

app = Flask(__name__)
app.secret_key = "secret123"

UPLOAD_FOLDER = r"C:\laragon\www\WebProject\uploads"

# ============================
# DB CONNECTION
# ============================
def get_db():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="",
        database="dbproject"
    )

# ==========================================
# SANITIZER → filename tanpa spasi & simbol
# ==========================================
def sanitize_filename(name):
    return "".join(c for c in name if c.isalnum() or c in ['_', '.', '-'])


@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    safe_name = sanitize_filename(filename)
    return send_from_directory(UPLOAD_FOLDER, safe_name)

def format_datetime(data):
    for row in data:
        if "waktu" in row and isinstance(row["waktu"], datetime):
            row["waktu"] = row["waktu"].strftime("%d-%m-%Y %H:%M:%S")
    return data

# ============================
# ROUTES WEBSITE
# ============================
@app.route("/")
def index():
    if "username" in session:
        return redirect("/dashboard")
    return redirect("/login")


# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    from auth import login_user
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        success, msg = login_user(username, password)
        if success:
            session["username"] = username
            return render_template("login_success.html")

        return render_template("login.html", error=msg)

    return render_template("login.html")


# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    from auth import register_user
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        success, msg = register_user(username, password)
        if success:
            return render_template("register_success.html")

        return render_template("register.html", error=msg)

    return render_template("register.html")


# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect("/login")

    db = get_db()
    cur = db.cursor(dictionary=True)

    cur.execute("SELECT COUNT(*) AS total FROM data_plate_terdeteksi WHERE DATE(waktu)=CURDATE()")
    total_hari_ini = cur.fetchone()["total"]

    cur.execute("""
        SELECT COUNT(*) AS total 
        FROM data_plate_terverifikasi 
        WHERE mode='MASUK' AND DATE(waktu)=CURDATE()
    """)
    total_masuk_hari_ini = cur.fetchone()["total"]

    cur.execute("""
        SELECT COUNT(*) AS total 
        FROM data_plate_terverifikasi 
        WHERE mode='KELUAR' AND DATE(waktu)=CURDATE()
    """)
    total_keluar_hari_ini = cur.fetchone()["total"]

    cur.execute("SELECT waktu FROM data_plate_terverifikasi ORDER BY id DESC LIMIT 1")
    last = cur.fetchone()
    last_open_time = last["waktu"].strftime("%d-%m-%Y %H:%M:%S") if last else "-"

    cur.execute("SELECT COUNT(*) AS total FROM data_plate_terdeteksi")
    total_deteksi = cur.fetchone()["total"]

    cur.execute("SELECT COUNT(*) AS total FROM data_plate_terverifikasi")
    total_verif = cur.fetchone()["total"]

    akurasi = round((total_verif / total_deteksi) * 100, 2) if total_deteksi else 0

    cur.close()
    db.close()

    return render_template(
        "dashboard.html",
        username=session["username"],
        total_hari_ini=total_hari_ini,
        total_masuk_hari_ini=total_masuk_hari_ini,
        total_keluar_hari_ini=total_keluar_hari_ini,
        last_open_time=last_open_time,
        akurasi=akurasi,
        active="dashboard"
    )


# ---------------- HISTORY ----------------
@app.route("/history")
def history():
    if "username" not in session:
        return redirect("/login")

    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("""
        SELECT d.*
        FROM data_plate_terdeteksi d
        JOIN (
            SELECT plat, MAX(id) AS max_id
            FROM data_plate_terdeteksi
            GROUP BY plat
        ) x
        ON d.id = x.max_id
        ORDER BY d.id DESC
    """)

    data = cur.fetchall()

    cur.close()
    db.close()

    data = format_datetime(data)

    # SANITASI NAMA GAMBAR
    for row in data:
        if "gambar" in row:
            row["gambar"] = sanitize_filename(row["gambar"])

    return render_template(
        "history.html",
        username=session["username"],
        data_table=data,
        active="history"
    )


# ---------------- TERDAFTAR ----------------
@app.route("/data-terdaftar")
def data_terdaftar():
    if "username" not in session:
        return redirect("/login")

    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM data_plate_terdaftar ORDER BY id DESC")
    data = cur.fetchall()

    cur.close()
    db.close()

    for row in data:
        row["gambar"] = sanitize_filename(row["gambar"])

    return render_template(
        "terdaftar.html",
        username=session["username"],
        data_table=data,
        active="terdaftar"
    )


# ---------------- TERVERIFIKASI ----------------
@app.route("/data-terverifikasi")
def data_terverifikasi():
    if "username" not in session:
        return redirect("/login")

    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("""
    SELECT 
        v.*, 
        s.status AS status_kendaraan
    FROM data_plate_terverifikasi v
    LEFT JOIN data_status_kendaraan s
        ON v.plat = s.plat
    ORDER BY v.id DESC
    """)
    data = cur.fetchall()

    cur.close()
    db.close()

    data = format_datetime(data)

    for row in data:
        row["gambar"] = sanitize_filename(row["gambar"])

    return render_template(
        "verifikasi.html",
        username=session["username"],
        data_table=data,
        active="terverifikasi"
    )


# =========================================================
# VERIFIKASI
# =========================================================
@app.route("/verifikasi/<int:id>", methods=["POST"])
def verifikasi(id):

    if "username" not in session:
        return jsonify({"success": False, "error": "Unauthorized"}), 401

    body = request.get_json(silent=True) or {}
    pemilik_manual = (body.get("pemilik") or "-").strip()

    db = get_db()
    cur = db.cursor(dictionary=True)

    try:
        cur.execute("SELECT * FROM data_plate_terdeteksi WHERE id=%s", (id,))
        row = cur.fetchone()

        if not row:
            return jsonify({"success": False, "error": "Data tidak ditemukan"}), 404

        plat = row["plat"]
        mode = row["mode"]
        gambar = sanitize_filename(row["gambar"])
        pemilik = pemilik_manual or "-"

        # UPDATE / INSERT TERDAFTAR
        cur.execute("SELECT id FROM data_plate_terdaftar WHERE plat=%s", (plat,))
        exists = cur.fetchone()

        if exists:
            cur.execute("""
                UPDATE data_plate_terdaftar
                SET pemilik=%s, waktu=NOW(), gambar=%s
                WHERE plat=%s
            """, (pemilik, gambar, plat))
        else:
            cur.execute("""
                INSERT INTO data_plate_terdaftar (plat, pemilik, waktu, gambar)
                VALUES (%s, %s, NOW(), %s)
            """, (plat, pemilik, gambar))

        # INSERT VERIFIKASI
        cur.execute("""
            INSERT INTO data_plate_terverifikasi
            (plat, pemilik, mode, status, waktu, gambar)
            VALUES (%s, %s, %s, 'diijinkan', NOW(), %s)
        """, (plat, pemilik, mode, gambar))

        # STATUS KENDARAAN
        status_baru = "di_dalam" if mode == "MASUK" else "di_luar"
        cur.execute("""
            INSERT INTO data_status_kendaraan (plat, status)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE status=%s, waktu_update=NOW()
        """, (plat, status_baru, status_baru))

        # HAPUS DETEKSI LAMA
        cur.execute("DELETE FROM data_plate_terdeteksi WHERE plat=%s", (plat,))

        db.commit()

    except Exception as e:
        db.rollback()
        return jsonify({"success": False, "error": str(e)}), 500

    finally:
        cur.close()
        db.close()

    publish_message("BUKA_GERBANG_MASUK" if mode == "MASUK" else "BUKA_GERBANG_KELUAR")

    return jsonify({"success": True, "plat": plat, "pemilik": pemilik})


# =========================================================
# API DARI main.py (SIMPAN GAMBAR)
# =========================================================
@app.route("/api/kirim-data", methods=["POST"])
def api_kirim_data():

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "No JSON"}), 400

    plat = data.get("plat")
    pemilik = data.get("pemilik") or "-"
    mode = data.get("mode") or "MASUK"
    status = data.get("status") or "ditolak"
    gambar_b64 = data.get("gambar")

    if not plat or not gambar_b64:
        return jsonify({"error": "Incomplete data"}), 400

    raw = base64.b64decode(gambar_b64)

    # SANITIZE FILENAME → Tidak ada spasi
    safe_plat = sanitize_filename(plat)
    filename = sanitize_filename(
        f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{mode}_{safe_plat}.jpg"
    )

    filepath = os.path.join(UPLOAD_FOLDER, filename)

    with open(filepath, "wb") as f:
        f.write(raw)

    dbx = get_db()
    cur = dbx.cursor()
    cur.execute("""
        INSERT INTO data_plate_terdeteksi
        (plat, pemilik, mode, kamera, terdaftar, waktu, status, gambar)
        VALUES (%s, %s, %s, %s, 'tidak', NOW(), %s, %s)
    """, (plat, pemilik, mode, mode, status, filename))

    dbx.commit()
    cur.close()
    dbx.close()

    return jsonify({"success": True, "filename": filename})


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.pop("username", None)
    return render_template("logout_success.html")


# =========================================================
# RUN SERVER
# =========================================================
if __name__ == "__main__":
    run_mqtt()
    app.run(debug=True, host="0.0.0.0", port=5000)
