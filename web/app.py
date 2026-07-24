from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from modules.facility_service import FacilityService
from modules.place_service import PlaceService
from modules.dashboard_service import DashboardService
from modules.repositories.game_repository import GameRepository
from modules.team_service import TeamService
from modules.season_service import SeasonService
from modules.person_service import PersonService


app = FastAPI(title="ASV Manager")
app.mount(
    "/static",
    StaticFiles(directory="web/static"),
    name="static"
)

templates = Jinja2Templates(directory="web/templates")

facility_service = FacilityService()
place_service = PlaceService()
dashboard_service = DashboardService()
game_repository = GameRepository()
team_service = TeamService()
season_service = SeasonService()
person_service = PersonService()


@app.get("/", response_class=HTMLResponse)
def index(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "facilities": facility_service.get_active(),
            "places": place_service.get_active(),
            "dashboard": dashboard_service.get_database_stats(),
            "active_page": "dashboard"
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



@app.get("/seasons/new", response_class=HTMLResponse)
def new_season(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="season_form.html",
        context={
            "active_page": "seasons"
        }
    )


@app.post("/seasons/new")
def create_season(
    name: str = Form(...),
    active: bool = Form(False)
):

    season_service.create_season(
        name=name,
        active=active
    )

    return RedirectResponse(
        "/seasons",
        status_code=303
    )



@app.get("/seasons/{season_id}", response_class=HTMLResponse)
def edit_season(
    request: Request,
    season_id: int
):

    season = season_service.get_season(season_id)

    return templates.TemplateResponse(
        request=request,
        name="season_form.html",
        context={
            "season": season,
            "active_page": "seasons"
        }
    )



@app.post("/seasons/{season_id}")
def update_season(
    season_id: int,
    name: str = Form(...),
    active: bool = Form(False)
):

    season_service.update_season(
        season_id=season_id,
        name=name,
        active=active
    )

    return RedirectResponse(
        "/seasons",
        status_code=303
    )


@app.get("/seasons", response_class=HTMLResponse)
def seasons(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="seasons.html",
        context={
            "seasons": season_service.get_all(),
            "active_page": "seasons"
        }
    )


@app.get("/teams", response_class=HTMLResponse)
def teams(request: Request):

    teams = team_service.get_all()

    return templates.TemplateResponse(
        request=request,
        name="teams.html",
        context={
            "teams": teams,
            "active_page": "teams"
        }
    )   


@app.get("/teams/new", response_class=HTMLResponse)
def new_team(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="team_form.html",
        context={
            "team": None,
            "seasons": season_service.get_active(),
            "active_page": "teams"
        }
    )


@app.post("/teams/new")
def create_team(

    name: str = Form(...),
    season_id: int = Form(...)
):

    team_service.create_team(
        name=name,
        season_id=season_id,
        active=True
    )

    return RedirectResponse(
        "/teams",
        status_code=303
    )


@app.get("/teams/{team_id}", response_class=HTMLResponse)
def edit_team(request: Request, team_id: int):

    team = team_service.get_team(team_id)

    return templates.TemplateResponse(
        request=request,
        name="team_form.html",
        context={
            "team": team,
            "seasons": season_service.get_active(),
            "active_page": "teams"
        }
    )

@app.get("/persons", response_class=HTMLResponse)
def persons(request: Request):

    persons = person_service.get_all()

    return templates.TemplateResponse(
        request=request,
        name="persons.html",
        context={
            "persons": persons,
            "active_page": "persons"
        }
    )



@app.get("/persons/{person_id}", response_class=HTMLResponse)
def edit_person(
    request: Request,
    person_id: int
):

    person = person_service.get_person(person_id)

    return templates.TemplateResponse(
        request=request,
        name="person_form.html",
        context={
            "person": person,
            "active_page": "persons"
        }
    )

@app.post("/persons/{person_id}")
def update_person(
    person_id: int,
    first_name: str = Form(...),
    last_name: str = Form(...),
    birth_date: str = Form(""),
    mobile: str = Form(""),
    email: str = Form(""),
    status: str = Form(""),
    active: bool = Form(False),
    note: str = Form("")
):

    person_service.update_person(
        person_id=person_id,
        first_name=first_name,
        last_name=last_name,
        birth_date=birth_date or None,
        mobile=mobile,
        email=email,
        status=status,
        active=active,
        note=note
    )

    return RedirectResponse(
        "/persons",
        status_code=303
    )    

@app.post("/teams/{team_id}")
def update_team(
    team_id: int,
    name: str = Form(...),
    season_id: int = Form(...),
    active: bool = Form(False)
):

    team_service.update_team_db(
        team_id=team_id,
        name=name,
        season_id=season_id,
        active=active
    )

    return RedirectResponse(
        "/teams",
        status_code=303
    )


     