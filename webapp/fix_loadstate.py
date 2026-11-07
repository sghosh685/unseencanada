import re

with open("/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/app.js", "r") as f:
    js = f.read()

# Fix loadState to initialize missing arrays
old_load = r"""  function loadState\(\) \{
    const saved = localStorage\.getItem\('unseen-canada-state'\);
    if \(saved\) \{
      try \{
        state = JSON\.parse\(saved\);
      \} catch \(e\) \{\}
    \}
  \}"""

new_load = """  function loadState() {
    const saved = localStorage.getItem('unseen-canada-state');
    if (saved) {
      try {
        state = JSON.parse(saved);
        if (!state.visitedPlaces) state.visitedPlaces = [];
        if (!state.unlockedAchievements) state.unlockedAchievements = [];
      } catch (e) {}
    }
  }"""

js = re.sub(old_load, new_load, js)

with open("/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/app.js", "w") as f:
    f.write(js)
