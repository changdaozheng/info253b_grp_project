from flask import Flask
from flask_smorest import Api
from flask_migrate import Migrate

from database import db
from config import DevelopmentConfig

from resources.users_route import users_blp as UserBlueprint
from resources.places_route import places_blp as PlaceBlueprint

def create_app():
    """Create Flask application during initialisation """

    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    # initialise SQLAlchemy with database config information

    db.init_app(app)
    migrate = Migrate(app, db)
    # create all db tables required
    with app.app_context():
        db.create_all()

    # init smorest api and Blueprints after initialising db
    api = Api(app)
    # api.register_blueprint(UserBlueprint)
    api.register_blueprint(PlaceBlueprint)

    return app

def remove_app(app, test_env=False):
    """Remove Flask application during teardown"""
    with app.app_context():
        db.session.remove()
        
        if test_env:
            db.drop_all()

if __name__ == "__main__":
    # initialise and run application
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5005)

    # application teardown
    # remove_app(app, test_env=True)
    # remove_app(app)