from app import app
from models.user import User
from models.document import Document
with app.app_context():
    print('Phase', User.query.filter_by(username='Phase').first() is not None)
    print('Docs', [d.title for d in Document.query.all()])
