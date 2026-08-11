import insightface
import numpy as np
import cv2

# Load ArcFace model
face_app = insightface.app.FaceAnalysis(name="buffalo_l")
face_app.prepare(ctx_id=0, det_size=(320, 320))


def get_embedding(image_path):
    """
    Extract face embedding from an image
    """
    img = cv2.imread(image_path)

    if img is None:
        return None

    faces = face_app.get(img)

    if len(faces) == 0:
        return None

    embedding = faces[0].embedding

    return embedding


def verify_embedding(known_embedding, test_embedding):
    """
    Compare two face embeddings
    """

    if known_embedding is None or test_embedding is None:
        return False

    known_embedding = np.array(known_embedding)
    test_embedding = np.array(test_embedding)

    similarity = np.dot(known_embedding, test_embedding) / (
        np.linalg.norm(known_embedding) * np.linalg.norm(test_embedding)
    )

    print("Face similarity:", similarity)

    # ArcFace recommended threshold
    if similarity > 0.45:
        return True

    return False