def generate_insights(total_commits, avg_files_changed, large_commits):
    insights = []

    if total_commits < 10:
        insights.append("Repository has a relatively small commit history.")

    if total_commits >= 10:
        insights.append("Repository shows consistent development activity.")

    if avg_files_changed > 5:
        insights.append("Commits tend to modify many files at once.")

    if avg_files_changed <= 5:
        insights.append("commit sizes appear manageable.")
    