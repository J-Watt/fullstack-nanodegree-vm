from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

ultimate = Category(name = "Ultimate")
hockey = Category(name = "Hockey")
basketball = Category(name = "Basketball")
snowboarding = Category(name = "Snowboarding")
soccer = Category(name = "Soccer")
football = Category(name = "Football")
golf = Category(name = "Golf")
lacrosse = Category(name = "Lacrosse")
baseball = Category(name = "Baseball")
tennis = Category(name = "Tennis")

session.add_all([
    Item(name = "Disc", description = "Official 175g game disc!",
         category = ultimate),
    Item(name = "Puck", description = "Official hockey puck!",
         category = hockey),
    Item(name = "Basketball", description = "Official basketball!",
         category = basketball),
    Item(name = "Snowboard", description = "Official snowboard!",
         category = snowboarding),
    Item(name = "Soccer Ball", description = "Official soccer ball!",
         category = soccer),
    Item(name = "Football", description = "Official football!",
         category = football),
    Item(name = "Golf Ball", description = "Official golf ball!",
         category = golf),
    Item(name = "Lacrosse Ball", description = "Official lacrosse ball!",
         category = lacrosse),
    Item(name = "Baseball", description = "Official baseball ball!",
         category = baseball),
    Item(name = "Tennis Ball", description = "Official Tennis ball!",
         category = tennis)])

session.commit()
