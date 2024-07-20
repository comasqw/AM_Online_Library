from fastapi import FastAPI, Request, HTTPException
from fastapi_templateapp import TemplateApp, validate_template_response
from routers import grammar_checker_router, letter_changer_router, library_router
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException

app = TemplateApp()

# routers
app.include_router(grammar_checker_router)
app.include_router(letter_changer_router)
app.include_router(library_router)


templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


# @app.get("/static/styles/styles.css")
# def get_css_file():
#     response = FileResponse("path/to/style.css")
#     response.headers["Cache-Control"] = "no-store"
#     return response


@app.get("/", response_class=HTMLResponse)
async def main_page(request: Request):
    template_response = {
        "request": request,
        "content": {}
    }

    validate_template_response(template_response)
    return templates.TemplateResponse("index.html", template_response)


@app.get("/privacy-policy", response_class=HTMLResponse)
async def privacy_policy(request: Request):
    template_response = {
        "request": request,
        "content": {}
    }

    validate_template_response(template_response)
    return templates.TemplateResponse("privacy_policy.html", template_response)
