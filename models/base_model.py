#!/usr/bin/python3
"""This module defines a base class for all models in our new_hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, String

Base = declarative_base()


class NewBaseModel:
    """A base class for all new_hbnb models"""

    new_id = Column(String(60), primary_key=True, nullable=False)
    new_created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    new_updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        self.new_id = str(uuid.uuid4())
        self.new_created_at = datetime.utcnow()
        self.new_updated_at = datetime.utcnow()
        if kwargs:
            for new_key, new_value in kwargs.items():
                if new_key == "new_created_at" or new_key == "new_updated_at":
                    new_value = datetime.strptime(new_value, '%Y-%m-%dT%H:%M:%S.%f')
                if hasattr(self, new_key):
                    setattr(self, new_key, new_value)

    def __str__(self):
        """Returns a string representation of the instance"""
        new_cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(new_cls, self.new_id, self.__dict__)

    def save(self):
        """Updates new_updated_at with current time when instance is changed"""
        from models import storage
        self.new_updated_at = datetime.utcnow()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        new_dictionary = {}
        new_dictionary.update(self.__dict__)
        new_dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        new_dictionary['new_created_at'] = self.new_created_at.isoformat()
        new_dictionary['new_updated_at'] = self.new_updated_at.isoformat()
        try:
            del new_dictionary["_sa_instance_state"]
        except KeyError:
            pass
        return new_dictionary

    def delete(self):
        """
        
        """
        from models import storage
        storage.delete(self)
