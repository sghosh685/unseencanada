const fs = require('fs');
const dataJs = fs.readFileSync('data.js', 'utf8');
const mockWindow = { CANADA_DATA: null };
eval('const window = mockWindow;\n' + dataJs);
const p = mockWindow.CANADA_DATA.provinces[8]; // Ontario
const total = (p.cities?.length || 0) + (p.parks?.length || 0) + (p.hiddenGems?.length || 0);
console.log(p.name, "Total places:", total);
