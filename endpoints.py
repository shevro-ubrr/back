from fastapi import APIRouter, Cookie, HTTPException, status

from course import courses_to_words, words_to_courses
from db.crud import get_user_info, create_user
from random import randint
from db.database import users_collection

router = APIRouter()

@router.post("/onboard")
async def onboard(answers: list[str], username: str = Cookie(...)):
    if not await get_user_info(username):
        await create_user(username)

    user = await get_user_info(username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create or fetch user"
        )

    if user["Recommended_Courses"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already has recommended courses"
        )
    
    recommended_course = randint(0, 2)
    course = list(courses_to_words.keys())[recommended_course]
    result = await users_collection.update_one(
        {"username": username},
        {"$push": {"Recommended_Courses": course}}
    )

    if result.modified_count == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to add recommended course"
        )

    return {
        "status": "success"
    }

@router.get("/recommended_courses")
async def get_recommended_courses(username: str = Cookie(...)):
    user = await get_user_info(username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch user"
        )

    return {
        "recommended_courses": [courses_to_words[course] for course in user["Recommended_Courses"]],
    }

@router.get("/my_courses")
async def get_user_courses(username: str = Cookie(...)):
    user = await get_user_info(username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch user"
        )

    return {
        "my_courses": [courses_to_words[course] for course in user["Courses"]],
    }

@router.post("/start_course")
async def start_course(keyword: str, username: str = Cookie(...)):
    user = await get_user_info(username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch user"
        )

    for course in user["Courses"]:
        if course == words_to_courses[keyword]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Course already started"
            )

    result = await users_collection.update_one(
        {"username": username},
        {"$push": {"Courses": words_to_courses[keyword]}}
    )

    if result.modified_count == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to add course"
        )

    return {
        "status": "success",
    }
