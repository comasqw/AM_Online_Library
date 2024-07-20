from fastapi import APIRouter, Form, Request, HTTPException
from fastapi_templateapp import validate_template_response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import httpx

grammar_checker_router = APIRouter(default_response_class=HTMLResponse)

templates = Jinja2Templates(directory="templates")
grammar_api_url = "https://grammar-checker-api-tqhi.onrender.com/check_text_grammar/api/"


@grammar_checker_router.get("/grammar_checker")
async def grammar_checker_form(request: Request):
    template_response = {
        "request": request,
        "content": {}
    }

    validate_template_response(template_response)
    return templates.TemplateResponse("grammar_checker_templates/grammar_checker_form.html", template_response)


@grammar_checker_router.post("/grammar_checker")
async def grammar_checker(request: Request, user_text: str = Form(min_length=1, max_length=150)):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(grammar_api_url, json=user_text, timeout=30)
            response_data = response.json()
            unknown_words = response_data["unknown_words"]
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": e})

    template_response = {
        "request": request,
        "content": {
            "user_text": user_text,
            "unknown_words": unknown_words
        }
    }

    validate_template_response(template_response)
    return templates.TemplateResponse("grammar_checker_templates/grammar_checker.html", template_response)

