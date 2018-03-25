import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Text, Float, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, backref
from sqlalchemy import create_engine
from datetime import datetime

# Create databse
Base = declarative_base()
class Items(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key = True)	
    name = Column(String(250), nullable = False)
    description = Column(Text, nullable = False)
    start_time = Column(DateTime, default = datetime.now(), nullable = True)
    users = relationship('User', secondary = 'items_user')

class User(Base):
	__tablename__ = 'user'

	id = Column(Integer, primary_key = True)
	username = Column(String(150), nullable = False)
	password = Column(String(250), nullable = False)
	itemss = relationship('Items', secondary = 'items_user')

class Bid(Base):
	__tablename__ = 'bid'

	id = Column(Integer, primary_key = True)
	price = Column(Float, nullable = False)
	items_id = Column(Integer, ForeignKey(Items.id))
	items = relationship(Items, backref = backref('items_bid', uselist = True))
	user_id = Column(Integer, ForeignKey(User.id))
	user = relationship(User, backref = backref('user_bid', uselist = True))

class ItemsUser(Base):
	__tablename__ = 'items_user'

	items_id = Column(Integer, ForeignKey(Items.id), primary_key = True)
	user_id = Column(Integer, ForeignKey(User.id), primary_key = True)
		
engine = create_engine('sqlite:///auction.db')
session = sessionmaker()
session.configure(bind = engine)
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

s = session()

# add 3 Users
john = User(username = 'John', password = '1')
s.add(john)
meit = User(username = 'Meitneri', password = '2')
s.add(meit)
diven = User(username = 'DivenKo', password = '3')
s.add(diven)

# add Item Baseball
baseball_items = Items(name = 'Baseball', description = 'good')
baseball_items.users.append(john)
baseball_items.users.append(meit)
baseball_items.users.append(diven)
s.add(baseball_items)

# add Bid
john_bid = Bid(price = '4', items = baseball_items, user = john)
s.add(john_bid)
# add more bid by other user
meit_bid1 = Bid(price = '5', items = baseball_items, user = meit)
s.add(meit_bid1)
meit_bid2 = Bid(price = '6', items = baseball_items, user = meit)
s.add(meit_bid2)
meit_bid3 = Bid(price = '7.4', items = baseball_items, user = meit)
s.add(meit_bid3)

diven_bid1 = Bid(price = '4', items = baseball_items, user = diven)
s.add(diven_bid1)
diven_bid2 = Bid(price = '7.4', items = baseball_items, user = diven)
s.add(diven_bid2)

# Query
it = s.query(Items).first()
print 'Items are being auctioned is: ' + it.name + "\n"

us = s.query(Items).filter(Items.name == it.name).first()
for x in range(len(it.users)):
	print "User: " + us.users[x].username + " is bidding at prices "
	b = s.query(User).filter(User.username == us.users[x].username).first()
	for y in range(len(b.user_bid)):
		print "\t" + b.user_bid[y].price
	print

max_bid_value = s.query(func.max(Bid.price)).filter(Bid.items_id == it.id).scalar()
print "Highest bid = " + str(max_bid_value) +" by Users: "
max_bid = s.query(Bid).filter(Bid.price == max_bid_value).all() 
for z in range(len(max_bid)):
	print "\t" + s.query(User).filter(User.id == max_bid[z].user_id).first().username

s.commit()
s.close()