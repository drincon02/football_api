from pydantic import BaseModel
from enum import Enum
from datetime import datetime

class UserBase(BaseModel):
    username: str
    permission_level: int = 1

class Userlogin(BaseModel):
    password: str
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True

class TeamBase(BaseModel):
    name: str
    year_founded: int
    league_id: int

class Team(TeamBase):
    id: int

    class Config:
        orm_mode = True

class LeagueBase(BaseModel):
    name: str
    country: str

class League(LeagueBase):
    id: int

    class Config:
        orm_mode = True

class MatchBase(BaseModel):
    home_team_id: int
    away_team_id: int
    home_team_goals: int
    away_team_goals: int
    match_date: str
    status: str = "pending"

class Match(BaseModel):
    id: int
    home_team_goals: int
    away_team_goals: int
    status: str = "pending"
    class Config:
        orm_mode = True


class Positions(str, Enum):
    gk = "Goalkeeper"
    df = "Defender"
    mf = "Midfielder"
    fw = "Forward"

class Playersbase(BaseModel):
    name: str
    age: int
    position: Positions
    team_id: int

class Players(Playersbase):
    id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str