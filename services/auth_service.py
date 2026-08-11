import os
import base64
from models.user import User
from models.login_log import LoginLog
from services.database import db
from services.face_service import get_embedding, verify_embedding

UPLOAD_FOLDER = "uploads/faces"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def register_user_base64(data):

    username = data["username"]
    password = data["password"]
    image_data = data["image"]

    existing = User.query.filter_by(username=username).first()

    if existing:
        return {"status":"error","message":"User already exists"}

    image_data = image_data.split(",")[1]
    image_bytes = base64.b64decode(image_data)

    path = os.path.join(UPLOAD_FOLDER, username+".jpg")

    with open(path,"wb") as f:
        f.write(image_bytes)

    embedding = get_embedding(path)

    if embedding is None:
        return {"status":"error","message":"Face not detected"}

    user = User(
        username=username,
        password=password,
        embedding=embedding,
        approved=True
    )

    db.session.add(user)
    db.session.commit()

    return {"status":"success","message":"Registration successful"}


def login_user_base64(data):

    username = data["username"]
    password = data["password"]
    image_data = data["image"]

    user = User.query.filter_by(username=username).first()

    if not user:

        log = LoginLog(username=username,success=False)
        db.session.add(log)
        db.session.commit()

        return {"status":"error","message":"User not found"}

    if user.password != password:

        log = LoginLog(username=username,success=False)
        db.session.add(log)
        db.session.commit()

        return {"status":"error","message":"Incorrect password"}

    image_data = image_data.split(",")[1]
    image_bytes = base64.b64decode(image_data)

    path = os.path.join(UPLOAD_FOLDER,"login.jpg")

    with open(path,"wb") as f:
        f.write(image_bytes)

    test_embedding = get_embedding(path)

    match = verify_embedding(user.embedding,test_embedding)

    log = LoginLog(username=username,success=match)
    db.session.add(log)
    db.session.commit()

    if not match:
        return {"status":"error","message":"Face verification failed"}

    return {"status":"success","username":user.username}