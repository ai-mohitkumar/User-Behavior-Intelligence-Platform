from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from typing import List, Dict, Any

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr

class Token(BaseModel):
    access_token: str
    token_type: str

class DatasetCreate(BaseModel):
    filename: str

class ResultOut(BaseModel):
    id: int
    dataset_id: int
    metrics: Dict[str, float]
    best_k: int
    insights: List[str]
    rules: Optional[List[Dict[str, Any]]]

    class Config:
        from_attributes = True

