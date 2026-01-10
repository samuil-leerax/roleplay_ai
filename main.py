from flask import Flask, send_from_directory, render_template

app = Flask(__name__, static_folder="web", template_folder="web")

@app.route("/")
def home():
    # Renders web/index.html
    return render_template("index.html")

# Optionally serve other files in web/ (JS, CSS, images)
@app.route("/<path:filename>")
def assets(filename):
    return send_from_directory(app.static_folder, filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)