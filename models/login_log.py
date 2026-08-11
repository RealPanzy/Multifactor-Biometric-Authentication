from services.database import db
from datetime import datetime

class LoginLog(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100))

    success = db.Column(db.Boolean)

    timestamp = db.Column(db.DateTime, default=datetime.utcnow)