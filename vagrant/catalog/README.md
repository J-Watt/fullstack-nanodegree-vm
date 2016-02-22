Catalog
======================

Udacity  
Full Stack Web Developer Nanodegree: project three  
By Jordan Alexander Watt

Flask based server providing a front end user interface for browsing catalog items, logging in using Facebook or Google+ and creating/editing their own,
along with a back end to read and write information to a database.


Quick Start
-----------

Create a database by running included `database_setup.py`. Run
`catalog_initialize.py` to populate the catalog with some default items. Finally `application.py` will run the server. By default the server can be accessed at http://localhost:8000/


What's Included
---------------

```
catalog
|-- application.py
|-- catalog_initialize.py
|-- client_secrets.json
|-- database_setup.py
|-- fb_client_secrets.json
|-- README.md
|-- static
|   |-- styles.css
|-- templates
|   |-- catbar.html
|   |--  category.html
|   |--  deleteitem.html
|   |--  edititem.html
|   |--  footer.html
|   |--  header.html
|   |--  index.html
|   |--  item.html
|   |--  itembar.html
|   |--  login.html
|   |--  main.html
|   |--  newitem.html
|   |--  publicitem.html
|   |--  useritems.html
```



Usage
-----

#####Setup:
Create a database by running included `database_setup.py`. Run
`catalog_initialize.py` to populate the catalog with some default items. Finally `application.py` will run the server. By default the server can be accessed at http://localhost:8000/

#####Catalog:
Users can browse items saved in the database through the user interface. Should they log in using Facebook or Google+ authentication they gain the ability to add items of their own. Users may also edit and delete their own items.


Features
--------

Supported features
* OAuth2
  * Secure Facebook login and signout
  * Secure Google+ login and signout
  * If registered with same email both login options will be recognized as one user
* Item Images
  * Image urls may be included and will be resized to fit
* Users
  * Creator of each item is visible only to logged in users
  * Users can see a list of their own creations
  * Message flashing to alert users after performing an action
* Simple URLs
  * Easily recognizable urls
  * Multiple items with the same name by including IDs
  * When url for item does not include ID will attempt to find the item without the ID
* APIs
  * ATOM feed
  * JSON endpoint for items, categories, or entire catalog


Bug Reports
-----------

* No currently known bugs.

Please report any bugs to JordanAlexWatt@hotmail.com


Versioning
----------

Catalog 1.0



Credits
-------

Catalog written by Jordan Alexander Watt (JAW)
following udacity course lectures. - JordanAlexWatt@hotmail.com

The python scripts templates and guides created by
Udacity and can be found [here]
(https://github.com/udacity)

Credit for all images linked to in the default examples goes to their original creators.

 
#####Supporting Resources  

[Udacity](http://www.udacity.com)

[Python](https://www.python.org/)

[Flask](http://flask.pocoo.org/)

[SQLAlchemy](http://www.sqlalchemy.org/)

[Facebook](https://www.facebook.com/)

[Google+](https://plus.google.com)




***

*Last edited February 21 2016*