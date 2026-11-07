const fs = require('fs');
const jsdom = require("jsdom");
const { JSDOM } = jsdom;

const html = fs.readFileSync('index.html', 'utf8');
const dataJs = fs.readFileSync('data.js', 'utf8');
const appJs = fs.readFileSync('app.js', 'utf8');

const dom = new JSDOM(html, { runScripts: "dangerously" });
dom.window.eval(dataJs);
try {
  dom.window.eval(appJs);
  console.log("App loaded successfully");
} catch (e) {
  console.error(e);
}
