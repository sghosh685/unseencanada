const fs = require('fs');
const { JSDOM } = require('jsdom');

const html = fs.readFileSync('/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/index.html', 'utf8');
const dataJs = fs.readFileSync('/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/data.js', 'utf8');
const appJs = fs.readFileSync('/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/app.js', 'utf8');

const dom = new JSDOM(html, { runScripts: "dangerously" });
const window = dom.window;

window.eval(dataJs);

try {
  window.eval(appJs);
  console.log("Successfully ran app.js!");
} catch (e) {
  console.error("Error running app.js:");
  console.error(e);
}
