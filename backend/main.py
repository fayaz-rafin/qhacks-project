# https://fastapi.tiangolo.com/tutorial/request-files/#optional-file-upload
import os
import dotenv
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from azure_functions import extract_value, upload_blob_stream
from redis_functions import existing_database, add_vectors, initialize_database
from cron_function import check_for_new_recalls, sample_recall
from pydantic import BaseModel, HttpUrl, Field

dotenv.load_dotenv()

OCR_API_KEY = os.environ["OCR_API_KEY"]
AZURE_API_KEY = os.environ["AZURE_API_KEY"]
AZURE_ENDPOINT = os.environ["AZURE_ENDPOINT"]

tags_metadata = [
    {
        "name": "server",
        "description": "Operations related to the server.",
        "externalDocs": {
            "description": "Azure Documentation",
            "url": "https://learn.microsoft.com/en-us/azure",
        },
    },
]

description = """This application allows users to upload receipt files and process the receipt data. It also provides 
functionality for performing cron jobs to check for new recalls and recalling specific products for users. The 
uploaded files are stored in Azure Blob Storage, and the receipt data is stored in a Redis database. The application 
utilizes OCR API for extracting values from the receipt files and Azure Functions for uploading the files to Azure 
Blob Storage. The application is built using FastAPI framework and follows the RESTful API design principles."""

app = FastAPI(
    title="recall",
    description=description,
    summary="Insert a summary here",
    version="0.0.1",
    contact={
        "name": "James",
        "url": "https://yorku.ca",
        "email": "example@gmail.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class UploadResponse(BaseModel):
    message: str = Field(..., example="Successfully uploaded sample_receipt.jpeg",
                         description="A success message indicating the file was uploaded.")
    user: str = Field(..., example="1234", alias="user", description="The user's identifier.")
    file_url: HttpUrl = Field(..., example="https://example.blob.core.windows.net/receipts/sample_receipt.jpeg",
                              description="The URL of the uploaded file.")


class CronResponse(BaseModel):
    message: str = Field(..., example="Cron job complete",
                         description="A message indicating the completion of the cron job.")


class RecallResponse(BaseModel):
    message: str = Field(..., example="Sample test complete",
                         description="A message indicating the completion of the sample recall.")


@app.post("/upload", response_model=UploadResponse, tags=["server"])
async def upload(file: UploadFile = File(...), user: str = Form(...)):
    """
    Uploads a file to the server and processes the receipt data.

    Parameters:
    - file: The uploaded receipt file.
    - user: The metadata associated with the upload.

    Returns:
    A dictionary containing upload information:
    - message: A success message indicating the file was uploaded.
    - user: The user metadata.
    - file_url: The URL of the uploaded file.

    Raises:
    None.
    """
    print("Processing file")
    contents = file.file.read()
    file_name = file.filename
    file_url = await upload_blob_stream(user, contents, file_name)
    receipt = extract_value(file_url)
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

    # print(receipt)

    return {"message": f"Successfully uploaded {file.filename}", "user": user, "file_url": file_url}


@app.post("/cron", response_model=CronResponse, tags=["server"])
def cron(user: str = Form(...)):
    """
    Perform a cron job to check for new recalls for a given user.

    Parameters:
    - user: The username of the user for whom to check for new recalls.

    Returns:
    A dictionary containing a message indicating the completion of the cron job.

    Raises:
    None.
    """
    check_for_new_recalls(user)
    return {"message": "Cron job complete"}


@app.post("/sample_recall", response_model=RecallResponse, tags=["server"])
def recall(user: str = Form(...), product: str = Form(...), email: str = Form(...)):
    """
    This function is used to recall a product for a specific user.

    Parameters:
    - user: The username of the user.
    - product: The name of the product to be recalled.

    Returns:
    A dictionary containing the message "Sample test complete".

    Raises:
    None.
    """
    sample_recall(user, product, email)
    return {"message": "Sample test complete"}
