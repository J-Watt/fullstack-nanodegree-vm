# ------------------------------------------------------------------------------
# Name:         catalog_initialize
# Purpose:      Populate catalog database with default categories & items
#
# Author:       Jordan Alexander Watt
#
# Modified:     5-2-2016
# Created:      12-1-2015
# ------------------------------------------------------------------------------

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User

# Connect to Database and create database session
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Default User
admin = User(name="Administrator", email="jordanalexwatt@hotmail.com")

# Default Categories
ultimate = Category(name="Ultimate")
hockey = Category(name="Hockey")
basketball = Category(name="Basketball")
snowboarding = Category(name="Snowboarding")
soccer = Category(name="Soccer")
football = Category(name="Football")
golf = Category(name="Golf")
lacrosse = Category(name="Lacrosse")
baseball = Category(name="Baseball")
tennis = Category(name="Tennis")

# Default starting Items
session.add_all([
    Item(name="Disc", description="Official 175g game disc!"
         "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam a "
         "risus sed nunc sagittis imperdiet. Mauris aliquet nunc et dolor "
         "vehicula, id facilisis ipsum bibendum. Nam suscipit, libero tincidun"
         " feugiat fermentum, eros ex luctus elit, eu porta nisl mauris ac "
         "nibh. Donec risus enim, tempor eget maximus quis, lobortis eu null. "
         "Fusce eleifend ut elit non scelerisque. Sed dapibus ornare ligula "
         "quis facilisis. Nam ullamcorper volutpat augue, ac venenatis nisl "
         "facilisis quis. Vestibulum velit augue, egestas at elementum vitae, "
         "convallis vel turpis. Sed tristique mi ut nisi viverra placerat. "
         "Donec vel enim tincidunt, iaculis purus eget, commodo mi. Vestibulm "
         "cursus dictum massa, sed tempor magna dapibus consequat. Praesent "
         "quis sem quis nunc consectetur dignissim. Vestibulum pellentesque "
         "ultrices suscipit. Duis vitae turpis non erat faucibus dapibus.",
         image="http://www.discace.com/frisbees/ultimate-frisbee-discs/frisb"
               "ee-discs-white.fw.png",
         category=ultimate, user=admin),
    Item(name="Gloves", description="Friction ultimate gloves!"
         "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus "
         "quis iaculis arcu, et rutrum nisi. Curabitur congue turpis dui, sed "
         "pretium tellus semper eu. Sed est massa, faucibus non leo non, "
         "consectetur lacinia est. Nullam eget diam quis dolor tincidunt luctu"
         " et vitae est. Nulla ac justo eu nisl mattis ornare non sed ligula. "
         "Fusce blandit sapien porttitor fermentum sodales. Nulla eget libero "
         "leo.",
         image="http://cdn.discstore.com/media/catalog/product/cache/1/image"
               "/9df78eab33525d08d6e5fb8d27136e95/f/r/friction_cu_"
               "spread_2.jpg",
         category=ultimate, user=admin),
    Item(name="Bag", description="Heckler ultimate bag!"
         "Lorem ipsum dolor sit amet, consectetur adipiscing elit. In dictum "
         "neque ac arcu fringilla lobortis. Vivamus neque sapien, facilisis "
         "tincidunt velit in, suscipit elementum felis. Maecenas sit amet "
         "sagittis nulla.",
         image="http://skydmagazine.com/wp-content/uploads/2014/06/"
               "heckler-bag-1200x600.jpg",
         category=ultimate, user=admin),
    Item(name="Puck", description="Official hockey puck!"
         "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus "
         "quis iaculis arcu, et rutrum nisi. Curabitur congue turpis dui, sed "
         "pretium tellus semper eu. Sed est massa, faucibus non leo non, "
         "consectetur lacinia est. Nullam eget diam quis dolor tincidunt luctu"
         " et vitae est. Nulla ac justo eu nisl mattis ornare non sed ligula. "
         "Fusce blandit sapien porttitor fermentum sodales. Nulla eget libero "
         "leo.",
         image="http://preview.turbosquid.com/Preview/2014/05/21__12_54_12/"
               "IceHockeyPuck_02.jpg48963c51-3cca-48e4-bce6-9a1579b5fafa"
               "Original.jpg",
         category=hockey, user=admin),
    Item(name="Stick", description="hockey stick!"
         "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam a "
         "risus sed nunc sagittis imperdiet. Mauris aliquet nunc et dolor "
         "vehicula, id facilisis ipsum bibendum. Nam suscipit, libero tincidun"
         " feugiat fermentum, eros ex luctus elit, eu porta nisl mauris ac "
         "nibh. Donec risus enim, tempor eget maximus quis, lobortis eu null. "
         "Fusce eleifend ut elit non scelerisque. Sed dapibus ornare ligula "
         "quis facilisis. Nam ullamcorper volutpat augue, ac venenatis nisl "
         "facilisis quis. Vestibulum velit augue, egestas at elementum vitae, "
         "convallis vel turpis. Sed tristique mi ut nisi viverra placerat. "
         "Donec vel enim tincidunt, iaculis purus eget, commodo mi. Vestibulu "
         "cursus dictum massa, sed tempor magna dapibus consequat. Praesent "
         "quis sem quis nunc consectetur dignissim. Vestibulum pellentesque "
         "ultrices suscipit. Duis vitae turpis non erat faucibus dapibus.",
         image="https://mmitii.files.wordpress.com/2013/10/hockey-stick.jpg",
         category=hockey, user=admin),
    Item(name="Bag", description="Official hockey bag!"
         "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus "
         "quis iaculis arcu, et rutrum nisi. Curabitur congue turpis dui, sed "
         "pretium tellus semper eu. Sed est massa, faucibus non leo non, "
         "consectetur lacinia est. Nullam eget diam quis dolor tincidunt luctu"
         " et vitae est. Nulla ac justo eu nisl mattis ornare non sed ligula. "
         "Fusce blandit sapien porttitor fermentum sodales. Nulla eget libero "
         "leo.",
         image="http://www.milesaheadnetwork.com/images/products/"
               "20090624__hockey_bag.jpg",
         category=hockey, user=admin),
    Item(name="Basketball", description="Official basketball!"
         "Lorem ipsum dolor sit amet, consectetur adipiscing elit. In dictum "
         "neque ac arcu fringilla lobortis. Vivamus neque sapien, facilisis "
         "tincidunt velit in, suscipit elementum felis. Maecenas sit amet "
         "sagittis nulla.",
         image="https://upload.wikimedia.org/wikipedia/commons/7/7a/"
               "Basketball.png",
         category=basketball, user=admin),
    Item(name="Snowboard", description="Official snowboard!"
         "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam a "
         "risus sed nunc sagittis imperdiet. Mauris aliquet nunc et dolor "
         "vehicula, id facilisis ipsum bibendum. Nam suscipit, libero tincidun"
         " feugiat fermentum, eros ex luctus elit, eu porta nisl mauris ac "
         "nibh. Donec risus enim, tempor eget maximus quis, lobortis eu null. "
         "Fusce eleifend ut elit non scelerisque. Sed dapibus ornare ligula "
         "quis facilisis. Nam ullamcorper volutpat augue, ac venenatis nisl "
         "facilisis quis. Vestibulum velit augue, egestas at elementum vitae, "
         "convallis vel turpis. Sed tristique mi ut nisi viverra placerat. "
         "Donec vel enim tincidunt, iaculis purus eget, commodo mi. Vestibulu "
         "cursus dictum massa, sed tempor magna dapibus consequat. Praesent "
         "quis sem quis nunc consectetur dignissim. Vestibulum pellentesque "
         "ultrices suscipit. Duis vitae turpis non erat faucibus dapibus.",
         image="http://skicarriage.co.uk/UserFiles/Image/White-Snowboard"
               "-With-Bindings.jpg",
         category=snowboarding, user=admin),
    Item(name="Soccer Ball", description="Official soccer ball!"
         "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus "
         "quis iaculis arcu, et rutrum nisi. Curabitur congue turpis dui, sed "
         "pretium tellus semper eu. Sed est massa, faucibus non leo non, "
         "consectetur lacinia est. Nullam eget diam quis dolor tincidunt luctu"
         " et vitae est. Nulla ac justo eu nisl mattis ornare non sed ligula. "
         "Fusce blandit sapien porttitor fermentum sodales. Nulla eget libero "
         "leo.",
         image="http://kindersay.com/files/images/soccer-ball.png",
         category=soccer, user=admin),
    Item(name="Football", description="Official football!"
         "Lorem ipsum dolor sit amet, consectetur adipiscing elit. In dictum "
         "neque ac arcu fringilla lobortis. Vivamus neque sapien, facilisis "
         "tincidunt velit in, suscipit elementum felis. Maecenas sit amet "
         "sagittis nulla.",
         image="http://www.clipartbest.com/cliparts/4T9/onb/4T9onb87c.jpeg",
         category=football, user=admin),
    Item(name="Golf Ball", description="Official golf ball!"
         "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam a "
         "risus sed nunc sagittis imperdiet. Mauris aliquet nunc et dolor "
         "vehicula, id facilisis ipsum bibendum. Nam suscipit, libero tincidun"
         " feugiat fermentum, eros ex luctus elit, eu porta nisl mauris ac "
         "nibh. Donec risus enim, tempor eget maximus quis, lobortis eu null. "
         "Fusce eleifend ut elit non scelerisque. Sed dapibus ornare ligula "
         "quis facilisis. Nam ullamcorper volutpat augue, ac venenatis nisl "
         "facilisis quis. Vestibulum velit augue, egestas at elementum vitae, "
         "convallis vel turpis. Sed tristique mi ut nisi viverra placerat. "
         "Donec vel enim tincidunt, iaculis purus eget, commodo mi. Vestibulu "
         "cursus dictum massa, sed tempor magna dapibus consequat. Praesent "
         "quis sem quis nunc consectetur dignissim. Vestibulum pellentesque "
         "ultrices suscipit. Duis vitae turpis non erat faucibus dapibus.",
         image="http://blog.scorgolf.com/wp-content/uploads/2012/03/"
               "golf-ball.jpg",
         category=golf, user=admin),
    Item(name="Gloves", description="Golfing gloves!"
         "Lorem ipsum dolor sit amet, consectetur adipiscing elit. In dictum "
         "neque ac arcu fringilla lobortis. Vivamus neque sapien, facilisis "
         "tincidunt velit in, suscipit elementum felis. Maecenas sit amet "
         "sagittis nulla.",
         image="http://yousansports.com/admincp/sdata/itmimgs/itm_s_155.jpg",
         category=golf, user=admin),
    Item(name="Lacrosse Ball", description="Official lacrosse ball!"
         "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus "
         "quis iaculis arcu, et rutrum nisi. Curabitur congue turpis dui, sed "
         "pretium tellus semper eu. Sed est massa, faucibus non leo non, "
         "consectetur lacinia est. Nullam eget diam quis dolor tincidunt luctu"
         " et vitae est. Nulla ac justo eu nisl mattis ornare non sed ligula. "
         "Fusce blandit sapien porttitor fermentum sodales. Nulla eget libero "
         "leo.",
         image="http://feeds2.yourstorewizards.com/1749/images/300x300/"
               "stx-unofficial-play-lacrosse-ball.jpg",
         category=lacrosse, user=admin),
    Item(name="Baseball", description="Official baseball ball!"
         "Lorem ipsum dolor sit amet, consectetur adipiscing elit. In dictum "
         "neque ac arcu fringilla lobortis. Vivamus neque sapien, facilisis "
         "tincidunt velit in, suscipit elementum felis. Maecenas sit amet "
         "sagittis nulla.",
         image="http://assets.imgstg.com/assets/console/finderproduct/"
               "images/Club%20Baseball.jpg",
         category=baseball, user=admin),
    Item(name="Baseball bat", description="Official baseball bat!"
         "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus "
         "quis iaculis arcu, et rutrum nisi. Curabitur congue turpis dui, sed "
         "pretium tellus semper eu. Sed est massa, faucibus non leo non, "
         "consectetur lacinia est. Nullam eget diam quis dolor tincidunt luctu"
         " et vitae est. Nulla ac justo eu nisl mattis ornare non sed ligula. "
         "Fusce blandit sapien porttitor fermentum sodales. Nulla eget libero "
         "leo.",
         image="http://i.ebayimg.com/00/s/NjA3WDc5MA==/z/w4YAAMXQDnpTX05p/"
               "$_32.JPG?set_id=880000500F",
         category=baseball, user=admin),
    Item(name="Tennis Ball", description="Official Tennis ball!"
         "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam a "
         "risus sed nunc sagittis imperdiet. Mauris aliquet nunc et dolor "
         "vehicula, id facilisis ipsum bibendum. Nam suscipit, libero tincidun"
         " feugiat fermentum, eros ex luctus elit, eu porta nisl mauris ac "
         "nibh. Donec risus enim, tempor eget maximus quis, lobortis eu null. "
         "Fusce eleifend ut elit non scelerisque. Sed dapibus ornare ligula "
         "quis facilisis. Nam ullamcorper volutpat augue, ac venenatis nisl "
         "facilisis quis. Vestibulum velit augue, egestas at elementum vitae, "
         "convallis vel turpis. Sed tristique mi ut nisi viverra placerat. "
         "Donec vel enim tincidunt, iaculis purus eget, commodo mi. Vestibulu "
         "cursus dictum massa, sed tempor magna dapibus consequat. Praesent "
         "quis sem quis nunc consectetur dignissim. Vestibulum pellentesque "
         "ultrices suscipit. Duis vitae turpis non erat faucibus dapibus.",
         image="http://media.coreperformance.com/images/411*308/relieve-"
               "soreness-with-just-a-tennis-ball.jpg",
         category=tennis, user=admin),
    Item(name="Tennis racquet", description="Tennis racquet!"
         "Lorem ipsum dolor sit amet, consectetur adipiscing elit. In dictum "
         "neque ac arcu fringilla lobortis. Vivamus neque sapien, facilisis "
         "tincidunt velit in, suscipit elementum felis. Maecenas sit amet "
         "sagittis nulla.",
         image="http://ecx.images-amazon.com/images/I/31RjRcg6oxL.jpg",
         category=tennis, user=admin)])

# Commit and save changes to Database
session.commit()
