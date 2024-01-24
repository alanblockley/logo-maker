import os
import json
import boto3
import base64
from PIL import Image
from io import BytesIO

# Setup our boto3 clients to be used
bedrock = boto3.client('bedrock-runtime')
s3 = boto3.client('s3')

# Define some constants
modelId = 'amazon.titan-image-generator-v1'
BUCKET = os.getenv('LOGO_BUCKET')

def lambda_handler(event, context):

    print(event)
    print("Boto3 Version:" + boto3.__version__)

    accept = 'application/json'
    contentType = 'application/json'
    i = 0

    body = json.dumps(
        {
            "taskType": "TEXT_IMAGE",
            "textToImageParams": {
                "text": "A trophy in the rain",   # Required
    #           "negativeText": "<text>"  # Optional
            },
            "imageGenerationConfig": {
                "numberOfImages": 1,   # Range: 1 to 5 
                "quality": "premium",  # Options: standard or premium
                "height": 768,         # Supported height list in the docs 
                "width": 1280,         # Supported width list in the docs
                "cfgScale": 7.5,       # Range: 1.0 (exclusive) to 10.0
                "seed": 42             # Range: 0 to 214783647
            }
        }
    )

    response = bedrock.invoke_model(body=body, modelId=modelId, accept=accept, contentType=contentType)

    response_body = json.loads(response.get("body").read())

    images = [Image.open(BytesIO(base64.b64decode(base64_image))) for base64_image in response_body.get("images")]
    
    for img in images:
        i=i+1
        # display(img)
        img.save("/tmp/image_" + str(i) + ".png")
        with open("/tmp/image_" + str(i) + ".png", 'rb') as data:
            s3_response = s3.upload_fileobj(data, BUCKET, "image_" + str(i) + ".png")    

        print(s3_response)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "IMAGE_SAVED"            
        }),
    }
