from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pixdb_setup import Photos, Events, User, Base
#from passlib.apps import custom_app_context as pwd_context

engine = create_engine('postgresql+psycopg2://postgres:XxxAahSn@2*5@localhost/pixtest')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

user1 =User(email_id = "sidra@gmail.com", username = "Sid Effendi", admin_code_id = "{ASP1,abcd0}", guest_code_id = "{abdc01}")
session.add(user1)
session.commit()

Item1 = Events(code_id = "ASP1", event_type = "Party", album_name = "Mashup",event_date="2016-11-10", event_loc="delhi",
	bucket_link="http://hjasdjsjdhjwd232349327r9347r93789378&Veggie Burger", event_email_id = "sidra@gmail.com")

session.add(Item1)
session.commit()

photo1 = Photos(image_url = "Partysdkjnvsjdvjksdvnjsd//", like_count = 2, share_count=3, photo_code_id = Item1.code_id)

session.add(photo1)
session.commit()

Item2 = Events(code_id = "abdc0", event_type = "Party", album_name = "Mashup",event_date="2016-11-10", event_loc="delhi",
	bucket_link="http://hjasdjsjdhjwd232349327r9347r93789378&Veggie Burger", event_email_id = "sidra@gmail.com")

session.add(Item2)
session.commit()

photo1 = Photos( photo_code_id = Item2.code_id)

session.add(photo1)
session.commit()

