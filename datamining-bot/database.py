from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean, func, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///navaras_dev.db'

Base = SQLAlchemy(app)
migrate = Migrate(app, Base)

manager = Manager(app)
manager.add_command('Base', MigrateCommand)

'''class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    name = Column(String(10), nullable=False)
    isActive = Column(Boolean, default=True)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(20), nullable=False)
    isActive = Column(Boolean, default=True)
    role_id = Column(Integer, ForeignKey(Role.id))
    role = relationship(Role)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
        }

movieGenre_table = Table('moviegenre', Base.metadata,
    Column('movie_id', Integer, ForeignKey('movie.id')),
    Column('genre_id', Integer, ForeignKey('genre.id'))
)

class Genre(Base.Model):
    __tablename__ = 'genre'

    id = Column(Integer, primary_key=True)
    name = Column(String)

class Movie(Base.Model):
    __tablename__ = 'movie'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    genre = relationship("Genre", secondary=movieGenre_table)
    '''

class Director(Base.Model):
    __tablename__ = 'director'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    ref = Column(String, nullable=True)

class Producer(Base.Model):
    __tablename__ = 'producer'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    ref = Column(String, nullable=True)

class Screenplay(Base.Model):
    __tablename__ = 'screenplay'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    ref = Column(String, nullable=True)

class Story(Base.Model):
    __tablename__ = 'story'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    ref = Column(String, nullable=True)

class Starring(Base.Model):
    __tablename__ = 'starring'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    ref = Column(String, nullable=True)

class Music(Base.Model):
    __tablename__ = 'music'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    ref = Column(String, nullable=True)

class Cinematography(Base.Model):
    __tablename__ = 'cinematography'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    ref = Column(String, nullable=True)

class Editor(Base.Model):
    __tablename__ = 'editor'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    ref = Column(String, nullable=True)

class ProductionCompany(Base.Model):
    __tablename__ = 'production'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    ref = Column(String, nullable=True)

class Language(Base.Model):
    __tablename__ = 'language'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    ref = Column(String, nullable=True)

class Movies(Base.Model):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    directedBy = Column(String, nullable=True)
    producedBy = Column(String, nullable=True)
    screenplayBy = Column(String, nullable=True)
    storyBy = Column(String, nullable=True)
    starringBy = Column(String, nullable=True)
    genre = Column(String, nullable=True)
    year = Column(Integer, nullable=True)
    musicBy = Column(String, nullable=True)
    cinematographyBy = Column(String, nullable=True)
    editedBy = Column(String, nullable=True)
    productionComp = Column(String, nullable=True)
    language_id = Column(Integer, ForeignKey(Language.id))
    poster = Column(String, nullable=True)
    thumbnail = Column(String, nullable=True)
    background = Column(String, nullable=True)
    description = Column(String, nullable=True)
    releaseDate = Column(DateTime)
    runningTime = Column(Integer)
    distributedBy = Column(String, nullable=True)
    ref = Column(String, nullable=True)
    '''director = relationship('Director', foreign_keys=[directedBy])
    producer = relationship('Producer', foreign_keys=[producedBy])
    screenplay = relationship('Screenplay', foreign_keys=[screenplayBy])
    story = relationship('Story', foreign_keys=[storyBy])
    starring = relationship('Starring', foreign_keys=[starringBy])
    music = relationship('Music', foreign_keys=[musicBy])
    cinematography = relationship('Cinematography', foreign_keys=[cinematographyBy])
    editor = relationship('Editor', foreign_keys=[editedBy])'''
    language = relationship('Language', foreign_keys=[language_id])


engine = create_engine('sqlite:///navaras_dev.db')
Base.metadata.create_all(engine)

if __name__ == '__main__':
    manager.run()