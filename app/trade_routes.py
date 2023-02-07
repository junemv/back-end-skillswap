from flask import Blueprint, request, jsonify, abort, make_response
from app import db
from app.models.trade import Trade
from app.models.user import User_
from app.user_routes import validate_model
from datetime import datetime

trades_bp = Blueprint("trades", __name__, url_prefix="/trades")

@trades_bp.route("", methods=["POST"])
def create_trade():
    '''
    POST method - allows client to post trade records to the trades table
    '''
    request_body = request.get_json()
    test_trade = Trade.from_json(request_body)
    try:
        new_trade = Trade.from_json(request_body)
    except:
        return make_response({"details": "Invalid data", "response": test_trade}, 400)

    new_trade.time_stamp = datetime.utcnow()
    db.session.add(new_trade)
    db.session.commit()

    response_body = {"trade": new_trade.to_json()}

    return make_response(jsonify(response_body), 201)

@trades_bp.route("", methods=["GET"])
def get_all_trades():
    '''
    GET method - allows client to get all trade records from the trades table
    '''
    trades = Trade.query.all()

    result = []
    for item in trades:
        result.append(item.to_json())

    return jsonify(result), 200

@trades_bp.route("/<user_id>", methods=["GET"])
def get_all_trades_for_user(user_id):
    '''
    GET method - allows user to view all trades
    '''
    user = validate_model(User_, user_id)

    trades = Trade.query.all()

    result = []
    for item in trades:
        if item.recip_user == user.user_id or item.send_user == user.user_id:
            result.append(item.to_json())

    return jsonify(result), 200

@trades_bp.route("/trade/<trade_id>", methods=["GET"])
def get_one_trade(trade_id):
    '''
    GET method - allows client to get a trade records from the trades table
    '''
    trade = validate_model(Trade, trade_id)

    return {"Trade": trade.to_json()}, 200

@trades_bp.route("/<trade_id>", methods=["DELETE"])
def delete_skill(trade_id):
    '''
    DELETE method - allows for the removal of specified trade record by ID
    '''
    trade = validate_model(Trade, trade_id)

    db.session.delete(trade)
    db.session.commit()
    
    return {"details": f"Trade {trade.trade_id} successfully deleted"}

@trades_bp.route("/<trade_id>/<user_id>/viewed", methods=["PATCH"])
def view_trade(trade_id, user_id):
    '''
    PATCH - updates viewed by send or recip based on onclick event in the front end
    '''

    trade = validate_model(Trade, trade_id)
    user = validate_model(User_, user_id)

    request_body = request.get_json()

    if user.user_id == request_body["send_user"]:
        trade.send_viewed = not trade.send_viewed
    elif user.user_id == request_body["recip_user"]:
        trade.recip_viewed = not trade.recip_viewed

    # trade.send_viewed = request_body["send_viewed"]
    # trade.recip_viewed = request_body["recip_viewed"]
    # trade.time_stamp = datetime.utcnow()

    db.session.commit()

    return make_response(jsonify({"trade": trade.to_json()}), 200)

@trades_bp.route("/<trade_id>/<user_id>/toggle_accept", methods=["PATCH"])
def update_skill(trade_id, user_id):
    '''
    PATCH - allows users to toggle the accept (by accepting or declining a trade) parameters
    '''

    trade = validate_model(Trade, trade_id)
    user = validate_model(User_, user_id)

    request_body = request.get_json()

    if user.user_id == request_body["send_user"]:
        trade.send_accept = not trade.send_accept
    elif user.user_id == request_body["recip_user"]:
        trade.recip_accept = not trade.recip_accept
    trade.time_stamp = datetime.now()

    db.session.commit()

    return make_response(jsonify({"trade": trade.to_json()}), 200)