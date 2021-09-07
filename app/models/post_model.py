from app.exceptions.post_exceptions import PostNotFound
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime
from os import getenv

load_dotenv()

URI = getenv('DATABASE_URI')
PORT = getenv('DATABASE_PORT')

client = MongoClient(URI, int(PORT))
db = client.kenzie


class Post():
    def __init__(self, title: str, content: str, tags: str, author: str) -> None:
        self.id = 1
        self.title = title
        self.content = content
        self.author = author
        self.tags = tags
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def save_post(self):
        last_post = list(db.posts.find().sort("_id", -1).limit(1))

        if last_post:
            self.id += last_post[0]["id"]

        _id = db.posts.insert_one(self.__dict__).inserted_id

        if not _id:
            raise TypeError

        new_post = db.posts.find_one({"_id": _id})
        del new_post["_id"]

        return new_post

    def update(self, update_data: object):
        post = db.posts.find_one_and_update({"id": self.id}, update_data)

        if not post:
            raise PostNotFound
        
        del post["_id"]

        return post

    @staticmethod
    def get_posts():
        posts = list(db.posts.find())

        for post in posts:
            del post["_id"]

        return posts

    @staticmethod
    def get_post_by_id(id: int):
        post = db.posts.find_one({"id": id})

        if not post:
            raise PostNotFound

        del post["_id"]

        return post

    @staticmethod
    def delete_post(id: int):
        post = db.posts.find_one_and_delete({"id": id})

        if not post:
            raise PostNotFound

        del post["_id"]

        return post