from flask import Flask, request, render_template, send_from_directory, jsonify
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Ensure upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    files = request.files.getlist("file")  # Get multiple files
    for file in files:
        if file.filename:
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], file.filename))

    return jsonify({"message": "Files uploaded successfully!"})

@app.route("/files")
def list_files():
    files = os.listdir(UPLOAD_FOLDER)
    return jsonify({"files": files})  # Returns JSON list of filenames

@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_input = request.form["user_input"]  # Get the text input from the form
        # add_text(user_input)  # Pass the user input to the add_text function
        # share_google_doc()  # Share the document with your email
        return render_template('index.html', result=f"Text '{user_input}' added to the Google Doc.")
    return render_template('index.html', result=None)
if __name__ == "__main__":
    app.run(debug=True)
