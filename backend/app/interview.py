from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
<<<<<<< HEAD
from . import models, schemas
from .database import SessionLocal
from typing import List
from .logger import logger
import os

router = APIRouter()

=======

from shared import models
from shared import schemas
from shared.database import SessionLocal
from typing import List
from shared.logger import logger
import os
from .util_queue import send_message_to_service_bus
from datetime import datetime
import uuid
# shared/schemas.py

from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime


router = APIRouter()



# class TaskMessage(BaseModel):
#     correlationId: str
#     sessionId: str
#     timestamp: datetime
#     source: str
#     destination: str
#     action: str
#     status: str
#     payload: Dict
    


>>>>>>> dfd1401 (MILESTONE)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dummy questions for demonstration
QUESTION_BANK = [
    {"question_id": 1, "question_text": "Tell me about yourself."},
    {"question_id": 2, "question_text": "What are your strengths?"},
    {"question_id": 3, "question_text": "Describe a challenge you faced."},
]

@router.post("/interview")
def create_interview(interview: schemas.InterviewCreate, db: Session = Depends(get_db)):
<<<<<<< HEAD
    db_interview = models.Interview(interview_name=interview.interview_name)
    db.add(db_interview)
    db.commit()
    db.refresh(db_interview)
    return db_interview

=======
    logger.info(f"/interview called with interview_name={interview.interview_name}, user_id={interview.user_id}")  # <-- log params
    db_interview = models.Interview(
        interview_name=interview.interview_name,
        user_id=interview.user_id
    )
    db.add(db_interview)
    db.commit()
    db.refresh(db_interview)
    # Remove or fix the next logger line if payload is not defined
    # logger.info(f"Starting Interview for user {payload.user_id} interview {payload.interview_id}")
    return db_interview



>>>>>>> dfd1401 (MILESTONE)
@router.post("/start_interview", response_model=List[schemas.QuestionAnswerOut])
def start_interview(payload: schemas.QuestionAnswerCreate, db: Session = Depends(get_db)):
    # Pick 3 new questions (could be random or sequential)
    selected_questions = QUESTION_BANK[:3]
    created = []
    for q in selected_questions:
        qa = models.QuestionAnswer(
            user_id=payload.user_id,
            interview_id=payload.interview_id,
            question_id=q["question_id"],
            question_text=q["question_text"],
            status="NEW"
        )
        db.add(qa)
        db.commit()
        db.refresh(qa)
        created.append(qa)
        logger.info(f"Inserted question {q['question_id']} for user {payload.user_id} interview {payload.interview_id}")
    return created

<<<<<<< HEAD
@router.get("/questions/{user_id}/{interview_id}", response_model=List[schemas.QuestionAnswerOut])
def get_questions(user_id: int, interview_id: int, db: Session = Depends(get_db)):
    questions = db.query(models.QuestionAnswer).filter_by(user_id=user_id, interview_id=interview_id).all()
    return questions

@router.patch("/question/{qa_id}", response_model=schemas.QuestionAnswerOut)
def update_question_answer(qa_id: int, update: schemas.QuestionAnswerUpdate, db: Session = Depends(get_db)):
    qa = db.query(models.QuestionAnswer).filter_by(id=qa_id).first()
    if not qa:
        raise HTTPException(status_code=404, detail="QuestionAnswer not found")
    for field, value in update.dict(exclude_unset=True).items():
        setattr(qa, field, value)
    db.commit()
    db.refresh(qa)
    logger.info(f"Updated QuestionAnswer {qa_id} with {update.dict(exclude_unset=True)}")
    return qa
=======
>>>>>>> dfd1401 (MILESTONE)

@router.post("/more_questions", response_model=List[schemas.QuestionAnswerOut])
def more_questions(payload: schemas.QuestionAnswerCreate, db: Session = Depends(get_db)):
    # Find how many questions already assigned
    existing_qids = {qa.question_id for qa in db.query(models.QuestionAnswer).filter_by(user_id=payload.user_id, interview_id=payload.interview_id)}
    # Pick next 3 not already assigned
    new_questions = [q for q in QUESTION_BANK if q["question_id"] not in existing_qids][:3]
    created = []
    for q in new_questions:
        qa = models.QuestionAnswer(
            user_id=payload.user_id,
            interview_id=payload.interview_id,
            question_id=q["question_id"],
            question_text=q["question_text"],
            status="NEW"
        )
        db.add(qa)
        db.commit()
        db.refresh(qa)
        created.append(qa)
        logger.info(f"Inserted more question {q['question_id']} for user {payload.user_id} interview {payload.interview_id}")
    return created

