from flask import Blueprint, request, jsonify, render_template, session, redirect
from services.auth_service import register_user_base64, login_user_base64
from models.user import User
from models.login_log import LoginLog
from models.document import Document
from models.document_permission import DocumentPermission
from services.database import db

auth_bp = Blueprint("auth", __name__)


def _current_user():
    if "user" not in session:
        return None
    return User.query.filter_by(username=session["user"]).first()


def _ensure_default_documents():
    owner = User.query.filter_by(username="Phase").first()
    if not owner:
        owner = User(username="Phase", password="phaseadmin", embedding=b"", approved=True, is_admin=True)
        db.session.add(owner)
        db.session.commit()

    existing = Document.query.first()
    if existing:
        return

    docs = [
        Document(title="Main Secret Plan", content="Top Secret: Only Phase-granted users can open this.", owner_username="Phase", is_public=False),
        Document(title="Employee Handbook", content="General employee handbook for everyone.", owner_username="Phase", is_public=True),
        Document(title="Security Procedures", content="Security procedures for all employees.", owner_username="Phase", is_public=True),
    ]
    db.session.add_all(docs)
    db.session.commit()


@auth_bp.route("/login")
def login_page():
    return render_template("login.html")


@auth_bp.route("/register")
def register_page():
    return render_template("register.html")


@auth_bp.route("/realtime_register", methods=["POST"])
def realtime_register():
    data = request.json
    result = register_user_base64(data)
    return jsonify(result)


@auth_bp.route("/realtime_login", methods=["POST"])
def realtime_login():
    data = request.json
    result = login_user_base64(data)

    if result["status"] == "success":
        session["user"] = result["username"]
        user = User.query.filter_by(username=result["username"]).first()
        if user.is_admin:
            return jsonify({"status": "admin"})
        return jsonify({"status": "success"})

    return jsonify(result)


@auth_bp.route("/portal")
def portal():
    if "user" not in session:
        return redirect("/login")
    _ensure_default_documents()
    logs = LoginLog.query.order_by(LoginLog.timestamp.desc()).limit(20).all()
    return render_template("dashboard.html", logs=logs)


@auth_bp.route("/documents")
def documents():
    if "user" not in session:
        return redirect("/login")

    user = _current_user()
    if not user:
        return redirect("/login")

    _ensure_default_documents()
    documents = Document.query.order_by(Document.id).all()
    return render_template("documents.html", documents=documents, current_user=user)


@auth_bp.route("/document/<int:doc_id>")
def view_document(doc_id):
    if "user" not in session:
        return redirect("/login")

    user = _current_user()
    document = Document.query.get(doc_id)
    if not document:
        return "Document not found", 404

    if not user.can_view_document(document):
        return "Access denied. You do not have permission to view this document.", 403

    return render_template("document_view.html", document=document)


@auth_bp.route("/manage_documents")
def manage_documents():
    if "user" not in session:
        return redirect("/login")

    user = _current_user()
    if not user or user.username != "Phase":
        return "Access denied. Only Phase can manage permissions.", 403

    _ensure_default_documents()
    documents = Document.query.order_by(Document.id).all()
    users = User.query.filter(User.username != "Phase").all()
    return render_template("manage_documents.html", documents=documents, users=users)


@auth_bp.route("/grant_permission/<int:doc_id>/<int:user_id>")
def grant_permission(doc_id, user_id):
    if "user" not in session:
        return redirect("/login")

    current = _current_user()
    if not current or current.username != "Phase":
        return "Access denied. Only Phase can grant permission.", 403

    document = Document.query.get(doc_id)
    user = User.query.get(user_id)
    if not document or not user:
        return "Invalid document or user.", 404

    existing = DocumentPermission.query.filter_by(document_id=doc_id, user_id=user_id).first()
    if not existing:
        perm = DocumentPermission(document_id=doc_id, user_id=user_id)
        db.session.add(perm)
        db.session.commit()

    return redirect("/manage_documents")


@auth_bp.route("/revoke_permission/<int:doc_id>/<int:user_id>")
def revoke_permission(doc_id, user_id):
    if "user" not in session:
        return redirect("/login")

    current = _current_user()
    if not current or current.username != "Phase":
        return "Access denied. Only Phase can revoke permission.", 403

    perm = DocumentPermission.query.filter_by(document_id=doc_id, user_id=user_id).first()
    if perm:
        db.session.delete(perm)
        db.session.commit()

    return redirect("/manage_documents")


@auth_bp.route("/admin")
def admin_dashboard():
    if "user" not in session:
        return redirect("/login")

    user = _current_user()
    if not user.is_admin:
        return "Access denied"

    users = User.query.all()
    logs = LoginLog.query.order_by(LoginLog.timestamp.desc()).limit(20)
    return render_template("admin.html", users=users, logs=logs)


@auth_bp.route("/approve/<int:user_id>")
def approve(user_id):
    if "user" not in session:
        return redirect("/login")

    user = _current_user()
    if not user.is_admin:
        return "Access denied"

    target = User.query.get(user_id)
    if target:
        target.approved = True
        db.session.commit()
    return redirect("/admin")
