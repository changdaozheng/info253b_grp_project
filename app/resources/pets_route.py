from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from uuid import UUID 

from schemas.pets_schema import PetsSchema
from models.pets_model import Pets

from database import db

pets_blp = Blueprint("pets", __name__, description="operations on pets table")

"""
CRUD
"""

@pets_blp.route("/pets")
class BulkOperations(MethodView):
    """Endpoints that handles operations on the entire pets table"""

    @pets_blp.arguments(PetsSchema)
    @pets_blp.response(200, PetsSchema)
    def post(self, pet_data):
        """Create new pet"""
        pet = Pets(**pet_data)

        try:
            db.session.add(pet)
            db.session.commit()
            
            return pet
        except SQLAlchemyError:
            abort(500, message="unable to create new pet")
    
    
    @pets_blp.response(200, PetsSchema(many=True))
    def get(self):
        """Retrieve all Pets information"""
        try: 
            pets = Pets.query.all()
            if len(pets) == 0:
                raise NoResultFound
            return pets

        except NoResultFound:
            abort(404, message="no Pets found")
        except SQLAlchemyError:
            abort(500, message="unable to retrieve all pet")



@pets_blp.route("/pets/<string:pet_id>")
class SpecificEntityOperations(MethodView):
    """Endpoints that handles operations on a specific pet"""

    @pets_blp.response(200, PetsSchema)
    def get(self, pet_id):
        """Read pet information"""
        try:
            pet_uuid = UUID(pet_id)
            target_pet = Pets.query.get(pet_uuid)
            
            if target_pet == None:
                raise NoResultFound
            
            return target_pet
        
        except NoResultFound:
            abort(404, message="pet not found")
        except SQLAlchemyError:
            abort(500, message="unable to get pet")



    @pets_blp.arguments(PetsSchema)
    @pets_blp.response(200, PetsSchema)
    def put(self, new_pet_data, pet_id):
        """Update pet information"""
        try:
            pet_uuid = UUID(pet_id)
            target_pet = Pets.query.get(pet_uuid)

            if target_pet == None:
                raise NoResultFound

            for k, v in new_pet_data.items():
                setattr(target_pet, k, v)
            
            db.session.commit()

            return target_pet

        except NoResultFound:
            abort(404, message="pet not found")
        except SQLAlchemyError:
            abort(500, message="unable to update pet information")
        


    @pets_blp.response(204)
    def delete(self, pet_id):
        """Delete pet"""
        try:
            pet_uuid = UUID(pet_id)
            target_pet = Pets.query.get(pet_uuid)
            
            if target_pet == None:
                raise NoResultFound

            db.session.delete(target_pet)
            db.session.commit()
            
            return

        except NoResultFound:
            return
        except SQLAlchemyError:
            abort(500, message="unable to delete pet")
