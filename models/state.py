#!/usr/bin/python3
""" NewState Module for HBNB project """
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship
from models.base_model import NewBaseModel, Base


class NewState(NewBaseModel, Base):
    """ State class """
    __tablename__ = "states"
    new_name = Column(String(128), nullable=False)
    cities = relationship('City', backref='state', cascade='all, delete-orphan')
