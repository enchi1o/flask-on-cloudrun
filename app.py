from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    send_from_directory,
)
from flask_sqlalchemy import SQLAlchemy
import os
import logging

# 設定環境變數
basedir = os.path.abspath(os.path.dirname(__file__))
cloudsql = os.environ.get("CLOUDSQL", False)
cloudstorage = os.environ.get("CLOUDSTORAGE", False)
db_user = os.environ.get("DB_USER", "mp_user")
db_pass = os.environ.get("DB_PASS", "89798198")
db_name = os.environ.get("DB_NAME", "demo")
cloud_sql_connection_name = "gke-test-403702:asia-east1:cloudrundemo"

# 設定 logging
if cloudstorage:
    log_file = "/app/flask_app.log"
else:
    log_file = "./flask_app.log"

logger = logging.getLogger("flask_app")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
file_handler.encoding = "utf-8"
logger.addHandler(file_handler)

# 設定 Flask
app = Flask(__name__, template_folder="template")
app.secret_key = "your_secret_key"
app.logger.addHandler(file_handler)

# 設定資料庫 URI
if cloudsql:
    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = f"mysql+pymysql://{db_user}:{db_pass}@localhost/{db_name}?unix_socket=/cloudsql/{cloud_sql_connection_name}"
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
        basedir, "data.sqlite"
    )
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
version = os.environ.get("VERSION", "1.0.0")

# 產生資料庫物件
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)


# 資料庫初始化
with app.app_context():
    db.create_all()


# 路由和處理函式配對
@app.route("/")
def index():
    return redirect(url_for("dashboard"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        if user is not None:
            return "This username is already registered"
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("login.html", version=version)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()
        if user is None:
            logger.info(f"Not found user: {username}")
            return "Not found user"
        if user.password == password:
            session["logged_in"] = True
            return redirect(url_for("dashboard"))

        return "Invalid username or password"

    return render_template("login.html", version=version)


@app.route("/dashboard")
def dashboard():
    if session.get("logged_in"):
        users = User.query.all()
        return render_template("dashboard.html", users=users, version=version)
    else:
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    return redirect(url_for("index"))


@app.route("/image/<path:filename>")
def get_image(filename):
    return send_from_directory("/app/image", filename)


if __name__ == "__main__":
    app.run(debug=True)
