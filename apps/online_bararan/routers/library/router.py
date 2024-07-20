from fastapi import APIRouter, Form, Request, HTTPException
from fastapi_templateapp import validate_template_response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from .modules import parse_word

library_router = APIRouter(default_response_class=HTMLResponse)

templates = Jinja2Templates(directory="templates")

library_form_template_path = "library_templates/library_form.html"
library_template_path = "library_templates/library.html"


@library_router.get("/library")
def library_form(request: Request):
    template_response = {
        "request": request,
        "content": {}
    }

    validate_template_response(template_response)
    return templates.TemplateResponse(library_form_template_path, template_response)


@library_router.post("/library")
async def library_form(request: Request, user_word: str = Form(...)):
    try:
        word_info = await parse_word(user_word)
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": e})

    error_not_found = False
    status_code = 200

    if isinstance(word_info, str):
        error_not_found = True
        status_code = 404

    template_response = {
        "request": request,
        "content": {
            "user_word": user_word,
            "word_info": word_info,
            "error_not_found": error_not_found
        }
    }

    validate_template_response(template_response)
    return templates.TemplateResponse(library_template_path, template_response, status_code=status_code)
