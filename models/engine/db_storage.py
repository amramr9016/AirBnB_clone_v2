"""

"""
# handles the details of how to connect to the database and execute SQL commands
from sqlalchemy import create_engine
from os import getenv
from sqlalchemy.orm import scoped_session, sessionmaker, Session
from sqlalchemy.exc import InvalidRequestError
from models.base_model import NewBaseModel, BaseModel
from models.new_amenity import NewAmenity
from models.new_city import NewCity
from models.new_place import NewPlace
from models.new_review import NewReview
from models.new_state import NewState
from models.new_user import NewUser


class NewDBStorage:
    """
    
    """
    new_engine = None
    new_session = None
    def __init__(self) -> None:
        username = getenv("HBNB_MYSQL_USER")
        password = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        database_name = getenv("HBNB_MYSQL_DB")
        database_url = "mysql+mysqldb://{}:{}@{}/{}".format(username,
                                                            password,
                                                            host,
                                                            database_name)
        self.new_engine = create_engine(database_url, pool_pre_ping=True)

        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.new_engine)

    def all(self, cls=None):
        """
        
        """
        objs_list = []
        if cls:
            if isinstance(cls, str):
                try:
                    cls = globals()[cls]
                except KeyError:
                    pass
            if issubclass(cls, BaseModel):
                objs_list = self.new_session.query(cls).all()
        else:
            for subclass in BaseModel.__subclasses__():
                objs_list.extend(self.new_session.query(subclass).all())
        obj_dict = {}
        for obj in objs_list:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            obj_dict[key] = obj
        return obj_dict
    
    def new(self, obj):
        """
        
        """
        self.new_session.add(obj)
        self.new_session.commit()

    def save(self):
        """"
        
        """
        self.new_session.commit()    

                
    def delete(self, obj=None):
        """
        
        """
        if obj:
            self.new_session.delete(obj)

    def reload(self):
        """
        
        """
        Base.metadata.drop_all(self.new_engine)
        Base.metadata.create_all(self.new_engine)
        session_factory = sessionmaker(bind=self.new_engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.new_session = Session()
