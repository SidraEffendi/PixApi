from sqlalchemy.ext.declarative import declarative_base
##### Use in configuration and class code ######
from sqlalchemy.orm import relationship, sessionmaker
##### For creating foriegn key relationship #####
from sqlalchemy import create_engine
from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime
from passlib.apps import custom_app_context as pwd_context
##### for data and time
#import time
import datetime
#from flask_babel import Babel

Base = declarative_base()
#####Instance of the declarative_base Class imported above #####
####### insert at end of the file ######

#date = datetime(int(year), int(month), 1)

class Events(Base):
    __tablename__ = 'events'

    id = Column(Integer)
    code_id = Column(String(20),primary_key=True, nullable=False)
    event_type = Column(String(250), nullable=False)
    album_name = Column(String(250), nullable=False)
    event_date = Column(DateTime, nullable=False)
    event_loc = Column(String(250), nullable=True)
    bucket_link = Column(Text, nullable=False)

    # We added this serialize function to be able to send JSON objects in a
	# serializable format
    @property
    def serialize(self):

        return {
            'id': self.id,
            'code_id': self.code_id,
            'event_type': self.event_type,
            'album_name': self.album_name,
            'event_date': self.event_date,
            'event_loc': self.event_loc,
            'bucket_link': self.bucket_link,
        }


class Photos(Base):
    __tablename__ = 'photos'

    id = Column(Integer, primary_key=True)
    image_url = Column(Text, nullable=True)
    like_count = Column(Integer, nullable=True)
    share_count = Column(Integer, nullable=True)
    photo_code_id = Column(String(20), ForeignKey('events.code_id', onupdate="CASCADE"))
    events = relationship(Events)

# We added this serialize function to be able to send JSON objects in a
# serializable format
    @property
    def serialize(self):

        return {
            'id': self.id,
            'image_url': self.image_url,
            'like_count': self.like_count,
            'share_count': self.share_count,
            'photo_code_id': self.photo_code_id,
        }

engine = create_engine('postgresql+psycopg2://pixliapp:pixli1234@pixtest2.cergfrcu9ucr.us-east-1.rds.amazonaws.com:5432/pixlitest3')


Base.metadata.create_all(engine)