from models.models import db, User

def create_user(username, password, face_path):

    user = User(
        username=username,
        password=password,
        face_path=face_path
    )

    db.session.add(user)
    db.session.commit()


def get_user_by_username(username):
    return User.query.filter_by(username=username).first()