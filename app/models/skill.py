from app import db
from flask import abort, make_response


class Skill(db.Model):
    skill_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tags = db.Column(db.ARRAY(db.String), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    time = db.Column(db.Integer)
    user = db.relationship("User", back_populates="skills")

    def to_json(self):
        return {
            "id": self.skill_id,
            "name": self.name,
            "tags": self.tags,
            "description": self.description,
            "time": self.time,
            "user_id": self.user_id,
        }

    @classmethod
    def from_json(cls, skill_json):
        if skill_json.get("name") and skill_json.get("description") and skill_json.get("time"):
            new_obj = cls(name=skill_json["name"], description=skill_json["description"], time=skill_json["time"])
            return new_obj
        else:
            abort(make_response({"Invalid data": "Name, description, and time ields cannot be blank"}, 400))