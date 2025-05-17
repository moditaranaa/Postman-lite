from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from postmanlite.models import APIRequestModel, APIResponseModel
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
from postmanlite.service import make_api_request

app = FastAPI(title= "Postman Lite Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def get_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/send-request", response_model=APIResponseModel)
async def send_request(request: APIRequestModel):
    """
    Endpoint to send an API request and return the response.
    """
    response = await make_api_request(
        url=str(request.url),
        method=request.method,
        headers=request.headers,
        body=request.body
    )
    return response