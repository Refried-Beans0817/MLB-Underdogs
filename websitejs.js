function showFakeData() {
    console.log("Script loaded successfully.");

    var searchInput = document.getElementById('searchInput').value;
    var resultsDiv = document.getElementById('results');

    if (searchInput) {
        resultsDiv.innerHTML = `
            <p>Results for: ${searchInput}</p>
            <table>
                <tr>
                    <th>Name</th>
                    <th>Team</th>
                    <th>Home Runs</th>
                    <th>AVG</th>
                </tr>
                <tr>
                    <td>Example Player</td>
                    <td>Yankees</td>
                    <td>20</td>
                    <td>.300</td>
                </tr>
            </table>
        `;
    } else {
        resultsDiv.innerHTML = "<p>Please enter a player name to search.</p>";
    }
}

