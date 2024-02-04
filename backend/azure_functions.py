# https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/sdk-overview-v4-0?view=doc-intel-4.0.0&tabs=python
# https://learn.microsoft.com/en-us/python/api/overview/azure/ai-documentintelligence-readme?view=azure-python-preview#using-prebuilt-models
# https://learn.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-python?tabs=managed-identity%2Croles-azure-portal%2Csign-in-azure-cli
# https://learn.microsoft.com/en-us/azure/storage/blobs/storage-blob-upload-python
import mimetypes
import os
import dotenv
import uuid
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, ContentSettings

dotenv.load_dotenv()

endpoint = os.environ["AZURE_ENDPOINT"]
key = os.environ["AZURE_API_KEY"]
blob_endpoint = os.environ["AZURE_BLOB_ENDPOINT"]
blob_key = os.environ["AZURE_BLOB_API_KEY"]


def extract_value(file: bytes):
    extracted_data = []
    document_analysis_client = DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    poller = document_analysis_client.begin_analyze_document("prebuilt-receipt", analyze_request=file, locale="en-US",
                                                             content_type="application/octet-stream")
    receipts = poller.result()

    for idx, receipt in enumerate(receipts.documents):
        confidence_interval = 0.90
        fields = {'idx': idx + 1, 'items': []}
        merchant_name = receipt.fields.get("MerchantName")
        if merchant_name:
            if merchant_name.confidence >= confidence_interval:
                fields['merchant_name'] = merchant_name.get('valueString')
        transaction_date = receipt.fields.get("TransactionDate")
        if transaction_date:
            if transaction_date.confidence >= confidence_interval:
                fields['transaction_date'] = transaction_date.get('valueDate')
        if receipt.fields.get("Items"):
            for idx, item in enumerate(receipt.fields.get("Items").get("valueArray")):
                item_info = {}
                item_description = item.get("valueObject").get("Description")
                if item_description:
                    item_info['description'] = item_description.get('valueString')
                item_quantity = item.get("valueObject").get("Quantity")
                if item_quantity:
                    item_info['quantity'] = item_quantity.get('valueNumber')
                item_total_price = item.get("valueObject").get("TotalPrice")
                if item_total_price:
                    item_info['price'] = item_total_price.get('valueCurrency')
                fields['items'].append(item_info)
        subtotal = receipt.fields.get("Subtotal")
        if subtotal:
            if subtotal.confidence >= confidence_interval:
                fields['subtotal'] = subtotal.get('valueCurrency')
        tax = receipt.fields.get("TotalTax")
        if tax:
            if tax.confidence >= confidence_interval:
                fields['tax'] = tax.get('valueCurrency')
        total = receipt.fields.get("Total")
        if total:
            if total.confidence >= confidence_interval:
                fields['total'] = total.get('valueCurrency')
        extracted_data.append(fields)
    return extracted_data


def upload_blob_stream(container_name: str, file: bytes, file_extension: str):
    blob_service_client = BlobServiceClient(account_url=blob_endpoint, credential=blob_key)

    # Generate a unique filename using UUID
    unique_identifier = str(uuid.uuid4())
    file_name = unique_identifier + file_extension

    blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_name)

    # Detect the content type based on the file extension
    content_type, _ = mimetypes.guess_type(file_name)

    # If content type couldn't be determined, default to 'application/octet-stream'
    if not content_type:
        content_type = 'application/octet-stream'

    content_settings = ContentSettings(content_type=content_type)

    blob_client.upload_blob(file, blob_type="BlockBlob", content_settings=content_settings)
    # print(blob_client.url)
    return blob_client.url


if __name__ == "__main__":
    with open("sample_receipt.jpeg", "rb") as f:
        file_name = f.name
        print(upload_blob_stream('u2', f, file_name))
