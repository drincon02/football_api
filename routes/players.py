from sqlalchemy.orm import Session
from dependencies import get_db, authenticate
from fastapi import Depends, HTTPException, APIRouter, status, Header
from typing import Annotated

from db.crud import create_player, get_players, get_player_by_id, get_player_by_name, get_player_by_team, get_team_by_id
from db.schemas import Playersbase, Players

router = APIRouter()

@router.post("/create_player")
async def createapi_player(player: Playersbase, db: Session = Depends(get_db), token: str = Header()):
    authenticate(token)
    
    if get_team_by_id(db, team_id=player.team_id) is False:
        raise HTTPException(status_code=404, detail="Team not found")

    return create_player(db, player)

@router.get("/get_players")
async def getapi_players(limit: int = 10, db: Session = Depends(get_db), token: str = Header()):
    authenticate(token)
    return get_players(db, limit=limit)

@router.get("/get_player_by_id")
async def getapi_player_by_id(id: int, db: Session = Depends(get_db), token: str = Header()):
    authenticate(token)
    player_id = get_player_by_id(db, player_id=id)
    if player_id is False:
        raise HTTPException(status_code=404, detail="Player not found")
    
@router.get("/get_player_by_name")
async def getapi_player_by_name(name: str, db: Session = Depends(get_db), token: str = Header()):
    authenticate(token)
    player_name = get_player_by_name(db, player_name=name)
    if player_name is False:
        raise HTTPException(status_code=404, detail="Player not found")
    return player_name

@router.get("/get_player_by_team")
async def getapi_player_by_team(team_id: int, db: Session = Depends(get_db), token: str = Header()):
    authenticate(token)
    players = get_player_by_team(db, team_id=team_id)
    if players is False:
        raise HTTPException(status_code=404, detail="No players found")
    return players