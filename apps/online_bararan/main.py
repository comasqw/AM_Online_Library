from fastapi import FastAPI, Request, HTTPException
from routers import grammar_checker_router, letter_changer_router, library_router
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging

logging.basicConfig(level=logging.DEBUG, filename='logs/errors_logs.log',
                    format='%(levelname)s (%(asctime)s): %(message)s (Line: %(lineno)d) [%(filename)s]',
                    datefmt='%d/%m/%Y %I:%M:%S',
                    encoding='utf-8')

app = FastAPI()

# routers
app.include_router(grammar_checker_router)
app.include_router(letter_changer_router)
app.include_router(library_router)


templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/static/styles/styles.css")
def get_css_file():
    response = FileResponse("path/to/style.css")
    response.headers["Cache-Control"] = "no-store"
    return response


@app.get("/", response_class=HTMLResponse)
async def main_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/privacy-policy", response_class=HTMLResponse)
async def privacy_policy(request: Request):
    return templates.TemplateResponse("privacy_policy.html", {"request": request})


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return templates.TemplateResponse("errors_templates/error_404.html", {"request": request}, status_code=404)


@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    status_code = exc.status_code
    detail: dict = exc.detail

    if status_code != 500:
        if status_code == 404:
            return templates.TemplateResponse(detail["template_path"], {"request": request,
                                                                        "status_code": status_code,
                                                                        "error_not_found": detail["error"],
                                                                        "content": detail["content"]}, status_code=404)
    else:
        # logging.exception(detail.get("error"))
        return templates.TemplateResponse("errors_templates/error_500.html", {"request": request}, status_code=500)
