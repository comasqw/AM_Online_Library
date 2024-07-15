from fastapi import APIRouter, Form, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from .modules import parse_word

library_router = APIRouter()

templates = Jinja2Templates(directory="templates")

library_form_template_path = "library_templates/library_form.html"
library_template_path = "library_templates/library.html"


@library_router.get("/library", response_class=HTMLResponse)
def library_form(request: Request):
    return templates.TemplateResponse(library_form_template_path, {"request": request})


@library_router.post("/library", response_class=HTMLResponse)
async def library_form(request: Request, user_word: str = Form(...)):
    try:
        word_info = await parse_word(user_word)
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": e})

    content = {
        "user_word": user_word,
        "word_info": word_info
    }

    error_not_found = {
                "error_while_scraping": False
            }

    detail = {
            "template_path": library_template_path,
            "error": error_not_found,
            "content": content
        }

    if isinstance(word_info, str):
        error_not_found["error_while_scraping"] = True
        raise HTTPException(status_code=404, detail=detail)

    return templates.TemplateResponse(library_template_path, {"request": request,
                                                              "content": detail["content"],
                                                              "error_not_found": detail["error"]})
