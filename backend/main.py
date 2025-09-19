from typing import List

import create_question
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, TypeAdapter

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5000",  # local
    ],
    # allow_origins = [
    #     "*"
    # ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 生成した問題をFrontendに送信する型
class GenerateQuestionResponse(BaseModel):
    level: int
    language: str
    source_code: str
    answer: str
    explanation: str


# ユーザが回答した内容をFrontendから受信する型
class EvaluateQuestionRequest(BaseModel):
    level: int
    language: str
    source_code: str
    answer: str
    explanation: str
    user_answer: str
    user_explanation: str


# 総合評価の各問題の採点詳細
class EvaluateQuestionDetail(BaseModel):
    index: int
    level: str
    position_score: float
    reason_score: float
    weighted_score: float
    feedback: str


# 総合評価をFrontendに送信する型
class EvaluateQuestionResponse(BaseModel):
    total_score: int
    grade: str
    per_item: List[EvaluateQuestionDetail]
    summary: str


@app.get("/")
def root():
    return {"status": "ok"}


@app.post("/generate_question", response_model=List[GenerateQuestionResponse])
def generate_scenario(language: str):
    questions_response = create_question.create_questions(language=language)
    questions_response = TypeAdapter(List[GenerateQuestionResponse]).validate_json(
        questions_response
    )
    return questions_response


@app.post("/evaluation", response_model=EvaluateQuestionResponse)
def evaluation_result(evaluation_requests: List[EvaluateQuestionRequest]):
    evaluation_response = create_question.evaluate_result(
        [
            evaluation_request.model_dump_json()
            for evaluation_request in evaluation_requests
        ]
    )
    evaluation_response = TypeAdapter(EvaluateQuestionResponse).validate_json(
        evaluation_response
    )

    return evaluation_response
