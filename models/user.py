#!/usr/bin/python3
"""This module defines a class NewUser"""
from models.base_model import BaseModel


class NewUser(BaseModel):
    """This class defines a user by various attributes"""
    new_email = ''
    new_password = ''
    new_first_name = ''
    new_last_name = ''
