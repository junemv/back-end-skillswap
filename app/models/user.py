from app import db
from flask import abort, make_response

class User_(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String)
    user_name = db.Column(db.String)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    city = db.Column(db.String, nullable=True)
    user_icon = db.Column(db.String, nullable=True)
    profile_desc = db.Column(db.String, nullable=True)
    notif_count = db.Column(db.Integer)
    skills = db.relationship("Skill", back_populates="user")

    def to_json(self):
        return {
            "id": self.user_id,
            "email": self.email,
            "user_name": self.user_name,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "city": self.city,
            "profile_desc": self.profile_desc,
            "notif_count": self.notif_count
        }

    @classmethod
    def from_json(cls, user_json):
        if user_json.get("user_name") and user_json.get("first_name") and user_json.get("last_name") and user_json.get("email"):
            if "city" not in user_json:
                user_json["city"] = ""
            if "profile_desc" not in user_json:
                user_json["profile_desc"] = ""
            if "notif_count" not in user_json:
                user_json["notif_count"] = 0

            new_obj = cls(user_name=user_json["user_name"], 
                        email=user_json["email"],
                        first_name=user_json["first_name"], 
                        last_name=user_json["last_name"],
                        city=user_json["city"],
                        profile_desc=user_json["profile_desc"],
                        notif_count=user_json["notif_count"])

            return new_obj
        else:
            abort(make_response({"Invalid data": "User name, first name, last name, and email fields cannot be blank"}, 400))