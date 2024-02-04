import requests
import os
import dotenv

dotenv.load_dotenv()

headers = {"Authorization": f"Bearer {os.environ['CLOUDFLARE_API_KEY']}"}
CLOUDFLARE_BASE_URL = os.environ["CLOUDFLARE_BASE_URL"]
CLOUDFLARE_ACCOUNT_ID = os.environ["CLOUDFLARE_ACCOUNT_ID"]


def run(model: str, input: dict):
    """
    Run the specified model with the given input.

    :param model: The name of the model to run.
    :param input: The input data for the model.
    :return: The response from the model.
    """
    response = requests.post(f"{CLOUDFLARE_BASE_URL}{model}", headers=headers, json=input)
    return response.json()


def generate_embeddings(text: str):
    """
    Generate embeddings for the given text using a pre-trained model.

    :param text: The input text for which embeddings need to be generated.
    :type text: str
    :return: The generated embeddings.
    :rtype: dict
    """
    model = "@cf/baai/bge-small-en-v1.5"
    input = {
        "text": text
    }
    output = run(model, input)
    return output


if __name__ == "__main__":
    input = "I am a test string"
    print(generate_embeddings(input))
