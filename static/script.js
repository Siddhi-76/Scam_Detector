/* ══════════════════════════════════════════════════════════════
   NIGRANI — Scam Detector  |  JavaScript Engine
   3D Particle Canvas • Light/Dark Mode • PDF Generation • Scanner
   ══════════════════════════════════════════════════════════════ */

// Global State
let currentAnalysis = null;
let currentInputText = "";
let currentFeatures = null;
let scanHistory = [];

// ── Theme Management ──────────────────────────────────────────
function initTheme() {
    const savedTheme = localStorage.getItem('nigrani-theme') || 'dark';
    setTheme(savedTheme);
}

function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme') || 'dark';
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    setTheme(newTheme);
}

function setTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('nigrani-theme', theme);

    const moonIcon = document.getElementById('moonIcon');
    const sunIcon = document.getElementById('sunIcon');

    if (moonIcon && sunIcon) {
        if (theme === 'light') {
            moonIcon.classList.add('hidden');
            sunIcon.classList.remove('hidden');
        } else {
            sunIcon.classList.add('hidden');
            moonIcon.classList.remove('hidden');
        }
    }
}

// ── 3D Background Canvas Engine ───────────────────────────────
(function initBackground() {
    const canvas = document.getElementById('bgCanvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    let width, height, particles = [], mouse = { x: -1000, y: -1000 };

    function resize() {
        width = canvas.width = window.innerWidth;
        height = canvas.height = window.innerHeight;
    }

    class Particle {
        constructor() {
            this.reset();
        }
        reset() {
            this.x = Math.random() * width;
            this.y = Math.random() * height;
            this.z = Math.random() * 2 + 0.5;
            this.vx = (Math.random() - 0.5) * 0.3;
            this.vy = (Math.random() - 0.5) * 0.3;
            this.radius = Math.random() * 1.5 + 0.5;
            this.opacity = Math.random() * 0.4 + 0.1;
        }
        update() {
            const dx = this.x - mouse.x;
            const dy = this.y - mouse.y;
            const dist = Math.sqrt(dx * dx + dy * dy);
            if (dist < 150) {
                const force = (150 - dist) / 150 * 0.02;
                this.vx += (dx / dist) * force;
                this.vy += (dy / dist) * force;
            }
            this.x += this.vx;
            this.y += this.vy;
            this.vx *= 0.99;
            this.vy *= 0.99;
            if (this.x < 0 || this.x > width) this.vx *= -1;
            if (this.y < 0 || this.y > height) this.vy *= -1;
        }
        draw() {
            const isLight = document.documentElement.getAttribute('data-theme') === 'light';
            const color = isLight ? '79, 70, 229' : '108, 99, 255';
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.radius * this.z, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(${color}, ${this.opacity * this.z})`;
            ctx.fill();
        }
    }

    function init() {
        resize();
        const count = Math.min(Math.floor((width * height) / 8000), 120);
        particles = [];
        for (let i = 0; i < count; i++) {
            particles.push(new Particle());
        }
    }

    function drawConnections() {
        const isLight = document.documentElement.getAttribute('data-theme') === 'light';
        const color = isLight ? '79, 70, 229' : '108, 99, 255';

        for (let i = 0; i < particles.length; i++) {
            for (let j = i + 1; j < particles.length; j++) {
                const dx = particles[i].x - particles[j].x;
                const dy = particles[i].y - particles[j].y;
                const dist = Math.sqrt(dx * dx + dy * dy);
                if (dist < 120) {
                    const opacity = (1 - dist / 120) * 0.12;
                    ctx.beginPath();
                    ctx.moveTo(particles[i].x, particles[i].y);
                    ctx.lineTo(particles[j].x, particles[j].y);
                    ctx.strokeStyle = `rgba(${color}, ${opacity})`;
                    ctx.lineWidth = 0.5;
                    ctx.stroke();
                }
            }
        }
    }

    function animate() {
        ctx.clearRect(0, 0, width, height);
        particles.forEach(p => {
            p.update();
            p.draw();
        });
        drawConnections();
        requestAnimationFrame(animate);
    }

    window.addEventListener('resize', init);
    window.addEventListener('mousemove', e => {
        mouse.x = e.clientX;
        mouse.y = e.clientY;
    });
    init();
    animate();
})();

// ── Cursor Glow & Tilt Effects ───────────────────────────────
(function initEffects() {
    const glow = document.getElementById('cursor-glow');
    if (glow) {
        let gx = 0, gy = 0, tx = 0, ty = 0;
        document.addEventListener('mousemove', e => { tx = e.clientX; ty = e.clientY; });
        function updateGlow() {
            gx += (tx - gx) * 0.08; gy += (ty - gy) * 0.08;
            glow.style.left = gx + 'px'; glow.style.top = gy + 'px';
            requestAnimationFrame(updateGlow);
        }
        updateGlow();
    }

    document.querySelectorAll('[data-tilt]').forEach(card => {
        card.addEventListener('mousemove', e => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left - rect.width / 2;
            const y = e.clientY - rect.top - rect.height / 2;
            card.style.transform = `perspective(800px) rotateX(${(-y / rect.height) * 8}deg) rotateY(${(x / rect.width) * 8}deg) scale(1.01)`;
        });
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'perspective(800px) rotateX(0) rotateY(0) scale(1)';
        });
    });
})();

// ── Counter Animation ─────────────────────────────────────────
(function initCounters() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const el = entry.target;
                const target = parseInt(el.getAttribute('data-count'));
                let current = 0;
                const step = Math.max(1, Math.floor(target / 40));
                const timer = setInterval(() => {
                    current += step;
                    if (current >= target) { current = target; clearInterval(timer); }
                    el.textContent = current;
                }, 30);
                observer.unobserve(el);
            }
        });
    }, { threshold: 0.5 });
    document.querySelectorAll('[data-count]').forEach(c => observer.observe(c));
})();

// ── Scanner Logic ─────────────────────────────────────────────
async function checkInput() {
    const input = document.getElementById('userInput').value.trim();
    const loading = document.getElementById('loading');
    const results = document.getElementById('results');
    const btn = document.getElementById('checkBtn');

    if (!input) {
        showToast('Please paste a URL or message first');
        document.getElementById('userInput').focus();
        return;
    }

    currentInputText = input;
    loading.classList.remove('hidden');
    results.classList.add('hidden');
    btn.disabled = true;

    try {
        const response = await fetch('/check', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ input: input })
        });
        const data = await response.json();
        currentAnalysis = data;
        currentFeatures = data.features || null;

        addToHistory(input, data);
        showResults(data);
    } catch (err) {
        showToast('Error connecting to server: ' + err.message);
    } finally {
        loading.classList.add('hidden');
        btn.disabled = false;
    }
}

function showResults(data) {
    const badge = document.getElementById('verdict-badge');
    const verdictIcon = document.getElementById('verdict-icon');
    const verdictText = document.getElementById('verdict-text');
    const scoreNum = document.getElementById('score-num');
    const scoreArc = document.getElementById('score-arc');
    const fill = document.getElementById('score-fill');
    const list = document.getElementById('reasons-list');
    const mlSection = document.getElementById('ml-verdict');
    const mlPred = document.getElementById('ml-pred-text');
    const results = document.getElementById('results');
    const typeBadge = document.getElementById('scan-type-badge');

    const verdictClass = data.verdict.toLowerCase().replace(' ', '-');
    badge.className = verdictClass;
    verdictIcon.innerHTML = data.score >= 60 ? '⛔' : data.score >= 30 ? '⚠️' : '✅';
    verdictText.textContent = data.verdict;

    typeBadge.textContent = (data.type || 'url').toUpperCase() + ' Analysis';

    const circumference = 326.73;
    const offset = circumference - (data.score / 100) * circumference;
    scoreArc.style.strokeDashoffset = offset;

    const scoreColor = data.score >= 60 ? 'var(--danger)' : data.score >= 30 ? 'var(--warning)' : 'var(--success)';
    scoreArc.style.stroke = scoreColor;
    scoreNum.style.color = scoreColor;
    scoreNum.textContent = data.score;

    fill.style.width = data.score + '%';
    fill.style.background = scoreColor;

    if (data.reasons && data.reasons.length > 0) {
        list.innerHTML = data.reasons.map(r => `<li>${escapeHtml(r)}</li>`).join('');
    } else {
        list.innerHTML = '<li class="safe-reason">No threat indicators found — clean!</li>';
    }

    if (data.ml_verdict) {
        mlSection.classList.remove('hidden');
        mlPred.textContent = data.ml_verdict;
        mlPred.style.color = data.ml_verdict === 'SCAM' ? 'var(--danger)' : 'var(--success)';
    } else {
        mlSection.classList.add('hidden');
    }

    const dlSection = document.getElementById('dl-verdict');
    const dlPred = document.getElementById('dl-pred-text');
    const dlConf = document.getElementById('dl-confidence');
    
    if (data.dl_verdict && data.dl_confidence) {
        dlSection.classList.remove('hidden');
        dlPred.textContent = data.dl_verdict;
        dlPred.style.color = data.dl_verdict === 'SCAM' ? 'var(--danger)' : 'var(--success)';
        dlConf.textContent = data.dl_confidence;
    } else {
        if(dlSection) dlSection.classList.add('hidden');
    }

    results.classList.remove('hidden');
    results.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

function reportPhishing() {
    if (!currentInputText) return;
    showToast("Report submitted successfully! Thank you for making the web safer.");
}

// ── Report Download ───────────────────────────────────────────
async function downloadReport() {
    if (!currentAnalysis || !currentInputText) {
        showToast('No active scan result to download');
        return;
    }

    showToast('Generating PDF Report...');
    try {
        const response = await fetch('/report', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                input: currentInputText,
                result: currentAnalysis,
                features: currentFeatures
            })
        });

        if (!response.ok) throw new Error('PDF Generation Failed');

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `NIGRANI_Threat_Report_${currentAnalysis.verdict}_${Date.now()}.pdf`;
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);

        showToast('Report Downloaded Successfully!');
    } catch (err) {
        showToast('Error generating PDF report: ' + err.message);
    }
}

// ── Helpers & Utilities ───────────────────────────────────────
function testSample(card) {
    const url = card.getAttribute('data-url');
    document.getElementById('userInput').value = url;
    document.getElementById('scanner').scrollIntoView({ behavior: 'smooth' });
    checkInput();
}

async function pasteFromClipboard() {
    try {
        const text = await navigator.clipboard.readText();
        document.getElementById('userInput').value = text;
        showToast('Pasted from clipboard');
    } catch {
        showToast('Clipboard access denied');
    }
}

function clearInput() {
    document.getElementById('userInput').value = '';
    document.getElementById('results').classList.add('hidden');
    document.getElementById('userInput').focus();
}

function scanAnother() {
    clearInput();
    document.getElementById('scanner').scrollIntoView({ behavior: 'smooth' });
}

function copyResult() {
    if (!currentAnalysis) return;
    const reportText = `NIGRANI Threat Report\nVerdict: ${currentAnalysis.verdict}\nScore: ${currentAnalysis.score}/100\nTarget: ${currentInputText}\nIndicators:\n${(currentAnalysis.reasons || []).map(r => '• ' + r).join('\n')}`;
    navigator.clipboard.writeText(reportText).then(() => showToast('Summary copied to clipboard'));
}

function addToHistory(input, data) {
    scanHistory.unshift({ input: input.substring(0, 100), score: data.score, verdict: data.verdict, time: new Date().toLocaleTimeString(), data: data });
    if (scanHistory.length > 15) scanHistory.pop();
    renderHistory();
}

function renderHistory() {
    const container = document.getElementById('history-list');
    const clearBtn = document.getElementById('clearHistoryBtn');
    if (scanHistory.length === 0) {
        container.innerHTML = '<div class="history-empty glass-card"><p>No scans yet.</p></div>';
        clearBtn.classList.add('hidden');
        return;
    }
    clearBtn.classList.remove('hidden');
    container.innerHTML = scanHistory.map((item, i) => {
        const dot = item.score >= 60 ? 'dot-danger' : item.score >= 30 ? 'dot-warning' : 'dot-success';
        return `<div class="history-item" onclick="replayHistory(${i})">
            <div class="history-dot ${dot}"></div>
            <div class="history-text">
                <div class="history-input">${escapeHtml(item.input)}</div>
                <div class="history-meta">${item.verdict} • ${item.time}</div>
            </div>
            <div class="history-score">${item.score}</div>
        </div>`;
    }).join('');
}

function replayHistory(i) {
    const item = scanHistory[i];
    document.getElementById('userInput').value = item.input;
    currentInputText = item.input;
    currentAnalysis = item.data;
    currentFeatures = item.data.features || null;
    showResults(item.data);
}

function clearHistory() {
    scanHistory = [];
    renderHistory();
    showToast('History cleared');
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function showToast(msg) {
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.textContent = msg;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 3000);
}

document.addEventListener('DOMContentLoaded', () => {
    initTheme();
    renderHistory();
});
