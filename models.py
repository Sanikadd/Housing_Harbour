# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import Column, Integer, String, Text, Float, Numeric, Boolean
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy import create_engine
# import pandas as pd
# db = SQLAlchemy()
# def create_building_table(file_path):
#     """
#     Creates the "building" table in the database.
#     Args:
#         file_path (str): The path to the CSV file containing building data.
#     """
#     df = pd.read_csv(file_path)
#     df.to_sql("building", db_engine, index=False, if_exists="replace")
# def create_neighborhood_table(file_path):
#     """
#     Creates the "neighborhood" table in the database.
#     Args:
#         file_path (str): The path to the CSV file containing neighborhood data.
#     """
#     df = pd.read_csv(file_path)
#     df.to_sql("neighborhood", db_engine, index=False, if_exists="replace")
# # Session to interact with the database
# db_engine = create_engine('sqlite:///hh_flask/new_db.sqlite3')  # Update the database URL
# def create_database():
#     """
#     Creates the database and all required tables.
#     """
#     create_building_table("25_buildings.csv")
#     create_neighborhood_table("neighborhood.csv")
# create_database()
# Base = declarative_base()  # Declarative base for SQLAlchemy models
# Session = sessionmaker(bind=db_engine)  # Session for interacting with the database
# session = Session()  # Create a database session

# class Building(Base):
#     """
#     Represents a building in the database.
#     """
#     __tablename__ = "building"

#     prop_id = Column(Integer, primary_key=True)
#     prop_name = Column(String(100))
#     prop_addr = Column(Text)
#     latitude = Column(Float)
#     longitude = Column(Float)
#     price = Column(Numeric(10, 2))
#     sqft = Column(Integer)
#     bhk = Column(Integer)
#     rent = Column(Numeric(10, 2))
#     sale_type = Column(String(50))
#     furnishing_type = Column(String(50))
#     reserved_parking = Column(Boolean)
#     kids_play_area = Column(Boolean)
#     gym = Column(Boolean)
#     swimming_pool = Column(Boolean)
#     club_house = Column(Boolean)

# class Neighborhood(Base):
#     """
#     Represents a neighborhood in the database.
#     """
#     __tablename__ = "neighborhood"

#     n_id = Column(Integer, primary_key=True)
#     n_name = Column(String(100))
#     n_addr = Column(Text)
#     latitude = Column(Float)
#     longitude = Column(Float)
#     n_type = Column(String(50))

# Base.metadata.create_all(db_engine)