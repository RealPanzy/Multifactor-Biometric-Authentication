from services.database import db

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    owner_username = db.Column(db.String(100), db.ForeignKey("user.username"), nullable=False)
    is_public = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    owner = db.relationship("User", backref=db.backref("owned_documents", lazy=True))

    permissions = db.relationship("DocumentPermission", backref="document", lazy=True, cascade="all, delete-orphan")
