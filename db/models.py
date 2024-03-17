from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    permission_level = Column(Integer, default=1)


class teams(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    year_founded = Column(Integer)
    league_id = Column(Integer, ForeignKey("leagues.id"))


    league = relationship("leagues", back_populates="teams")
    players = relationship("players", back_populates="team")


class leagues(Base):
    __tablename__ = "leagues"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    country = Column(String, index=True)
    teams = relationship("teams", back_populates="league")

class matches(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    home_team_id = Column(Integer, ForeignKey("teams.id"))
    away_team_id = Column(Integer, ForeignKey("teams.id"))
    home_team_goals = Column(Integer)
    away_team_goals = Column(Integer)
    match_date = Column(String, index=True)
    status = Column(String, index=True, default="pending")

    home_team = relationship("teams", foreign_keys=[home_team_id])
    away_team = relationship("teams", foreign_keys=[away_team_id])

class players(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
    position = Column(String, index=True)
    team_id = Column(Integer, ForeignKey("teams.id"))

    team = relationship("teams", back_populates="players")