from db.database import users_collection
from db.models import UserInDB


async def create_user(username: str):
    return await users_collection.insert_one(UserInDB(username=username).model_dump())

async def get_user_info(username: str):
    return await users_collection.find_one({"username": username})
