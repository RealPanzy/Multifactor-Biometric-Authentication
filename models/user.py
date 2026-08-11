from services.database import db

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    embedding = db.Column(db.PickleType, nullable=False)
    approved = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)

    def can_view_document(self, document):
        if document.is_public:
            return True

        if self.username == document.owner_username:
            return True

        if self.is_admin:
            return True

        has_perm = any(p.user_id == self.id for p in document.permissions)
        return has_perm
