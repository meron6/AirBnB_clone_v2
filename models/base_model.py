from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime
from datetime import datetime
import models
import uuid

Base = declarative_base()

class BaseModel:
    """Base class for other classes to inherit from"""
    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Initialize class instance"""
        if kwargs:
            for k, v in kwargs.items():
                if k != '__class__':
                    setattr(self, k, v)
            if 'id' not in kwargs:
                setattr(self, 'id', str(uuid.uuid4()))
            time_format = "%Y-%m-%dT%H:%M:%S.%f"
            if 'created_at' in kwargs:
                setattr(self, 'created_at', datetime.strptime(kwargs['created_at'], time_format))
            if 'updated_at' in kwargs:
                setattr(self, 'updated_at', datetime.strptime(kwargs['updated_at'], time_format))
        else:
            self.id = str(uuid.uuid4())
            self.created_at = self.updated_at = datetime.utcnow()

    def save(self):
        """Updates updated_at with the current datetime"""
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def delete(self):
        """Deletes the instance from storage"""
        models.storage.delete(self)

    def to_dict(self):
        """Returns a dictionary containing all keys/values of the instance"""
        instance_dict = self.__dict__.copy()
        if '_sa_instance_state' in instance_dict:
            del instance_dict['_sa_instance_state']
        instance_dict['created_at'] = self.created_at.isoformat()
        instance_dict['updated_at'] = self.updated_at.isoformat()
        return instance_dict

