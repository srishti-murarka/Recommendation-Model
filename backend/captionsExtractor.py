import os
import sys
from google.cloud import vision
import io
import time
import requests
from google.auth import credentials
import json
from dotenv import load_dotenv
import base64
load_dotenv()

def perform_prediction(image_path):
    GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
    headers = {
        'Authorization': 'Bearer ' + os.getenv("GCP_ACCESS_TOKEN"),
        'Content-Type': 'application/json; charset=utf-8',
    }

    with io.open(image_path, 'rb') as image_file:
        content = base64.b64encode(image_file.read())

    requestJSON = {
        "instances": [
            {
                "image": {
                    "bytesBase64Encoded": content.decode('utf-8')
                    }
            }
        ],
        "parameters": {
            "sampleCount": 1,
            "language": "en"
        }
    }

    url = f"https://us-central1-aiplatform.googleapis.com/v1/projects/{GCP_PROJECT_ID}/locations/us-central1/publishers/google/models/imagetext:predict"

    response = requests.post(url, headers=headers, data=json.dumps(requestJSON))

    if response.status_code != 200:
        raise Exception(response.text)
    else:
        print(response.json()["predictions"][0])
        return response.json()["predictions"][0]

def extract_captions(image_path):
    client = vision.ImageAnnotatorClient()

    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    reponse = client.label_detection(image=image)
    labels = reponse.label_annotations

    captions = [label.description for label in labels]

    return captions

def main():
    # Process each image in the folder
    with open ("./captions.txt", "w") as file:
        for filename in os.listdir("posts"):
            if filename.endswith(('.jpg', '.jpeg', '.png')):
                image_path = os.path.join("posts", filename)
                
                # Describe the image
                # description = describe_image(image_path, google_credentials, openai_api_key)
                caption = perform_prediction(image_path)

                # Print the description
                print(f'Image: {filename}')
                print('Description:')
                print(caption)
                print('---------------------')
                file.write(caption + "\n")
                time.sleep(0.5)


if __name__ == "__main__":
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./gcpconfig.json"
    # if len(sys.argv) != 4:
    #     print("Usage: python generate.py <folder_path> <google_credentials>")
    # else:
    main()