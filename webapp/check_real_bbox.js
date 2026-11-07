const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');
const jsdom = require('jsdom');
const { JSDOM } = jsdom;

const dom = new JSDOM(html);
const document = dom.window.document;

// JSDOM doesn't implement getBBox natively for SVGs.
// BUT we can parse the 'd' attribute and calculate it ourselves!
const svgPathBBox = require('svg-path-bbox'); // We can install this!

['CA-BC', 'CA-AB', 'CA-ON', 'CA-QC', 'CA-NL'].forEach(id => {
  const el = document.getElementById(id);
  if (el) {
    let d = el.getAttribute('d');
    if (!d) {
       // if it's a <g>, find all <path>s
       const paths = el.querySelectorAll('path');
       let allD = '';
       paths.forEach(p => allD += p.getAttribute('d') + ' ');
       d = allD;
    }
    try {
      const bbox = svgPathBBox(d);
      const x = bbox[0];
      const y = bbox[1];
      const width = bbox[2] - bbox[0];
      const height = bbox[3] - bbox[1];
      let cx = x + width / 2;
      let cy = y + height / 2;
      console.log(`${id}: x=${x.toFixed(1)}, y=${y.toFixed(1)}, w=${width.toFixed(1)}, h=${height.toFixed(1)} -> cx=${cx.toFixed(1)} (${(cx/629*100).toFixed(1)}%), cy=${cy.toFixed(1)} (${(cy/609*100).toFixed(1)}%)`);
    } catch(e) {}
  }
});
