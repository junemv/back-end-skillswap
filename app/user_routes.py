from flask import Blueprint, request, jsonify, abort, make_response
from app import db
from app.models.user import User_

user_bp = Blueprint("users", __name__, url_prefix="/users")


def validate_model(cls, model_id):
    '''
    helper function - throws an error code for an invalid ID
    '''
    try:
        model_id = int(model_id)
    except:
        abort(make_response(jsonify({"msg": f"{cls.__name__} with ID: {model_id} is invalid."}), 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response(jsonify({"msg": f"{cls.__name__} with ID: {model_id} is not found."}), 404))
    
    return model


@user_bp.route("", methods=["POST"])
def create_user():
    '''
    POST method - allows client to post user_ records to the users_ table
    '''
    request_body = request.get_json()
    try:
        new_user = User_.from_json(request_body)
    except:
        return make_response({"details": "Invalid data", "request body": f"{request_body}"}, 400)

    db.session.add(new_user)
    db.session.commit()

    response_body = {"user": new_user.to_json()}

    return make_response(jsonify(response_body), 201)


@user_bp.route("", methods=["GET"])
def get_all_users():
    '''
    GET method - allows client to get all user records from the user_ table
    '''
    users = User_.query.all()

    result = []
    for item in users:
        result.append(item.to_json())

    return jsonify(result), 200


@user_bp.route("/<user_id>", methods=["GET"])
def get_one_user(user_id):
    '''
    GET method - allows user to get one user table record by ID
    '''
    user = validate_model(User_, user_id)

    return {"user": user.to_json()}


@user_bp.route("/username/<username>", methods=["GET"])
def get_one_user_by_user_name(username):
    '''
    GET method - allows user to get one user table record by User Name
    '''
    try:
        user = User_.query.filter_by(user_name=username).first()
        make_response()
    except:
        abort(make_response(jsonify({"msg": f"User name: {username} does not exist."}), 400))

    return {"user": user.to_json()}


@user_bp.route("/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    '''
    DELETE method - allows user to remove specified user record by ID
    '''
    user = validate_model(User_, user_id)

    db.session.delete(user)
    db.session.commit()

    return {"details": f"User {user.user_id} '{user.user_name}' successfully deleted"}

@user_bp.route("/<user_id>/update_user", methods=["PATCH"])
def update_user(user_id):
    user = validate_model(User_, user_id)

    request_body = request.get_json()

    user.first_name = request_body["first_name"]
    user.last_name = request_body["last_name"]
    user.city = request_body["city"]
    user.user_icon = request_body["user_icon"]
    user.profile_desc = request_body["profile_desc"]

    db.session.commit()

    return make_response(jsonify({"user": user.to_json()}), 200)