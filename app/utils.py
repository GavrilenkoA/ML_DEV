from passlib.context import CryptContext
import os
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt
from dotenv import load_dotenv
import pandas as pd
from io import BytesIO
from fastapi import UploadFile
from catboost import CatBoostClassifier
from data_models import User, Predictions

load_dotenv()
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
ALGORITHM = "HS256"
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")  # should be kept secret

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.now() + expires_delta
    else:
        expires_delta = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt


def read_uploaded_excel(file: UploadFile) -> pd.DataFrame:
    content = BytesIO(file.file.read())
    data = pd.read_excel(content)
    return data


def update_credits(db, email: str, deduct_value: int = 1):
    user = db.query(User).filter_by(email=email).first()
    user.credits -= deduct_value
    db.commit()
    # не закрываю бд


def write_predictions(db, prediction_batch: list):
    predictions_objects = [Predictions(**prediction) for prediction in prediction_batch]

    db.add_all(predictions_objects)
    db.commit()
    db.close()


def get_predictions(inference_data: pd.DataFrame, db, email: str) -> None:
    model = CatBoostClassifier()
    model_path = "ml_models/catboost_model.cbm"
    model.load_model(model_path)

    prediction_batch = []
    mapper_labels = {1: "GBM", 0: "LGG"}
    labels = model.predict(inference_data)
    scores = model.predict_proba(inference_data)[:, 0]

    for label, score in zip(labels, scores):
        current_prediction = {"diagnosis": mapper_labels[label], "score": score, "email": email}
        update_credits(db, email)
        prediction_batch.append(current_prediction)

    write_predictions(db, prediction_batch)
