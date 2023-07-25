from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/images", StaticFiles(directory="images"), name="images")

templates = Jinja2Templates(directory="templates")


@app.get("/live/{key}", response_class=HTMLResponse)
async def read_item(request: Request, key: str):
    if key == '9155190037':
        return templates.TemplateResponse("live.html", {"request": request})
    return JSONResponse(content={'message': 'you are not allowed to see this page'})
