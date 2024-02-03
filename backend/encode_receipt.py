import base64

# Read the file as binary data
with open("sample_receipt.jpg", "rb") as file:
    file_data = file.read()

# Encode the binary data into Base64
encoded_data = base64.b64encode(file_data).decode('utf-8')
print(encoded_data)

# Construct the request body
request_body = {
    "filename": "receipt.png",
    "filedata": encoded_data
}