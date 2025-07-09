from bson import ObjectId
from pydantic import BaseModel, Field
from typing import List
from course import Course


class User(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)

class UserInDB(User):
    Courses: List[Course] = []
    Recommended_Courses: List[str] = []

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
