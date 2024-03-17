from sqlalchemy.orm import Session
from dependencies import get_db, authenticate
from fastapi import Depends, HTTPException, APIRouter, status, Header
from typing import Annotated

from db.crud import create_league, get_leagues, get_league_by_name, delete_league, update_league_name
from db.schemas import LeagueBase

router = APIRouter()


@router.post("/create_league")
async def createapi_league(league: LeagueBase, db: Session = Depends(get_db), token: str = Header()):
    authenticate(token)
    return create_league(db, league)
    
@router.get("/get_leagues")
async def getapi_leagues(limit: int = 10, db: Session = Depends(get_db), token: str = Header()):
    authenticate(token)
    return get_leagues(db, limit=limit)

@router.get("/get_league_by_name")
async def getapi_league_by_name(name: str, db: Session = Depends(get_db), token: str = Header()):
    authenticate(token)
    return get_league_by_name(db, league_name=name)

@router.delete("/delete_league")
async def deleteapi_league(league_id: int, db: Session = Depends(get_db), token: str = Header()):
    authenticate(token)
    old_league = delete_league(db, league_id=league_id)
    if old_league is False:
        raise HTTPException(status_code=404, detail="League not found")
    
@router.put("/update_league_name")
async def updateapi_league_name(league_id: int, new_name: str, db: Session = Depends(get_db), token: str = Header()):
    authenticate(token)
    old_league = update_league_name(db, league_id=league_id, new_name=new_name)
    if old_league is False:
        raise HTTPException(status_code=404, detail="League not found")
    return old_league