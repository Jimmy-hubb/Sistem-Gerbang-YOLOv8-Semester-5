from flask import Flask, render_template, request, redirect, url_for, session
from auth import register_user, login_user, init_db
import os

app = Flask(__name__)
app.secret_key = "secret123"  # ubah jika produksi

# Inisialisasi database
init_db()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))

# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        success, result = login_user(username, password)

        if not success:
            return render_template("login.html", error=result)

        # Simpan session
        session["user_id"] = result
        session["username"] = username

        # Tampilkan SweetAlert login berhasil
        return render_template("login_success.html")

    return render_template("login.html")


# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        success, result = register_user(username, password)

        if not success:
            return render_template("register.html", error=result)

        # Tampilkan SweetAlert berhasil
        return render_template("register_success.html")
    
    return render_template("register.html")


# ---------------- DASHBOARD (Proteksi) ----------------
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    return render_template("dashboard.html", username=session.get("username"))

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)
