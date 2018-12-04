from flask import jsonify


def page_not_found(e):
    return jsonify(error="Page not found"), 404
