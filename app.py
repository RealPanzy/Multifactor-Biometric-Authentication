from flask import Flask, render_template, session, redirect
from config import Config
from services.database import db
from routes.auth_routes import auth_bp
from models.login_log import LoginLog
from models.user import User
from models.document import Document
from models.document_permission import DocumentPermission
import os


app = Flask(__name__)
app.config.from_object(Config)

# secret key for sessions
app.secret_key = "supersecretkey"


# initialize database
db.init_app(app)


# create upload folders
os.makedirs("uploads", exist_ok=True)
os.makedirs("uploads/faces", exist_ok=True)


# register blueprint routes
app.register_blueprint(auth_bp)


# -----------------------------
# COMPANY LANDING PAGE
# -----------------------------
@app.route("/")
def home():
    return render_template("company_home.html")


# -----------------------------
# LOGOUT
# -----------------------------
@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


# -----------------------------
# RUN SERVER
# -----------------------------
if __name__ == "__main__":

    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        from models.user import User
        if not User.query.filter_by(username="Phase").first():
            user = User(username="Phase", password="phaseadmin", embedding=b"", approved=True, is_admin=True)
            db.session.add(user)
            db.session.commit()
            print("Created Phase account")

    print("Starting Flask server...")

    app.run(debug=True)