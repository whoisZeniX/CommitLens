from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///commits.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Analysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    repo_name = db.Column(db.String(200))
    total_commits = db.Column(db.Integer)
    avg_files_changed = db.Column(db.Float)
    large_commits = db.Column(db.Integer)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])   
def analyze():
    repo_path = request.form.get("repo_path")

    return jsonify({
        "message": f"recieved.form.get: {repo_path}"
    })

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)    
