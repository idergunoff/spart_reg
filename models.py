from sqlalchemy import create_engine, Column, Integer, BigInteger, String, DateTime, Date, Text, Boolean, ForeignKey, Time, Float, func, desc, or_
from sqlalchemy.orm import sessionmaker, relationship, declarative_base


DATABASE_NAME = 'spart_db.sqlite'

engine = create_engine(f'sqlite:///{DATABASE_NAME}', echo=False)
Session = sessionmaker(bind=engine)

Base = declarative_base()


class Admin(Base):
    __tablename__ = 'admin'

    admin_id = Column(BigInteger, primary_key=True)
    username = Column(String)
    confirm = Column(Boolean)


class Person(Base):
    __tablename__ = 'person'

    id = Column(Integer, primary_key=True)
    full_name = Column(String)
    birthday = Column(String)
    phone = Column(String)
    company = Column(String)
    position = Column(String)

    beach_volleyballs_1 = relationship('BeachVolleyball', back_populates='p_1', foreign_keys='BeachVolleyball.player_1')
    beach_volleyballs_2 = relationship('BeachVolleyball', back_populates='p_2', foreign_keys='BeachVolleyball.player_2')

    streetballs_1 = relationship('Streetball', back_populates='p_1', foreign_keys='Streetball.player_1')
    streetballs_2 = relationship('Streetball', back_populates='p_2', foreign_keys='Streetball.player_2')
    streetballs_3 = relationship('Streetball', back_populates='p_3', foreign_keys='Streetball.player_3')
    streetballs_4 = relationship('Streetball', back_populates='p_4', foreign_keys='Streetball.player_4')

    workouts = relationship('Workout', back_populates='p')

    wakeboardings = relationship('Wakeboarding', back_populates='p')

    rock_climbings = relationship('RockClimbing', back_populates='p')

    family_catamaran_racings_1 = relationship('FamilyCatamaranRacing', back_populates='p_1', foreign_keys='FamilyCatamaranRacing.player_1')
    family_catamaran_racings_2 = relationship('FamilyCatamaranRacing', back_populates='p_2', foreign_keys='FamilyCatamaranRacing.player_2')

    children_climbing_walls = relationship('ChildrenClimbingWall', back_populates='p')

    chesses = relationship('Chess', back_populates='p')

    figital_footballs_1 = relationship('FigitalFootball', back_populates='p_1', foreign_keys='FigitalFootball.player_1')
    figital_footballs_2 = relationship('FigitalFootball', back_populates='p_2', foreign_keys='FigitalFootball.player_2')
    figital_footballs_3 = relationship('FigitalFootball', back_populates='p_3', foreign_keys='FigitalFootball.player_3')
    figital_footballs_4 = relationship('FigitalFootball', back_populates='p_4', foreign_keys='FigitalFootball.player_4')

    sup_surfings = relationship('SupSurfing', back_populates='p')


class BeachVolleyball(Base):
    __tablename__ = 'beach_volleyball'

    id = Column(Integer, primary_key=True)
    username_reg = Column(String)
    date_reg = Column(DateTime)
    player_1 = Column(Integer, ForeignKey('person.id'))
    player_2 = Column(Integer, ForeignKey('person.id'))

    p_1 = relationship('Person', back_populates='beach_volleyballs_1', foreign_keys=[player_1])
    p_2 = relationship('Person', back_populates='beach_volleyballs_2', foreign_keys=[player_2])


class Streetball(Base):
    __tablename__ = 'streetball'

    id = Column(Integer, primary_key=True)
    username_reg = Column(String)
    date_reg = Column(DateTime)
    player_1 = Column(Integer, ForeignKey('person.id'))
    player_2 = Column(Integer, ForeignKey('person.id'))
    player_3 = Column(Integer, ForeignKey('person.id'))
    player_4 = Column(Integer, ForeignKey('person.id'))

    p_1 = relationship('Person', back_populates='streetballs_1', foreign_keys=[player_1])
    p_2 = relationship('Person', back_populates='streetballs_2', foreign_keys=[player_2])
    p_3 = relationship('Person', back_populates='streetballs_3', foreign_keys=[player_3])
    p_4 = relationship('Person', back_populates='streetballs_4', foreign_keys=[player_4])


class Workout(Base):
    __tablename__ = 'workout'

    id = Column(Integer, primary_key=True)
    username_reg = Column(String)
    date_reg = Column(DateTime)
    player = Column(Integer, ForeignKey('person.id'))

    p = relationship('Person', back_populates='workouts')


class Wakeboarding(Base):
    __tablename__ = 'wakeboarding'

    id = Column(Integer, primary_key=True)
    username_reg = Column(String)
    date_reg = Column(DateTime)
    player = Column(Integer, ForeignKey('person.id'))

    p = relationship('Person', back_populates='wakeboardings')


class RockClimbing(Base):
    __tablename__ = 'rock_climbing'

    id = Column(Integer, primary_key=True)
    username_reg = Column(String)
    date_reg = Column(DateTime)
    player = Column(Integer, ForeignKey('person.id'))

    p = relationship('Person', back_populates='rock_climbings')


class FamilyCatamaranRacing(Base):
    __tablename__ = 'family_catamaran_racing'

    id = Column(Integer, primary_key=True)
    username_reg = Column(String)
    date_reg = Column(DateTime)
    player_1 = Column(Integer, ForeignKey('person.id'))
    player_2 = Column(Integer, ForeignKey('person.id'))


    p_1 = relationship('Person', back_populates='family_catamaran_racings_1', foreign_keys=[player_1])
    p_2 = relationship('Person', back_populates='family_catamaran_racings_2', foreign_keys=[player_2])


class ChildrenClimbingWall(Base):
    __tablename__ = 'children_climbing_wall'

    id = Column(Integer, primary_key=True)
    username_reg = Column(String)
    date_reg = Column(DateTime)
    parent_name = Column(String)
    player = Column(Integer, ForeignKey('person.id'))

    p = relationship('Person', back_populates='children_climbing_walls')


class Chess(Base):
    __tablename__ = 'chess'

    id = Column(Integer, primary_key=True)
    username_reg = Column(String)
    date_reg = Column(DateTime)
    player = Column(Integer, ForeignKey('person.id'))

    p = relationship('Person', back_populates='chesses')


class FigitalFootball(Base):
    __tablename__ = 'figital_football'

    id = Column(Integer, primary_key=True)
    username_reg = Column(String)
    date_reg = Column(DateTime)
    player_1 = Column(Integer, ForeignKey('person.id'))
    player_2 = Column(Integer, ForeignKey('person.id'))
    player_3 = Column(Integer, ForeignKey('person.id'))
    player_4 = Column(Integer, ForeignKey('person.id'))

    p_1 = relationship('Person', back_populates='figital_footballs_1', foreign_keys=[player_1])
    p_2 = relationship('Person', back_populates='figital_footballs_2', foreign_keys=[player_2])
    p_3 = relationship('Person', back_populates='figital_footballs_3', foreign_keys=[player_3])
    p_4 = relationship('Person', back_populates='figital_footballs_4', foreign_keys=[player_4])


class SupSurfing(Base):
    __tablename__ = 'sup_surfing'

    id = Column(Integer, primary_key=True)
    username_reg = Column(String)
    date_reg = Column(DateTime)
    player = Column(Integer, ForeignKey('person.id'))

    p = relationship('Person', back_populates='sup_surfings')

Base.metadata.create_all(engine)
