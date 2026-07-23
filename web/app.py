from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from modules.facility_service import FacilityService
from modules.place_service import PlaceService
from modules.dashboard_service import DashboardService
from modules.repositories.game_repository import GameRepository


app = FastAPI(title="ASV Manager")

templates = Jinja2Templates(directory="web/templates")

facility_service = FacilityService()
place_service = PlaceService()
dashboard_service = DashboardService()
game_repository = GameRepository()


@app.get("/", response_class=HTMLResponse)
def index(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "facilities": facility_service.get_active(),
            "places": place_service.get_active(),
            "dashboard": dashboard_service.get_database_stats()
        }
    )


@app.get("/facilities")
def facilities():

    return facility_service.get_active()


@app.get("/places")
def places():

    return place_service.get_active()

@app.get("/games", response_class=HTMLResponse)
def games(request: Request):

    games = game_repository.get_all_games()

    return templates.TemplateResponse(
        request=request,
        name="games.html",
        context={
            "games": games
        }
    )    