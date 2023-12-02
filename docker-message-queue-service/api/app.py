import os

import flask


def create_app():
    app = flask.Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']

    from db import db
    db.init_app(app)

    from videos import videos
    app.register_blueprint(videos, url_prefix='/videos')

    with app.app_context():
        db.create_all()

    return app



if __name__ == '__main__':
    main()