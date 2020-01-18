from flask_sqlalchemy import SQLAlchemy

# SQLAlchemy object essentially links to our flask app and 
# looks at all of the objects that we tell it to, and maps those objects to rows in a database
db = SQLAlchemy()