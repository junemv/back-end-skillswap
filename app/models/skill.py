from app import db
from flask import abort, make_response

class Skill(db.Model):
    skill_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tags = db.Column(db.ARRAY(db.String), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user_.user_id"))
    user_name = db.Column(db.String)
    name = db.Column(db.String)
    description = db.Column(db.String)
    time = db.Column(db.Integer)
    user = db.relationship("User_", back_populates="skills")

    def to_json(self):
        return {
            "id": self.skill_id,
            "name": self.name,
            "tags": self.tags,
            "description": self.description,
            "time": self.time,
            "user_name": self.user_name,
            "user_id": self.user_id
        }

    @classmethod
    def from_json(cls, skill_json):
        if skill_json.get("name") and skill_json.get("description") and skill_json.get("time") and skill_json.get("user_id"):
          #add user_name to conditional
            if "tags" not in skill_json:
                skill_json["tags"] = None

            new_obj = cls(name=skill_json["name"], 
                        tags=skill_json["tags"], 
                        description=skill_json["description"], 
                        time=skill_json["time"],
                        user_name=skill_json["user_name"],
                        user_id=skill_json["user_id"])

            return new_obj
        else:
            abort(make_response({"Invalid data": "Name, description, and time fields cannot be blank"}, 400))