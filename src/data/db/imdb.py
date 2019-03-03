from datetime import datetime

from sqlalchemy import Column, String, DateTime, Boolean, Integer, Float
from sqlalchemy.dialects import postgresql

from data.db import Base


# class TitleBasics(Base):
#     __tablename__ = "title"
#     id = Column(String, primary_key=True)
#     created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
#     updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
#     titleType = Column(String)
#     primaryTitle = Column(String)
#     originalTitle = Column(String)
#     isAdult = Column(Boolean)
#     startYear = Column(Integer)
#     endYear = Column(Integer)
#     runtimeMinutes = Column(Integer)
#     genres = Column(postgresql.ARRAY(String))
#     poster = Column(String)
#
#
# class TitleAkas(Base):
#     __tablename__ = "title_akas"
#     id = Column(Integer, primary_key=True)
#     created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
#     updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
#     ordering = Column(Integer)
#     titleId = Column(String)
#     title = Column(String)
#     region = Column(String)
#     language = Column(String)
#     types = Column(postgresql.ARRAY(String))
#     attributes = Column(postgresql.ARRAY(String))
#     isOriginalTitle = Column(Boolean)
#
#
# class TitleCrew(Base):
#     __tablename__ = "title_crew"
#     id = Column(String, primary_key=True)
#     created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
#     updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
#     directors = Column(postgresql.ARRAY(String))
#     writers = Column(postgresql.ARRAY(String))
#
#
# class TitleEpisode(Base):
#     __tablename__ = "title_episode"
#     id = Column(String, primary_key=True)
#     created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
#     updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
#     seasonNumber = Column(Integer)
#     episodeNumber = Column(Integer)
#
#
# class TitlePrincipals(Base):
#     __tablename__ = "title_principals"
#     id = Column(Integer, primary_key=True)
#     created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
#     updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
#     ordering = Column(Integer)
#     title_id = Column(String)
#     name_id = Column(String)
#     category = Column(String)
#     job = Column(String)
#     characters = Column(String)
#
#
# class TitleRatings(Base):
#     __tablename__ = "title_ratings"
#     id = Column(String, primary_key=True)
#     created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
#     updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
#     averageRating = Column(Float)
#     numVotes = Column(Integer)
#
#
# class NameBasics(Base):
#     __tablename__ = "name_basics"
#     id = Column(String, primary_key=True)
#     created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
#     updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
#     primaryName = Column(String)
#     birthYear = Column(Integer)
#     deathYear = Column(Integer)
#     primaryProfession = Column(postgresql.ARRAY(String))
#     knownForTitles = Column(postgresql.ARRAY(String))