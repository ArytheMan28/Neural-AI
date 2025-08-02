from flask import Flask, render_template, request
import openai  # or import your model logic here

app = Flask(__name__)

# Example text generation function (edit this as needed)
def generate_text(prompt):
    # Replace this with your own logic or API call
    return f"You asked: {prompt}"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/pages/imgGen")
def imgGen():
    return render_template("pages/imgGen.html")

@app.route("/pages/textGen", methods=["GET", "POST"])
def textGen():
    output = ""
    if request.method == "POST":
        prompt = request.form.get("prompt")
        if prompt:
            output = generate_text(prompt)
    return render_template("pages/textGen.html", output=output)

@app.route("/pages/codie")
def codie():
    return render_template("pages/codie.html")

if __name__ == "__main__":
    app.run(debug=True)
