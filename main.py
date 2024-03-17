from fastapi import FastAPI
#from .routes import players, teams, matches, leagues
from admin import admin
from routes import players, teams, matches, leagues

from db.database import SessionLocal, engine
from db import models

#models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(players.router, prefix="/api/players")
app.include_router(teams.router, prefix="/api/teams")
app.include_router(matches.router, prefix="/api/matches")
app.include_router(leagues.router, prefix="/api/leagues")

app.include_router(admin.router, prefix="/admin")