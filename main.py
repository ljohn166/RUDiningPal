#main
from fastapi import FastAPI, Request, Form, BackgroundTasks, Query
from fastapi.responses import HTMLResponse
#from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

init_db()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.mount("/", response_class=HTMLResponse)
async def home(request: Request):
    dining_halls = ['Busch', 'Livingston', 'Neilson']
    return templates.TemplateResponse("index.html", {"request": request}, dining_halls=dining_halls)

@app.get("/results", response_class=HTMLResponse)
async def get_started(request: Request):
    hall = request.form['dining_hall']
    meal = request.form['meal_time']
    preferences = request.form.getlist('preferences')
    #check database for generated result, if it exists, display that, if it doesn't scrape menu and call gemini
    #store results, return combinations 
    return templates.TemplateResponse("results.html", {"request": request}, combinations=combinations)