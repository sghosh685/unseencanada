const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');
const jsdom = require('jsdom');
const { JSDOM } = jsdom;

const dom = new JSDOM(html, { runScripts: "dangerously", resources: "usable" });
dom.window.CANADA_DATA = {
  provinces: [
    { id: "CA-BC", name: "British Columbia" },
    { id: "CA-AB", name: "Alberta" },
    { id: "CA-MB", name: "Manitoba" },
    { id: "CA-QC", name: "Quebec" }
  ],
  themes: [{primary: 'red', hover: 'red', bg: 'red'}]
};

setTimeout(() => {
  const labels = dom.window.document.querySelectorAll('.province-label');
  console.log("Labels found:", labels.length);
  labels.forEach(l => {
    console.log(l.id, l.style.left, l.style.top);
  });
  const svg = dom.window.document.querySelector('svg#canada-map');
  console.log("SVG present:", !!svg);
}, 1000);
