from pymongo import AsyncMongoClient , ASCENDING

from app.core.config import settings

client = AsyncMongoClient(settings.MONGODB_URL)
db = client[settings.DATABASE_NAME]

user_collection = db['user']

async def create_indexes():
    await user_collection.create_index(
        [("email", ASCENDING)],
        unique= True,
        name="email_unique_index"
    )