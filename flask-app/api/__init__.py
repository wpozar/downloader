from flask import Flask, jsonify

from .routes import rest_api


def create_app(config):
    app = Flask(__name__)
    app.config.from_mapping(config)

    @app.route('/ping', methods=['GET'])
    def ping():
        response_dict = {'response': 'pong'}
        return jsonify(response_dict), 200

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'error': error.description}), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': error.description}), 404

    app.register_blueprint(rest_api, url_prefix='/api/v1')

    return app
