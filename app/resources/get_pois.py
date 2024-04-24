# Tutorial: https://www.kaggle.com/code/virajkadam/finding-places-of-interest-in-a-city-using-osm-nx

import osmnx as ox
import geocoder


def get_current_gps_coordinates():
    g = geocoder.ip('me')#this function is used to find the current information using our IP Add
    if g.latlng is not None: #g.latlng tells if the coordiates are found or not
        return g.latlng
    else:
        return None

def get_current_location():
    coordinates = get_current_gps_coordinates()
    if coordinates is not None:
        latitude, longitude = coordinates
        print(f"Your current GPS coordinates are:")
        print(f"Latitude: {latitude}")
        print(f"Longitude: {longitude}")
        return longitude, latitude
    else:
        print("Unable to retrieve your GPS coordinates.")    

def get_pois(center_lat, center_lng):
    # for more tags: https://wiki.openstreetmap.org/wiki/Map_features
    # tags = {'amenity': ['restaurants', 'community_center', 'fountain', 'social_center', 'bench', 'dog_toilet', 'shelter', 'animal_boarding', 'animal_breeding', 'animal_shelter' ],'leisure': ['park', 'dog_park', 'fishing', 'garden', 'marina', 'nature_reserve', 'picnic_table', 'pitch', 'playground', 'swimming_area']}
    tags={'leisure': ['park', 'dog_park']}
    gdf = ox.features.features_from_point(center_point=(center_lat, center_lng), dist=1000, tags=tags)

    # get first 5 rows
    # print(gdf.head())

    # indexs = gdf.index.get_level_values('osmid')
    # print("Osmid",indexs[0])
    
    # first_row = gdf.iloc[0]
    # print("Name",first_row['name'])

    # from shapely.geometry import Polygon
    # polygon_coords = first_row['geometry']
    # # Create a Shapely Polygon object
    # polygon = Polygon(polygon_coords)
    # # Get the centroid of the polygon
    # centroid = polygon.centroid
    # print("Center point: ",centroid.y, centroid.x)
    # print("Category: ",first_row['leisure'])
    # print("City: ",first_row['addr:city'])
    # print("State: ",first_row['addr:state'])
    # print("Country: ",first_row['addr:country'])
    # print("Opening hours: ",first_row['opening_hours'])
    print(f"gdf_len:{len(gdf)}")
    return gdf


from geopy.geocoders import Nominatim
def reverse_geocode(lat, lng):
    geolocator = Nominatim(user_agent="reverse_geocode")
    location = geolocator.reverse((lat, lng), exactly_one=True)
    if location:
        address = location.address
        city = location.raw.get('address').get('city')
        state = location.raw.get('address').get('state')
        country = location.raw.get('address').get('country')
        return city, state, country
    else:
        return None, None, None


def main():
    lng, lat = get_current_location()
    return get_pois(lat, lng)

if __name__ == "__main__":
    main()

