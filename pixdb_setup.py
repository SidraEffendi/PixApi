from sqlalchemy.ext.declarative import declarative_base
##### Use in configuration and class code ######
from sqlalchemy.orm import relationship, sessionmaker
##### For creating foriegn key relationship #####
from sqlalchemy import create_engine
from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime, Boolean, ARRAY
from passlib.apps import custom_app_context as pwd_context
##### Used for creating hash codes and verification #####
import random, string
from itsdangerous import(TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
##### For cryptographically signed tokens #####
##### for data and time
import datetime

Base = declarative_base()
#####Instance of the declarative_base Class imported above #####
####### insert at end of the file ######

#date = datetime(int(year), int(month), 1)

secret_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))

class User(Base):
    __tablename__ = 'userr'
    id = Column(Integer, autoincrement=True)
    email_id= Column(String(100),unique =True,primary_key=True)
    username = Column(String(32), index=True)
    admin_code_id = Column(ARRAY(String(32)),unique =True, nullable=True)
    guest_code_id = Column(ARRAY(String(32)),unique =True, nullable=True)
    #password_hash = Column(String(100))

    #def hash_password(self, password):
     #   self.password_hash = pwd_context.encrypt(password)

    #def verify_password(self, password):
     #   return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=6000):
        s = Serializer(secret_key, expires_in = expiration)
        return s.dumps({'id': self.id })

    # We added this serialize function to be able to send JSON objects in a
	# serializable format
    @property
    def serialize(self):

        return {
            'guest_code_id': self.guest_code_id,
        }

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(secret_key)
        try:
            data = s.loads(token)
        except SignatureExpired:
            #Valid Token, but expired
            return None
        except BadSignature:
            #Invalid Token
            return None
        user_email_id = data['email_id']
        return user_email_id

class Events(Base):
    __tablename__ = 'events'

    id = Column(Integer,autoincrement = True)
    code_id = Column(String(20),primary_key=True, nullable=False)
    event_type = Column(String(250), nullable=False)
    album_name = Column(String(250), nullable=False)
    event_date = Column(DateTime, nullable=False)
    event_loc = Column(String(250), nullable=True)
    bucket_link = Column(Text, nullable=False)
    event_email_id = Column(String(100), ForeignKey('userr.email_id', onupdate="CASCADE"))
    userr = relationship(User)

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
            'event_email_id': self.event_email_id,
        }


class Photos(Base):
    __tablename__ = 'photos'

    id = Column(Integer, primary_key=True)
    image_url = Column(Text, nullable=True,unique=True)
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

engine = create_engine('postgresql+psycopg2://postgres:XxxAahSn@2*5@localhost/pixtest')


Base.metadata.create_all(engine)