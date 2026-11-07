const fs = require('fs');
const jsdom = require('jsdom');
const { JSDOM } = jsdom;

const html = fs.readFileSync('index.html', 'utf8');

const dom = new JSDOM(html, {
  url: "http://localhost:8080/#province/CA-ON",
  runScripts: "dangerously",
  resources: "usable"
});

// Since JSDOM doesn't support getBBox natively
dom.window.SVGElement.prototype.getBBox = function() {
  return { x: 0, y: 0, width: 100, height: 100 };
};

setTimeout(() => {
  try {
     console.log("Active view:", dom.window.document.querySelector('.view.active').id);
     console.log("Drilldown Title:", dom.window.document.getElementById('drilldown-name').textContent);
     
     const gridHtml = dom.window.document.getElementById('grid-cities').innerHTML;
     console.log("Grid Cities content len:", gridHtml.length);
     console.log("Sample grid content:", gridHtml.substring(0, 100));
  } catch (e) {
     console.error("Test failed:", e);
  }
}, 1000);
