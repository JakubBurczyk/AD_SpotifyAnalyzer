from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base


from sqlalchemy import Column, Integer, String, Date, SmallInteger, Table, Float, MetaData, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()

class Artist(Base):
    __tablename__ = 'artist'
    artist_id = Column(Integer, primary_key=True)
    name = Column(String(50))

    def __repr__(self):
        return "<artist(id='{0}', name={1})>".format(self.artist_id, self.name)


class Song(Base):
    __tablename__ = 'song'
    song_id = Column(Integer, primary_key=True)
    title = Column(String(50))

    def __repr__(self):
        return "<song(id='{0}', name={1})>".format(self.song_id, self.title)

class SongArtist(Base):
    __tablename__ = 'song_artist'
    song_id = Column(Integer, primary_key=True)
    artist_id = Column(Integer, primary_key=True)

    def __repr__(self):
        return "<song id='{0}', artist id={1})>".format(self.song_id, self.artist_id)

class Trend(Base):
    __tablename__ = 'trend'
    trend_id = Column(Integer, primary_key=True)
    trend = Column(String(50))

    def __repr__(self):
        return "<trend(id='{0}', trend={1})>".format(self.trend_id, self.trend)

class Day(Base):
    __tablename__ = 'day'
    day_id = Column(Integer, primary_key=True)
    date = Column(Date)

    def __repr__(self):
        return "<date(id='{0}', date={1})>".format(self.day_id, self.date)

class Region(Base):
    __tablename__ = 'region'
    region_id = Column(Integer, primary_key=True)
    name = Column(String(50))

    def __repr__(self):
        return "<region(id='{0}', name={1})>".format(self.region_id, self.name)

class Category(Base):
    __tablename__ = 'category'
    category_id = Column(Integer, primary_key=True)
    name = Column(String(50))

    def __repr__(self):
        return "<category(id='{0}', name={1})>".format(self.category_id, self.name)

class Chart(Base):
    __tablename__ = 'chart'
    chart_id = Column(Integer, primary_key=True)
    position = Column(Integer)
    song_id = Column(Integer)
    day_id = Column(Integer)
    region_id = Column(Integer)
    category_id = Column(Integer)
    trend_id = Column(Integer)
    streams = Column(Integer)

    def __repr__(self):
        return "<chart(id='{0}', position={1}, song={2}, streams={3})>".format(self.chart_id, self.position, self.song_id, self.streams)