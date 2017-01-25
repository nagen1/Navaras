from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from database import Movies, Genre, movieGenre_table

Base = declarative_base()
engine = create_engine('sqlite:///navaras_dev.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
dbsession = DBSession()

movie = dbsession.query(Movies).filter(Movies.id == '1').one()

'''movie.name = 'Movie 1'

genre = Genre()
genre.name = 'Genre 1'

dbsession.add(movie)
dbsession.add(genre)
dbsession.commit()
genre = Genre()
genre.name = "Comedy 1"

movie = Movies()
movie.name = "Movie Name 1"
movie.genre.append(genre)


dbsession.add(movie)
dbsession.commit()'''

for genre in movie.genre:
    print(genre.name)