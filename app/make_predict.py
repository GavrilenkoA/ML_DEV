from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, BackgroundTasks
from sqlalchemy.orm import Session, load_only

from database import create_session
from data_models import User, Predictions
from utils import verify_password, create_access_token

from processing_data import process_data
from utils import get_predictions, read_uploaded_excel
from check_data import Patient



app = FastAPI()


@app.post("/signin/")
async def login(username: str, email: str, password: str, db: Session = Depends(create_session)):
    if not db.query(User).filter_by(username=username).first():
        raise HTTPException(status_code=401, detail="User with this username haven't registered")

    if not db.query(User).filter_by(email=email).first():
        raise HTTPException(status_code=401, detail="User with this username haven't registered")

    # select password_hash from db to check input password
    user = db.query(User).filter_by(username=username).first()
    password_hash = user.password_hash
    if not verify_password(password, password_hash):
        raise HTTPException(status_code=401, detail="Incorrect password")

    token = create_access_token(email)

    return {"access_token": token, "email": email}


@app.post("/predict/")
def predict(background_tasks: BackgroundTasks, file: UploadFile = File(...), data_auth: dict = Depends(login), db: Session = Depends(create_session)):
    df = read_uploaded_excel(file)
    patients_data = df.to_dict(orient="records")
    _ = [Patient(**patient_data) for patient_data in patients_data]
    processed_data = process_data(df)

    background_tasks.add_task(get_predictions, processed_data, db, data_auth["email"])

    return {"message": "Prediction written in a database"}


@app.get("/return_predictions/")
def return_predictions(data_auth: dict = Depends(login), db: Session = Depends(create_session)):
    predictions = db.query(Predictions)\
                .filter_by(email=data_auth["email"])

    all_predictions = predictions.all()
    return all_predictions





