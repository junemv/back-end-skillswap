from flask import Blueprint, request, jsonify, abort, make_response
from app import db
from app.models.skill import Skill
from app.user_routes import validate_model

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


@skills_bp.route("/<skill_id>", methods=["GET"])
def get_one_skill(skill_id):
    '''
    GET method - allows user to get one skill table record by ID
    '''
    skill = validate_model(Skill, skill_id)

    return {"skill": skill.to_json()}


@skills_bp.route("/<user_id>", methods=["GET"])
def get_all_user_skills_by_user_id(user_id):
    '''
    GET method - allows user to get one user table record by User Name
    '''
    try:
        user = Skill.query.filter_by(user_id=id).first()
        make_response()
    except:
        abort(make_response(jsonify({"msg": f"User id: {user_id} does not exist."}), 400))

    return {"user": user.to_json()}


@skills_bp.route("/<skill_id>", methods=["DELETE"])
def delete_skill(skill_id):
    '''
    DELETE method - allows user to remove specified skill record by ID
    '''
    skill = validate_model(Skill, skill_id)

    db.session.delete(skill)
    db.session.commit()
    
    return {"details": f"Skill {skill.skill_id} '{skill.name}' successfully deleted"}

@skills_bp.route("/<skill_id>/update_skill", methods=["PATCH"])
def update_skill(skill_id):
    skill = validate_model(Skill, skill_id)

    request_body = request.get_json()

    skill.name = request_body["name"]
    skill.tags = request_body["tags"]
    skill.description = request_body["description"]
    skill.time = request_body["time"]

    db.session.commit()

    return make_response(jsonify({"skill": skill.to_json()}), 200)