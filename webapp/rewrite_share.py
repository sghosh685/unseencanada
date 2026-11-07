import re

with open("/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/app.js", "r") as f:
    content = f.read()

share_logic = """
  function openShareModal() {
    const modal = document.getElementById('share-modal');
    if (!modal) return;
    
    // Generate the preview and put it on the canvas
    generateImage((dataUrl) => {
      const img = new Image();
      img.onload = () => {
        const canvas = document.getElementById('share-canvas');
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        // scale down for preview
        canvas.width = 600;
        canvas.height = 500;
        ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
      };
      img.src = dataUrl;
    });

    modal.classList.remove('hidden');
    modal.style.display = 'flex';
  }

  function closeShareModal() {
    const modal = document.getElementById('share-modal');
    if (modal) {
       modal.classList.add('hidden');
       modal.style.display = 'none';
    }
  }

  function handleShare() {
    generateImage((dataUrl) => {
      if (navigator.share) {
        fetch(dataUrl)
          .then(res => res.blob())
          .then(blob => {
            const file = new File([blob], 'my-canada.png', { type: 'image/png' });
            navigator.share({
              title: 'My Canada Map',
              text: `I've explored ${state.visitedProvinces.length} provinces & territories in Canada!`,
              files: [file]
            }).catch(console.error);
          });
      } else {
        handleDownload(); // Fallback
      }
    });
  }
"""

pattern = re.compile(r"function handleShare\(\) \{.*?\}\n  \}", re.DOTALL)
content = pattern.sub(share_logic.strip(), content)

content = content.replace("document.getElementById('share-btn')?.addEventListener('click', handleShare);", 
"""document.getElementById('share-btn')?.addEventListener('click', openShareModal);
    document.getElementById('share-native-btn')?.addEventListener('click', handleShare);
    document.getElementById('share-close')?.addEventListener('click', closeShareModal);
    document.getElementById('share-modal')?.addEventListener('click', (e) => {
      if (e.target.id === 'share-modal') closeShareModal();
    });""")

with open("/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/app.js", "w") as f:
    f.write(content)
