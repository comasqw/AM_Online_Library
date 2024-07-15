from fastapi import APIRouter, Form, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import httpx

grammar_checker_router = APIRouter()

templates = Jinja2Templates(directory="templates")
grammar_api_url = "https://grammar-checker-api-tqhi.onrender.com/check_text_grammar/api/"


@grammar_checker_router.get("/grammar_checker", response_class=HTMLResponse)
async def grammar_checker_form(request: Request):
    return templates.TemplateResponse("grammar_checker_templates/grammar_checker_form.html", {"request": request})


@grammar_checker_router.post("/grammar_checker", response_class=HTMLResponse)
async def grammar_checker(request: Request, user_text: str = Form(min_length=1, max_length=150)):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(grammar_api_url, json=user_text, timeout=30)
            response_data = response.json()
            unknown_words = response_data["unknown_words"]
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": e})

    return templates.TemplateResponse("grammar_checker_templates/grammar_checker.html", {"request": request,
                                                                                         "user_text": user_text,
                                                                                         "unknown_words": unknown_words})
