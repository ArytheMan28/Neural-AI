from flask import Flask, render_template, request, jsonify
import os, requests

app = Flask(__name__)

HF_KEY = os.getenv("hugging_face_key")
MODEL = "HuggingFaceH4/zephyr-7b-beta"  # solid free model on HF Inference

def hf_chat(prompt: str) -> str:
    if not HF_KEY:
        return "Error: hugging_face_key not set in environment."
    url = f"https://api-inference.huggingface.co/models/{MODEL}"
    headers = {"Authorization": f"Bearer {HF_KEY}"}
    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 200, "return_full_text": False}
    }
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=60)
        r.raise_for_status()
        data = r.json()
        if isinstance(data, list) and data and "generated_text" in data[0]:
            return data[0]["generated_text"].strip()
        if isinstance(data, dict) and "error" in data:
            return f"Model error: {data['error']}"
        return f"Unexpected response: {data}"
    except Exception as e:
        return f"Request failed: {e}"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/pages/textGen", methods=["GET","POST"])
def textGen():
    output = ""
    if request.method == "POST":
        prompt = (request.form.get("prompt") or "").strip()
        app.logger.info(f"TEXT prompt: {prompt!r}")
        if prompt:
            output = hf_chat(prompt)
    return render_template("pages/textGen.html", output=output)

# Optional JSON endpoint if your JS uses fetch()
@app.route("/api/text", methods=["POST"])
def api_text():
    prompt = (request.get_json(silent=True) or {}).get("prompt","")
    return jsonify({"text": hf_chat(prompt)})
