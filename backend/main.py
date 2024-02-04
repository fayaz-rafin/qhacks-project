# https://fastapi.tiangolo.com/tutorial/request-files/#optional-file-upload
import os
import dotenv
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from azure_functions import extract_value, upload_blob_stream
from redis_functions import existing_database, add_vectors, initialize_database
from cron_function import check_for_new_recalls, sample_recall

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
def upload(file: UploadFile = File(...), user: str = Form(...)):
    """
    Uploads a file to the server
    :param file: Receipt file
    :param user: Metadata
    :return:
    """
    contents = file.file.read()
    receipt = extract_value(contents)
    try:
        rds = existing_database(user)
    except Exception as e:
        rds = initialize_database(user)
    for transaction in receipt:
        for item in transaction['items']:
            embed_json = {'description': item['description']}
            if 'merchant_name' in transaction:
                embed_json['merchant_name'] = transaction['merchant_name']
            if 'transaction_date' in transaction:
                embed_json['transaction_date'] = transaction['transaction_date']
            add_vectors(rds, [item['description']], [embed_json])
    file_name = file.filename
    file_url = upload_blob_stream(user, contents, file_name)
    # print(receipt)

    return {"message": f"Successfully uploaded {file.filename}", "user": user, "file_url": file_url}


@app.post("/cron")
def cron(user: str = Form(...)):
    """
    Cron job to check for new recalls
    :return:
    """
    check_for_new_recalls(user)
    return {"message": "Cron job complete"}


@app.post("/sample_recall")
def recall(user: str = Form(...), product: str = Form(...)):
    """
    Cron job to check for new recalls
    :return:
    """
    sample_recall(user, product)
    return {"message": "Sample test complete"}
