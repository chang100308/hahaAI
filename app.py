from flask import Flask, render_template, request, jsonify
from google import genai
from google.genai import types
import json
import base64

app = Flask(__name__)

# --- CONFIGURATION ---
API_KEY = "AIzaSyCSr4FlZkACSs29tRwY64kW7DNYPcATKnY"
client = genai.Client(api_key=API_KEY)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_image():
    try:
        data = request.get_json()
        image_base64 = data.get('image')
        
        # Using the newest stable 2026 model
        model_id = "gemini-2.5-flash"

        prompt = "Perform OCR. Return ONLY a JSON object with: {'original_content': '...', 'summary_detailed': '...'}"

        response = client.models.generate_content(
            model=model_id,
            contents=[
                prompt,
                types.Part.from_bytes(
                    data=base64.b64decode(image_base64),
                    mime_type='image/jpeg'
                )
            ]
        )

        # Remove any Markdown wrapping (```json) the AI might add
        raw_text = response.text.strip()
        if "```" in raw_text:
            raw_text = raw_text.split("```")[1].replace("json", "").strip()
        
        return jsonify(json.loads(raw_text))

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

import os
API_KEY = os.environ.get("GEMINI_API_KEY") 
client = genai.Client(api_key=API_KEY)

if __name__ == '__main__':
    # Get the port from the environment (default to 5000)
    port = int(os.environ.get("PORT", 5000))
    # host='0.0.0.0' is required for deployment
    app.run(host='0.0.0.0', port=port)