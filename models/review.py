#!/usr/bin/python3
""" NewReview module for the HBNB project """
from models.base_model import BaseModel


class NewReview(BaseModel):
    """ Review class to store review information """
    new_place_id = ""
    new_user_id = ""
    new_text = ""
