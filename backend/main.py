import base64
import os
import dotenv
from typing import Optional
import requests

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware

dotenv.load_dotenv()

OCR_API_KEY = os.environ["OCR_API_KEY"]

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
    https://fastapi.tiangolo.com/tutorial/request-files/#optional-file-upload
    Uploads a file to the server
    :param file: Receipt file
    :param user: Metadata
    :return:
    """
    try:
        contents = file.file.read()
        encoded_contents = base64.b64encode(contents).decode('utf-8')
        base64encoded = f"data:image/{file.filename.split('.')[-1]};base64,{encoded_contents}"
        # print(base64encoded)
        # with open(file.filename, 'wb') as f:
        #     f.write(contents)
        url = "https://api.ocr.space/parse/image"
        body_json = {
            "apikey": OCR_API_KEY,
            "language": "eng",
            "isTable": "true",
            "filetype": "jpg",
            "OCREngine": "1",
            "base64Image": base64encoded
        }
        x = requests.post(url, json=body_json)
        print(x.text)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()
    # print(user)
    # print(f"data:image/{file.filename.split('.')[-1]};base64,{encoded_contents}")

    return {"message": f"Successfully uploaded {file.filename}", "base64_contents": encoded_contents}

