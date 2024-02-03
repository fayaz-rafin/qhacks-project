import os
import dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient

dotenv.load_dotenv()

endpoint = os.environ["AZURE_ENDPOINT"]
key = os.environ["AZURE_API_KEY"]


def extract_value(file):

    extracted_data = []
    document_analysis_client = DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    poller = document_analysis_client.begin_analyze_document("prebuilt-receipt", analyze_request=file, locale="en-US",
                                                             content_type="application/octet-stream")
    receipts = poller.result()

    for idx, receipt in enumerate(receipts.documents):
        fields = {'idx': idx + 1}
        print(f"--------Analysis of receipt #{idx + 1}--------")
        print(f"Receipt type: {receipt.doc_type if receipt.doc_type else 'N/A'}")
        merchant_name = receipt.fields.get("MerchantName")
        if merchant_name:
            print(f"Merchant Name: {merchant_name.get('valueString')} has confidence: " f"{merchant_name.confidence}")
        transaction_date = receipt.fields.get("TransactionDate")
        if transaction_date:
            print(
                f"Transaction Date: {transaction_date.get('valueDate')} has confidence: "
                f"{transaction_date.confidence}"
            )
        if receipt.fields.get("Items"):
            print("Receipt items:")
            for idx, item in enumerate(receipt.fields.get("Items").get("valueArray")):
                print(f"...Item #{idx + 1}")
                item_description = item.get("valueObject").get("Description")
                if item_description:
                    print(
                        f"......Item Description: {item_description.get('valueString')} has confidence: "
                        f"{item_description.confidence}"
                    )
                item_quantity = item.get("valueObject").get("Quantity")
                if item_quantity:
                    print(
                        f"......Item Quantity: {item_quantity.get('valueString')} has confidence: "
                        f"{item_quantity.confidence}"
                    )
                item_total_price = item.get("valueObject").get("TotalPrice")
                if item_total_price:
                    print(
                        # f"......Total Item Price: {format_price(item_total_price.get('valueCurrency'))} has confidence: "
                        f"......Total Item Price: {item_total_price.get('valueCurrency')} has confidence: "
                        f"{item_total_price.confidence}"
                    )
        # subtotal = receipt.fields.get("Subtotal")
        # if subtotal:
        #     print(f"Subtotal: {format_price(subtotal.get('valueCurrency'))} has confidence: {subtotal.confidence}")
        # tax = receipt.fields.get("TotalTax")
        # if tax:
        #     print(f"Total tax: {format_price(tax.get('valueCurrency'))} has confidence: {tax.confidence}")
        # tip = receipt.fields.get("Tip")
        # if tip:
        #     print(f"Tip: {format_price(tip.get('valueCurrency'))} has confidence: {tip.confidence}")
        # total = receipt.fields.get("Total")
        # if total:
        #     print(f"Total: {format_price(total.get('valueCurrency'))} has confidence: {total.confidence}")
        # print("--------------------------------------")
