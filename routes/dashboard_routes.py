from flask import Blueprint, render_template, session, redirect
from models.models import User

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/login")

    user = User.query.filter_by(username=session["user"]).first()

    return render_template("dashboard.html", user=user)

@dashboard_bp.route("/profile")
def profile():

    if "user" not in session:
        return redirect("/login")

    return render_template("profile.html")


@dashboard_bp.route("/admin")
def admin():

    if session.get("role") != "admin":
        return "Access denied"

    users = User.query.all()

    return render_template("admin.html", users=users)

@dashboard_bp.route("/approve/<int:user_id>")
def approve_user(user_id):

    if session.get("role") != "admin":
        return "Access denied"

    user = User.query.get(user_id)

    user.approved = True

    db.session.commit()

    return redirect("/admin")