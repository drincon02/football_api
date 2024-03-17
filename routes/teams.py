from sqlalchemy.orm import Session
from dependencies import get_db, authenticate
from fastapi import Depends, HTTPException, APIRouter, status, Header
from typing import Annotated

from db.crud import create_team, get_teams, get_team_by_id, get_team_by_name

from db.schemas import TeamBase, Team

router = APIRouter()

# This is an exmample of how not to do it because if someone put a random team id it will create the record anyhow
@router.post("/create_team")
async def createapi_team(team: TeamBase, db: Session = Depends(get_db), token: str = Header()):
    authenticate(token)


    return create_team(db, team)

@router.get("/get_teams")
async def getapi_teams(limit: int = 10, db: Session = Depends(get_db), token: str = Header()):
    authenticate(token)
    return get_teams(db, limit=limit)

@router.get("/get_team_by_id")
async def getapi_team_by_id(id: int, db: Session = Depends(get_db), token: str = Header()):
    authenticate(token)
    team_id = get_team_by_id(db, team_id=id)
    if team_id is False:
        raise HTTPException(status_code=404, detail="Team not found")
    
@router.get("/get_team_by_name")
async def getapi_team_by_name(name: str, db: Session = Depends(get_db), token: str = Header()):
    authenticate(token)
    team_name = get_team_by_name(db, team_name=name)
    if team_name is False:
        raise HTTPException(status_code=404, detail="Team not found")
    return team_name