<<<<<<< HEAD
@router.post("/upload_answer/{user_id}/{interview_id}/{question_id}")
def upload_answer_recording(
    user_id: int,
    interview_id: int,
    question_id: int,
    file: UploadFile = File(...)
):
    upload_dir = f"uploads/{user_id}/{interview_id}"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = f"{upload_dir}/{question_id}_{file.filename}"
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())
    logger.info(f"Saved answer recording at {os.path.abspath(file_path)}")
    return {"path": file_path}

@router.post("/upload_answer/{user_id}/{interview_id}/{question_id}/{recording_type}")
def upload_answer_recording(
    user_id: int,
    interview_id: int,
    question_id: int,
    recording_type: str,  # e.g., "audio", "camera", "screen", "combined"
    file: UploadFile = File(...)
):
    allowed_types = {"audio", "camera", "screen", "combined"}
    if recording_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Invalid recording type")
    upload_dir = f"uploads/{user_id}/{interview_id}"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = f"{upload_dir}/{question_id}_{recording_type}_{file.filename}"
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())
    logger.info(f"Saved {recording_type} recording at {os.path.abspath(file_path)}")
    return {"path": file_path}
=======


# /question API updates the status of question after user answers it.
@router.patch("/question/{qa_id}", response_model=schemas.QuestionAnswerOut)
def update_question_answer(qa_id: int, update: schemas.QuestionAnswerUpdate, db: Session = Depends(get_db)):
    qa = db.query(models.QuestionAnswer).filter_by(id=qa_id).first()
    if not qa:
        raise HTTPException(status_code=404, detail="QuestionAnswer not found")
    for field, value in update.dict(exclude_unset=True).items():
        setattr(qa, field, value)
    db.commit()
    db.refresh(qa)
    logger.info(f"Updated QuestionAnswer {qa_id} with {update.dict(exclude_unset=True)}")
    return qa


>>>>>>> dfd1401 (MILESTONE)

@router.post("/upload_answer/{user_id}/{interview_id}/{question_id}/{type}")
async def upload_answer_type(
    user_id: int,
    interview_id: int,
    question_id: int,
<<<<<<< HEAD
    type: str,  # e.g., "audio", "camera", "screen", "combined"
    file: UploadFile = File(...)
):
=======
    type: str,
    file: UploadFile = File(...)
):
    # Save file logic...
    file_path = f"uploads/{user_id}/{interview_id}/{question_id}_{type}_{file.filename}"
    
>>>>>>> dfd1401 (MILESTONE)
    allowed_types = {"audio", "camera", "screen", "combined"}
    if type not in allowed_types:
        raise HTTPException(status_code=400, detail="Invalid recording type")
    upload_dir = f"uploads/{user_id}/{interview_id}"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = f"{upload_dir}/{question_id}_{type}_{file.filename}"
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())
    logger.info(f"Saved {type} recording at {os.path.abspath(file_path)}")
<<<<<<< HEAD
    return {"path": file_path}
=======
    #return {"path": file_path}

    # After saving the last type (e.g., "combined"), enqueue the message
    if type == "combined":
        message = {
            "correlationId": str(uuid.uuid4()),
            "sessionId": f"{user_id}-{interview_id}",
            "userId": user_id,
            "interviewId": interview_id,
            "questionId": question_id,
            "timestamp": datetime.utcnow().isoformat(),
            "action": "process_answer",
            "status": "new",
            "payload": {
                "audioPath": f"uploads/{user_id}/{interview_id}/{question_id}_audio_{file.filename}",
                "cameraPath": f"uploads/{user_id}/{interview_id}/{question_id}_camera_{file.filename}",
                "screenPath": f"uploads/{user_id}/{interview_id}/{question_id}_screen_{file.filename}",
                "combinedPath": file_path
            }
        }
        send_message_to_service_bus(message)

    return {"path": file_path}
>>>>>>> dfd1401 (MILESTONE)
