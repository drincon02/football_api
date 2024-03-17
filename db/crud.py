from . import models, schemas
from sqlalchemy.orm import Session


def create_league(db: Session, league: schemas.LeagueBase):
    db_league = models.leagues(name=league.name, country=league.country)
    db.add(db_league)
    db.commit()
    db.refresh(db_league)
    return db_league

def get_leagues(db: Session, limit: int = 10):
    return db.query(models.leagues).limit(limit).all()

def get_league_by_name(db: Session, league_name: str):
    league = db.query(models.leagues).filter(models.leagues.name == league_name).first()
    if not league:
        return False
    return league
    
def update_league_name(db: Session, league_id: int, new_name: str):
    league = db.query(models.leagues).filter(models.leagues.id == league_id).first()
    if league is None:
        return False
    league.name = new_name
    db.commit()
    db.refresh(league)
    return league

def delete_league(db: Session, league_id: int):
    league = db.query(models.leagues).filter(models.leagues.id == league_id).first()
    if league is None:
        return False
    db.delete(league)
    db.commit()
    return {"Success": "League Deleted"}

def create_team(db: Session, team: schemas.TeamBase):
    db_team = models.teams(name=team.name, year_founded=team.year_founded, league_id=team.league_id)
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team

def get_teams(db: Session, limit: int = 10):
    return db.query(models.teams).limit(limit).all()

def get_team_by_id(db: Session, team_id: int):
    team = db.query(models.teams).filter(models.teams.id == team_id).first()
    if team is None:
        return False
    return team

def get_team_by_name(db: Session, team_name: str):
    team = db.query(models.teams).filter(models.teams.name == team_name).first()
    if team is None:
        return False
    return team

def create_player(db: Session, player: schemas.Playersbase):
    db_player = models.players(name=player.name, age=player.age, position=player.position, team_id=player.team_id)
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player

def get_players(db: Session, limit: int = 10):
    return db.query(models.players).limit(limit).all()

def get_player_by_id(db: Session, player_id: int):
    player = db.query(models.players).filter(models.players.id == player_id).first()
    if player is None:
        return False
    return player

def get_player_by_name(db: Session, player_name: str):
    player = db.query(models.players).filter(models.players.name == player_name).first()
    if player is None:
        return False
    return player

def get_player_by_team(db: Session, team_id: int):
    players = db.query(models.players).filter(models.players.team_id == team_id).all()
    if players is None:
        return False
    return players

def create_match(db: Session, match: schemas.MatchBase):
    db_match = models.matches(home_team_id=match.home_team_id, away_team_id=match.away_team_id, home_team_goals=match.home_team_goals, away_team_goals=match.away_team_goals, match_date=match.match_date, status=match.status)
    db.add(db_match)
    db.commit()
    db.refresh(db_match)
    return db_match

def get_matches(db: Session, limit: int = 10):
    return db.query(models.matches).limit(limit).all()

def get_match_by_id(db: Session, match_id: int):
    match = db.query(models.matches).filter(models.matches.id == match_id).first()
    if match is None:
        return False
    return match

def get_match_by_date(db: Session, match_date: str):
    match = db.query(models.matches).filter(models.matches.match_date == match_date).first()
    if not match:
        return False
    return match

def update_match(db: Session, updated_match: schemas.Match):
    match = db.query(models.matches).filter(models.matches.id == updated_match.id).first()
    if match is None:
        return False
    match.home_team_goals = updated_match.home_team_goals
    match.away_team_goals = updated_match.away_team_goals
    match.status = updated_match.status
    db.commit()
    db.refresh(match)
    return match

def get_matches_by_team(db: Session, team_id: int):
    matches = db.query(models.matches).filter(models.matches.home_team_id == team_id).all()
    matches += db.query(models.matches).filter(models.matches.away_team_id == team_id).all()
    if matches is None:
        return False
    return matches

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(username=user.username, hashed_password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session, limit: int = 10):
    return db.query(models.User).limit(limit).all()

def get_user_by_id(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        return False
    return user

def get_user_by_name(db: Session, username: str):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        return False
    return user
