# https://fastapi.tiangolo.com/tutorial/request-files/#optional-file-upload
import base64
import os
import dotenv

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware

from azure_functions import extract_value

dotenv.load_dotenv()

OCR_API_KEY = os.environ["OCR_API_KEY"]
AZURE_API_KEY = os.environ["AZURE_API_KEY"]
AZURE_ENDPOINT = os.environ["AZURE_ENDPOINT"]

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/upload")
def upload(file: UploadFile = File(...), user:str = Form(...)):
    """
    Uploads a file to the server
    :param file: Receipt file
    :param user: Metadata
    :return:
    """
    contents = file.file.read()
    receipt = extract_value(contents)
    print(receipt)
    print(user)

    return {"message": f"Successfully uploaded {file.filename}", "user": user, "receipt": receipt}

