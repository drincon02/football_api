from sqlalchemy.orm import Session
from dependencies import get_db, authenticate
from fastapi import Depends, HTTPException, APIRouter, status, Header
from typing import Annotated

from db.crud import create_match, get_matches, get_match_by_id, update_match, get_team_by_id, get_matches_by_team
from db.schemas import MatchBase, Match
from datetime import datetime

router = APIRouter()

@router.post("/create_match")
async def createapi_match(match: MatchBase, db: Session = Depends(get_db), token: str = Header()):
    authenticate(token)
    if match.home_team_id == match.away_team_id:
        raise HTTPException(status_code=400, detail="Home team and away team cannot be the same")
    if get_team_by_id(db, team_id=match.home_team_id) is False:
        raise HTTPException(status_code=404, detail="Home team not found")
    if get_team_by_id(db, team_id=match.away_team_id) is False:
        raise HTTPException(status_code=404, detail="Away team not found")

    if match.home_team_goals < 0 or match.away_team_goals < 0:
        raise HTTPException(status_code=400, detail="Goals cannot be negative")
    
    if match.status not in ["pending", "completed"]:
        raise HTTPException(status_code=400, detail="Invalid status")
    
    home_team = get_team_by_id(db, team_id=match.home_team_id)
    away_team = get_team_by_id(db, team_id=match.away_team_id)
    if home_team.league_id != away_team.league_id:
        raise HTTPException(status_code=400, detail="Home team and away team must be in the same league")
    try:
        datetime.strptime(match.match_date, '%Y-%m-%d')
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Date should be in yyyy-mm-dd format.")

    return create_match(db, match)

@router.get("/get_matches")
async def getapi_matches(limit: int = 10, db: Session = Depends(get_db), token: str = Header()):
    authenticate(token)
    return get_matches(db, limit=limit)

@router.get("/get_match_by_id")
async def getapi_match_by_id(id: int, db: Session = Depends(get_db), token: str = Header()):
    authenticate(token)
    match_id = get_match_by_id(db, match_id=id)
    if match_id is False:
        raise HTTPException(status_code=404, detail="Match not found")
    
@router.put("/update_match")
async def updateapi_match(match: Match, db: Session = Depends(get_db), token: str = Header()):
    authenticate(token)
    if match.home_team_goals < 0 or match.away_team_goals < 0:
        raise HTTPException(status_code=400, detail="Goals cannot be negative")
    if match.status not in ["pending", "completed"]:
        raise HTTPException(status_code=400, detail="Invalid status")
    return update_match(db, match)

@router.get("/get_matches_by_team")
async def getapi_matches_by_team(team_id: int, db: Session = Depends(get_db), token: str = Header()):
    authenticate(token)
    matches = get_matches_by_team(db, team_id=team_id)
    if matches is False:
        raise HTTPException(status_code=404, detail="No matches found")
    return matches