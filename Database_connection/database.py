'''
SQLAlchemy is an ORM(object Relational Mapping), which our fastAPI is going to be using, to create a database, be able 
to create a connection to the database and use all the databasee records within out application.
'''
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = 'sqlite:///./todos.db' # we are telling SQLAlchemy to store our databse in file called todos.db

engine = create_engine(     # create engine is the main SQLAlchemy fucntion to set up the database connection
    SQLALCHEMY_DATABASE_URL,
    connect_args={'check_same_thread': False}
)


'''
A session in SQLALchemy is how you talk to the database (run queries, add rows, commit changes)
sessionmaker() is a factory that gives you new session objects

'''
sessionLocal = sessionmaker(
    autocommit=False, # require explicit commit
    autoflush=False,  # don't automatically flush changes before queries
    bind=engine       # use the engine you just created
)

# This is how we define your ORM models(tables)
Base = declarative_base()