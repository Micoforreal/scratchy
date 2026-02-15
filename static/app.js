// API Base URL
const API_BASE = window.location.origin;

// DOM Elements
const runBtn = document.getElementById('runBtn');
const statusBox = document.getElementById('status');
const statusText = document.getElementById('statusText');
const statusIndicator = statusBox.querySelector('.status-indicator');
const progressSection = document.getElementById('progressSection');
const progressFill = document.getElementById('progressFill');
const progressText = document.getElementById('progressText');
const latestReport = document.getElementById('latestReport');
const reportsList = document.getElementById('reportsList');

// State
let currentRunId = null;
let statusCheckInterval = null;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadReportsList();
    loadLatestReport();

    runBtn.addEventListener('click', triggerRun);
});

// Trigger a new agent run
async function triggerRun() {
    try {
        runBtn.disabled = true;
        runBtn.innerHTML = '<span class="btn-icon">⏳</span> Starting...';

        const response = await fetch(`${API_BASE}/api/run`, {
            method: 'POST'
        });

        const data = await response.json();

        if (data.success) {
            currentRunId = data.run_id;
            updateStatus('running', 'Running...');
            progressSection.classList.remove('hidden');

            // Start polling for status
            startStatusPolling();
        } else {
            throw new Error(data.message || 'Failed to start run');
        }
    } catch (error) {
        console.error('Error triggering run:', error);
        alert('Failed to start agent run: ' + error.message);
        resetRunButton();
    }
}

// Start polling for status updates
function startStatusPolling() {
    if (statusCheckInterval) {
        clearInterval(statusCheckInterval);
    }

    statusCheckInterval = setInterval(checkStatus, 2000);
    checkStatus(); // Check immediately
}

// Check run status
async function checkStatus() {
    if (!currentRunId) return;

    try {
        const response = await fetch(`${API_BASE}/api/status/${currentRunId}`);
        const data = await response.json();

        // Update progress
        if (data.progress) {
            progressText.textContent = data.progress;

            // Estimate progress percentage based on stage
            let percentage = 0;
            if (data.progress.includes('Collecting')) percentage = 20;
            else if (data.progress.includes('Processing')) percentage = 40;
            else if (data.progress.includes('Detecting')) percentage = 60;
            else if (data.progress.includes('explanations')) percentage = 75;
            else if (data.progress.includes('ideas')) percentage = 90;
            else if (data.progress.includes('report')) percentage = 95;
            else if (data.status === 'completed') percentage = 100;

            progressFill.style.width = percentage + '%';
        }

        // Update status
        if (data.status === 'completed') {
            updateStatus('completed', 'Completed!');
            stopStatusPolling();
            resetRunButton();

            // Reload reports
            setTimeout(() => {
                loadLatestReport();
                loadReportsList();
                progressSection.classList.add('hidden');
            }, 2000);

        } else if (data.status === 'failed') {
            updateStatus('failed', 'Failed: ' + (data.error || 'Unknown error'));
            stopStatusPolling();
            resetRunButton();

            setTimeout(() => {
                progressSection.classList.add('hidden');
            }, 5000);
        }

    } catch (error) {
        console.error('Error checking status:', error);
    }
}

// Stop status polling
function stopStatusPolling() {
    if (statusCheckInterval) {
        clearInterval(statusCheckInterval);
        statusCheckInterval = null;
    }
}

// Update status display
function updateStatus(status, text) {
    statusText.textContent = text;
    statusIndicator.className = `status-indicator ${status}`;
}

// Reset run button
function resetRunButton() {
    runBtn.disabled = false;
    runBtn.innerHTML = '<span class="btn-icon">▶</span> Run Agent';
}

// Load latest report
async function loadLatestReport() {
    try {
        const response = await fetch(`${API_BASE}/api/latest`);

        if (response.ok) {
            const data = await response.json();
            latestReport.innerHTML = data.html;
        } else {
            latestReport.innerHTML = '<p class="empty-state">No reports generated yet. Click "Run Agent" to start!</p>';
        }
    } catch (error) {
        console.error('Error loading latest report:', error);
        latestReport.innerHTML = '<p class="empty-state">Error loading report</p>';
    }
}

// Load reports list
async function loadReportsList() {
    try {
        const response = await fetch(`${API_BASE}/api/reports`);
        const data = await response.json();

        if (data.reports && data.reports.length > 0) {
            reportsList.innerHTML = data.reports.map(report => `
                <div class="report-item" onclick="viewReport('${report.filename}')">
                    <h3>${formatFilename(report.filename)}</h3>
                    <div class="report-meta">
                        <span>📅 ${formatDate(report.modified)}</span>
                        <span>📄 ${formatSize(report.size)}</span>
                    </div>
                </div>
            `).join('');
        } else {
            reportsList.innerHTML = '<p class="empty-state">No reports yet</p>';
        }
    } catch (error) {
        console.error('Error loading reports:', error);
        reportsList.innerHTML = '<p class="empty-state">Error loading reports</p>';
    }
}

// View a specific report
async function viewReport(filename) {
    try {
        const response = await fetch(`${API_BASE}/api/reports/${filename}`);
        const data = await response.json();

        if (data.html) {
            latestReport.innerHTML = data.html;
            latestReport.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    } catch (error) {
        console.error('Error viewing report:', error);
        alert('Failed to load report');
    }
}

// Format filename for display
function formatFilename(filename) {
    // Extract timestamp from filename like "narrative_brief_20250215_143000.md"
    const match = filename.match(/narrative_brief_(\d{8})_(\d{6})\.md/);
    if (match) {
        const date = match[1];
        const time = match[2];
        return `Report - ${date.slice(0, 4)}-${date.slice(4, 6)}-${date.slice(6, 8)} ${time.slice(0, 2)}:${time.slice(2, 4)}`;
    }
    return filename;
}

// Format date for display
function formatDate(isoString) {
    const date = new Date(isoString);
    return date.toLocaleString();
}

// Format file size
function formatSize(bytes) {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
}
