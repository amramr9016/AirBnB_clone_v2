#!/usr/bin/python3
""" NewPlace Module for HBNB project """
from models.base_model import BaseModel


class NewPlace(BaseModel):
    """ A place to stay """
    new_city_id = ""
    new_user_id = ""
    new_name = ""
    new_description = ""
    new_number_rooms = 0
    new_number_bathrooms = 0
    new_max_guest = 0
    new_price_by_night = 0
    new_latitude = 0.0
    new_longitude = 0.0
    new_amenity_ids = []
