# Custom Redirect Chrome Extension

This Chrome extension allows you to create custom shortcuts to redirect to specific URLs quickly.

## Features

- **Add Shortcuts:** Define custom shortcuts and their corresponding URLs.
- **Delete Shortcuts:** Delete existing shortcuts.
- **Storage:** Utilizes Chrome's `storage.sync` API to persist shortcuts across sessions.
- **Easy Access:** Accessible via the extension icon in the browser toolbar.
- **Bulk Upload:** Upload Json file for shortcuts

## Usage

1. **Installation:**
    - Download or clone the repository.
    - Navigate to `chrome://extensions` in your Chrome browser.
    - Enable **Developer mode** in the top right corner.
    - Click on **Load unpacked** and select the extension folder.

2. **Adding Shortcuts:**
    - Click on the extension icon in the toolbar or open the extension's options page.
    - Enter a unique shortcut and the corresponding URL you want it to redirect to.
    - Click **Add Shortcut** to save.

3. **Using Shortcuts:**
    - Once added, you can use the shortcuts directly in the address bar by typing `u` followed by your shortcut and pressing `Enter`.

4. **Upload Shortcurts:**
    - Supports only json format file only
  
    ```
    {
        "g": "https://www.google.com/search?q=",
        "yt": "https://www.youtube.com/results?search_query=",
        "gh": "https://github.com/search?q="
    }
    ```

## Files

- `manifest.json`: Configuration file specifying extension details and permissions.
- `options.html`: HTML page for managing shortcuts.
- `options.js`: JavaScript file handling UI interactions and storage operations.
- `background.js`: Service worker for background tasks (if applicable).
- `icons/`: Directory containing icons used for the extension.

## Comparison with Traditional Bookmarks

| Feature | Custom Redirect Chrome Extension | Traditional Bookmarks |
|---------|---------------------------------|----------------------|
| **Custom Shortcuts** | Allows creation of short, memorable shortcuts for URLs. | Limited to folder-based organization. |
| **Direct Access** | Access shortcuts directly from browser toolbar or omnibox (`u` keyword). | Requires navigation through bookmarks menu. |
| **Persistent Storage** | Syncs shortcuts across devices using Chrome's `storage.sync` API. | Syncing may vary across browsers and devices. |
| **User Interface** | User-friendly interface (`options.html`) for easy shortcut management. | Bookmarks menu can be cumbersome for managing large collections. |
| **Extension Features** | Can include additional functionalities (e.g., background tasks) for enhanced browsing. | Limited to basic bookmarking and folder organization. |
| **Integration** | Integrated into browser toolbar for quick access and efficient browsing. | Separate from browser interface; requires navigation away from current page. |


## Contributing

Feel free to fork this repository, propose changes, or report issues. Contributions are welcome!
