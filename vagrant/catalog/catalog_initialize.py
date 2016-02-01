from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

admin = User(name = "Administrator", email = "jordanalexwatt@hotmail.com")

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
         category = ultimate, user = admin),
    Item(name = "Puck", description = "Official hockey puck!",
         category = hockey, user = admin),
    Item(name = "Basketball", description = "Official basketball!",
         category = basketball, user = admin),
    Item(name = "Snowboard", description = "Official snowboard!",
         category = snowboarding, user = admin),
    Item(name = "Soccer Ball", description = "Official soccer ball!",
         category = soccer, user = admin),
    Item(name = "Football", description = "Official football!",
         category = football),
    Item(name = "Golf Ball", description = "Official golf ball!",
         category = golf, user = admin),
    Item(name = "Lacrosse Ball", description = "Official lacrosse ball!",
         category = lacrosse, user = admin),
    Item(name = "Baseball", description = "Official baseball ball!",
         category = baseball, user = admin),
    Item(name = "Tennis Ball", description = "Official Tennis ball!",
         category = tennis, user = admin)])

session.commit()
