from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from git import Repo
import os 

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

@app.route("/history")
def history():
    analyses = Analysis.query.order_by(Analysis.id.desc()).all()
    return render_template("dashboard.html", analyses=analyses)

@app.route("/analyze", methods=["POST"])
def analyze():
    repo_path = request.form.get("repo_path")

    if not os.path.exists(repo_path):
        return jsonify({
            "message": "path does not exist"
        })   
    
    try:
        repo = Repo(repo_path)
        commits = list(repo.iter_commits())

        total_commits = len(commits)

        file_changes = []

        for commit in commits:
            file_changes.append(len(commit.stats.files))

        avg_files_changed = 0

        if len(file_changes) > 0:
            avg_files_changed = sum(file_changes) / len(file_changes)

        large_commits = len([x for x in file_changes if x > 5])

        analysis = Analysis(
            repo_name=repo_path,
            total_commits=total_commits,
            avg_files_changed=avg_files_changed,
            large_commits=large_commits
        )        

        db.session.add(analysis)
        db.session.commit()

        return jsonify({
            "message": "analysis complete",
            "total_commits": total_commits,
            "avg_files_changed": round(avg_files_changed, 2),
            "large_commits": large_commits
        })
    
    except Exception:
        return jsonify({
            "message": "not a valid git repository"
        })
    
if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)        