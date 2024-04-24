from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from uuid import UUID 

from schemas.users_schema import UsersSchema, UserFavPlacesSchema
from models.users_model import Users
from models.user_fav_places_model import UserFavPlaces

from database import db

users_blp = Blueprint("users", __name__, description="operations on users table")

"""
CRUD Methods
"""
@users_blp.route("/users")
class UsersBulkOperations(MethodView):
    """Endpoints that handles operations on the entire users table"""

    @users_blp.arguments(UsersSchema)
    @users_blp.response(200, UsersSchema)
    def post(self, user_data):
        """Create new user"""
        user = Users(**user_data)

        try:
            db.session.add(user)
            db.session.commit()
            
            return user
        except SQLAlchemyError:
            abort(500, message="unable to create new user")
    
    
    @users_blp.response(200, UsersSchema(many=True))
    def get(self):
        """Retrieve all users information"""
        try: 
            users = Users.query.all()
            if len(users) == 0:
                print("no users found")
                raise NoResultFound
            return users

        except NoResultFound:
            abort(404, message="no users found")
        except SQLAlchemyError:
            abort(500, message="unable to retrieve all user")



@users_blp.route("/users/<string:user_id>")
class UsersSpecificEntityOperations(MethodView):
    """Endpoints that handles operations on a specific user"""

    @users_blp.response(200, UsersSchema)
    def get(self, user_id):
        """Read user information"""
        try:
            user_uuid = UUID(user_id)
            target_user = Users.query.get(user_uuid)
            
            if target_user == None:
                raise NoResultFound
            
            return target_user
        
        except NoResultFound:
            abort(404, message="user not found")
        except SQLAlchemyError:
            abort(500, message="unable to get user")



    @users_blp.arguments(UsersSchema)
    @users_blp.response(200, UsersSchema)
    def put(self, new_user_data, user_id):
        """Update user information"""
        try:
            user_uuid = UUID(user_id)
            target_user = Users.query.get(user_uuid)

            if target_user == None:
                raise NoResultFound

            for k, v in new_user_data.items():
                setattr(target_user, k, v)
            
            db.session.commit()

            return target_user

        except NoResultFound:
            abort(404, message="user not found")
        except SQLAlchemyError:
            abort(500, message="unable to update user information")
        


    @users_blp.response(204)
    def delete(self, user_id):
        """Delete user"""
        try:
            user_uuid = UUID(user_id)
            target_user = Users.query.get(user_uuid)
            
            if target_user == None:
                raise NoResultFound

            db.session.delete(target_user)
            db.session.commit()
            
            return

        except NoResultFound:
            return
        except SQLAlchemyError:
            abort(500, message="unable to delete user")


"""
Application logic for users
"""
@users_blp.route("/users/<string:user_id>/favourites")
class FavLocationBulkOperations(MethodView):
    """Endpoints that handles operations on the entire user favourite table"""

    @users_blp.arguments(UserFavPlacesSchema)
    @users_blp.response(200, UserFavPlacesSchema)
    def post(self, favourite_place_data, user_id):
        """Create new user"""
        favourite_place = UserFavPlaces(user_id, **favourite_place_data)

        try:
            db.session.add(favourite_place)
            db.session.commit()
            
            return favourite_place
        except SQLAlchemyError:
            abort(500, message="unable to create register new favourite place")


