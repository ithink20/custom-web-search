chrome.runtime.onInstalled.addListener(() => {
    chrome.storage.sync.set({ urls: {} });
});

chrome.omnibox.onInputChanged.addListener((text, suggest) => {
    chrome.storage.sync.get('urls', (data) => {
        const urls = data.urls || {};
        const suggestions = [];
        for (const [shortcut, url] of Object.entries(urls)) {
            suggestions.push({
                content: `${shortcut} ${text}`,
                description: `${shortcut}: ${url}`
            });
        }
        chrome.omnibox.setDefaultSuggestion({ description: 'Type a shortcut and query' });
        suggest(suggestions);
    });
});

chrome.omnibox.onInputEntered.addListener((text, disposition) => {
    const [shortcut, ...rest] = text.split(' ');
    const query = rest.join(' ');
    chrome.storage.sync.get('urls', (data) => {
        const urls = data.urls || {};
        const baseUrl = urls[shortcut] || urls['g'];
        const redirectUrl = baseUrl + encodeURIComponent(query);

        chrome.tabs.update({ url: redirectUrl });
    });
});
