#!/usr/bin/python3
"""
Instantiates a new storage object.

-> If the environmental variable 'NEW_TYPE_STORAGE' is set to 'db',
   instantiates a database storage engine (DBStorage).
-> Otherwise, instantiates a file storage engine (FileStorage).
"""
from os import getenv


if getenv("NEW_TYPE_STORAGE") == "db":
    from models.engine.db_storage import DBStorage
    new_storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    new_storage = FileStorage()
new_storage.reload()
