from flask.views import MethodView
from flask_smorest import Blueprint, abort

from schemas.places_schema import PlaceSchema, PlaceUpdateSchema
from models.places_model import PlaceModel

from database import db
from sqlalchemy.exc import SQLAlchemyError

from .get_pois import main, reverse_geocode
from shapely.geometry import Polygon
import pandas as pd


places_blp = Blueprint("places", __name__, description="Operations on places")


@places_blp.route("/places")
class PlacesAPI(MethodView):
    @places_blp.response(200, PlaceSchema(many=True))
    def get(self):
        """Get all places"""
        print("GET /places")
        places = PlaceModel.query.all()
        return places
    



    # @places_blp.arguments(PlaceSchema)
    @places_blp.response(201, PlaceSchema(many=True))
    def post(self):
        """Create a new place"""
        print("POST /places")
        places = main()
        if not places.empty: ## when GeoDataFrame is empty
            for i in range(len(places)):
                osmid = int(places.index.get_level_values('osmid')[i])
                print('osmid:', osmid)
                row = places.iloc[i]
                corrds = row['geometry']
                if corrds.geom_type == 'MultiPolygon':
                    centroid = corrds.centroid
                else:
                    # Create a Shapely Polygon object
                    polygon = Polygon(corrds)
                    # Get the centroid of the polygon
                    centroid = polygon.centroid
                # lat, lng = centroid.y, centroid.x
                # city, state, country = reverse_geocode(lat, lng)
                place_data = {
                    'osmid': osmid,
                    'name': row['name'],
                    'lat': centroid.y,
                    'lng': centroid.x,
                    'category': row['leisure'],
                    'city': row['addr:city'] if not pd.isna(row['addr:city']) else None,
                    'state': row['addr:state'] if not pd.isna(row['addr:state']) else None,
                    'country': row['addr:country'] if not pd.isna(row['addr:country']) else None,
                }
                place = PlaceModel(**place_data)
                # print('Place:', place_data)
                try: 
                    db.session.add(place)
                    db.session.commit()
                    # print(f"Inserting place {place_data['name']}")
                except SQLAlchemyError:
                    abort(400, message="An error occurred while inserting the place.")
        places = PlaceModel.query.all()
        places_data = PlaceSchema(many=True).dump(places)
        print('---->>>>>>', places_data)
        return places_data

@places_blp.route("/place/<int:place_id>") 
class PlaceAPI(MethodView):
    @places_blp.response(200, PlaceSchema)
    def get(self, place_id):
        """Get place by id"""
        try:
            print(f"GET /place/{place_id}")
            place = PlaceModel.query.get_or_404(place_id)
            return place
        except KeyError:
            abort(400, message="Place not found.")

    @places_blp.arguments(PlaceUpdateSchema)
    @places_blp.response(200, PlaceSchema)
    def put(self, place_data, place_id):
        """Update place by id"""
        place = PlaceModel.query.get(place_id)
        if place:
            place.osmid = place_data["osmid"]
            place.name = place_data["name"]
            place.lat = place_data["lat"]
            place.lng = place_data["lng"]
            place.city = place_data["city"]
            place.state = place_data["state"]
            place.country = place_data["country"]
            place.category = place_data["category"]
        else:
            place = PlaceModel(id=place_id, **place_data)
        
        db.session.add(place)
        db.session.commit()
        
        return place

    def delete(self, place_id):
        """Delete place by id"""
        place = PlaceModel.query.get(place_id)
        if place:
            db.session.delete(place)
            db.session.commit()
            return place
        else:
            abort(400, message="Place not found.")
