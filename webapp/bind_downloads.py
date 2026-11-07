import re

with open("/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/app.js", "r") as f:
    content = f.read()

# Update generateImage to accept format
gen_old = r'function generateImage\(callback\) \{'
gen_new = r'function generateImage(callback, format = "image/png") {'

content = re.sub(gen_old, gen_new, content)

gen_cb_old = r"callback\(canvas\.toDataURL\('image/png'\)\);"
gen_cb_new = r"callback(canvas.toDataURL(format));"

content = re.sub(gen_cb_old, gen_cb_new, content)

# Update bindEvents to wire new buttons
bind_old = r"document\.getElementById\('download-btn'\)\?\.addEventListener\('click', handleDownload\);"
bind_new = """    document.getElementById('download-btn-png')?.addEventListener('click', () => handleDownload('png'));
    document.getElementById('download-btn-jpg')?.addEventListener('click', () => handleDownload('jpeg'));"""

content = re.sub(bind_old, bind_new, content)

# Update handleDownload
hd_old = r"""  function handleDownload\(\) \{
    generateImage\(\(dataUrl\) => \{
      const a = document\.createElement\('a'\);
      a\.download = 'my-canada\.png';
      a\.href = dataUrl;
      a\.click\(\);
    \}\);
  \}"""

hd_new = """  function handleDownload(type = 'png') {
    const mimeType = type === 'jpeg' ? 'image/jpeg' : 'image/png';
    const ext = type === 'jpeg' ? 'jpg' : 'png';
    generateImage((dataUrl) => {
      const a = document.createElement('a');
      a.download = `my-canada.${ext}`;
      a.href = dataUrl;
      a.click();
    }, mimeType);
  }"""

content = re.sub(hd_old, hd_new, content, flags=re.DOTALL)

# Also update stats logic for progress-text-card and progress-fill-card
stats_update_old = r"""    const statProvBar = document\.getElementById\('stat-provinces-bar'\);"""

stats_update_new = """    const txtCard = document.getElementById('progress-text-card');
    if (txtCard) txtCard.textContent = `${percentage}% of Canada explored`;
    const fillCard = document.getElementById('progress-fill-card');
    if (fillCard) fillCard.style.width = `${percentage}%`;

    const statProvBar = document.getElementById('stat-provinces-bar');"""

content = re.sub(stats_update_old, stats_update_new, content)

with open("/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/app.js", "w") as f:
    f.write(content)
