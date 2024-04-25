document.addEventListener('DOMContentLoaded', async () => {
    const playerListContainer = document.getElementById('playerList');

    try {
        const response = await fetch('YOUR_LAMBDA_API_ENDPOINT');
        const data = await response.json();

        if (data.statusCode === 200) {
            const players = data.body;
            const playerList = document.createElement('ul');

            players.forEach(player => {
                const listItem = document.createElement('li');
                listItem.textContent = `${player.playerName} - ${player.PlayerValue}`;
                playerList.appendChild(listItem);
            });

            playerListContainer.appendChild(playerList);
        } else {
            playerListContainer.textContent = 'Failed to load player data.';
        }
    } catch (error) {
        console.error('Error fetching player data:', error);
        playerListContainer.textContent = 'Failed to load player data.';
    }
});
