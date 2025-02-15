from flask import Flask, render_template, request, jsonify
import os
import shutil
import base64
import json
from openai import OpenAI
from pydantic import BaseModel
from uploads import uploads_bp
from keys import OPENAI_KEY

app = Flask(__name__)
app.register_blueprint(uploads_bp, url_prefix="/uploads")

class Output(BaseModel):
    text: str

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/convert', methods=['POST'])
def convert():
    client = OpenAI(api_key=OPENAI_KEY)
    
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    
    folder = "/Users/jakehopkins/Documents/Flask_Test/uploads"
    
    if not os.path.exists(folder):
        return jsonify({"message": "Folder not found!"}), 400
    
    image_files = [f for f in os.listdir(folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    if not image_files:
        return jsonify({"message": "No image files found!"}), 400
    
    results = []
    
    for image_file in image_files:
        image_path = os.path.join(folder, image_file)
        base64_image = encode_image(image_path)
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Extract the text from this image word for word and return it in JSON format with a 'text' field containing the extracted text as a string."
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                        }
                    ]
                }
            ],
            response_format={"type": "json_object"},
            max_tokens=2000,
            timeout=60
        )
        
        json_output = response.choices[0].message.content
        structured_output = Output.model_validate(json.loads(json_output))
        results.append({image_file: structured_output.model_dump()})
        
        print("Conversion Results:")
        print(results)
    
    return jsonify({"message": "Conversion successful!", "results": results})

if __name__ == "__main__":
    app.run(debug=True)