from app import db
from flask import abort, make_response

class User_(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    city = db.Column(db.String, nullable=True)
    user_icon = db.Column(db.String, nullable=True)
    profile_desc = db.Column(db.String, nullable=True)
    skills = db.relationship("Skill", back_populates="user")

    def to_json(self):
        return {
            "id": self.user_id,
            "user name": self.user_name,
            "first name": self.first_name,
            "last name": self.last_name,
            "city": self.city,
            "profile description": self.profile_desc,
        }

    @classmethod
    def from_json(cls, user_json):
        if user_json.get("user_name") and user_json.get("first_name") and user_json.get("last_name"):
            new_obj = cls(user_name=user_json["user_name"], first_name=user_json["first_name"], last_name=user_json["last_name"])
            return new_obj
        else:
            abort(make_response({"Invalid data": "User name, first name, and last name fields cannot be blank"}, 400))