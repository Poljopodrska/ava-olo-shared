from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import os

app = FastAPI(title="AVA OLO Dashboard Hub")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def dashboard_landing(request: Request):
    return templates.TemplateResponse("dashboard_landing.html", {
        "request": request,
        "title": "AVA OLO Agricultural Dashboards"
    })

@app.get("/business")
async def business_dashboard(request: Request):
    return templates.TemplateResponse("placeholder_dashboard.html", {
        "request": request,
        "dashboard_type": "Business Dashboard",
        "message": "Coming Soon - Business Analytics"
    })

@app.get("/agronomic")
async def agronomic_dashboard(request: Request):
    return templates.TemplateResponse("placeholder_dashboard.html", {
        "request": request,
        "dashboard_type": "Agronomic Dashboard", 
        "message": "Coming Soon - Crop Analytics"
    })

@app.get("/database")
async def database_dashboard_redirect():
    # Redirect to existing database dashboard
    return RedirectResponse(url="/database-dashboard")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)