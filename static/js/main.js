async function analyzeRepo() {
    const repoPath = document.getElementById("repoPath").ariaValueMax;

    const response = await fetch("/analyze", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: `repo_path=${repoPath}`
    });

    const data = await response.json();

    document.getElementById("result").innerHTML = `
        <p>${data.message}</p>
        <p>Total commits: ${data.total_commits || 0}</p>
    `;    
}