const fs = require('fs');
const path = require('path');

const sourceDir = path.join(__dirname, '../dist/src/pages');
const targetDir = path.join(__dirname, '../dist');

// Function to move files/folders
function moveDirectoryContents(src, dest) {
    if (!fs.existsSync(src)) return;

    // Create the target directory if it doesn't exist
    if (!fs.existsSync(dest)) {
        fs.mkdirSync(dest, { recursive: true });
    }

    fs.readdirSync(src).forEach(item => {
        const srcPath = path.join(src, item);
        const destPath = path.join(dest, item);

        const stat = fs.statSync(srcPath);

        if (stat.isDirectory()) {
            // Check if the directory contains an index.html file
            const indexPath = path.join(srcPath, 'index.html');
            if (fs.existsSync(indexPath)) {
                // This is a page directory (e.g., 'about', 'activities'). 
                // Move it to the root of 'dist' to create the clean URL.
                console.log(`Moving directory: ${item} to ${destPath}`);
                // Move the entire folder (e.g., /distsrc/pages/activities -> /dist/activities)
                fs.renameSync(srcPath, destPath); 
            } else {
                // If it's a sub-folder without index.html, we might ignore it or handle it differently.
                // Given your tree, we'll assume only direct page folders need moving.
                console.log(`Skipping directory without index.html: ${item}`);
            }
        }
        // NOTE: We don't expect files directly in src/pages/, only folders.
    });
}

console.log("Starting Clean URL structure creation...");
moveDirectoryContents(sourceDir, targetDir);
console.log("Clean URL structure complete. Files are now in /dist/<pagename>/index.html");