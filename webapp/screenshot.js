const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  
  // Set viewport to desktop
  await page.setViewport({ width: 1200, height: 900 });
  
  // Navigate
  await page.goto('http://localhost:8081', { waitUntil: 'networkidle2' });
  
  // Wait for map and labels
  await page.waitForSelector('.map-label');
  
  // Take screenshot of the UI
  await page.screenshot({ path: 'ui_screenshot.png' });
  console.log("UI screenshot saved.");
  
  // Mark a province as visited
  await page.click('#label-CA-ON');
  // Wait for the modal or drilldown.
  // Actually, clicking the label goes to drilldown. Clicking the province toggles it.
  
  // Instead of testing interactions right now, let's just grab the UI screenshot.
  
  await browser.close();
})();
