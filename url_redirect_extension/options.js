// Function to handle adding shortcuts
function addShortcut() {
    const shortcut = document.getElementById('shortcut').value.trim();
    const url = document.getElementById('url').value.trim();

    if (shortcut && url) {
        chrome.storage.sync.get('urls', (data) => {
            const urls = data.urls || {};
            urls[shortcut] = url;
            chrome.storage.sync.set({ urls }, () => {
                displayShortcuts();
                document.getElementById('shortcut').value = '';
                document.getElementById('url').value = '';
            });
        });
    }
}

// Event listener for clicking the "Add Shortcut" button
document.getElementById('addShortcut').addEventListener('click', addShortcut);

// Event listener for pressing Enter key to add shortcut
document.addEventListener('keypress', (event) => {
    const key = event.key;
    if (key === 'Enter') {
        addShortcut();
    }
});

// Function to display existing shortcuts
function displayShortcuts() {
    chrome.storage.sync.get('urls', (data) => {
        const urls = data.urls || {};
        const shortcutList = document.getElementById('shortcutList');
        shortcutList.innerHTML = '';
        for (const [shortcut, url] of Object.entries(urls)) {
            const listItem = document.createElement('li');
            listItem.classList.add('shortcut-item');

            const textSpan = document.createElement('span');
            textSpan.textContent = `${shortcut}: `;

            const urlSpan = document.createElement('span');
            urlSpan.textContent = String(url);
            if (url.length > 30) {
                urlSpan.textContent = url.substring(0, 50) + '...';
                urlSpan.setAttribute('title', String(url)); // Set full URL as title attribute
            }

            textSpan.appendChild(urlSpan);

            const deleteIcon = document.createElement('i');
            deleteIcon.className = 'fas fa-trash-alt delete-icon';
            deleteIcon.addEventListener('click', () => {
                chrome.storage.sync.get('urls', (data) => {
                    const updatedUrls = data.urls || {};
                    delete updatedUrls[shortcut];
                    chrome.storage.sync.set({ urls: updatedUrls }, () => {
                        displayShortcuts();
                    });
                });
            });

            listItem.appendChild(textSpan);
            listItem.appendChild(deleteIcon);
            shortcutList.appendChild(listItem);
        }
    });
}


// Initial display of shortcuts
displayShortcuts();
