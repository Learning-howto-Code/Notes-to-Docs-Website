import base64
import json
from openai import OpenAI
from keys import OPENAI_KEY
from pydantic import BaseModel

client = OpenAI(api_key=OPENAI_KEY)

class Output(BaseModel):
    title: set
    document_text: str

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# Path to your image
image_path = "/Users/jakehopkins/Downloads/IMG_1059.jpeg"

# Getting the Base64 string
base64_image = encode_image(image_path)

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Extract the text from this image and return a structured JSON output."},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}},
            ],
        }
    ],
    response_format="json",  # Request JSON format
)

# Parse the JSON output into a Pydantic model
json_output = json.loads(response.choices[0].message.content)
structured_output = Output(**json_output)

print(structured_output)
