from app.exceptions.post_exceptions import InvalidKeys, PostNotFound
from flask import Flask, request, jsonify
from app.models.post_model import Post
from datetime import datetime

def init_app(app: Flask):
    @app.get('/posts')
    def read_posts():
        posts = Post.get_posts()
        return jsonify(posts), 200

    @app.get('/posts/<int:id>')
    def read_post_by_id(id: int):
        try:
            post = Post.get_post_by_id(id)
            return post.__dict__, 200

        except PostNotFound:
            return {"msg": "Post Not found."}, 404

    @app.post('/posts')
    def create_post():
        data = request.json
        data["created_at"] = datetime.utcnow()
        data["updated_at"] = datetime.utcnow()

        try:
            post = Post(**data)
            new_post = post.save_post()
            return new_post, 201

        except TypeError:
            return {"msg": "Missing keys."}, 400

    @app.delete('/posts/<int:id>')
    def delete_post(id: int):
        try:
            post = Post.delete_post(id)
            return post, 200

        except PostNotFound:
            return {"msg": "Post Not found."}, 404

    @app.patch('/posts/<int:id>')
    def update_post(id: int):
        try:
            request.json["updated_at"] = datetime.utcnow()
            post = Post.get_post_by_id(id)

            for key in request.json:
                if not key in post.__dict__:
                    raise InvalidKeys

            post = post.update(request.json)

            return post, 200

        except PostNotFound:
            return {"msg": "Post Not found."}, 404

        except InvalidKeys:
            return {"msg": "Invalid key(s)."}, 400
