// Function to handle adding shortcuts
function addShortcut() {
    const shortcut = document.getElementById('shortcut').value.trim();
    const url = document.getElementById('url').value.trim();

    if (shortcut && url) {
        chrome.storage.local.get('urls', (data) => {
            const urls = data.urls || {};
            urls[shortcut] = url;
            chrome.storage.local.set({ urls }, () => {
                displayShortcuts();
                document.getElementById('shortcut').value = '';
                document.getElementById('url').value = '';
                var error = chrome.runtime.lastError;  
                if (error) {  
                    alert(error);  
                }
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
    chrome.storage.local.get('urls', (data) => {
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
            if (url.length > 50) {
                urlSpan.textContent = url.substring(0, 50) + '...';
                urlSpan.setAttribute('title', String(url)); // Set full URL as title attribute
            }

            textSpan.appendChild(urlSpan);

            const deleteIcon = document.createElement('i');
            deleteIcon.className = 'fas fa-trash-alt delete-icon';
            deleteIcon.addEventListener('click', () => {
                chrome.storage.local.get('urls', (data) => {
                    const updatedUrls = data.urls || {};
                    delete updatedUrls[shortcut];
                    chrome.storage.local.set({ urls: updatedUrls }, () => {
                        displayShortcuts();
                        var error = chrome.runtime.lastError;  
                        if (error) {  
                            alert(error);  
                        }
                    });
                });
            });

            listItem.appendChild(textSpan);
            listItem.appendChild(deleteIcon);
            shortcutList.appendChild(listItem);
        }
    });
}

function handleJsonUpload() {
    const fileInput = document.getElementById('jsonFile');
    const file = fileInput.files[0];

    if (file) {
        const reader = new FileReader();
        reader.onload = function(event) {
            try {
                const json = JSON.parse(event.target.result);

                chrome.storage.local.get('urls', (data) => {
                    const urls = data.urls || {};
                    // Merge new shortcuts with existing ones, overwriting duplicates
                    const mergedUrls = { ...urls, ...json };

                    chrome.storage.local.set({ urls: mergedUrls }, () => {
                        displayShortcuts();
                        var error = chrome.runtime.lastError;  
                        if (error) {  
                            alert('***Upload Failed*** Check Extension Error');  
                        } else {
                            alert('Shortcuts successfully uploaded and updated!');
                        }
                    });
                });
            } catch (e) {
                alert('Error parsing JSON file. Please ensure it is correctly formatted.');
            }
        };
        reader.readAsText(file);
    } else {
        alert('Please select a JSON file to upload.');
    }
}

// Event listener for uploading the JSON file
document.getElementById('uploadJson').addEventListener('click', handleJsonUpload);


// Initial display of shortcuts
displayShortcuts();
