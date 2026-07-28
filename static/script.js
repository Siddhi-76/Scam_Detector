async function checkInput() {
    const input = document.getElementById("userInput").value.trim();
    const loading = document.getElementById("loading");
    const results = document.getElementById("results");

    if (!input) {
        alert("Please paste a URL or message first.");
        return;
    }

    // Show loading, hide old results
    loading.classList.remove("hidden");
    results.classList.add("hidden");

    try {
        const response = await fetch("/check", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ input: input })
        });
        const data = await response.json();
        showResults(data);
    } catch (err) {
        alert("Error connecting to server: " + err.message);
    } finally {
        loading.classList.add("hidden");
    }
}

function showResults(data) {
    const badge = document.getElementById("verdict-badge");
    const fill = document.getElementById("score-fill");
    const scoreEl = document.getElementById("score-num");
    const list = document.getElementById("reasons-list");
    const mlDiv = document.getElementById("ml-verdict");
    const results = document.getElementById("results");

    // Set verdict badge text and colour
    badge.textContent = data.verdict;
    badge.className = data.verdict.toLowerCase().replace(" ", "-");

    // Set score bar width and number
    scoreEl.textContent = data.score + " / 100";
    fill.style.width = data.score + "%";
    fill.style.background = data.score >= 60 ? "#dc2626" : data.score >= 30 ? "#d97706" : "#059669";

    // Populate reasons list
    list.innerHTML = (data.reasons || []).map(r => `<li>${r}</li>`).join("");

    // ML verdict (if available)
    mlDiv.textContent = data.ml_verdict ? `ML Model: ${data.ml_verdict}` : "";

    results.classList.remove("hidden");
}

// Allow pressing Enter to submit
document.addEventListener("keydown", e => {
    if (e.key === "Enter" && e.ctrlKey) checkInput();
});
