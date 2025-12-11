document.addEventListener('DOMContentLoaded', () => {
    const grid = document.getElementById('monitor-grid');
    const lastUpdatedEl = document.getElementById('last-updated');

    // Poll every 60 seconds (60000ms) - kept user requirement 1 min, but maybe 30s is better visually?
    // User explicitly said "read ... every 1 minsutes".
    const POLL_INTERVAL = 60000;

    async function fetchData() {
        try {
            const response = await fetch('/api/monitor');
            if (!response.ok) throw new Error('Network response was not ok');
            const data = await response.json();
            renderGrid(data);
            updateTimestamp();
        } catch (error) {
            console.error('Error fetching data:', error);
            // Optionally show error state in UI
        }
    }

    function renderGrid(data) {
        grid.innerHTML = '';

        if (data.length === 0) {
            grid.innerHTML = '<div class="loading-state"><p>No data available.</p></div>';
            return;
        }

        data.forEach(item => {
            const card = document.createElement('div');
            const statusClass = `status-${item.status.toLowerCase()}`;

            card.className = `monitor-card ${statusClass}`;
            card.innerHTML = `
                <div class="card-header">
                    <span class="card-title">${item.name}</span>
                    <span class="status-indicator"></span>
                </div>
                <div class="card-value">${item.value}</div>
                <div class="card-status-text">${item.status}</div>
            `;
            grid.appendChild(card);
        });
    }

    function updateTimestamp() {
        const now = new Date();
        lastUpdatedEl.textContent = `Last updated: ${now.toLocaleTimeString()}`;
    }

    // Initial fetch
    fetchData();

    // Start polling
    setInterval(fetchData, POLL_INTERVAL);
});
