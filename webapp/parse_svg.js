const fs = require('fs');

const svg = fs.readFileSync('index.html', 'utf8');

// Use a simple regex to find all <path> and <g> ids and their paths
const data = {};

// We can't perfectly parse paths easily without a library.
// But we can just use the DOM! Wait, jsdom can't getBBox.
// Let's just fix the setupMap function to force display:block!
