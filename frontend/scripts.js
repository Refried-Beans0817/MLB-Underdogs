document.addEventListener('DOMContentLoaded', () => {
    // Fetch data from the backend and populate player list
    fetchPlayers();
});

async function fetchPlayers() {
    try {
        const response = await fetch('https://your-api-endpoint.com/undervalued-players');
        const data = await response.json();
        displayPlayers(data);
    } catch (error) {
        console.error('Error fetching players:', error);
    }
}

function displayPlayers(players) {
    const playerList = document.getElementById('player-list');
    playerList.innerHTML = '';

    players.forEach(player => {
        const playerItem = document.createElement('div');
        playerItem.classList.add('player-item');
        playerItem.innerHTML = `
            <h2>${player.name}</h2>
            <p>Position: ${player.position}</p>
            <p>Games: ${player.games}</p>
            <!-- Add more player details as needed -->
        `;
        playerList.appendChild(playerItem);
    });
}
