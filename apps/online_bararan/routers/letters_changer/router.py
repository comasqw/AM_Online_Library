from fastapi import APIRouter, Form, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from .modules import change_letters

letter_changer_router = APIRouter()

templates = Jinja2Templates(directory="templates")


@letter_changer_router.get("/letter_changer", response_class=HTMLResponse)
async def letter_changer_form(request: Request):
    return templates.TemplateResponse("letter_changer_templates/letter_changer_form.html", {"request": request})


@letter_changer_router.post("/letter_changer", response_class=HTMLResponse)
async def letter_changer(request: Request, user_text: str = Form(..., min_length=1, max_length=5000)):
    try:
        changed_text = await change_letters(user_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": e})

    return templates.TemplateResponse("letter_changer_templates/letter_changer.html", {"request": request, "user_text": user_text,
                                                              "changed_text": changed_text})
