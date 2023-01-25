from flask import Blueprint, request, jsonify, abort, make_response
from app import db
from app.models.skill import Skill

skills_bp = Blueprint("skills", __name__, url_prefix="/skills")

@skills_bp.route("", methods=["POST"])
def create_skill():
    '''
    POST method - allows client to post skill records to the skills table
    '''
    request_body = request.get_json()
    try:
        new_skill = Skill.from_json(request_body)
    except:
        return make_response({"details": "Invalid data"}, 400)

    db.session.add(new_skill)
    db.session.commit()

    response_body = {"skill": new_skill.to_json()}

    return make_response(jsonify(response_body), 201)


@skills_bp.route("", methods=["GET"])
def get_all_skills():
    '''
    GET method - allows client to get all skill records from the skills table
    '''
    skills = Skill.query.all()

    result = []
    for item in skills:
        result.append(item.to_json())

    return jsonify(result), 200

@skills_bp.route("/<skill_id>", methods=["DELETE"])
def delete_skill(skill_id):
    '''
    DELETE method - allows user to remove specified skill record
    '''
    # skill = validate_model(Skill, skill_id)
    skill = Skill.query.get(skill_id)

    db.session.delete(skill)
    db.session.commit()

    # return {"details": "successfully deleted"}
    return {"details": f"Skill {skill.skill_id} '{skill.name}' successfully deleted"}
