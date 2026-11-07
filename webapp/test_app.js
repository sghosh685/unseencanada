const fs = require('fs');

const dataJs = fs.readFileSync('data.js', 'utf8');
const appJs = fs.readFileSync('app.js', 'utf8');

const logs = [];
const mockDocument = {
  getElementById: (id) => { return { addEventListener: () => {}, classList: { add: () => {}, remove: () => {} }, style: {}, dataset: {}, getBBox: () => { return {x:0, y:0, width:100, height:100} }, appendChild: () => {}, innerHTML: '', setAttribute: () => {}, removeAttribute: () => {} } },
  querySelectorAll: () => [],
  querySelector: () => null,
  createElement: () => { return { style: {}, classList: { add: () => {}, remove: () => {} }, dataset: {}, addEventListener: () => {}, setAttribute: () => {} } },
  documentElement: { style: { setProperty: () => {} } },
  body: { appendChild: () => {} },
  readyState: 'loading',
  addEventListener: (e, cb) => {
      if (e === 'DOMContentLoaded') {
          try {
              cb();
          } catch(err) {
              console.log("ERROR in DOMContentLoaded", err);
          }
      }
  }
};
const mockWindow = {
  CANADA_DATA: null,
  location: { hash: '' },
  addEventListener: () => {},
  requestAnimationFrame: (cb) => cb(),
  setTimeout: (cb) => cb(),
};
global.document = mockDocument;
global.window = mockWindow;
global.localStorage = { getItem: () => null, setItem: () => {} };
global.console = { log: console.log, error: console.error };

eval(dataJs);
eval(appJs);

