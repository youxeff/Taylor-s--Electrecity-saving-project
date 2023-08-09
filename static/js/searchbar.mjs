document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search-input');
    const searchButton = document.getElementById('search-button');
    const searchResults = document.getElementById('search-results');

    searchButton.addEventListener('click', function() {
        const searchTerm = searchInput.value.trim();

        if (searchTerm !== '') {
            // Clear previous search results
            searchResults.innerHTML = '';

            // Perform search and display results
            performSearch(searchTerm)
                .then(function(searchResultsData) {
                    displaySearchResults(searchResultsData);
                })
                .catch(function(error) {
                    console.error('Search failed:', error);
                });
        }
    });

    function performSearch(searchTerm) {
        // Make an AJAX request to the Python backend
        return fetch('/searchbar?q=' + encodeURIComponent(searchTerm))
            .then(function(response) {
                if (!response.ok) {
                    throw new Error('Search request failed');
                }
                return response.json();
            })
            .then(function(data) {
                return data.search_results;
            });
    }

    function displaySearchResults(searchResultsData) {
        // Iterate over the search results and create HTML elements to display them
        searchResultsData.forEach(function(result) {
            const resultDiv = document.createElement('div');
            const titleHeading = document.createElement('h3');
            const contentParagraph = document.createElement('p');

            titleHeading.textContent = result.name;
            contentParagraph.textContent = result.description;

            resultDiv.appendChild(titleHeading);
            resultDiv.appendChild(contentParagraph);

            searchResults.appendChild(resultDiv);
        });
    }
});
