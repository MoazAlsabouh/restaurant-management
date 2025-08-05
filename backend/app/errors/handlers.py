from flask import jsonify
from app.auth.auth import AuthError

def register_error_handlers(app):
    @app.errorhandler(400)
    def not_processed(error):
        return jsonify({"success": False, "error": 400, "message": "This transaction cannot be processed"}), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"success": False, "error": 404, "message": "resource not found"}), 404

    @app.errorhandler(409)
    def not_insert_data(error):
        return jsonify({"success": False, "error": 409, "message": "It is not possible to add data to a name in the database"}), 409

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({"success": False, "error": 422, "message": "unprocessable"}), 422

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({"success": False, "error": error.status_code, "message": error.error}), error.status_code
