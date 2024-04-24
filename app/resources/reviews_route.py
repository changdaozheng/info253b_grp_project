import uuid
import re

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, ArgumentError, InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import joinedload
from uuid import UUID 
from flask import request

from schemas.users_schema import UsersSchema
from schemas.reviews_schema import ReviewsSchema, ReviewsInputSchema, ReviewsSchemaSingle

from models.users_model import Users
from models.reviews_model import Reviews
from models.pets_model import Pets
from models.places_model import Places

from database import db

reviews_blp = Blueprint("reviews", __name__, description="operations on users table")

"""
Helper Functions 
"""

def uuid_condition_check(target_number, source_to_check):
    result = False
    if source_to_check is None:
        result = True
    else:
        if target_number == uuid.UUID(hex=source_to_check):
            result = True
    return result


def int_condition_check(target_number, source_to_check):
    result = False
    if source_to_check is None:
        result = True
    else:
        if target_number == source_to_check:
            result = True
    return result

def str_condition_check(target, source_to_check):
    result = False
    if source_to_check is None:
        result = True
    else:
        if re.search(source_to_check, target):
            result = True
    return result


def is_valid_user(user_id):
    return Users.query.get(user_id) != None

def is_valid_pet(pet_id):
    return Pets.query.get(pet_id) != None

def is_valid_place(place_id):
    return Places.query.get(place_id) != None


"""
CRUD
"""
@reviews_blp.route("/reviews")
class BulkOperations(MethodView):
    """ Endpoints that handle multiple reviews"""

    @reviews_blp.response(200, ReviewsSchema(many=True))
    def get(self):
        """ get all the reviews under the certain condition
            TODO change place_id to place_category, search based on place_category
        """
        user_id = request.args.get('user_id')
        place_id = request.args.get('place_id')
        pet_id = request.args.get('pet_id')
        score = request.args.get('score')
        content = request.args.get('content')
        title = request.args.get('title')

        try:
            reviews = Reviews.query.all()

            if len(reviews) == 0:
                raise NoResultFound
            result = []

            for review in reviews:
                if (uuid_condition_check(review.user_id, user_id) and
                    uuid_condition_check(review.pet_id, pet_id) and
                    int_condition_check(review.score, score) and
                    str_condition_check(review.content, content) and
                    uuid_condition_check(review.place_id, place_id) and
                    str_condition_check(review.title, title)):
                    result.append(review)
            return result

        except NoResultFound:
            abort(404, message="no reviews found")
        except SQLAlchemyError:
            abort(500, message="unable to retrieve reviews")

@reviews_blp.route("/reviews/<string:user_id>")
class SpecificEntityOperations(MethodView):
    """ Endpoints that handle specified reviews"""

    @reviews_blp.arguments(ReviewsInputSchema)
    @reviews_blp.response(201, ReviewsSchema)
    def post(self, review_data, user_id):
        """ post a review of the current user"""
        
        review_data = request.get_json()
        user_id_temp = UUID(user_id)
        pet_id_temp = UUID(review_data["pet_id"])
        place_id_temp = UUID(review_data["place_id"])

        if not is_valid_user(user_id_temp):
            abort(400, message="user not found")
        elif not is_valid_pet(pet_id_temp):
            abort(400, message="pet not found")
        elif not is_valid_place(place_id_temp):
            abort(400, message="place not found")

        review = Reviews(user_id=user_id_temp, pet_id=pet_id_temp, place_id=place_id_temp,
                         score=review_data["score"], content=review_data["content"], title=review_data["title"])
        
        try:
            review = Reviews(user_id=user_id_temp, pet_id=pet_id_temp, place_id=place_id_temp, score=review_data["score"], content=review_data["content"], title=review_data["title"])
            db.session.add(review)
            db.session.commit()

            return review

        except SQLAlchemyError as e:
            abort(500, message="unable to post a review" + str(e))
   


@reviews_blp.route("/reviews/<string:user_id>/<string:review_id>")
class SpecificEntityOperations(MethodView):

    @reviews_blp.response(201, ReviewsSchema)
    @reviews_blp.arguments(ReviewsInputSchema)
    def put(self, review_data, user_id, review_id):
        """edit a review"""
        # review_data = request.get_json()
        try:
            review_uuid = uuid.UUID(hex=review_id)
            # print(review_uuid.hex)
            review = Reviews.query.get(review_uuid)
            # print(review.user_id)
            # print(user_id)

            if review is None:
                raise NoResultFound
            if review.user_id == uuid.UUID(hex=user_id):
                review.pet_id = review_data["pet_id"]
                review.place_id = review_data["place_id"]
                review.score = review_data["score"]
                review.content = review_data["content"]
                review.title = review_data["title"]
                db.session.commit()
            else:
                abort(403, message="unauthorized to make the change")
            return review

        except NoResultFound:
            abort(404, message="review not found")
        except SQLAlchemyError as e:
            abort(500, message="unable to update this review" + str(e))

    @reviews_blp.response(204)
    def delete(self, user_id, review_id):
        """delete a review"""
        review_uuid = UUID(review_id)

        try:
            review = Reviews.query.get(review_uuid)

            if review is None:
                raise NoResultFound

            if review.user_id == review_uuid:
                db.session.delete(review)
                db.session.commit()

        except NoResultFound:
            abort(404, message="review not found")
        except SQLAlchemyError:
            abort(500, message="unable to delete review")


"""
Search
"""

@reviews_blp.route("/reviews/petbreed/<string:breed>")
class SearchByBreed(MethodView):

    @reviews_blp.response(200, ReviewsSchema(many=True))
    def get(self, breed):
        """Read user information"""
        reviews = Reviews.query.join(Pets).filter(Pets.breed == breed).all()

        return reviews



