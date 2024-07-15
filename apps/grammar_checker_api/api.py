from grammar_checker import checker
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Body
from concurrent.futures import ThreadPoolExecutor

app = FastAPI()
max_characters = 150
executor = ThreadPoolExecutor(max_workers=5)


def check_grammar(user_text: str):
    grammar_checker = checker.AMSpellChecker(user_text)
    try:
        unknown_words = grammar_checker.main()
        return {"unknown_words": unknown_words}
    except Exception as e:
        return {"error": f"Error during text processing - {e}"}


@app.post("/check_text_grammar/api/")
def check_text_grammar(user_text: str = Body()):
    if len(user_text.split()) <= max_characters:
        future = executor.submit(check_grammar, user_text)
        result = future.result()
        return JSONResponse(result)
    else:
        return JSONResponse({"error": f"There are more than {max_characters} characters in the text"})


@app.on_event("shutdown")
def shutdown_event():
    executor.shutdown(wait=True)
