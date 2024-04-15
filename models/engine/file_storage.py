#!/usr/bin/python3
"""This module defines a class to manage new_file storage for hbnb clone"""
import json
from models.new_base_model import NewBaseModel
from models.new_user import NewUser
from models.new_place import NewPlace
from models.new_state import NewState
from models.new_city import NewCity
from models.new_amenity import NewAmenity
from models.new_review import NewReview


class NewFileStorage:
    """This class manages storage of hbnb models in JSON format"""
    new_file_path = 'file.json'
    new_objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage.

        Args:
            cls (class, optional): If specified, filters the result to include
                only objects of the specified class.

        Returns:
            dict: A dictionary containing objects in storage.
        """
        if cls:
            if isinstance(cls, str):
                cls = globals().get(cls)
            if cls and issubclass(cls, NewBaseModel):
                cls_dict = {k: v for k,
                            v in self.new_objects.items() if isinstance(v, cls)}
                return cls_dict
        return NewFileStorage.new_objects

    def new(self, obj):
        """Adds new object to storage dictionary"""
        self.all().update({obj.to_dict()['__class__'] + '.' + obj.id: obj})

    def save(self):
        """Saves storage dictionary to file"""
        with open(NewFileStorage.new_file_path, 'w') as f:
            temp = {}
            temp.update(NewFileStorage.new_objects)
            for key, val in temp.items():
                temp[key] = val.to_dict()
            json.dump(temp, f)

    def reload(self):
        """Loads storage dictionary from file."""
        classes = {
                    'NewBaseModel': NewBaseModel, 'NewUser': NewUser, 'NewPlace': NewPlace,
                    'NewState': NewState, 'NewCity': NewCity, 'NewAmenity': NewAmenity,
                    'NewReview': NewReview
                  }
        try:
            temp = {}
            with open(NewFileStorage.new_file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                        self.all()[key] = classes[val['__class__']](**val)
        except FileNotFoundError:
            pass
        except json.decoder.JSONDecodeError:
            pass

    def delete(self, obj=None):
        """
         Delete obj from new_objects if it’s inside - if obj is equal to None,
           the method should not do anything
        """
        if obj is None:
            return
        obj_to_del = f"{obj.__class__.__name__}.{obj.id}"

        try:
            del NewFileStorage.new_objects[obj_to_del]
        except AttributeError:
            pass
        except KeyboardInterrupt:
            pass
