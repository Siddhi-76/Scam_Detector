/* ══════════════════════════════════════════════════════════════
   NIGRANI — Scam Detector  |  JavaScript Engine (Tailwind/Glassmorphism)
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
    
    const themeToggles = [document.getElementById('theme-toggle'), document.getElementById('theme-toggle-mobile')];
    themeToggles.forEach(toggle => {
        if(toggle) toggle.addEventListener('click', toggleTheme);
    });
}

function toggleTheme() {
    const currentTheme = document.documentElement.classList.contains('light') ? 'light' : 'dark';
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    setTheme(newTheme);
}

function setTheme(theme) {
    const htmlEl = document.documentElement;
    const fabIcon = document.getElementById('fab-theme-icon');

    if (theme === 'light') {
        htmlEl.classList.remove('dark');
        htmlEl.classList.add('light');
        if (fabIcon) fabIcon.textContent = 'dark_mode';
        
        // Adjust Three.js materials if they exist
        if (window.shieldMaterial && window.coreMaterial) {
            window.shieldMaterial.color.setHex(0x2563eb); // Tech Blue
            window.shieldMaterial.emissive.setHex(0x2563eb);
            window.shieldMaterial.opacity = 0.6;
            window.coreMaterial.color.setHex(0x2563eb);
            window.coreMaterial.opacity = 0.9;
        }
    } else {
        htmlEl.classList.remove('light');
        htmlEl.classList.add('dark');
        if (fabIcon) fabIcon.textContent = 'light_mode';
        
        // Adjust Three.js materials
         if (window.shieldMaterial && window.coreMaterial) {
            window.shieldMaterial.color.setHex(0x00ffff);
            window.shieldMaterial.emissive.setHex(0x00ffff);
            window.shieldMaterial.opacity = 0.3;
            window.coreMaterial.color.setHex(0x00ffff);
            window.coreMaterial.opacity = 0.8;
        }
    }
    localStorage.setItem('nigrani-theme', theme);
}

// Mouse tracking globally (for flashlight CSS)
document.addEventListener('mousemove', (e) => {
    document.documentElement.style.setProperty('--mouse-x', `${e.clientX}px`);
    document.documentElement.style.setProperty('--mouse-y', `${e.clientY}px`);
});

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
    document.getElementById('data-modules').classList.add('hidden');
    btn.disabled = true;
    
    // Animate button scanning
    btn.innerHTML = `<span class="material-symbols-outlined animate-spin">refresh</span><span>Scanning...</span>`;

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
        btn.innerHTML = `<span class="material-symbols-outlined">troubleshoot</span><span>Initiate Scan</span>`;
    }
}

function showResults(data) {
    const badge = document.getElementById('verdict-badge');
    const verdictIcon = document.getElementById('verdict-icon');
    const verdictText = document.getElementById('verdict-text');
    const scoreNum = document.getElementById('score-num');
    const scoreRing = document.getElementById('score-ring');
    const scoreBar = document.getElementById('score-bar');
    const list = document.getElementById('reasons-list');
    
    const mlSection = document.getElementById('ml-verdict');
    const mlPred = document.getElementById('ml-pred-text');
    
    const dlSection = document.getElementById('dl-verdict');
    const dlPred = document.getElementById('dl-pred-text');
    const dlConf = document.getElementById('dl-confidence');
    
    const results = document.getElementById('results');
    const typeBadge = document.getElementById('scan-type-badge');

    // 1. Theme and Verdict Colors
    let colorHex = '#4ade80'; // Success
    let colorClass = 'text-[#4ade80]';
    let bgClass = 'bg-[#0e3b2e] border-[#1a664f]';
    let icon = 'check_circle';
    
    if (data.score >= 60) {
        colorHex = '#ef4444'; // Danger
        colorClass = 'text-error';
        bgClass = 'bg-error-container border-error/50';
        icon = 'cancel';
    } else if (data.score >= 30) {
        colorHex = '#eab308'; // Warning
        colorClass = 'text-[#eab308]';
        bgClass = 'bg-[#422c06] border-[#855a0c]';
        icon = 'warning';
    }

    badge.className = `flex items-center gap-2 px-5 py-2.5 rounded-full font-code-lg font-bold interactive-button cursor-default ${bgClass} ${colorClass}`;
    verdictIcon.textContent = icon;
    verdictText.textContent = data.verdict.toUpperCase();

    typeBadge.textContent = (data.type || 'url').toUpperCase() + ' ANALYSIS';

    // 2. Score Animation
    // Dasharray is 452.4. Max offset is 452.4 (0%), min offset is 0 (100%)
    const circumference = 452.4;
    const offset = circumference - (data.score / 100) * circumference;
    scoreRing.style.strokeDashoffset = offset;
    scoreRing.style.color = colorHex;
    
    scoreNum.textContent = data.score;
    scoreNum.style.color = colorHex;

    scoreBar.style.width = data.score + '%';
    scoreBar.style.backgroundColor = colorHex;

    // 3. Reasons
    if (data.reasons && data.reasons.length > 0) {
        list.innerHTML = data.reasons.map(r => `<li class="flex items-start gap-2"><span class="material-symbols-outlined text-sm mt-0.5 text-error">priority_high</span><span>${escapeHtml(r)}</span></li>`).join('');
    } else {
        list.innerHTML = `<li class="flex items-start gap-2 text-[#4ade80]"><span class="material-symbols-outlined text-sm mt-0.5">check</span><span>No threat indicators found — clean!</span></li>`;
    }

    // 4. ML / DL Models
    if (data.ml_verdict) {
        mlSection.classList.remove('hidden');
        mlPred.textContent = data.ml_verdict;
        mlPred.className = data.ml_verdict === 'SCAM' ? 'font-bold text-error' : 'font-bold text-[#4ade80]';
    } else {
        mlSection.classList.add('hidden');
    }

    if (data.dl_verdict && data.dl_confidence) {
        dlSection.classList.remove('hidden');
        dlPred.textContent = data.dl_verdict;
        dlPred.className = data.dl_verdict === 'SCAM' ? 'font-bold text-error' : 'font-bold text-[#4ade80]';
        dlConf.textContent = data.dl_confidence;
    } else {
        dlSection.classList.add('hidden');
    }

    // 5. Data Modules (if URL features exist)
    const dataModules = document.getElementById('data-modules');
    if (data.type === 'url' && currentFeatures) {
        dataModules.classList.remove('hidden');
        
        // Entropy
        const entropy = currentFeatures.url_entropy || 0;
        document.getElementById('mod-entropy-val').textContent = entropy.toFixed(2) + ' bits';
        const entPct = Math.min((entropy / 5) * 100, 100);
        document.getElementById('mod-entropy-bar').style.width = entPct + '%';
        document.getElementById('mod-entropy-bar').className = `h-full transition-all duration-1000 ${entropy > 4.5 ? 'bg-error' : 'bg-primary-fixed'}`;

        // Levenshtein
        const lev = currentFeatures.brand_levenshtein || 0;
        document.getElementById('mod-lev-val').textContent = lev + (lev > 5 && lev < 20 ? ' (Suspicious)' : '');
        const levPct = Math.min((lev / 20) * 100, 100);
        document.getElementById('mod-lev-bar').style.width = levPct + '%';
        document.getElementById('mod-lev-bar').className = `h-full transition-all duration-1000 ${lev > 5 && lev < 20 ? 'bg-error' : 'bg-primary-fixed'}`;

        // Subdomain (Network layer mock)
        const subdomains = currentFeatures.subdomain_count || 0;
        document.getElementById('mod-net-val').textContent = subdomains + ' Nodes';
        document.getElementById('mod-net-bar-1').className = `h-1 flex-1 transition-all duration-1000 ${subdomains >= 1 ? 'bg-primary-fixed opacity-100' : 'bg-surface-container-high'}`;
        document.getElementById('mod-net-bar-2').className = `h-1 flex-1 transition-all duration-1000 ${subdomains >= 2 ? (subdomains > 3 ? 'bg-error' : 'bg-primary-fixed opacity-80') : 'bg-surface-container-high'}`;
        document.getElementById('mod-net-bar-3').className = `h-1 flex-1 transition-all duration-1000 ${subdomains >= 3 ? (subdomains > 3 ? 'bg-error' : 'bg-primary-fixed opacity-40') : 'bg-surface-container-high'}`;
    } else {
        dataModules.classList.add('hidden');
    }

    results.classList.remove('hidden');
    results.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

async function reportPhishing() {
    if (!currentInputText) return;
    
    try {
        const response = await fetch('/report_phishing', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ input: currentInputText })
        });
        if (response.ok) {
            showToast("Threat signature logged to database for analysis!");
        } else {
            showToast("Failed to log threat signature.");
        }
    } catch (err) {
        showToast("Error connecting to server.");
    }
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
    document.getElementById('data-modules').classList.add('hidden');
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
        container.innerHTML = `<div class="bg-surface-container-lowest border border-outline-variant p-8 rounded-lg text-center interactive-module text-on-surface-variant font-code-sm">No active scans in current session. Initialize scanner to build history matrix.</div>`;
        clearBtn.classList.add('hidden');
        return;
    }
    clearBtn.classList.remove('hidden');
    container.innerHTML = scanHistory.map((item, i) => {
        let colorClass = 'text-[#4ade80]';
        let bgClass = 'bg-[#4ade80]/10 border-[#4ade80]/30';
        if (item.score >= 60) {
            colorClass = 'text-error'; bgClass = 'bg-error/10 border-error/30';
        } else if (item.score >= 30) {
            colorClass = 'text-[#eab308]'; bgClass = 'bg-[#eab308]/10 border-[#eab308]/30';
        }
        
        return `<div class="bg-surface-container-low border border-outline-variant p-4 rounded-lg flex justify-between items-center interactive-module cursor-pointer hover:border-primary-fixed" onclick="replayHistory(${i})">
            <div>
                <div class="font-code-sm text-xs ${colorClass} font-bold mb-1">${item.verdict.toUpperCase()} • ${item.time}</div>
                <div class="text-on-surface text-sm truncate max-w-xs md:max-w-md">${escapeHtml(item.input)}</div>
            </div>
            <div class="flex items-center justify-center w-12 h-12 rounded-full border ${bgClass} ${colorClass} font-code-lg font-bold">
                ${item.score}
            </div>
        </div>`;
    }).join('<div class="h-4"></div>');
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
    showToast('History matrix cleared');
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function showToast(msg) {
    const toast = document.createElement('div');
    toast.className = 'fixed bottom-20 left-1/2 transform -translate-x-1/2 bg-surface-container-highest border border-outline-variant text-on-surface px-6 py-3 rounded-full font-code-sm z-[100] shadow-2xl animate-fade-in-up';
    toast.textContent = msg;
    document.body.appendChild(toast);
    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translate(-50%, 20px)';
        toast.style.transition = 'all 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// Custom animation for toasts
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeInUp {
        from { opacity: 0; transform: translate(-50%, 20px); }
        to { opacity: 1; transform: translate(-50%, 0); }
    }
    .animate-fade-in-up {
        animation: fadeInUp 0.3s ease-out forwards;
    }
`;
document.head.appendChild(style);

document.addEventListener('DOMContentLoaded', () => {
    initTheme();
    renderHistory();
});
