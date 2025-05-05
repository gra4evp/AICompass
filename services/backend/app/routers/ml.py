from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

router = APIRouter(prefix="/ml", tags=["Machine Learning"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def ml_home(request: Request):
    return templates.TemplateResponse("ml.html", {"request": request})

@router.get("/intro", response_class=HTMLResponse)
async def ml_intro(request: Request):
    return templates.TemplateResponse("ml/intro.html", {"request": request})

@router.get("/linear-regression", response_class=HTMLResponse)
async def linear_regression(request: Request):
    return templates.TemplateResponse("ml/linear_regression.html", {"request": request})

@router.get("/regularization", response_class=HTMLResponse)
async def regularization(request: Request):
    return templates.TemplateResponse("ml/regularization.html", {"request": request})

@router.get("/classification", response_class=HTMLResponse)
async def classification(request: Request):
    return templates.TemplateResponse("ml/classification.html", {"request": request})

@router.get("/logistic-regression", response_class=HTMLResponse)
async def logistic_regression(request: Request):
    return templates.TemplateResponse("ml/logistic_regression.html", {"request": request})

@router.get("/decision-trees", response_class=HTMLResponse)
async def decision_trees(request: Request):
    return templates.TemplateResponse("ml/decision_trees.html", {"request": request})

@router.get("/random-forest", response_class=HTMLResponse)
async def random_forest(request: Request):
    return templates.TemplateResponse("ml/random_forest.html", {"request": request}) 