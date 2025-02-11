function updateStatus() {
    fetch('/api/status')
        .then(response => response.json())
        .then(data => {
            // Update LINE status
            const lineStatus = document.getElementById('line-status');
            lineStatus.textContent = data.status === 'online' ? 'Connected' : 'Disconnected';
            lineStatus.className = `badge ${data.status === 'online' ? 'bg-success' : 'bg-danger'}`;

            // Update Discord status
            const discordStatus = document.getElementById('discord-status');
            discordStatus.textContent = data.status === 'online' ? 'Connected' : 'Disconnected';
            discordStatus.className = `badge ${data.status === 'online' ? 'bg-success' : 'bg-danger'}`;

            // Update message count
            document.getElementById('message-count').textContent = data.message_count;
        })
        .catch(error => {
            console.error('Error fetching status:', error);
            // Set status to disconnected on error
            document.querySelectorAll('.badge').forEach(badge => {
                badge.textContent = 'Disconnected';
                badge.className = 'badge bg-danger';
            });
        });
}

// Update status every 5 seconds
setInterval(updateStatus, 5000);

// Initial status update
updateStatus();