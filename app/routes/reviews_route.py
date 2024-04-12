import uuid
import re

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from uuid import UUID as uuid_constructor
from flask import request

from schemas.users_schema import UsersSchema
from schemas.reviews_schema import ReviewsSchema, ReviewsInputSchema, ReviewsSchemaSingle
from models.users_model import Users
from models.reviews import Reviews

from database import db

reviews_blp = Blueprint("reviews", __name__, description="operations on users table")


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

    @reviews_blp.response(201, ReviewsSchema)
    @reviews_blp.arguments(ReviewsInputSchema)
    def post(self, review_data, user_id):
        # review_data = request.get_json()
        """ post a review of the current user"""
        user_id_temp = uuid.UUID(hex=user_id)
        pet_id_temp = review_data["pet_id"]
        place_id_temp = review_data["place_id"]

        review = Reviews(user_id=user_id_temp, pet_id=pet_id_temp, place_id=place_id_temp,
                         score=review_data["score"], content=review_data["content"], title=review_data["title"])

        try:
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
        print(review_data)
        print(review_id)
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
        review_uuid = uuid.UUID(hex=review_id)

        try:
            print(review_uuid.hex)
            review = Reviews.query.get(review_uuid)
            print(review)

            if review is None:
                raise NoResultFound

            if review.user_id == uuid.UUID(hex=user_id):
                db.session.delete(review)
                db.session.commit()

        except NoResultFound:
            abort(404, message="review not found")
        except SQLAlchemyError:
            abort(500, message="unable to delete review")


